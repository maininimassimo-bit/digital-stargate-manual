# BKL-030 — D3 Overhead Pilot Plan

| Campo | Valore |
|---|---|
| Identificativo | BKL-030-D3 |
| Stato | D3-A complete — D3-B required during normal imaging context |
| Target | EAGLE30154 |
| Baseline | `main` at `136fe59f1bd0f642bf81173645b7029a58070ba3` |
| Account target | `EAGLE30154\PrimaLuceLab` non-elevated |
| Safety | Read-only; no device/control/remediation path |

## Purpose

Measure the runtime cost of the already-governed EAGLE health source discovery before choosing collector cadences. The discovery is intentionally used as a conservative upper-bound workload because it queries the broad D1 source set in one bounded process; the future collector may split sources into fast/medium/slow cadence classes.

D3 does not activate the permanent collector and does not define operational severity thresholds.

## Pilot implementation

Script:

`Measure-EagleHealthDiscoveryOverhead.ps1`

Default bounded execution:

- 3 discovery iterations;
- 15 seconds between iterations;
- each discovery executes in a separate Windows PowerShell 5.1 process;
- process monitored every ~200 ms while alive;
- child discovery evidence retained under the pilot bundle.

Measured evidence:

- elapsed time per run;
- process CPU seconds per run;
- peak process working set;
- process exit code;
- stderr bytes;
- child discovery evidence bytes/files;
- relevant process context at pilot start;
- explicit `nina_running_at_start` and `phd2_running_at_start` flags.

## Execution phases

### D3-A — idle/actual-current-context pilot — COMPLETE

Executed on EAGLE30154 on 2026-09-03 in the actual current context. Corrected pilot evidence recorded in:

`evidence/BKL-030-D3A-Overhead-Pilot-2026-09-03.md`

Observed corrected summary:

- 3 iterations;
- 0 failures;
- average elapsed time 9502.1 ms;
- maximum elapsed time 11308.9 ms;
- average available CPU sample 5.859 seconds;
- maximum CPU sample 5.984 seconds;
- maximum peak working set 232718336 bytes;
- 0 stderr bytes on every run;
- N.I.N.A. not running at start;
- PHD2 not running at start.

These values are descriptive upper-bound evidence, not acceptance thresholds.

### D3-B — imaging-context pilot — REQUIRED

Because D3-A reported N.I.N.A. not running, repeat the same bounded pilot during a future normal N.I.N.A. session. Do not connect equipment or start an imaging sequence solely to satisfy D3.

D3 is complete only when evidence is sufficient to choose initial cadence classes without introducing unacceptable host contention. No numeric acceptance threshold is pre-declared because repository evidence does not yet establish one.

## Safety and rollback

The pilot:

- does not install a producer;
- does not create or modify Scheduled Tasks;
- does not start/stop services;
- does not modify registry/configuration;
- does not issue N.I.N.A., ASCOM, dome, mount, power, router or Safety Authority commands.

Rollback is deletion of the generated evidence bundle only if explicitly desired; no runtime configuration rollback is otherwise required.

## Runtime command

During a future normal N.I.N.A. session, execute from the repository root:

```powershell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass `
  -File ".\scripts\telemetry\Measure-EagleHealthDiscoveryOverhead.ps1" `
  -Iterations 3 `
  -IntervalSeconds 15
```

Expected terminal disposition:

`BKL-030 D3 PILOT RESULT: MEASURED (descriptive evidence only; no thresholds or acceptance inferred)`

The resulting JSON must be reviewed before D3 completion or cadence decisions are recorded.
