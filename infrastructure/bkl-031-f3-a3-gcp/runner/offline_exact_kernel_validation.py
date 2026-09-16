#!/usr/bin/env python3
"""Read-only, network-free validation of the remediated runner against exact de442s."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from scientific_runner import (
    KERNEL_SHA256,
    PROFILE_SHA256,
    calculate,
    canonical_bytes,
    digest_file,
    validate_campaign,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kernel", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).parents[1]
    campaign_path = Path(__file__).with_name("BKL-031-F3-A3-SYNTHETIC-CAMPAIGN-001.json")
    profile_path = root / "method-profile" / "BKL-031-F3-A3-METHOD-PROFILE-001.json"
    if digest_file(args.kernel) != KERNEL_SHA256:
        raise SystemExit("exact kernel digest mismatch")
    if digest_file(profile_path) != PROFILE_SHA256:
        raise SystemExit("exact method profile digest mismatch")
    campaign = validate_campaign(campaign_path.read_bytes())
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    first = calculate(campaign, args.kernel, profile)
    second = calculate(campaign, args.kernel, profile)
    if canonical_bytes(first) != canonical_bytes(second):
        raise SystemExit("offline exact-kernel result is not repeatable")
    if len(first.get("vectors", [])) != 8:
        raise SystemExit("offline exact-kernel vector count mismatch")
    if first.get("metricEvaluationCount", 0) <= 0:
        raise SystemExit("offline exact-kernel metric set is empty")
    if first.get("metricPassCount") != first.get("metricEvaluationCount"):
        raise SystemExit("offline exact-kernel metric acceptance failed")
    if first.get("allEvaluatedMetricsPass") is not True or first.get("transit", {}).get("pass") is not True:
        raise SystemExit("offline exact-kernel campaign did not pass")
    print("DSG_OFFLINE_EXACT_KERNEL_VALIDATION=" + json.dumps({
        "kernelSha256": KERNEL_SHA256,
        "targets": campaign["targets"],
        "targetResolution": {"mars": "mars barycenter", "moon": "moon"},
        "vectorCount": len(first["vectors"]),
        "metricPassCount": first["metricPassCount"],
        "metricEvaluationCount": first["metricEvaluationCount"],
        "transit": first["transit"],
        "repeatabilityPass": True,
        "allEvaluatedMetricsPass": True,
        "network": "NONE",
        "cloudMutation": "NONE",
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
