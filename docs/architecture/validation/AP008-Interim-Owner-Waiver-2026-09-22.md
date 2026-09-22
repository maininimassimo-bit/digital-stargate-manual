# AP-008 Interim Owner Waiver — 2026-09-22

| Campo | Valore |
|---|---|
| Waiver ID | `W-AP008-INTERIM-OWNERS-2026-09-22` |
| Authorized by | Massimo Mainini, AP-008 accountable owner |
| Effective date | 2026-09-22 |
| Scope | AP-008 shadow-pilot governance coordination only |
| Status | ACTIVE FOR SHADOW COORDINATION / NOT A LIVE APPROVAL |

## Authorization

The accountable owner authorizes Massimo Mainini to act on an interim basis as:

1. read-only session adapter owner;
2. consumer/portal reconciliation owner;
3. security/trust review coordinator;
4. disable/rollback operations owner.

## Compensating controls

- production traffic remains at 100% on the previous revision;
- canary remains at 0% production traffic;
- `runtime_event_published=false`;
- `safety_authority=NONE` and `command_authority=NONE`;
- no broker, scheduler or command path is introduced;
- all technical evidence remains attributable to the actual operator and timestamp;
- this waiver is recorded as a governance exception and is not represented as independent
  security approval or ARB approval.

## Explicit exclusions

This waiver does not:

- satisfy independent security/trust review;
- satisfy four-eyes or segregation-of-duties requirements;
- approve a live adapter or production promotion;
- approve a broker, scheduler, command path or Safety Authority integration;
- replace the required independent ARB decision.

## Exit condition

Replace this waiver with distinct role assignments and an independent security reviewer when
available. The current bounded scope is `READY_FOR_LIVE_INTEGRATION_WITH_WAIVER`; this waiver
does not expand the approved read-only scope.
