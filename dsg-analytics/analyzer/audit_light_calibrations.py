#!/usr/bin/env python3
"""Audit explicit N.I.N.A. exposure types against an immutable catalog baseline.

Only identifies the calibration-as-LIGHT defect. It does not validate raw image
binaries or reinterpret other historical analytics severities.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

from analyze_session import CALIBRATION_IMAGE_TYPES, IMAGE_TYPE_RE, parse_nina


def baseline_json(root, revision, path):
    return json.loads(subprocess.check_output(["git", "show", f"{revision}:{path}"],
                                             cwd=root, encoding="utf-8-sig"))


def audit(root, revision):
    revision = subprocess.check_output(["git", "rev-parse", f"{revision}^{{commit}}"],
                                       cwd=root, text=True).strip()
    catalog = baseline_json(root, revision, "docs/data/scientific-session-catalog.json")
    records = []
    for session in sorted(catalog["sessions"], key=lambda row: row["sessionId"]):
        identity = session["sessionId"]
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2}", identity):
            raise ValueError("Invalid session identity")
        path = f"data/sessions/{identity[:4]}/{identity[5:7]}/{identity}"
        metrics_path = path + "/normalized/session-metrics.json"
        metrics = baseline_json(root, revision, metrics_path)
        counts = Counter()
        evidence = []
        for log in sorted((root / path / "raw/nina").rglob("*")):
            if not log.is_file():
                continue
            raw = log.read_bytes()
            historical = subprocess.check_output(["git", "show", f"{revision}:{log.relative_to(root).as_posix()}"], cwd=root)
            if hashlib.sha256(raw).digest() != hashlib.sha256(historical).digest():
                raise ValueError(f"Raw log drift from audit baseline: {identity}")
            evidence.append({"path": log.relative_to(root).as_posix(),
                             "sha256": hashlib.sha256(raw).hexdigest()})
            for line in raw.decode("utf-8", errors="replace").splitlines():
                low = line.lower()
                if "takeexposure" not in low or not any(x in low for x in ("starting instruction", "starting", "executing")):
                    continue
                match = IMAGE_TYPE_RE.search(line)
                counts[match.group("type").upper() if match else "UNTYPED"] += 1
        excluded = sum(count for kind, count in counts.items() if kind in CALIBRATION_IMAGE_TYPES)
        record = {"sessionId": identity, "instructionTypes": dict(sorted(counts.items())),
                  "excludedNonLightStarts": excluded, "rawLogDigests": evidence,
                  "baselineSeverity": metrics.get("severity"),
                  "state": "AFFECTED" if excluded else ("NO_TYPED_EXPOSURE_EVIDENCE" if not counts else "NO_CALIBRATION_FALSE_POSITIVE")}
        if excluded:
            corrected = parse_nina(root / path / "raw/nina")
            keys = ("light_started", "light_completed", "light_failed_explicit", "light_interrupted_unmatched", "technical_exposures_estimated")
            record["baselineCounters"] = {key: metrics.get("nina", {}).get(key) for key in keys}
            record["correctedCounters"] = {key: corrected[key] for key in keys}
        records.append(record)
    return {"kind": "DSG_LIGHT_CALIBRATION_AUDIT_V1", "baselineRevision": revision,
            "scope": "EXPLICIT_CALIBRATION_AS_LIGHT_ONLY", "sessionCount": len(records),
            "affectedSessionCount": sum(row["state"] == "AFFECTED" for row in records),
            "records": records}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-ref", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    report = audit(root, args.baseline_ref)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Audited {report['sessionCount']} catalog sessions; {report['affectedSessionCount']} affected")
