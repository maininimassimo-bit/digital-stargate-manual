# AP-014 EAGLE Automatic Session Deployment Runbook

| Campo | Valore |
|---|---|
| Identificativo | AP14-OPS-EAGLE-AUTO-001 |
| Versione | 1.1 |
| Stato | Deployed; NO_SESSION runtime validated |
| Data | 2026-08-18 |
| Host | EAGLE / PrimaLuceLab |

## Objective

Operate and verify the governed automatic session producer on EAGLE so every future complete observing session is published through the AP-014 automatic portal pipeline, while no-observation nights terminate safely as `NO_SESSION`.

This runbook changes the physical EAGLE runtime and must therefore be executed on EAGLE. Repository commits alone do not prove deployment.

## Current production baseline

Before any runtime change verify:

- `maininimassimo-bit/DigitalStarGate.Reporting` is at or after `c902c51ddaae7493cbfecc019fef554ffc22ca7a`;
- `DigitalStarGate.Reporting` runtime version is `1.0.6`;
- `maininimassimo-bit/digital-stargate-manual` runtime clone is synchronized to current `main` before launcher execution;
- runtime clone path is `C:\DigitalStarGate\digital-stargate-manual-ap14-runtime`;
- runtime config is `C:\DigitalStarGate\Automation\reporting.config.psd1`;
- EAGLE scientific repository clone is clean before any pull/install action.

Current evidence sources:

```text
C:\Users\PrimaLuceLab\AppData\Local\NINA\Logs
C:\Users\PrimaLuceLab\Documents\PHD2
C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv
```

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

If the existing task references installed preflight/launcher files, retain their content and hashes before replacement.

## 2. Synchronize source repositories

Use fast-forward only. Stop on unrelated local changes.

Runtime manual repository:

```powershell
Set-Location 'C:\DigitalStarGate\digital-stargate-manual-ap14-runtime'
git status --porcelain
git switch main
git fetch origin
git pull --ff-only origin main
git rev-list --left-right --count HEAD...origin/main
```

Reporting source repository:

```powershell
Set-Location 'C:\DigitalStarGate\DigitalStarGate.Reporting-src'
git status --porcelain
git switch main
git fetch origin
git pull --ff-only origin main
Get-Content .\VERSION
```

Expected Reporting version is `1.0.6`.

## 3. Install/upgrade Reporting

From `C:\DigitalStarGate\DigitalStarGate.Reporting-src`:

```powershell
.\Install-DSGReporting.ps1 `
  -RepositoryRoot 'C:\DigitalStarGate\digital-stargate-manual-ap14-runtime' `
  -RuntimeConfigPath 'C:\DigitalStarGate\Automation\reporting.config.psd1'

Get-Module -ListAvailable DigitalStarGate.Reporting |
    Sort-Object Version -Descending |
    Select-Object -First 1 Name,Version,ModuleBase
```

The installer derives the destination version from the module manifest and validates the exact module instance imported from the installed manifest. A hard-coded module version or verification based on an arbitrary already-loaded module instance is not acceptable.

Verify the effective configuration:

```powershell
$config = 'C:\DigitalStarGate\Automation\reporting.config.psd1'
Test-Path $config
Get-Content $config -Raw
```

## 4. Governed preflight and Scheduled Task

Production chain:

```text
Scheduled Task
  -> C:\DigitalStarGate\Automation\Invoke-DSGSessionPreflight.ps1
  -> C:\DigitalStarGate\Automation\Invoke-DSGAutomaticSession.ps1
  -> DigitalStarGate.Reporting
```

The preflight must require:

- runtime clone exists and is a Git working tree;
- clean working tree;
- current branch exactly `main`;
- successful `git fetch origin main`;
- successful `git pull --ff-only origin main`;
- local `HEAD` exactly equal to `origin/main`.

Any failed invariant stops before session import/publication.

Verify task:

```powershell
Get-ScheduledTask -TaskName 'Digital StarGate - Daily Session Upload' | Format-List *
Get-ScheduledTaskInfo -TaskName 'Digital StarGate - Daily Session Upload' | Format-List *
```

Production trigger is daily at `07:20` local.

## 5. NO_SESSION acceptance behavior

For a night with no NINA/PHD2 observing evidence in the exact candidate window, Reporting 1.0.6 must return before creating staging or parsing CloudWatcher.

Expected log:

```text
MODULE version=1.0.6
DISCOVERY ... status=NO_SESSION nina=0 phd2=0 weatherRows=0
END outcome=NO_SESSION
```

Expected process/task result: `0`.

Production evidence on 18 August 2026:

- `LastRunTime = 2026-08-18 07:20:20` local;
- `LastTaskResult = 0`;
- candidate session `2026-08-17_2026-08-18` -> `NO_SESSION`;
- NINA files `0`;
- PHD2 files `0`;
- weather rows `0`;
- final outcome `NO_SESSION`.

This path is accepted in production.

## 6. M27 controlled replay

Do not use the daily wrapper blindly for the historical M27 session. Determine the actual session start/end from NINA/PHD2 evidence first, then use the certified Reporting commands with that explicit window.

```powershell
Import-Module DigitalStarGate.Reporting -Force
$config = 'C:\DigitalStarGate\Automation\reporting.config.psd1'

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

## 7. GitHub automatic chain

After EAGLE pushes `session/<session-id>`, no manual catalog or page edit is permitted.

Expected automatic chain:

1. `promote-session-package.yml` validates COMPLETE evidence, manifest hashes, scope and fast-forward ancestry;
2. package is promoted to `main`;
3. `analyze-session-automatic.yml` is explicitly dispatched;
4. analytics/history/target projections are regenerated;
5. `scientific-session-catalog.json` is regenerated;
6. `scientific-observation-index.json` is regenerated;
7. `deploy-pages.yml` is explicitly dispatched;
8. Session Explorer, Session Detail, Mission Control and enterprise search reflect the shared updated projections.

## 8. Acceptance evidence

Retain:

- deployment backup directory;
- old/new preflight and launcher hashes;
- task XML and post-deployment task definition;
- installed Reporting version/path;
- runtime repository branch/HEAD/clean status;
- automatic daily log and task result;
- actual M27 time window;
- preview/package status and evidence counts;
- session branch/commit SHA;
- promotion workflow run;
- analytics workflow run;
- Pages workflow run;
- resulting catalog/index commit;
- portal verification.

Record results in `docs/architecture/validation/AP14-W07-EAGLE-M27-OAT-Result.md`. The runtime `NO_SESSION` sub-gate is already PASS; overall OAT acceptance still requires the remaining real-session and downstream gates.

## 9. Rollback

If the scheduled runtime fails before overall acceptance:

1. disable `Digital StarGate - Daily Session Upload` only when continued execution could create unsafe or corrupt state;
2. restore the previous task XML from the deployment backup only after inspecting it;
3. restore previous preflight/launcher files only from captured backup/hash;
4. do not delete any produced scientific/session evidence;
5. do not force-push or rewrite Git history;
6. record the failure and remediation evidence before retry.

A failed AP-014 automation deployment must not affect AP-013B XISF transport/import.
