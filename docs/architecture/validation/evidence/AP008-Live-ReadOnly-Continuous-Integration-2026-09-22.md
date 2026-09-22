# AP-008 Live Read-Only Continuous Integration — 2026-09-22

| Field | Result |
|---|---|
| Owner / accountable | Massimo Mainini |
| Host | `EAGLE30154` |
| Task | `DigitalStarGate-ObservatoryStatusTelemetry` |
| Runtime | `Start-ObservatoryStatusTelemetryRuntime.ps1` |
| Mode | Continuous read-only telemetry publication |
| Production relay | `dsg-observatory-status-relay-cfjug35c6q-ew.a.run.app` |
| Poll cadence | 15 seconds |
| Freshness | 60 seconds for the continuous runtime |
| Task result during verification | `267009` (`0x41301`, running) |

## Activation

The owner-authorized Windows Scheduled Task was installed and started on EAGLE30154 using
the repository runtime and the existing machine-scope DPAPI secret. The runtime health record
reported `state=RUNNING`, `transport.enabled=true`, active source
`NINA_OBSERVATORY_TELEMETRY`, `consecutive_failures=0`, and a populated publish correlation ID.

## Continuous read-back

Production read-back verified:

- Observatory Status: HTTP `200`, `quality=CURRENT`, observed timestamp advanced from
  `2026-09-22T17:53:23Z` to `2026-09-22T17:53:55Z`, then to `2026-09-22T17:54:57Z`;
- EAGLE Health: HTTP `200`, `quality=CURRENT`, observed timestamp advanced to
  `2026-09-22T17:54:11Z` on the next 60-second cadence;
- command route `/v1/command`: HTTP `404`;
- no deployment, revision change, traffic promotion, broker, or device command was performed.

The portal remains read-only and fail-closed for missing or stale snapshots. Continuous
publication does not change `runtime_event_published=false`, `safety_authority=NONE`, or
`command_authority=NONE`.
