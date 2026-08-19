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

## Build and commissioning artifact

The project targets `net8.0-windows7.0` and uses centrally managed NuGet references pinned to the installed N.I.N.A. 3.2.0.9001 API surface.

Do **not** install Visual Studio, MSBuild, or a developer toolchain on the EAGLE. Builds are performed by the dedicated Windows GitHub Actions workflow:

`NINA Dome Telemetry Exporter`

A successful workflow run must complete all of these gates:

1. restore;
2. build Release;
3. verify the plugin DLL;
4. upload the commissioning artifact.

The commissioning artifact is named:

`DigitalStarGate.Nina.DomeTelemetryExporter`

and contains:

`DigitalStarGate.Nina.DomeTelemetryExporter.dll`

Before installation, record the workflow run, branch/head SHA and SHA-256 of the DLL.

## EAGLE commissioning guardrails

Commissioning is controlled and reversible:

- use only a DLL produced by a green CI run for the intended branch/head;
- stop N.I.N.A. before copying or removing the plugin DLL;
- back up any target plugin directory before modification;
- install only the exporter DLL and no development dependencies;
- restart N.I.N.A. and verify normal equipment operation before accepting telemetry;
- the expected output is `%LOCALAPPDATA%\DigitalStarGate\telemetry\nina-dome.json`;
- if the plugin does not load, N.I.N.A. behaves abnormally, or no valid projection is produced, remove the DLL and restart N.I.N.A.;
- do not issue dome motion commands merely to test telemetry. Validate initially against the current naturally observed shutter state.

No `systems.dome` integration is accepted until the local projection has been observed with valid timestamps/freshness under the normal operational N.I.N.A./TS Shelter workflow.
