# BKL-036-F3 — Archived Evidence Health Score

| Field | Value |
|---|---|
| Identifier | `BKL-036-F3` |
| Status | In Progress — repository-only implementation candidate |
| Version | 0.1 |
| Date | 2026-09-19 |
| Parent | BKL-036 — Observatory Health Score |
| Authority | Read-only projection |
| Runtime impact | None |
| Safety Authority | No |

## Purpose

Publish a deterministic `0–100` score derived only from telemetry already acquired and archived in the repository.

## Policy

The seven mandatory domains are weather, dome, mount, camera, power, network and EAGLE health. All domains have equal weight. A qualifying domain is `PRESENT`, `COMPARABLE` and `CURRENT` under its own authoritative freshness contract and contributes `100`. The final score is the mean of the seven domain values.

If any mandatory domain is missing, stale, unavailable, partial, conflicting or not comparable, the score is `UNAVAILABLE`; no partial score is calculated.

## Public projection

The static portal consumer reads `docs/data/bkl-036-f3-health-score.json`. It must display:

- score or `UNAVAILABLE`;
- evaluation timestamp;
- source plane `repository_evidence`;
- explicit `repository evidence / non-live / non-real-time` label;
- source locators and fail-closed reasons.

The current repository evidence is intentionally published as `UNAVAILABLE`: the archived evidence does not establish all seven domains as simultaneously comparable and current. No evidence is fabricated to produce `100`.

## Boundaries

F3 does not consume live telemetry, introduce transport, alter EAGLE/CloudWatcher runtime, replace BKL-032 readiness, alter thresholds, issue commands, schedule sessions, remediate faults or change local physical interlocks.

## Validation

- `.github/scripts/generate-bkl-036-f3-health-score.mjs` — deterministic projection generation/check;
- `.github/scripts/verify-bkl-036-f3-health-score.mjs` — contract and publication boundary;
- `.github/scripts/test-bkl-036-f3-health-score.mjs` — six bounded fail-closed cases.
