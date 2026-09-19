# BKL-036-F3 — Archived Evidence Score Validation Plan

| Field | Value |
|---|---|
| Identifier | `BKL-036-F3-VAL-001` |
| Status | Proposed |
| Version | 0.1 |
| Date | 2026-09-19 |
| Runtime traffic | None authorized |
| Safety Authority | Local physical interlocks only |

## Acceptance criteria

- the contract is versioned and limited to repository-archived evidence;
- exactly seven mandatory domains are present;
- each qualifying domain contributes exactly `100` with equal weight;
- all seven qualifying domains are required for an available score;
- any missing, stale, unavailable, partial, conflicting or non-comparable domain produces `UNAVAILABLE` and `score=null`;
- the public projection labels itself repository evidence, non-live and non-real-time;
- timestamp, source locator and reasons are published;
- no readiness, safety, command, scheduling or remediation semantics are exposed;
- no live source, transport, consumer, EAGLE or CloudWatcher runtime is invoked.

## Commands

    node .github/scripts/generate-bkl-036-f3-health-score.mjs --check
    node .github/scripts/verify-bkl-036-f3-health-score.mjs
    node --test .github/scripts/test-bkl-036-f3-health-score.mjs

## Residual conditions

Source-specific freshness and retention remain governed by each source. A future operational or non-binary score requires a separate policy decision and independent ARB/Release Quality review.
