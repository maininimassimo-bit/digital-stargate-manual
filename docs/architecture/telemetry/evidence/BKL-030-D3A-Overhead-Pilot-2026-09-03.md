# BKL-030 — D3-A Overhead Pilot Evidence — 2026-09-03

## Disposition

**D3-A COMPLETE — current/idle operational context measured successfully. D3 remains OPEN pending D3-B imaging-context evidence.**

This evidence records the corrected bounded overhead pilot executed on `EAGLE30154` after fixing child-process exit-code capture in `Measure-EagleHealthDiscoveryOverhead.ps1`.

## Runtime context

- Computer: `EAGLE30154`
- Repository branch: `bkl-030-d3-overhead-pilot`
- Pilot script commit: `205f6ecd5a2a8d7452e7cae33beb2c7a36fa8a23`
- Evidence bundle: `C:\DigitalStarGate\TelemetryEvidence\eagle-health-overhead-pilot-20260903-085836`
- Iterations: 3
- Interval: 15 seconds
- N.I.N.A. running at pilot start: `False`
- PHD2 running at pilot start: `False`
- Mode: read-only bounded measurement; no producer install or runtime configuration mutation.

## Corrected execution results

| Run | Elapsed ms | Exit code | CPU seconds | Peak working set bytes | stderr bytes |
|---:|---:|---:|---:|---:|---:|
| 1 | 11308.9 | 0 | 5.984 | 209715200 | 0 |
| 2 | 8575.2 | 0 | unavailable for this sample | 213704704 | 0 |
| 3 | 8622.2 | 0 | 5.734 | 232718336 | 0 |

Summary emitted by the pilot:

```text
iterations                 : 3
failures                   : 0
elapsed_ms_avg             : 9502.1
elapsed_ms_max             : 11308.9
cpu_seconds_avg            : 5.859
cpu_seconds_max            : 5.984
peak_working_set_bytes_max : 232718336
discovery_evidence_files   : 6
discovery_evidence_bytes   : 375692
nina_running_at_start      : False
phd2_running_at_start      : False
```

The missing CPU-seconds sample on run 2 is treated as a measurement gap for that field only. The process exit code was `0`, stderr was empty and the run produced discovery evidence, so it is not classified as a failed run.

## Interpretation

The monolithic D1 discovery workload is intentionally a conservative upper bound for the future collector because it queries the broad source set in one process. D3-A demonstrates that this bounded workload can complete repeatedly without process failure in the observed non-imaging context.

The observed upper-bound cost is descriptive evidence only:

- average wall duration ~9.5 seconds;
- maximum wall duration ~11.3 seconds;
- observed CPU consumption ~5.9 process-seconds where available;
- maximum observed working set ~232.7 MB (~222 MiB);
- no stderr output;
- no failed iterations.

No HEALTHY/DEGRADED/CRITICAL judgement or numeric cadence acceptance threshold is inferred from these measurements.

## D3 status

D3-A is complete. D3 is **not complete** because N.I.N.A. and PHD2 were not running at pilot start. Per the approved D3 plan, D3-B must repeat the same bounded measurement during a future normal N.I.N.A. operational session. N.I.N.A., PHD2, equipment or an imaging sequence must not be started solely for the pilot.

## Safety

No Scheduled Task, service, registry, update state, device, network, power, dome, mount, ASCOM control path or Safety Authority configuration was modified.

**Disposition: D3-A COMPLETE; D3-B REQUIRED DURING NORMAL IMAGING CONTEXT; BKL-030 remains In Progress.**
