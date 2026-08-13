# AP-014 EAGLE Automatic Session Deployment Runbook

| Campo | Valore |
|---|---|
| Identificativo | AP14-OPS-EAGLE-AUTO-001 |
| Versione | 1.0 |
| Stato | Ready for execution |
| Data | 2026-08-13 |
| Host | EAGLE / PrimaLuceLab |

## Objective

Deploy the governed automatic session producer on EAGLE so every future complete observing session is published through the AP-014 automatic portal pipeline.

This runbook changes the physical EAGLE runtime and must therefore be executed on EAGLE. Repository commits alone do not prove deployment.

## Source baselines

Before execution verify:

- `maininimassimo-bit/DigitalStarGate.Reporting` is at or after `e177d0b0d8c76d00ea7bfa6ede5bcaed3e1cc3f7`;
- `maininimassimo-bit/digital-stargate-manual` is at or after `cb79a02ac27994812b2a3f917efd828e3c663cae`;
- EAGLE scientific repository clone is clean before any pull/install action.

## 1. Capture current runtime before modification

```powershell
$taskName = 'Digital StarGate - Daily Session Upload'
$backupRoot = 'C:\DigitalStarGate\SessionReports\deployment-backup\' + (Get-Date -Format 'yyyyMMdd-HHmmss')
New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null

$task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($task) {
    Export-ScheduledTask -TaskName $taskName | Set-Content (Join-Path $backupRoot 'scheduled-task.xml') -Encoding UTF8
    Get-ScheduledTaskInfo -TaskName $taskName | Format-List * | Out-File (Join-Path $backupRoot 'scheduled-task-info.txt')
    $task.Actions | Format-List * | Out-File (Join-Path $backupRoot 'scheduled-task-actions.txt')
}

Get-Module -ListAvailable DigitalStarGate.Reporting |
    Select-Object Name,Version,ModuleBase |
    Format-Table -AutoSize |
    Out-File (Join-Path $backupRoot 'reporting-modules.txt')
```

If the existing task references an installed `Invoke-DSGAutomaticSession.ps1`, copy it and retain its hash before replacement:

```powershell
Copy-Item '<existing-launcher-path>' (Join-Path $backupRoot 'Invoke-DSGAutomaticSession.previous.ps1')
Get-FileHash '<existing-launcher-path>' -Algorithm SHA256 |
    Format-List * |
    Out-File (Join-Path $backupRoot 'previous-launcher-sha256.txt')
```

## 2. Synchronize source repositories

Use fast-forward only. Stop on unrelated local changes.

```powershell
Set-Location 'C:\DigitalStarGate\digital-stargate-manual'
git status --short
git checkout main
git pull --ff-only origin main
```

Synchronize the local clone of `DigitalStarGate.Reporting` in the same way. If it does not exist, clone it into the governed installation source directory selected for EAGLE. Do not overwrite an unknown existing directory.

Expected source files include:

```text
Invoke-DSGAutomaticSession.ps1
Install-DSGAutomaticSessionTask.ps1
Install-DSGReporting.ps1
DigitalStarGate.Reporting\DigitalStarGate.Reporting.psd1
```

## 3. Install/upgrade Reporting

From the synchronized `DigitalStarGate.Reporting` source directory:

```powershell
.\Install-DSGReporting.ps1 -RepositoryRoot 'C:\DigitalStarGate\digital-stargate-manual'

Get-Module -ListAvailable DigitalStarGate.Reporting |
    Sort-Object Version -Descending |
    Select-Object -First 1 Name,Version,ModuleBase
```

The installer derives the destination version from the module manifest. A hard-coded `1.0.3` installation path is not acceptable.

Verify the effective configuration:

```powershell
$config = 'C:\DigitalStarGate\digital-stargate-manual\templates\reporting\reporting.config.psd1'
Test-Path $config
Get-Content $config -Raw
```

