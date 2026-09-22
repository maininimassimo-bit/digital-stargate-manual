# BKL-036-F5 — Source Mapping and Live Envelope Gate

| Field | Value |
|---|---|
| Package | BKL-036-F5 |
| Gate | Source mapping and envelope contract |
| Status | Implemented as fail-closed contract fixture; live OAT not executed |
| Owner / accountable | Massimo Mainini |
| Authority | Descriptive projection only |

## Mapping

| Domain | AP-008 source | Required compatibility |
|---|---|---|
| weather | `systems.weather` in Observatory Status | current, schema-valid, comparable |
| dome | `systems.dome` in Observatory Status | current, schema-valid, comparable |
| mount | `systems.mount` in Observatory Status | current, schema-valid, comparable |
| camera | `systems.camera` in Observatory Status | current, schema-valid, comparable |
| power | `systems.power` in Observatory Status | current, schema-valid, comparable |
| network | `systems.network` in Observatory Status | current, schema-valid, comparable |
| eagle_health | EAGLE Health read-only projection | current, schema-valid, comparable |

The seven domains are a complete set. A missing, stale, malformed, unknown, partial or
conflicting domain makes the aggregate `UNAVAILABLE`; no partial score is emitted.

The contract is separate from BKL-032 readiness and does not create safety, command,
broker, scheduler or remediation authority. `runtime_event_published=false` remains mandatory.

The current fixture deliberately remains `UNAVAILABLE` until an owner-authorized F5 OAT
records all seven production read-backs.
