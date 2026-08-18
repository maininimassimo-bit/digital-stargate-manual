# Digital StarGate Dome Telemetry Exporter for N.I.N.A.

Minimal read-only N.I.N.A. 3.2 plugin used by Digital StarGate Observatory Status.

## Safety boundary

The plugin:

- receives `IDomeMediator` through N.I.N.A. MEF dependency injection;
- registers only as an `IDomeConsumer`;
- consumes the `DomeInfo` snapshots already broadcast by N.I.N.A.;
- never calls `Connect`, `Disconnect`, `GetDevice`, `Action`, `SendCommand*`, `OpenShutter`, `CloseShutter`, `Park`, `FindHome`, `SlewToAzimuth`, or any ASCOM/COM API;
- never changes equipment state;
- writes only `%LOCALAPPDATA%\DigitalStarGate\telemetry\nina-dome.json`.

This projection is operational telemetry, not a safety authority. Physical/local interlocks remain authoritative.

## Projection

Example:

```json
{
  "schemaVersion": 1,
  "source": "nina-dome-exporter",
  "connected": true,
  "state": "CLOSED",
  "rawShutterStatus": "ShutterClosed",
  "observedAtUtc": "2026-08-18T18:30:00.0000000Z",
  "reason": null
}
```

State mapping:

| N.I.N.A. `ShutterState` | DSG state |
| --- | --- |
| `ShutterOpen` | `OPEN` |
| `ShutterClosed` | `CLOSED` |
| `ShutterOpening` / `ShutterClosing` | `MOVING` |
| `ShutterError` | `FAULT` |
| disconnected/unavailable/unmapped | `UNKNOWN` |

`safe` is deliberately not inferred by this plugin.

## Build on the EAGLE

The project targets .NET Framework 4.8 and references the assemblies installed with N.I.N.A. directly. By default:

```text
C:\Program Files\N.I.N.A. - Nighttime Imaging 'N' Astronomy
```

Override with MSBuild property `NinaInstallDir` if required.

From a Developer PowerShell/Command Prompt with MSBuild available:

```powershell
msbuild .\integrations\nina\DigitalStarGate.DomeTelemetryExporter\DigitalStarGate.DomeTelemetryExporter.csproj /p:Configuration=Release
```

Do not install the DLL into N.I.N.A. until the build has succeeded and the resulting references have been reviewed against the EAGLE's installed N.I.N.A. 3.2.0.9001 assemblies.