Expected evidence sources remain the certified EAGLE paths for PrimaLuceLab NINA logs, PHD2 logs and `C:\DigitalStarGate\Weather\CloudWatcher.csv`.

## 4. Install the governed launcher and task

The launcher path supplied to the task must point to the synchronized/versioned `Invoke-DSGAutomaticSession.ps1`.

First perform a WhatIf registration:

```powershell
.\Install-DSGAutomaticSessionTask.ps1 `
  -LauncherPath '<full-versioned-launcher-path>' `
  -TaskName 'Digital StarGate - Daily Session Upload' `
  -DailyTime '06:30' `
  -WhatIf
```

After inspection, register the task:

```powershell
.\Install-DSGAutomaticSessionTask.ps1 `
  -LauncherPath '<full-versioned-launcher-path>' `
  -TaskName 'Digital StarGate - Daily Session Upload' `
  -DailyTime '06:30'
```

Then verify action, principal, trigger and next run:

```powershell
Get-ScheduledTask -TaskName 'Digital StarGate - Daily Session Upload' | Format-List *
Get-ScheduledTaskInfo -TaskName 'Digital StarGate - Daily Session Upload' | Format-List *
```

## 5. M 27 controlled replay

Do not use the daily wrapper blindly for the historical M 27 session. Determine the real session start/end from NINA/PHD2 evidence first, then use the certified Reporting commands with that explicit window.

```powershell
Import-Module DigitalStarGate.Reporting -Force
$config = 'C:\DigitalStarGate\digital-stargate-manual\templates\reporting\reporting.config.psd1'

$preview = Import-DSGSession `
  -SessionStart '<actual-M27-start>' `
  -SessionEnd '<actual-M27-end>' `
  -ConfigPath $config

$preview | Format-List *
```

Proceed only if `Status = COMPLETE`.

Then:

```powershell
$package = Import-DSGSession `
  -SessionStart '<actual-M27-start>' `
  -SessionEnd '<actual-M27-end>' `
  -ConfigPath $config `
  -CopyToRepository

Get-DSGSessionStatus -SessionId $package.SessionId -ConfigPath $config

Publish-DSGSession `
  -SessionId $package.SessionId `
  -ConfigPath $config `
  -CreateBranch `
  -Push
```

## 6. GitHub automatic chain

After the EAGLE pushes `session/<session-id>` no manual catalog or page edit is permitted.

Expected automatic chain:

1. `promote-session-package.yml` validates COMPLETE evidence, manifest hashes, scope and fast-forward ancestry;
2. package is promoted to `main`;
3. `analyze-session-automatic.yml` is explicitly dispatched;
4. analytics/history/target projections are regenerated;
5. `scientific-session-catalog.json` is regenerated;
6. `scientific-observation-index.json` is regenerated;
7. `deploy-pages.yml` is explicitly dispatched;
8. Session Explorer, Session Detail, Mission Control and enterprise search reflect the shared updated projections.

## 7. Acceptance evidence

Retain:

- deployment backup directory;
- old/new launcher SHA-256;
- task XML and post-deployment task definition;
- installed Reporting version/path;
- actual M 27 time window;
- preview/package status and evidence counts;
- session branch/commit SHA;
- promotion workflow run;
- analytics workflow run;
- Pages workflow run;
- resulting catalog/index commit;
- portal verification.

Record the result in `docs/architecture/validation/AP14-W07-EAGLE-M27-OAT-Result.md`. Only an Accepted result can unlock `AP-014-Operational-Acceptance.md`.

## 8. Rollback

If the new scheduled runtime fails before acceptance:

1. disable `Digital StarGate - Daily Session Upload`;
2. restore the previous task XML from the deployment backup only after inspecting it;
3. restore the previous launcher only from the captured backup/hash;
4. do not delete any produced scientific/session evidence;
5. do not force-push or rewrite Git history;
6. record the failure and remediation evidence before retry.

A failed AP-014 automation deployment must not affect AP-013B XISF transport/import.
