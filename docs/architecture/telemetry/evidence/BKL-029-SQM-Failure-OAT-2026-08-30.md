# BKL-029 — SQM Failure OAT Evidence — 2026-08-30

## Status

**PASS — failure half only. Recovery verification remains pending.**

## Scope

Controlled, non-invasive validation of BKL-029 failure behavior for the Digital StarGate N.I.N.A. Observatory Telemetry Exporter SQM adapter.

The test intentionally changed only the plugin-local SQM endpoint configuration. No CloudWatcher, network, router, power system, dome, mount, camera, SafetyMonitor or physical safety interlock was modified.

## Test host

- Computer: `EAGLE30154`
- Repository/runtime branch: `main`
- Plugin family: Digital StarGate Observatory Telemetry Exporter
- SQM adapter transport: HTTP read-only
- Nominal source: AAG CloudWatcher SOLO HTTP
- Failure simulation endpoint: `http://127.0.0.1:65534/cgi-bin/cgiLastData`

## Governed configuration

N.I.N.A. was confirmed stopped before configuration change.

The following command was executed:

```powershell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass `
  -File .\scripts\telemetry\Set-NinaSqmSourceConfiguration.ps1 `
  -Endpoint "http://127.0.0.1:65534/cgi-bin/cgiLastData" `
  -PollSeconds 30 `
  -FreshnessSeconds 120 `
  -HttpTimeoutSeconds 2
```

Resulting configuration:

```json
{
  "endpoint": "http://127.0.0.1:65534/cgi-bin/cgiLastData",
  "pollSeconds": 30,
  "freshnessSeconds": 120,
  "httpTimeoutSeconds": 2
}
```

The configuration script explicitly reported:

```text
No NINA process was started. No equipment connection was opened. No device command was sent.
```

## Local N.I.N.A. projection evidence

After N.I.N.A. startup, `services.sqm` reported:

```json
{
  "connected": null,
  "state": "UNKNOWN",
  "reason": "SQM_HTTP_READ_FAILED",
  "details": {
    "source": "AAG CloudWatcher SOLO HTTP / lightmpsas",
    "endpoint": "http://127.0.0.1:65534/cgi-bin/cgiLastData",
    "configurationSource": "C:\\Users\\PrimaLuceLab\\AppData\\Local\\DigitalStarGate\\telemetry\\sqm-source.json",
    "sqmMagArcsec2": null,
    "observedAtUtc": null,
    "freshUntilUtc": null,
    "quality": "UNKNOWN",
    "serial": null,
    "firmware": null
  }
}
```

This satisfies the required fail-safe behavior:

- no stale or synthetic SQM value was retained as current;
- the value became `null`;
- quality became `UNKNOWN`;
- failure reason was explicit;
- the active configuration source was traceable.

## Other telemetry remained independent

During the SQM failure condition the N.I.N.A. projection reported:

```text
Dome    : CLOSED
Mount   : UNKNOWN
Camera  : UNKNOWN
Weather : AVAILABLE
Power   : MAINS_PRESENT
Network : ONLINE
Safety  : SAFE
```

The SQM failure did not force unrelated telemetry domains to `UNKNOWN` and did not affect Power, Network, Weather, Dome or the observed SafetyMonitor state.

## Canonical Observatory Status evidence

`Export-NinaObservatoryStatus.ps1` produced:

```text
Observed UTC: 2026-08-30T21:41:17.9142225Z
Dome: CLOSED/CURRENT; Mount: UNKNOWN/CURRENT; Camera: UNKNOWN/CURRENT
Weather: AVAILABLE/CURRENT; SQM: /UNKNOWN; Safety observed: SAFE
Power: MAINS_PRESENT/CURRENT; Network: ONLINE/CURRENT
```

Canonical SQM fields:

```text
sqm_mag_arcsec2     : null
sqm_quality         : UNKNOWN
sqm_observed_at_utc : null
sqm_fresh_until_utc : null
sqm_source          : NINA Observatory Telemetry Exporter / CloudWatcher SOLO SQM Adapter
```

## Safety boundary evidence

Canonical safety state remained:

```json
{
  "observed_state": "SAFE",
  "authority": "NINA_SAFETY_MONITOR_OBSERVATION",
  "reasons": [
    "Observed through NINA SafetyMonitor; local physical interlocks remain authoritative"
  ]
}
```

This confirms that BKL-029 SQM failure does not become a Safety Authority input and does not alter the local physical safety chain.

## Result

**FAILURE HALF: PASS**

Verified properties:

- controlled SQM source loss produces `UNKNOWN/null`;
- no proxy or last-known SQM is promoted as current;
- source/configuration traceability is retained;
- unrelated telemetry continues independently;
- Safety Authority separation is preserved;
- no equipment command or network/device configuration change was required.

## Remaining OAT

Recovery half remains mandatory:

1. stop N.I.N.A.;
2. remove the temporary SQM source configuration using the governed script;
3. restart N.I.N.A.;
4. verify `configurationSource = built-in-defaults`;
5. verify source returns to serial `2382`, firmware `5.88`;
6. verify `sqmMagArcsec2` returns to a real instrumental value;
7. verify quality returns to `CURRENT`;
8. verify canonical projection also returns to `CURRENT`;
9. verify Safety remains independent.

BKL-029 G6 must not be marked fully complete until this recovery evidence is captured.
