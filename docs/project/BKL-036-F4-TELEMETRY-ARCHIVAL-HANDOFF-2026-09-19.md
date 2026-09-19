# BKL-036-F4 — Telemetry Archival Handoff

| Campo | Valore |
|---|---|
| Identifier | BKL-036-F4-HANDOFF-001 |
| Status | Implementation candidate |
| Capability | Observatory Health Score |
| Scope | Read-only snapshot import and repository archival |

## Owner decision

The Repository Owner authorized the next BKL-036 gate after F3 to implement governed telemetry acquisition/archival. This increment is intentionally bounded to a local snapshot importer and its machine-readable contract.

## Delivered boundary

- repository evidence only;
- no live network transport;
- no commands or scheduling;
- no remediation;
- local physical interlocks remain Safety Authority;
- incomplete evidence remains fail-closed;
- F3 remains UNAVAILABLE with the current fixture.

## Next dependency

A separate runtime activation gate is required before connecting the importer to EAGLE30154, CloudWatcher, N.I.N.A. or any hosted relay. That gate must approve source authority, credentials, retention, failure behavior and publication cadence.
