# AP-008 / BKL-036-F5 — Final Live Read-Only Evidence

| Field | Value |
|---|---|
| Date | 2026-09-22 |
| Owner / accountable | Massimo Mainini |
| Host | EAGLE30154 |
| Relay | `dsg-observatory-status-relay`, `europe-west1` |
| Production revision | `dsg-observatory-status-relay-00019-keq` |
| Production traffic | `100%` |

## Result

AP-008 live integration is operational within the approved read-only waiver. Observatory
Status, EAGLE Health and SessionCompleted shadow remain transport-only; no broker, command
path, automatic remediation or Safety Authority transfer is enabled.

The EAGLE policy is active and evaluated fail-closed. The five-minute CPU/memory window
reached five valid samples. Production read-back returned:

```text
HTTP 200
quality=CURRENT
state=UNAVAILABLE
reason=TIME_SYNC_NOT_CURRENT
```

This is the expected governed result because `last_successful_sync_utc` is absent on the
host. A numeric score is therefore intentionally not emitted.

## Runtime evidence

- EAGLE publish returned HTTP `202` with idempotency correlation.
- `GET /v1/eagle-health` returned the current fail-closed projection.
- `GET /health` returned `RUNNING` with zero rejected requests at verification.
- `GET /v1/command` remains `404`.
- Scheduled task `DigitalStarGate-EagleHealthTelemetry` points to the AP-008 worktree and
  completed with `LastTaskResult = 0`.
- The bearer token remained in the existing DPAPI secret path and was not printed.

## Waiver boundary

Accepted limitations remain: secret lifecycle, IAM/bucket, CORS/data exposure, log
redaction and supply-chain risks. Rollback remains available within one hour for an
unresolvable technical issue. Enabling time synchronization or otherwise remediating the
host is outside this read-only AP-008 scope.
