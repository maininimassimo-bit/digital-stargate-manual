# BKL-036-F5 — EAGLE Health Policy Activation Package

## Scope

This package activates the owner-confirmed BKL-036-F5 policy in the read-only
EAGLE Health projection path. It does not add command, broker, scheduler,
remediation or safety-authority behavior.

## Implemented behavior

- the collector keeps a bounded five-minute window with samples at most once per minute;
- CPU is `DEGRADED` only when all five window samples are above 90%;
- available memory is `DEGRADED` only when all five window samples are below 20%;
- either `C:` or `D:` below 20% free is immediately `DEGRADED`;
- `time_sync` is valid only with a present, non-future `last_successful_sync_utc` and a fresh envelope;
- missing, stale or uncomputable required data is `UNAVAILABLE` and has no score;
- the first normalized valid window recovers the descriptive state to `HEALTHY`;
- the relay accepts only `HEALTHY`, `DEGRADED` or `UNAVAILABLE` with deterministic reasons.

## Verification

| Check | Result |
|---|---|
| BKL-036-F5 deterministic policy validator | PASS |
| PowerShell parse validation | PASS |
| Relay Python compile validation | PASS |
| Empty required signal set fails closed to `UNAVAILABLE` | PASS |
| Command path introduced | NO |
| Safety authority introduced | NO |

## OAT boundary

This package is source-complete but not live-activated from the current
operator host. The current host is not `EAGLE30154` and has no authorized
EAGLE runtime worktree or scheduled task. The final OAT must therefore run on
EAGLE30154 using the existing secret path, publish one projection, and verify
production `GET /v1/eagle-health` returns `200` with a current
`HEALTHY`, `DEGRADED` or fail-closed `UNAVAILABLE` summary. No bearer token is
to be printed or copied into evidence.

## Rollback

Rollback remains the existing Cloud Run revision rollback and local publisher
disable path. This package does not change production traffic or promote a
revision.
