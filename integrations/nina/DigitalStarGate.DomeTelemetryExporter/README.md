# Digital StarGate Observatory Telemetry Exporter for N.I.N.A.

Author: **Massimo Mainini**

Read-only N.I.N.A. plugin used as the local telemetry boundary for Digital StarGate Observatory Status.

## Architecture

The plugin consolidates equipment snapshots already owned by N.I.N.A. into one local projection:

`%LOCALAPPDATA%\DigitalStarGate\telemetry\nina-observatory-status.json`

The intended Observatory Status service surface is:

| Service | N.I.N.A. source | Current policy |
| --- | --- | --- |
| Dome / roof | `IDomeMediator` | Export connection and shutter state |
| Mount | `ITelescopeMediator` | Export connection and available park/home/tracking state |
| Imaging camera | `ICameraMediator` | Export connection and available temperature/exposure state |
| Weather | `IWeatherDataMediator` | Export available observing-condition measurements |
| Safety Monitor | `ISafetyMonitorMediator` | Export observed safety-monitor state as evidence only |
| Power | not yet verified | `UNKNOWN` until an approved source is integrated |
| Network | not yet verified | `UNKNOWN` until an approved source is integrated |

The previous direct CloudWatcher CSV adapter remains a migration/rollback path while the unified N.I.N.A. weather projection is commissioned and compared against the already verified weather feed. It should not become a second long-term authoritative path.

## Safety boundary

The plugin is observational only. It:

- receives N.I.N.A. mediators through MEF dependency injection;
- reads mediator snapshots only;
- never calls equipment connect/disconnect operations;
- never calls ASCOM/COM device APIs directly;
- never issues shutter, mount, camera, switch, safety or other equipment commands;
- never changes equipment state;
- writes only the local Digital StarGate telemetry projection.

Telemetry is **not** a safety authority. Local physical interlocks and the approved local safety chain remain independent and authoritative.

## Projection contract

The unified projection uses `schemaVersion: 2` and `source: nina-observatory-telemetry-exporter`. Each service reports at minimum `connected`, `state`, `reason` and `details`. Missing, disconnected, unsupported or unreadable information degrades to `UNKNOWN`; the exporter must never invent operational state.

Example shape:

```json
{
  "schemaVersion": 2,
  "source": "nina-observatory-telemetry-exporter",
  "author": "Massimo Mainini",
  "observedAtUtc": "2026-08-19T11:00:00.0000000Z",
  "services": {
    "dome": { "connected": true, "state": "CLOSED", "reason": null, "details": {} },
    "mount": { "connected": true, "state": "PARKED", "reason": null, "details": {} },
    "camera": { "connected": true, "state": "READY", "reason": null, "details": {} },
    "weather": { "connected": true, "state": "AVAILABLE", "reason": null, "details": {} },
    "safety": { "connected": true, "state": "SAFE", "reason": null, "details": {} },
    "power": { "connected": null, "state": "UNKNOWN", "reason": "NO_VERIFIED_POWER_SOURCE", "details": {} },
    "network": { "connected": null, "state": "UNKNOWN", "reason": "NO_VERIFIED_NETWORK_SOURCE", "details": {} }
  }
}
```

## Migration and commissioning

The project continues to use the dedicated Windows GitHub Actions build. A new plugin artifact must be accepted only after a green build and controlled EAGLE commissioning.

Commissioning order:

1. build the unified exporter in CI;
2. verify artifact SHA-256;
3. stop N.I.N.A. before replacing the pilot DLL;
4. install the artifact in the verified N.I.N.A. plugin API directory;
5. restart N.I.N.A. and confirm normal equipment operation;
6. verify the unified JSON without issuing equipment motion commands;
7. compare N.I.N.A. weather telemetry with the existing CloudWatcher adapter during the migration window;
8. only after equivalence/freshness validation, make the unified N.I.N.A. projection the primary Observatory Status input and retire the duplicate weather path.

Power and network must remain `UNKNOWN` until their actual local sources and contracts have been verified. No runtime values, protocols or device semantics may be inferred merely to complete the page.
