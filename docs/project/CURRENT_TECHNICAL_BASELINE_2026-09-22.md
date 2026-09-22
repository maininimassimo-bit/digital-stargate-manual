# Digital StarGate — Current Technical Baseline 22/09/2026

| Field | Value |
|---|---|
| Identifier | `DSG-BASELINE-2026-09-22` |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Current package | BKL-036-F5 live read-only score gate |
| Predecessor closure | AP-008 bounded read-only integration |
| Owner | Massimo Mainini |

## Reconciled state

AP-008 is closed for its bounded read-only scope. Production Cloud Run revision
`dsg-observatory-status-relay-00015-hak` remains at 100% traffic with rollback
`dsg-observatory-status-relay-00005-rof`. The GitHub Pages portal consumes the production
Observatory Status and EAGLE Health projections without ingest credentials.

EAGLE30154 continuously publishes Observatory Status through the owner-authorized Windows
Scheduled Task. Continuous read-back verified HTTP `200` / `CURRENT` with advancing timestamps;
`/v1/command` remains `404`.

## Boundaries

- `runtime_event_published=false`;
- `safety_authority=NONE` and `command_authority=NONE` in the telemetry contract;
- local physical interlocks remain the only Safety Authority;
- no broker, remediation, automatic target selection or device command is introduced;
- BKL-032 remains the readiness/go-no-go authority.

## Next gate

BKL-036-F5 is owner-authorized as an implementation candidate. The seven-domain source mapping,
live envelope schema and fail-closed `UNAVAILABLE` fixture are now validated. The next gate is
owner-authorized production OAT, followed by independent ARB/RQ review. The archived F3
projection remains unchanged and `UNAVAILABLE` until F5 is independently accepted.
