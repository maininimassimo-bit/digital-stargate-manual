# Digital StarGate Observatory Telemetry Exporter for N.I.N.A.

Author: **Massimo Mainini**

Read-only N.I.N.A. plugin used as the **single local telemetry boundary** for Digital StarGate Observatory Status.

## Architecture

The plugin consolidates all approved local Observatory Status signals into one projection:

`%LOCALAPPDATA%\DigitalStarGate\telemetry\nina-observatory-status.json`

The intended Observatory Status service surface is:

| Service | Source / adapter | Current policy |
| --- | --- | --- |
| Dome / roof | `IDomeMediator` | Export connection and shutter state |
| Mount | `ITelescopeMediator` | Export connection and available park/home/tracking state |
| Imaging camera | `ICameraMediator` | Export connection and available temperature/exposure state |
| Weather | `IWeatherDataMediator` | Export available observing-condition measurements |
| Safety Monitor | `ISafetyMonitorMediator` | Export observed safety-monitor state as evidence only |
| Power | internal `PowerTelemetryAdapter` boundary | Remain `UNKNOWN` until an approved passive/read-only source is available |
| Network | internal `NetworkTelemetryAdapter` boundary | Integrate only passive/read-only host observations; management-only semantics remain `UNKNOWN` |

The previous direct CloudWatcher CSV adapter remains a migration/rollback path while the unified N.I.N.A. weather projection is commissioned and compared against the already verified weather feed. It should not become a second long-term authoritative path.

Standalone Power or Network producers are **not** part of the target runtime architecture. Discovery scripts may exist for commissioning and evidence collection, but validated Power/Network observations must ultimately be consumed by internal adapters in this plugin and emitted through the same unified N.I.N.A. projection.

## Power and Network adapter boundaries

The plugin owns the orchestration and projection lifecycle; vendor- or host-specific logic stays behind small read-only adapters.

Target internal structure:

```text
DomeTelemetryExporterPlugin
  |
  +-- N.I.N.A. mediator adapters
  |     dome / mount / camera / weather / safety
  |
  +-- PowerTelemetryAdapter
  |     passive/read-only source only
  |
  +-- NetworkTelemetryAdapter
        default route / gateway / Internet / DNS observations
        no router management commands
```

### Network policy

The Network adapter may derive only what its evidence supports. Passive EAGLE host checks can support a local `ONLINE`, `DEGRADED`, `OFFLINE` or `UNKNOWN` network observation, subject to commissioning and freshness validation.

The following fields must stay unresolved unless an approved direct source exists:

```text
active_link  = null / UNKNOWN
vpn          = null / UNKNOWN
lte_failover = null / UNKNOWN
```

A separate discovery utility such as `scripts/telemetry/Export-PassiveNetworkTelemetry.ps1` is therefore a commissioning/test harness only. Its logic may be migrated behind `NetworkTelemetryAdapter`, but the script is not intended to become a second production producer.

### Power policy

Power telemetry follows the same pattern. EAGLE Manager X / PLLService discovery has not produced a reliable passive Power source. Therefore the plugin continues to emit Power as `UNKNOWN` until a source with a provable read-only boundary is approved.

No proprietary IPC probing, port switching, relay command or control API may be introduced merely to populate the Power status.

## Safety boundary

The plugin is observational only. It:

- receives N.I.N.A. mediators through MEF dependency injection;
- reads mediator snapshots only;
- uses only explicitly approved passive/read-only local adapters for Power and Network;
- never calls equipment connect/disconnect operations;
- never calls ASCOM/COM device APIs directly for control;
- never issues shutter, mount, camera, switch, safety, power, router or other equipment commands;
- never changes equipment or network state;
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

1. verify the candidate Power/Network source independently with read-only discovery evidence;
2. implement the approved source behind the corresponding internal plugin adapter;
3. build the unified exporter in CI;
4. verify artifact SHA-256;
5. stop N.I.N.A. before replacing the pilot DLL;
6. install the artifact in the verified N.I.N.A. plugin API directory;
7. restart N.I.N.A. and confirm normal equipment and network operation;
8. verify the unified JSON without issuing equipment, power or network commands;
9. compare N.I.N.A. weather telemetry with the existing CloudWatcher adapter during the migration window;
10. validate Power/Network freshness and failure behaviour;
11. only after equivalence/freshness validation, make the unified N.I.N.A. projection the primary Observatory Status input and retire duplicate runtime paths.

Power and Network must remain `UNKNOWN` wherever their actual local sources or semantics have not been verified. No runtime values, protocols or device semantics may be inferred merely to complete the page.
