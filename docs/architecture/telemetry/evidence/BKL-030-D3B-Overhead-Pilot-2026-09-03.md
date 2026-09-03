# BKL-030 — D3-B Imaging-Context Overhead Pilot Evidence — 2026-09-03

## Disposition

**D3-B COMPLETE. D3 Overhead Pilot COMPLETE.**

This evidence records the bounded BKL-030 overhead pilot executed on `EAGLE30154` during a normal imaging session with both N.I.N.A. and PHD2 active. The pilot remained read-only and did not modify the imaging sequence or observatory control paths.

## Runtime context

- Computer: `EAGLE30154`
- Repository branch at execution: `main`
- Repository baseline: `7928d87bf38514d041f3417546958d843ac122b9`
- Evidence bundle: `C:\DigitalStarGate\TelemetryEvidence\eagle-health-overhead-pilot-20260903-195917`
- Iterations: 3
- Interval: 15 seconds
- N.I.N.A. running at pilot start: `True`
- PHD2 running at pilot start: `True`
- Mode: read-only bounded measurement; no producer install or runtime configuration mutation.

## D3-B execution results

| Run | Elapsed ms | Exit code | CPU seconds | Peak working set bytes | stderr bytes |
|---:|---:|---:|---:|---:|---:|
| 1 | 23204.4 | 0 | 7.422 | 176107520 | 0 |
| 2 | 13801.0 | 0 | unavailable for this sample | 206995456 | 0 |
| 3 | 13304.2 | 0 | 6.750 | 173277184 | 0 |

Summary:

```text
iterations                 : 3
failures                   : 0
elapsed_ms_avg             : 16769.9
elapsed_ms_max             : 23204.4
cpu_seconds_avg            : 7.086
cpu_seconds_max            : 7.422
peak_working_set_bytes_max : 206995456
discovery_evidence_files   : 6
discovery_evidence_bytes   : 399842
nina_running_at_start      : True
phd2_running_at_start      : True
```

The missing CPU-seconds sample on run 2 is a measurement gap for that field only. Exit code was `0`, stderr was empty and discovery evidence was produced, therefore the run is not a failure.

## D3-A / D3-B comparison

| Metric | D3-A non-imaging | D3-B N.I.N.A./PHD2 active | Observation |
|---|---:|---:|---|
| Failures | 0/3 | 0/3 | Stable in both contexts |
| stderr | 0 | 0 | No child-process error evidence |
| Average elapsed | 9502.1 ms | 16769.9 ms | Imaging context materially increases wall latency |
| Maximum elapsed | 11308.9 ms | 23204.4 ms | Full discovery can exceed 20 s under imaging load |
| Average available CPU | 5.859 s | 7.086 s | Higher process CPU under imaging load |
| Maximum CPU | 5.984 s | 7.422 s | Higher process CPU under imaging load |
| Maximum working set | 232718336 B | 206995456 B | No observed memory increase in imaging pilot |

The comparison is descriptive evidence, not an operational threshold.

## Architecture consequence

D3 provides sufficient evidence to reject frequent execution of the monolithic discovery workload as the target collection design. The future collector shall separate source groups by cost and volatility rather than execute the full D1 discovery at a fast cadence.

Initial architecture direction, to be formalized in G2/G3:

- fast cadence: only low-cost volatile host signals required for current health;
- medium cadence: moderate-cost inventory/status signals;
- slow/on-change cadence: Event Log scans, Scheduled Task inventory/result interpretation, update/reboot/drift evidence, physical disk/reliability inventory and other expensive or slowly changing sources;
- detailed SMART remains unavailable non-elevated unless a separately governed adapter is later justified.

No concrete polling interval is accepted by D3. Cadence values require contract/implementation evidence and must preserve imaging workload priority.

## Safety

No N.I.N.A./PHD2 process was stopped, restarted or controlled. No Scheduled Task, service, registry, Windows Update, USB/COM, device, network, power, dome, mount or Safety Authority configuration was modified.

**Disposition: D3-A COMPLETE; D3-B COMPLETE; D3 COMPLETE. Proceed to D4 Failure Model. BKL-030 remains In Progress.**
