# AP-014 EAGLE Reporting Runtime Inspection Checklist

- **Identifier:** AP14-W07-EAGLE-OAT-001
- **Status:** Executed; runtime baseline validated
- **Date:** 2026-08-18
- **Target host:** EAGLE / account `PrimaLuceLab`
- **Scope:** Read-only/runtime verification for AP-014 automatic session producer

## Purpose

Collect and preserve the minimum runtime evidence required to prove that the documented EAGLE reporting automation matches the governed source before any replay or automatic publication.

The original field inspection was executed on 13 August 2026. This revision records the reconciled production baseline validated through the unattended `NO_SESSION` run of 18 August 2026.

## Current governed runtime baseline

- Scheduled Task: `Digital StarGate - Daily Session Upload`.
- Trigger: daily at `07:20` local.
- Runtime repository: `C:\DigitalStarGate\digital-stargate-manual-ap14-runtime`.
- Required repository branch: `main`.
- Preflight: `C:\DigitalStarGate\Automation\Invoke-DSGSessionPreflight.ps1`.
- Launcher: `C:\DigitalStarGate\Automation\Invoke-DSGAutomaticSession.ps1`.
- Runtime configuration: `C:\DigitalStarGate\Automation\reporting.config.psd1`.
- Reporting module baseline: `DigitalStarGate.Reporting 1.0.6`.
- Compatibility target: Windows 10 LTSC / Windows PowerShell 5.1.
- NINA source: `C:\Users\PrimaLuceLab\AppData\Local\NINA\Logs`.
- PHD2 source: `C:\Users\PrimaLuceLab\Documents\PHD2`.
- CloudWatcher source: `C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv`.

The preflight is fail-safe: the launcher must not run unless the runtime clone is a clean Git working tree on `main`, successfully fast-forward synchronized, with local `HEAD` equal to `origin/main`.

## Read-only inspection

Run on EAGLE from PowerShell. Elevation is only required if Windows task permissions require it.

```powershell
$taskName = 'Digital StarGate - Daily Session Upload'
$task = Get-ScheduledTask -TaskName $taskName -ErrorAction Stop
$info = Get-ScheduledTaskInfo -TaskName $taskName -ErrorAction Stop

$task | Select-Object TaskName, State, Author, Description | Format-List
$task.Principal | Format-List UserId, LogonType, RunLevel
$task.Triggers | Format-List *
$task.Actions | Format-List Execute, Arguments, WorkingDirectory
$task.Settings | Format-List MultipleInstances, StartWhenAvailable, ExecutionTimeLimit
$info | Format-List LastRunTime, LastTaskResult, NextRunTime, NumberOfMissedRuns
```

Inspect the preflight and launcher without editing:

```powershell
Get-Item 'C:\DigitalStarGate\Automation\Invoke-DSGSessionPreflight.ps1' |
  Select-Object FullName, Length, LastWriteTime

Get-Item 'C:\DigitalStarGate\Automation\Invoke-DSGAutomaticSession.ps1' |
  Select-Object FullName, Length, LastWriteTime

Get-FileHash 'C:\DigitalStarGate\Automation\Invoke-DSGAutomaticSession.ps1' -Algorithm SHA256
```

Inspect Reporting and runtime configuration:

```powershell
Get-Module -ListAvailable DigitalStarGate.Reporting |
  Sort-Object Version -Descending |
  Select-Object Name, Version, ModuleBase

$config = 'C:\DigitalStarGate\Automation\reporting.config.psd1'
Test-Path $config
Get-Content $config -Raw
```

Inspect the runtime repository:

```powershell
Set-Location 'C:\DigitalStarGate\digital-stargate-manual-ap14-runtime'
git branch --show-current
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
git status --porcelain
```

Expected steady state is `main`, `HEAD = origin/main`, `0 0`, and an empty porcelain status.

## Session discovery semantics

Reporting 1.0.6 separates session existence detection from evidence collection:

- discovery uses the exact candidate window and NINA/PHD2 `CreationTime` or `LastWriteTime`;
- the wider evidence boundary is used only after discovery identifies a real candidate session;
- if neither NINA nor PHD2 exists in the exact candidate window, the result must be `NO_SESSION` before staging creation and before CloudWatcher parsing.

Expected unattended no-observation outcome:

```text
DISCOVERY ... status=NO_SESSION nina=0 phd2=0 weatherRows=0
END outcome=NO_SESSION
```

with process/task result `0`.

## Production evidence — 18 August 2026

The scheduled task executed at `2026-08-18 07:20:20` local and returned `LastTaskResult = 0`.

The automation log recorded:

```text
MODULE version=1.0.6
DISCOVERY session=2026-08-17_2026-08-18 status=NO_SESSION nina=0 phd2=0 weatherRows=0
END outcome=NO_SESSION
```

The runtime `NO_SESSION` sub-gate is therefore **PASS**.

## Stop conditions

Do not replay, install or modify the task if any of the following is true:

- task action does not invoke the governed preflight/launcher chain;
- preflight or launcher content cannot be inspected;
- runtime configuration or evidence paths differ without an approved reconciliation;
- runtime clone is not on `main`;
- runtime clone is dirty or cannot be proven aligned with `origin/main`;
- source evidence required for a real-session replay is absent;
- the launcher performs destructive cleanup, reset, force checkout, force push or history rewrite;
- a safety-relevant source or observatory state is uncertain.

## Evidence to retain

- Scheduled Task definition and `Get-ScheduledTaskInfo` output;
- preflight/launcher paths and launcher SHA-256;
- installed Reporting version and module path;
- runtime configuration;
- NINA/PHD2/weather source inventory for real-session OATs;
- Git branch/HEAD/working-tree state;
- daily automation log proving the final outcome.

## Next gate

The runtime `NO_SESSION` behavior is accepted. The next AP-014 OAT work is the controlled real-session package/publish path: repository copy, manifest/content/hash verification, session branch publication, governed promotion, analytics and Pages validation.
