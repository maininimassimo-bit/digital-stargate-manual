# BKL-029 — SQM Recovery OAT Evidence — 2026-08-30

## Status

**PASS — recovery half complete. G6 runtime OAT satisfied.**

## Scope

Controlled recovery validation after the BKL-029 SQM failure OAT. The goal was to prove that removing the temporary SQM source override restores the approved AAG CloudWatcher SOLO source and returns SQM telemetry to `CURRENT` without affecting other telemetry domains or Safety Authority separation.

## Test host

- Computer: `EAGLE30154`
- Plugin family: Digital StarGate Observatory Telemetry Exporter
- Nominal SQM source: AAG CloudWatcher SOLO HTTP
- Expected device identity: Serial `2382`, firmware `5.88`

## Configuration recovery

N.I.N.A. was confirmed stopped before changing configuration.

The governed command was executed:

```powershell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass `
  -File .\scripts\telemetry\Set-NinaSqmSourceConfiguration.ps1 `
  -RemoveConfiguration
```

Evidence:

```text
Previous SQM configuration backed up to:
C:\Users\PrimaLuceLab\AppData\Local\DigitalStarGate\telemetry\configuration-backups\sqm-source.20260830-214417.json

SQM source configuration removed. Built-in defaults will apply at next NINA start.
```

The configuration file was verified absent:

```text
Test-Path %LOCALAPPDATA%\DigitalStarGate\telemetry\sqm-source.json
False
```

## Local N.I.N.A. projection evidence

After normal N.I.N.A. restart the SQM service recovered to:

```json
{
  "connected": true,
  "state": "AVAILABLE",
  "reason": null,
  "details": {
    "source": "AAG CloudWatcher SOLO HTTP / lightmpsas",
    "endpoint": "http://meteo.deeplab.space:8080/cgi-bin/cgiLastData",
    "configurationSource": "built-in-defaults",
    "sqmMagArcsec2": 18.44,
    "observedAtUtc": "2026-08-30T21:46:13.0000000Z",
    "freshUntilUtc": "2026-08-30T21:48:13.0000000Z",
    "quality": "CURRENT",
    "serial": "2382",
    "firmware": "5.88"
  }
}
```

Verified recovery properties:

- approved built-in endpoint restored;
- configuration provenance returned to `built-in-defaults`;
- instrumental SQM value restored;
- quality returned to `CURRENT`;
- identity restored to serial `2382`, firmware `5.88`;
- source timestamp and freshness restored.

## Other telemetry remained independent

During recovery the N.I.N.A. projection reported:

```text
Dome    : CLOSED
Mount   : UNKNOWN
Camera  : UNKNOWN
Weather : AVAILABLE
Power   : MAINS_PRESENT
Network : ONLINE
Safety  : SAFE
```

No unrelated telemetry regression was observed.

## Canonical Observatory Status evidence

`Export-NinaObservatoryStatus.ps1` produced:

```text
Observed UTC: 2026-08-30T21:46:24.9833427Z
Dome: CLOSED/CURRENT; Mount: UNKNOWN/CURRENT; Camera: UNKNOWN/CURRENT
Weather: AVAILABLE/CURRENT; SQM: 18.44/CURRENT; Safety observed: SAFE
Power: MAINS_PRESENT/CURRENT; Network: ONLINE/CURRENT
```

Canonical SQM fields:

```text
sqm_mag_arcsec2     : 18.44
sqm_quality         : CURRENT
sqm_observed_at_utc : 2026-08-30T21:46:13.0000000Z
sqm_fresh_until_utc : 2026-08-30T21:48:13.0000000Z
sqm_source          : NINA Observatory Telemetry Exporter / CloudWatcher SOLO SQM Adapter
```

## Safety boundary evidence

Canonical safety state after recovery:

```json
{
  "observed_state": "SAFE",
  "authority": "NINA_SAFETY_MONITOR_OBSERVATION",
  "reasons": [
    "Observed through NINA SafetyMonitor; local physical interlocks remain authoritative"
  ]
}
```

This confirms recovery of SQM telemetry has no coupling to Safety Authority decisions or physical interlocks.

## G6 conclusion

The complete controlled sequence has now been verified:

```text
CURRENT -> UNKNOWN/null -> CURRENT
```

with:

- no device command;
- no CloudWatcher configuration change;
- no network/router change;
- no retained stale value promoted as current;
- unrelated telemetry domains remaining independent;
- local physical Safety Authority remaining authoritative.

**BKL-029 G6 Runtime OAT: PASS.**

## Remaining capability work

The principal remaining BKL-029 capability gate is G3 historical scientific aggregation and evidence for:

- start;
- end;
- min;
- max;
- mean;
- median;
- valid samples;
- temporal coverage;
- source;
- quality.

No BKL-029 acceptance or closure is declared by this evidence alone.
