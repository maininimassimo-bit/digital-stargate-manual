# BKL-030 — EAGLE Health D3 Overhead Pilot — 2026-08-31

## Status

**PASS — deterministic 180-second read-only overhead pilot completed on EAGLE30154.**

This is D3 measurement evidence only. It does not commission the BKL-030 producer and does not constitute BKL-030 acceptance.

## Execution

- Host: `EAGLE30154`
- Script: `scripts/telemetry/Measure-EagleHealthCollectorOverhead.ps1`
- Duration requested: 180 s
- Actual duration: 180.01 s
- Poll interval: 15 s
- Expected samples: 12
- Observed samples: 12
- Probe errors: 0
- N.I.N.A. observed running: true
- Evidence bundle: `C:\DigitalStarGate\TelemetryEvidence\eagle-health-overhead-pilot-20260831-082608`

## Measured overhead

| Metric | Measured value |
|---|---:|
| Total collector CPU time | 5.21875 s |
| Collector CPU as % of one logical CPU | 2.8991% |
| Collector working set average | 102,444,715 bytes (~97.70 MiB) |
| Collector working set maximum | 114,696,192 bytes (~109.39 MiB) |
| Probe elapsed average | 2405.475 ms |
| Probe elapsed maximum | 2955.4 ms |
| Schedule lag average | 9.125 ms |
| Schedule lag maximum | 20 ms |
| Host CPU after-probe average | 28.25% |
| Host CPU after-probe maximum | 86% |

## Interpretation

1. The complete pilot probe set executes successfully at 15-second scheduling with negligible schedule drift relative to the requested cadence.
2. The measured collector process consumed approximately 2.90% of one logical processor over the full pilot interval.
3. Working-set footprint remained approximately 92–109 MiB during the observed run and averaged about 97.70 MiB.
4. The complete probe set itself required approximately 2.4 seconds on average and up to 2.96 seconds in the measured run.
5. The host CPU peak of 86% is host-level evidence only. This pilot does not attribute that peak to the collector; the measured collector CPU time remains the authoritative process-specific overhead evidence.
6. Zero probe errors were observed while N.I.N.A. was running.

## Cadence implications

The pilot intentionally exercised a broad combined probe set every 15 seconds. The measured ~2.4 s probe duration means the production collector should not execute every source at this frequency.

Architecture disposition for the next implementation slice:

- **fast class candidate:** CPU, memory, process presence and plugin heartbeat;
- **medium class candidate:** storage capacity, log-source freshness and Scheduled Task state;
- **slow class candidate:** Event Log summaries, pending reboot, Windows Update, COM inventory and optional reliability/SMART evidence.

Exact production intervals remain a configuration decision for G3 and require implementation verification. D3 validates that a lightweight collector is feasible, but it does not authorize permanent execution or define severity thresholds.

## Safety review

No dome, mount, camera, power, network, relay, roof or Safety Authority command was issued. No Windows service, Scheduled Task, registry value or update state was changed. The pilot only read host telemetry and wrote its evidence bundle.

## Gate disposition

- D1 source discovery: PASS
- D2 privilege/source assessment: PASS
- G2 projection contract: DEFINED
- D3 overhead pilot: **PASS**
- G3 collector implementation: **BLOCKED until BKL-029 closure**
- G4 CI: NOT EXECUTED for BKL-030 collector
- G5 runtime OAT: NOT EXECUTED for BKL-030 collector
- G6 history: NOT EXECUTED
- G7 portal: NOT EXECUTED
- G8 Safety review: NOT EXECUTED as acceptance gate

**BKL-030 remains Planned.**
