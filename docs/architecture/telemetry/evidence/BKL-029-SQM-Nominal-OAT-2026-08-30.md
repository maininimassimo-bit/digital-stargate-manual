# BKL-029 — SQM Nominal Runtime OAT — 2026-08-30

## Scope

Nominal runtime acceptance evidence for the Digital StarGate SQM telemetry path commissioned on `EAGLE30154` through the existing N.I.N.A. Observatory Telemetry Exporter.

This evidence covers the normal operating path only. Failure/recovery behavior remains a separate OAT gate.

## Commissioned artifact

```text
Plugin: Digital StarGate Observatory Telemetry Exporter
Version: 0.3.0.0
Host: EAGLE30154
Source commit: d1338e43d71f8b12f74d95822c36b184dbeda1b4
Workflow: NINA Dome Telemetry Exporter #50
Workflow result: completed / success
Artifact DLL SHA256: 2547f5c173b73c1d8594967617024e60715abe1ad93aa0257f72769372f5c93a
Installer result: PILOT INSTALL RESULT: PASS
```

The previous versioned plugin was backed up before replacement. N.I.N.A. was not running during installation and no equipment connection or command was issued by the installer.

## Runtime source

```text
Source: AAG CloudWatcher SOLO HTTP / lightmpsas
Endpoint: http://meteo.deeplab.space:8080/cgi-bin/cgiLastData
Device serial: 2382
Firmware: 5.88
Site: Manciano, physically close enough to Digital StarGate for scientific night-quality telemetry
```

The source field is explicit `lightmpsas`; no brightness/LDR proxy is used.

## Local N.I.N.A. projection evidence

Observed local projection:

```text
schemaVersion: 2
source: nina-observatory-telemetry-exporter
plugin version: 0.3.0.0
services.sqm.connected: true
services.sqm.state: AVAILABLE
services.sqm.details.sqmMagArcsec2: 18.56
services.sqm.details.quality: CURRENT
services.sqm.details.serial: 2382
services.sqm.details.firmware: 5.88
services.sqm.details.observedAtUtc: 2026-08-30T21:08:47Z
services.sqm.details.freshUntilUtc: 2026-08-30T21:10:47Z
```

The local N.I.N.A. projection continued to update independently of SQM source cadence through the existing plugin projection timer.

## Canonical Observatory Status evidence

`Export-NinaObservatoryStatus.ps1` successfully mapped the plugin projection to the canonical Observatory Status contract:

```text
weather.sqm_mag_arcsec2: 18.56
weather.sqm_quality: CURRENT
weather.sqm_observed_at_utc: 2026-08-30T21:09:15Z
weather.sqm_fresh_until_utc: 2026-08-30T21:11:15Z
weather.sqm_source: NINA Observatory Telemetry Exporter / CloudWatcher SOLO SQM Adapter
```

Observed concurrent service state:

```text
Power: MAINS_PRESENT / CURRENT
Network: ONLINE / CURRENT
Safety observed: UNKNOWN
Safety authority: NINA_SAFETY_MONITOR_OBSERVATION
Reason: NINA SafetyMonitor state unavailable or stale; local physical interlocks remain authoritative
```

The SQM path did not alter or synthesize Safety Authority state.

## Cadence measurement

Twenty observations were sampled every 15 seconds from the N.I.N.A. local projection. Unique source timestamps observed:

```text
21:11:18
21:11:47   +29 s
21:12:19   +32 s
21:12:47   +28 s
21:13:19   +32 s
21:13:48   +29 s
21:14:19   +31 s
21:14:48   +29 s
21:15:20   +32 s
21:15:52   +32 s
```

Derived cadence evidence:

```text
minimum interval: 28 s
maximum interval: 32 s
mean interval: approximately 30.4 s
observed quality: CURRENT for all 20 checks
observed serial: 2382 for all 20 checks
observed firmware: 5.88 for all 20 checks
```

The SQM value evolved gradually during the observation window from approximately `18.55` to `18.53` mag/arcsec², with no discontinuity or invalid sample observed.

## Freshness assessment

Current shadow settings:

```text
plugin SQM poll interval: 30 s
HTTP timeout: 5 s
SQM freshness window: 120 s
plugin projection interval: 5 s
```

The measured source cadence of approximately 30.4 seconds validates the 30-second polling design.

A 120-second source freshness window corresponds to approximately four missed source update cycles. This is accepted as a conservative commissioning value for failure detection pending the controlled failure/recovery OAT.

## Architecture disposition

Nominal runtime path:

```text
CloudWatcher SOLO 2382
  -> HTTP GET /cgi-bin/cgiLastData
  -> SqmTelemetryAdapter in N.I.N.A. plugin
  -> nina-observatory-status.json
  -> Export-NinaObservatoryStatus.ps1
  -> weather.sqm_* canonical projection
```

Nominal OAT disposition:

```text
G1 Source discovery: SATISFIED
G2 Realtime contract: RUNTIME VERIFIED
G6 Nominal cadence/freshness: PASS
G6 Failure/recovery behavior: PENDING
G3 Scientific history: PENDING
```

## Remaining OAT

Before final BKL-029 runtime acceptance:

1. perform a controlled non-invasive source-unreachable test;
2. verify the SQM service fails to `UNKNOWN` or `STALE` with `sqmMagArcsec2 = null`;
3. verify no change to local Safety Authority/interlocks;
4. restore source reachability;
5. verify automatic recovery to `CURRENT` with serial `2382`, firmware `5.88` and a fresh `lightmpsas` value;
6. retain evidence of transition timing relative to the 30 s poll and 120 s freshness settings.

No destructive network, CloudWatcher or observatory configuration change is authorized for this test.
