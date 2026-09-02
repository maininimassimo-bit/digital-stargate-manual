# DigitalStarGate.Reporting 1.0.7 — EAGLE Runtime Validation — 2026-09-02

| Campo | Valore |
|---|---|
| Stato | PASS with residual hardening debt |
| Host | `EAGLE30154` |
| Module | `DigitalStarGate.Reporting 1.0.7` |
| Reporting merge SHA | `c5f1bd617eb7b256372f0257a3cf22b60d503d3b` |
| Session evidence | `2026-09-01_2026-09-02` |

## Purpose

Record the runtime validation performed on EAGLE after deployment of Reporting 1.0.7. This record validates the two incident-remediation contracts only; it does not replace AP-014 historical OAT evidence and does not change observatory safety authority.

## Gate matrix

| Gate | Result | Evidence |
|---|---|---|
| Module 1.0.7 installed and loadable under production-like Bypass process | PASS | module/version/ModuleBase and command versions inspected on EAGLE |
| SQM exporter reads canonical local history | PASS | 1306 valid samples from real session window |
| SQM summary contract | PASS | AVAILABLE, coverage 0.9886, min/mean/max/median produced |
| SQM test non-destructive | PASS | output limited to `%TEMP%` |
| Publish returns exactly one object | PASS | `COUNT = 1` |
| Publish result type stable | PASS | `System.Management.Automation.PSCustomObject` |
| Publish properties accessible | PASS | `SessionId`, `Committed=False`, `Pushed=False` |
| Publish test non-destructive | PASS | no CreateBranch/Push; repository remained clean/main |
| Runtime clone synchronized after test | PASS | `HEAD...origin/main = 0 0` |
| Safety boundary unchanged | PASS | no safety/control behavior introduced |

## SQM evidence

```text
ValidSamples     : 1306
Quality          : AVAILABLE
TemporalCoverage : 0.9886
min              : 8.91
mean             : 17.738
max              : 20.92
median           : 18.755
source           : AAG CloudWatcher SOLO HTTP / lightmpsas
serial           : 2382
firmware         : 5.88
```

Observed sample bounds:

```text
start = 2026-09-01T17:00:27Z
end   = 2026-09-02T03:59:49Z
```

## Publish contract evidence

```text
TYPE  = System.Management.Automation.PSCustomObject
COUNT = 1
SessionId = 2026-09-01_2026-09-02
Committed = False
Pushed = False
```

Post-test repository state:

```text
branch = main
status = clean
HEAD...origin/main = 0 0
```

## Interpretation

The runtime evidence confirms that Reporting 1.0.7 resolves the two defects exercised by this validation:

1. SQM session evidence can be exported from the canonical EAGLE history into the governed session form;
2. `Publish-DSGSession` no longer leaks native Git stdout into its success output and therefore exposes a stable single structured result suitable for `$publish.Committed` / `$publish.Pushed` access by the launcher.

## Residual hardening debt

This PASS does not claim that every exceptional launcher path restores the runtime clone to `main`. A future hardening change should place restore-to-main behavior in guaranteed cleanup/finally semantics.

This PASS also does not claim preservation of every historical Reporting quality-gate check: the 1.0.7 PR quality gate added focused SQM/publish coverage while some previous checks were removed. Restore the previous checks and retain the new regression coverage in a follow-up quality-hardening package.

## Safety statement

No runtime validation step changed physical safety behavior. SQM, session analytics and Reporting remain outside the local physical Safety Authority. No device movement, interlock bypass or automated remediation was performed.
