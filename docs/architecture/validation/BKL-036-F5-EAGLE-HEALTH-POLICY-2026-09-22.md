# BKL-036-F5 — EAGLE Health Comparability Policy

| Field | Value |
|---|---|
| Status | Owner-confirmed policy definition |
| Required signals | `cpu`, `memory`, `storage`, `uptime`, `time_sync` |
| Comparable aggregate states | `HEALTHY`, `DEGRADED` |
| Unavailable aggregate state | `UNAVAILABLE` |
| Authority | Descriptive read-only projection only |

## Rules

- `time_sync` is valid only when `last_successful_sync_utc` is present and fresh; service
  state and `time_source` are not separate requirements.
- Freshness is evaluated from `fresh_until_utc`. An expired, missing or invalid value makes
  the aggregate `UNAVAILABLE`.
- CPU above 90% for at least five valid samples over five minutes is `DEGRADED`.
- Available memory below 20% for at least five valid samples over five minutes is `DEGRADED`.
- Storage is evaluated only for `C:` and `D:`. Either volume below 20% free is immediately
  `DEGRADED`; exactly 20% is normal.
- Missing, non-numeric or uncomputable CPU, memory or storage data is `UNAVAILABLE`.
- `uptime` is mandatory and must be current, but has no degradation threshold in this policy.
- Recovery from `DEGRADED` to `HEALTHY` occurs on the first normalized valid sample.

## Aggregate and score

- all five valid and no threshold exceeded → `HEALTHY`, EAGLE contribution `100`;
- at least one valid threshold exceeded → `DEGRADED`, EAGLE contribution `50`;
- any required signal unavailable → `UNAVAILABLE`, aggregate score remains `UNAVAILABLE`;
- `HEALTHY` and `DEGRADED` are comparable for BKL-036-F5;
- `UNAVAILABLE` is never converted to zero and never produces a partial score.

The machine-readable policy is in `docs/data/bkl-036-f5-eagle-health-policy-v1.json` and is
covered by `.github/scripts/verify-bkl-036-f5-eagle-health-policy.mjs`.
