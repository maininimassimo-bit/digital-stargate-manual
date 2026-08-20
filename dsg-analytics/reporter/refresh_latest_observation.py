#!/usr/bin/env python3
"""Refresh latest-observation.json from the latest governed session.

The script resolves the newest normalized session package, rebuilds the latest
observation through update_latest_observation.py, and preserves generated_at
when the semantic payload is unchanged. This makes the operation idempotent
for GitHub Pages builds while still reacting to governed metadata corrections.
"""
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

from update_latest_observation import build_payload, read_json


def latest_session_dir(repo_root: Path) -> Path:
    candidates = sorted(
        path.parent.parent
        for path in repo_root.glob("data/sessions/*/*/*/normalized/session-metrics.json")
    )
    if not candidates:
        raise SystemExit("No normalized session metrics found.")
    return max(candidates, key=lambda path: path.name)


def semantic_payload(payload: dict) -> dict:
    value = deepcopy(payload)
    value.pop("generated_at", None)
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/data/realtime/latest-observation.json"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = args.repo_root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    session_dir = latest_session_dir(root)
    metrics = read_json(session_dir / "normalized" / "session-metrics.json")
    existing = read_json(output, default={})
    rebuilt = build_payload(session_dir, metrics, existing)

    if semantic_payload(existing) == semantic_payload(rebuilt):
        rebuilt["generated_at"] = existing.get("generated_at", rebuilt["generated_at"])
        print(f"Latest observation already current for {rebuilt['session_id']}")
        return 0

    if args.check:
        print(
            "Latest observation projection is stale for "
            f"{rebuilt['session_id']}; run with --write semantics (without --check)."
        )
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(rebuilt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Refreshed {output.relative_to(root)} for {rebuilt['session_id']} "
        f"from {rebuilt['target'].get('coordinate_source')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
