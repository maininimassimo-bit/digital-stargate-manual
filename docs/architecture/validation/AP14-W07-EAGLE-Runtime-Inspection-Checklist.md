# AP-014 EAGLE Reporting Runtime Inspection Checklist

- **Identifier:** AP14-W07-EAGLE-OAT-001
- **Status:** Ready for field execution
- **Date:** 2026-08-13
- **Target host:** EAGLE / account `PrimaLuceLab`
- **Scope:** Read-only inspection before M 27 session replay

## Purpose

Collect the minimum runtime evidence required to reconcile the documented EAGLE reporting automation with the versioned source before replaying M 27.

## Documented runtime baseline

The `DigitalStarGate.Reporting` release notes identify:

- Scheduled Task: `Digital StarGate - Daily Session Upload`;
- automation launcher: `Invoke-DSGAutomaticSession.ps1`;
- compatibility target: Windows 10 LTSC / Windows PowerShell 5.1;
- operational module lineage: installed `DigitalStarGate.Reporting` 1.0.3 with fixes later promoted into source baseline 1.0.4.

The launcher itself is not currently versioned in the accessible GitHub repositories. No replacement launcher is authorized until the installed file has been inspected and reconciled.

## Read-only inspection

Run on EAGLE from an elevated PowerShell only if required to read the task definition. These commands do not change the task or session data.

```powershell
$taskName = 'Digital StarGate - Daily Session Upload'
$task = Get-ScheduledTask -TaskName $taskName -ErrorAction Stop
$info = Get-ScheduledTaskInfo -TaskName $taskName -ErrorAction Stop

$task | Select-Object TaskName, State, Author, Description |
  Format-List

$task.Principal | Format-List UserId, LogonType, RunLevel
$task.Triggers | Format-List *
$task.Actions | Format-List Execute, Arguments, WorkingDirectory
$task.Settings | Format-List MultipleInstances, StartWhenAvailable, ExecutionTimeLimit
$info | Format-List LastRunTime, LastTaskResult, NextRunTime, NumberOfMissedRuns
```

Resolve the launcher path from `Actions.Arguments` and inspect it without editing:

```powershell
Get-Item '<resolved Invoke-DSGAutomaticSession.ps1 path>' |
  Select-Object FullName, Length, LastWriteTime

Get-FileHash '<resolved Invoke-DSGAutomaticSession.ps1 path>' -Algorithm SHA256
Get-Content '<resolved Invoke-DSGAutomaticSession.ps1 path>' -Raw
```

Inspect the installed reporting module and configuration:

```powershell
Get-Module -ListAvailable DigitalStarGate.Reporting |
  Select-Object Name, Version, ModuleBase

$config = 'C:\DigitalStarGate\digital-stargate-manual\templates\reporting\reporting.config.psd1'
Test-Path $config
Get-Content $config -Raw
```

Expected source paths from the certified Reporting baseline are:

```text
C:\Users\PrimaLuceLab\AppData\Local\NINA\Logs
C:\Users\PrimaLuceLab\Documents\PHD2
C:\DigitalStarGate\Weather\CloudWatcher.csv
```

## M 27 evidence presence

Before replay, verify that source evidence exists for the night 10/11 August 2026. Do not create placeholder evidence.

```powershell
Get-ChildItem 'C:\Users\PrimaLuceLab\AppData\Local\NINA\Logs' -File -Recurse |
  Where-Object LastWriteTime -ge '2026-08-10T12:00:00' |
  Where-Object LastWriteTime -le '2026-08-11T12:00:00' |
  Select-Object FullName, Length, LastWriteTime

Get-ChildItem 'C:\Users\PrimaLuceLab\Documents\PHD2' -File -Recurse |
  Where-Object LastWriteTime -ge '2026-08-10T12:00:00' |
  Where-Object LastWriteTime -le '2026-08-11T12:00:00' |
  Select-Object FullName, Length, LastWriteTime

Get-Item 'C:\DigitalStarGate\Weather\CloudWatcher.csv' |
  Select-Object FullName, Length, LastWriteTime
```

The wide inspection window is diagnostic only. The actual `Import-DSGSession` replay must use the real observing session start/end determined from NINA/PHD2 evidence, not guessed values.

## Stop conditions

Do not replay or modify the task if any of the following is true:

- task action does not invoke the documented reporting automation;
- launcher content cannot be inspected;
- module/configuration paths differ from the documented baseline without explanation;
- NINA or PHD2 evidence for M 27 is absent;
- CloudWatcher source is absent and the resulting session would be `PARTIAL`;
- repository working tree on EAGLE contains unrelated changes;
- the launcher performs destructive cleanup or force Git operations.

## Evidence to retain

- task definition and `Get-ScheduledTaskInfo` output;
- launcher full path, SHA-256 and source text;
- installed module version and module path;
- reporting configuration;
- M 27 NINA/PHD2/weather source inventory;
- Git branch/HEAD/working-tree status on the EAGLE clone.

## Next gate

After this inspection, reconcile `Invoke-DSGAutomaticSession.ps1` against `DigitalStarGate.Reporting` source. Only then execute the M 27 replay and observe the downstream `manifest -> analytics -> catalog -> Pages` pipeline.
