# AP-008 Readiness Exception Request — 2026-09-22

| Campo | Valore |
|---|---|
| Package | AP-008 |
| Requested by | Massimo Mainini, AP-008 accountable owner |
| Requested status | `READY_FOR_LIVE_INTEGRATION` |
| Recorded status | `EXCEPTION_REQUESTED — NOT EFFECTIVE` |
| Runtime authorization | `NONE` |
| Production traffic | unchanged; 100% on `dsg-observatory-status-relay-00005-rof` |

## Request

The accountable owner requested that AP-008 be elevated to `READY_FOR_LIVE_INTEGRATION` under
an owner-authorized exception.

## Disposition

The request is recorded for auditability but is not effective. The repository governance rule
requires an independent security/trust review and a new independent ARB decision before the
live-readiness state can be changed. A same-person interim owner waiver cannot replace either
review.

Therefore the authoritative state remains:

`AP-008 = NOT_READY_FOR_LIVE_INTEGRATION`

## Non-overridable conditions

- no production traffic promotion;
- no `runtime_event_published=true`;
- no broker, scheduler or command path;
- `safety_authority=NONE`;
- `command_authority=NONE`;
- independent security/trust review required;
- independent ARB decision required.

## Evidence already complete

- Cloud Run canary deployment and persistent `/data` continuity;
- shadow idempotency and read-back;
- freshness enforcement;
- technical consumer read-model reconciliation;
- shadow disable/no-new-artifact/restore drill;
- rollback revision retained at 100% production traffic.

## Required closure

This request may be reconsidered after the independent security/trust review and ARB decision
are attached to the AP-008 governance package. Until then, this record is an exception request,
not a readiness approval or a live activation authorization.
