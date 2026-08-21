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

canonical_fingerprint() {
  python - "${governed_paths[@]}" <<'PY'
import csv, hashlib, io, json, os, pathlib, re, sys

VOLATILE_KEYS = {
    'generated_at', 'generated_at_utc', 'updated_at', 'updated_at_utc',
    'created_at', 'created_at_utc', 'build_timestamp', 'timestamp_generated'
}
TEXT_VOLATILE = (
    re.compile(r'^Generated at:.*$', re.I),
    re.compile(r'^- Generato:.*$', re.I),
)

def strip_json(value):
    if isinstance(value, dict):
        return {k: strip_json(v) for k, v in sorted(value.items()) if k not in VOLATILE_KEYS}
    if isinstance(value, list):
        return [strip_json(v) for v in value]
    return value

def canonical_csv(path):
    text = path.read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    rows = list(csv.DictReader(io.StringIO(text)))
    fields = [f for f in (rows[0].keys() if rows else []) if f not in VOLATILE_KEYS]
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    for row in rows:
        writer.writerow({f: row.get(f, '') for f in fields})
    return out.getvalue().encode()

def canonical_text(path):
    lines = path.read_text(encoding='utf-8-sig', errors='replace').replace('\r\n', '\n').split('\n')
    kept = []
    for line in lines:
        if any(p.match(line) for p in TEXT_VOLATILE):
            continue
        kept.append(line)
    return '\n'.join(kept).encode()

files = []
for raw in sys.argv[1:]:
    p = pathlib.Path(raw)
    if p.is_file():
        files.append(p)
    elif p.is_dir():
        files.extend(x for x in p.rglob('*') if x.is_file())

h = hashlib.sha256()
for path in sorted(set(files), key=lambda x: x.as_posix()):
    if path.suffix.lower() == '.pdf':
        # PDF binary metadata is non-semantic; the same metrics also drive the Markdown report.
        continue
    try:
        if path.suffix.lower() == '.json':
            value = json.loads(path.read_text(encoding='utf-8-sig'))
            data = json.dumps(strip_json(value), ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
        elif path.suffix.lower() == '.csv':
            data = canonical_csv(path)
        elif path.suffix.lower() in {'.md', '.txt'}:
            data = canonical_text(path)
        else:
            data = path.read_bytes()
    except Exception as exc:
        raise SystemExit(f'Canonicalization failed for {path}: {exc}')
    h.update(path.as_posix().encode())
    h.update(b'\0')
    h.update(data)
    h.update(b'\0')
print(h.hexdigest())
PY
}

cleanup() {
  git reset --hard -q HEAD
  git clean -fdq -- "${governed_paths[@]}"
}
trap cleanup EXIT

run_pipeline
first_semantic="$(canonical_fingerprint)"
first_status="$(git status --short --untracked-files=all -- "${governed_paths[@]}" || true)"

run_pipeline
second_semantic="$(canonical_fingerprint)"
second_status="$(git status --short --untracked-files=all -- "${governed_paths[@]}" || true)"

if [[ "$first_semantic" != "$second_semantic" ]]; then
  echo 'Real-session downstream semantic idempotency FAILED: second pass changed governed scientific/projection state.'
  echo "first-semantic-sha256=$first_semantic"
  echo "second-semantic-sha256=$second_semantic"
  git status --short --untracked-files=all -- "${governed_paths[@]}"
  exit 1
fi

echo "Real-session downstream semantic idempotency PASS for $id"
echo "semantic-state-sha256=$second_semantic"
if [[ "$first_status" != "$second_status" ]]; then
  echo 'NOTICE: byte-level workspace churn differs between passes, but canonical scientific state is invariant.'
fi
