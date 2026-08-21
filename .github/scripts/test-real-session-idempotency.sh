#!/usr/bin/env bash
set -euo pipefail

id="${1:-2026-08-15_2026-08-16}"
year="${id:0:4}"
month="${id:5:2}"
session="data/sessions/$year/$month/$id"
metrics="$session/normalized/session-metrics.json"
report_dir="docs/session-reports/$year/$month/$id"
latest_observation='docs/data/realtime/latest-observation.json'

governed_paths=(
  data/sessions
  data/analytics
  docs/session-reports
  docs/analytics/history-validation.md
  docs/data/realtime/latest-observation.json
  docs/data/scientific-session-catalog.json
  docs/data/scientific-observation-index.json
)

manifest="$session/manifest.json"
test -f "$manifest" || { echo "Manifest missing: $manifest"; exit 1; }
python - "$manifest" "$id" <<'PY'
import json, sys
path, expected = sys.argv[1:]
with open(path, encoding='utf-8-sig') as fh:
    manifest = json.load(fh)
if manifest.get('session_id') != expected:
    raise SystemExit(f"session_id mismatch: {manifest.get('session_id')}")
if manifest.get('report_status') != 'COMPLETE':
    raise SystemExit(f"session is not COMPLETE: {manifest.get('report_status')}")
PY

run_pipeline() {
  python dsg-analytics/analyzer/analyze_session.py --session "$session"
  mkdir -p "$report_dir"
  python dsg-analytics/reporter/generate_markdown_report.py --metrics "$metrics" --output "$report_dir/report-sessione.md"
  python dsg-analytics/reporter/generate_pdf_report.py --metrics "$metrics" --output "$report_dir/Report_Sessione_$id.pdf"
  python dsg-analytics/history/update_history.py --metrics "$metrics" --history 'data/analytics/history/sessions.csv'
  python dsg-analytics/reporter/update_latest_observation.py --session "$session" --output "$latest_observation"
  python dsg-analytics/history/consolidate_history.py
  python dsg-analytics/target/extract_target_metrics.py --repo-root .
  python dsg-analytics/target/build_targets.py --repo-root .
  node .github/scripts/generate-scientific-session-catalog.mjs --write
  node .github/scripts/generate-scientific-catalog.mjs --write
  python dsg-analytics/reporter/build_session_reports_index.py --repo-root .
  node .github/scripts/generate-scientific-session-catalog.mjs --check
  node .github/scripts/generate-scientific-catalog.mjs --check
}

cleanup() {
  git reset --hard -q HEAD
  git clean -fdq -- "${governed_paths[@]}"
}
trap cleanup EXIT

run_pipeline
first_tree="$(git diff --binary -- "${governed_paths[@]}" | sha256sum | awk '{print $1}')"
first_status="$(git status --porcelain --untracked-files=all -- "${governed_paths[@]}" | sha256sum | awk '{print $1}')"

run_pipeline
second_tree="$(git diff --binary -- "${governed_paths[@]}" | sha256sum | awk '{print $1}')"
second_status="$(git status --porcelain --untracked-files=all -- "${governed_paths[@]}" | sha256sum | awk '{print $1}')"

if [[ "$first_tree" != "$second_tree" || "$first_status" != "$second_status" ]]; then
  echo 'Real-session downstream idempotency FAILED: second pass changed governed output state.'
  git status --short --untracked-files=all -- "${governed_paths[@]}"
  exit 1
fi

echo "Real-session downstream idempotency PASS for $id"
echo "governed-diff-sha256=$second_tree"
