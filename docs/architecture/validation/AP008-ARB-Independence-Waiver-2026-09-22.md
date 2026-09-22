# AP-008 ARB Independence Waiver — 2026-09-22

| Campo | Valore |
|---|---|
| Waiver ID | `W-AP008-ARB-INDEPENDENCE-2026-09-22` |
| Authorized by | Massimo Mainini, AP-008 accountable owner |
| Review mode | AI-assisted, owner-authorized |
| Requested role | ARB reviewer / re-review coordinator |
| Independent human ARB review | NOT SATISFIED |
| Scope | shadow pilot and bounded read-only governance package |
| Status | ACTIVE FOR SHADOW RE-REVIEW / NOT A LIVE APPROVAL |

## Authorization and limitation

The accountable owner authorizes an AI-assisted ARB re-review of the AP-008 package. This
waiver permits preparation and publication of a conditional disposition, but it does not make
the review equivalent to an independent human ARB decision.

The waiver does not authorize production promotion, live activation, broker/scheduler/command
integration or Safety Authority changes.

## Compensating controls

- production remains on `dsg-observatory-status-relay-00005-rof`;
- canary remains at 0% production traffic;
- security review remains explicitly conditional and non-independent;
- `runtime_event_published=false`;
- `safety_authority=NONE` and `command_authority=NONE`;
- technical OAT and shadow disable/restore evidence remain recorded.

## Exit condition

Replace this waiver with an independent human ARB review and decision before AP-008 can be
marked `READY_FOR_LIVE_INTEGRATION`.
