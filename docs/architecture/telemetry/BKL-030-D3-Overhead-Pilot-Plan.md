# BKL-030 — D3 Overhead Pilot Plan

| Campo | Valore |
|---|---|
| Identificativo | BKL-030-D3 |
| Stato | **COMPLETE — D3-A and D3-B executed** |
| Target | EAGLE30154 |
| Runtime baseline | `main` at `7928d87bf38514d041f3417546958d843ac122b9` for D3-B |
| Account target | `EAGLE30154\PrimaLuceLab` non-elevated |
| Safety | Read-only; no device/control/remediation path |

## Purpose

Measure the runtime cost of the already-governed EAGLE health source discovery before choosing collector cadences. The discovery is intentionally used as a conservative upper-bound workload because it queries the broad D1 source set in one bounded process; the future collector will split sources into fast/medium/slow classes.

D3 does not activate the permanent collector and does not define operational severity thresholds.

## Pilot implementation

Script: `Measure-EagleHealthDiscoveryOverhead.ps1`.

Bounded execution:

- 3 discovery iterations;
- 15 seconds between iterations;
- each discovery in a separate Windows PowerShell 5.1 process;
- process monitored at ~200 ms;
- child discovery evidence retained.

Measured evidence: wall duration, process CPU seconds, peak working set, exit code, stderr bytes, evidence size, and N.I.N.A./PHD2 process context.

## D3-A — non-imaging context — COMPLETE

Evidence: `evidence/BKL-030-D3A-Overhead-Pilot-2026-09-03.md`.

Observed summary:

- 3 iterations, 0 failures;
- average elapsed 9502.1 ms;
- maximum elapsed 11308.9 ms;
- average available CPU 5.859 s;
- maximum CPU 5.984 s;
- maximum peak working set 232718336 B;
- zero stderr;
- N.I.N.A. `False`, PHD2 `False` at start.

## D3-B — normal imaging context — COMPLETE

Evidence: `evidence/BKL-030-D3B-Overhead-Pilot-2026-09-03.md`.

Executed during a normal imaging session with N.I.N.A. and PHD2 both active. No process or equipment was started solely for the test.

Observed summary:

- 3 iterations, 0 failures;
- average elapsed 16769.9 ms;
- maximum elapsed 23204.4 ms;
- average available CPU 7.086 s;
- maximum CPU 7.422 s;
- maximum peak working set 206995456 B;
- zero stderr;
- N.I.N.A. `True`, PHD2 `True` at start.

## Interpretation and architecture decision

Both contexts completed without child-process failure or stderr. The imaging context materially increased wall latency and CPU cost of the monolithic discovery. Therefore D3 provides enough evidence to reject frequent full-discovery polling as the target design.

The future collector shall separate source groups by cost/volatility:

- **fast**: only low-cost volatile signals required for current host health;
- **medium**: moderate-cost inventory/status signals;
- **slow/on-change**: Event Log scans, Scheduled Task/result evidence, Windows Update/pending reboot, configuration drift, physical disk/reliability and similarly expensive or slowly changing sources.

No numeric polling interval or health severity threshold is accepted by D3. Concrete cadence values belong to G2/G3 contract/implementation work and must preserve N.I.N.A./PHD2 imaging priority.

## Safety and rollback

The pilot did not install a producer, create/modify Scheduled Tasks, start/stop services, modify registry/configuration, trigger Windows Update, reset USB/COM, or issue commands to N.I.N.A., ASCOM, dome, mount, power, router or Safety Authority.

Rollback is not required because no runtime configuration was changed.

## Closure

**D3-A COMPLETE. D3-B COMPLETE. D3 COMPLETE. Proceed to D4 Failure Model. BKL-030 remains In Progress.**
