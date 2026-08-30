# BKL-029 — SQM History Aggregation OAT — 2026-08-31

## Status

**PASS — collector spool and standalone session-window aggregation verified.**

This evidence does not yet declare full G3 complete: integration through `Collect-SessionLogs.ps1` into an actual session package remains to be runtime-verified.

## Runtime host and implementation

- Host: `EAGLE30154`
- Plugin: Digital StarGate Observatory Telemetry Exporter `0.3.1.0`
- Branch: `feature/bkl-029-sqm-history`
- Workflow build: NINA Dome Telemetry Exporter #54 — `success`
- SQM source: AAG CloudWatcher SOLO HTTP / `lightmpsas`
- Source identity: serial `2382`, firmware `5.88`
- Spool: `%LOCALAPPDATA%\DigitalStarGate\telemetry\sqm-history.ndjson`

## Collector spool evidence

The append-only spool was observed with 14 valid samples in the test window and 14 unique source timestamps.

All samples were:

- `quality = CURRENT`;
- positive instrumental `sqmMagArcsec2` values;
- source `AAG CloudWatcher SOLO HTTP / lightmpsas`;
- serial `2382`;
- firmware `5.88`.

No duplicate source timestamp was observed in the tested window.

## Aggregation window

```text
SessionStart = 2026-08-30T22:07:52.0000000Z
SessionEnd   = 2026-08-30T22:14:23.0000000Z
RawSamples   = 14
```

Window duration is 391 seconds. With the verified/expected cadence of 30 seconds, the aggregator computes:

```text
expected_samples = floor(391 / 30) + 1 = 14
valid_samples    = 14
temporal_coverage = 1.0
```

## Aggregator command

The repository script `scripts/reporting/Export-SqmSessionHistory.ps1` was executed with:

```text
ExpectedCadenceSeconds = 30
```

and produced:

```text
SQM session history: 14 valid samples; coverage=1; quality=AVAILABLE
```

## Produced summary

```json
{
  "schema_version": "1.0",
  "start": "2026-08-30T22:07:52.0000000Z",
  "end": "2026-08-30T22:14:23.0000000Z",
  "min": 18.45,
  "max": 18.52,
  "mean": 18.4707,
  "median": 18.465,
  "valid_samples": 14,
  "temporal_coverage": 1,
  "expected_cadence_seconds": 30,
  "source": "AAG CloudWatcher SOLO HTTP / lightmpsas",
  "serial": "2382",
  "firmware": "5.88",
  "quality": "AVAILABLE"
}
```

## Independent mathematical verification

The 14 raw values were:

```text
18.45, 18.45, 18.45, 18.45,
18.46, 18.46, 18.47, 18.46,
18.50, 18.52, 18.48, 18.47,
18.49, 18.48
```

Independent verification gives:

```text
count  = 14
sum    = 258.59
min    = 18.45
max    = 18.52
mean   = 18.4707142857... -> 18.4707
median = 18.465
```

The generated `sqm-summary.json` therefore matches the raw evidence.

## Safety and architecture disposition

This historical path remains downstream of the read-only SQM collector. It does not:

- alter the CloudWatcher SOLO;
- issue equipment commands;
- influence SafetyMonitor;
- replace local physical safety interlocks;
- derive SQM from brightness/cloud/weather proxies.

Only `CURRENT` instrumental samples are included in aggregation.

## Quality-gate result

| Gate | Result | Evidence |
|---|---|---|
| Plugin CI 0.3.1.0 | Passed | NINA Dome Telemetry Exporter #54 |
| SQM spool creation | Passed | runtime `sqm-history.ndjson` |
| Unique source timestamps | Passed | 14/14 unique in test window |
| Provenance | Passed | source, serial 2382, FW 5.88 preserved |
| Standalone session aggregation | Passed | `sqm-summary.json` generated |
| Statistics correctness | Passed | independent mathematical verification |
| Temporal coverage | Passed | 14 expected / 14 valid = 1.0 |
| Safety separation | Passed | read-only historical path |
| `Collect-SessionLogs.ps1` package integration | **Not Executed** | runtime package test still required |

## Remaining G3 action

Run the existing `Collect-SessionLogs.ps1` flow against a real session window containing SQM samples and verify that the resulting session package contains:

```text
raw/sqm/sqm-history.ndjson
raw/sqm/sqm-summary.json
```

with values consistent with the standalone aggregation. Full G3 must remain open until that package-level evidence is captured.
