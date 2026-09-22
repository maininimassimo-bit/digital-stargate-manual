# AP-008 Readiness Exception Request — 2026-09-22

| Campo | Valore |
|---|---|
| Package | AP-008 |
| Requested by | Massimo Mainini, AP-008 accountable owner |
| Requested status | `READY_FOR_LIVE_INTEGRATION` |
| Recorded status | `GRANTED WITH WAIVER — READ-ONLY SCOPE ONLY` |
| Runtime authorization | `NONE` |
| Production traffic | 100% on `dsg-observatory-status-relay-00015-hak`; `00005-rof` retained for rollback |

## Request

The accountable owner requested that AP-008 be elevated to `READY_FOR_LIVE_INTEGRATION` under
an owner-authorized exception.

## Disposition

The request is granted only for the bounded read-only scope under the owner-witnessed security
and ARB attestations, explicit accepted-risk register and one-hour rollback rule. The waiver
does not authorize command, broker, scheduler, Safety Authority or live event publication
semantics.

The authoritative readiness state is:

`AP-008 = READY_FOR_LIVE_INTEGRATION_WITH_WAIVER`

## Non-overridable conditions

- no production traffic promotion;
- no `runtime_event_published=true`;
- no broker, scheduler or command path;
- `safety_authority=NONE`;
- `command_authority=NONE`;
- independent human review remains a follow-up improvement, not a prerequisite for this
  owner-witnessed waiver scope.

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
