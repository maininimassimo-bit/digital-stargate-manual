# AP-008 Security/Trust Review Independence Waiver — 2026-09-22

| Campo | Valore |
|---|---|
| Waiver ID | `W-AP008-SECURITY-REVIEW-INDEPENDENCE-2026-09-22` |
| Authorized by | Massimo Mainini, AP-008 accountable owner |
| Review mode | AI-assisted, owner-authorized |
| Requested role | Security/trust reviewer |
| Independent human review | NOT SATISFIED |
| Scope | AP-008 shadow transport and bounded read-only boundary |
| Status | ACTIVE FOR CANDIDATE REVIEW / NOT A LIVE APPROVAL |

## Authorization and limitation

The accountable owner authorizes an AI-assisted security/trust assessment of the AP-008
candidate package. This waiver permits preparation and publication of findings, but does not
make the assessment equivalent to an independent human security review.

The waiver does not authorize production promotion, live activation, broker/scheduler/command
integration or Safety Authority changes.

## Compensating controls

- production remains on `dsg-observatory-status-relay-00005-rof`;
- canary remains at 0% production traffic;
- technical OAT, persistence, idempotency, freshness and disable/restore evidence are retained;
- `runtime_event_published=false`;
- `safety_authority=NONE` and `command_authority=NONE`;
- independent ARB decision remains mandatory.

## Exit condition

Replace this waiver with an independent human security/trust review before AP-008 can be marked
`READY_FOR_LIVE_INTEGRATION`.
