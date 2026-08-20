# AP-014 EAGLE Automatic Session Deployment Runbook

| Campo | Valore |
|---|---|
| Identificativo | AP14-OPS-EAGLE-AUTO-001 |
| Versione | 1.2 |
| Stato | Deployed; NO_SESSION runtime validated; BKL-019 logging gate pending execution |
| Data | 2026-08-20 |
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

## 6. BKL-019 — N.I.N.A. C8 informational logging gate

This is a physical-runtime gate. It must be executed on `EAGLE30154` with the actual C8 N.I.N.A. profile. Repository state, Observatory Status connectivity, old M27 logs, or successful Reporting CI do **not** prove this gate.

### 6.1 Preconditions and evidence preservation

1. Do not change mount, dome, weather or local safety interlocks.
2. Start from a safe operating state appropriate for a controlled N.I.N.A. test.
3. Record the active N.I.N.A. profile name and N.I.N.A. version.
4. Capture screenshots or an equivalent immutable record of the logging setting before and after the change.
5. Preserve the pre-change log file and its SHA-256; never overwrite or delete historical N.I.N.A. evidence.
6. If changing the logging level requires restarting N.I.N.A., close it normally and verify that no observing sequence is active before restart.

Evidence directory:

```powershell
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$evidence = "C:\DigitalStarGate\SessionReports\runtime-evidence\bkl019-nina-logging-$stamp"
New-Item -ItemType Directory -Path $evidence -Force | Out-Null

$ninaLogs = 'C:\Users\PrimaLuceLab\AppData\Local\NINA\Logs'
Get-ChildItem $ninaLogs -File |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 10 Name,Length,CreationTime,LastWriteTime |
  Format-Table -AutoSize |
  Out-File (Join-Path $evidence 'nina-logs-before.txt')
```

### 6.2 Required configuration

In the active C8 N.I.N.A. profile, set the application logging level to **Information** or a more verbose level that includes informational lifecycle events. Do not select a quieter level such as Warning/Error for this gate.

The exact UI label and persisted setting must be recorded from the installed N.I.N.A. version; do not infer a configuration-file key from documentation or another machine.

After applying the setting, restart N.I.N.A. if required by the installed version and confirm the same C8 profile is active.

### 6.3 Controlled telemetry test

Run a short, non-destructive controlled sequence using the normal C8 equipment/profile. The test must generate a **new** N.I.N.A. log after the configuration change.

The captured log must contain enough direct evidence to reconstruct, without filename inference:

- active target identity;
- sequence start or equivalent execution context;
- exposure lifecycle evidence, including at least one exposure start and completion/saved outcome;
- exposure duration where emitted by N.I.N.A.;
- filter identity where a filter is used and emitted by N.I.N.A.;
- image/save path or equivalent artifact correlation where emitted;
- timestamped events sufficient to correlate the exposure with PHD2/CloudWatcher evidence when those systems participate.

Not every scientific metadata field is expected to originate from N.I.N.A. The gate proves that N.I.N.A. is no longer suppressing the informational lifecycle telemetry needed by the governed analytics pipeline. Metadata not emitted by N.I.N.A. must continue to come from a governed evidence/registry source and must not be guessed.

### 6.4 Evidence capture

After the controlled sequence:

```powershell
$latest = Get-ChildItem $ninaLogs -File |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1

$latest | Select-Object FullName,Length,CreationTime,LastWriteTime |
  Format-List |
  Out-File (Join-Path $evidence 'nina-log-after.txt')

Get-FileHash $latest.FullName -Algorithm SHA256 |
  Format-List |
  Out-File (Join-Path $evidence 'nina-log-after.sha256.txt')

Copy-Item $latest.FullName (Join-Path $evidence $latest.Name) -Force
```

Record separately:

- active profile name;
- N.I.N.A. version;
- configured logging level;
- test start/end local time;
- target used;
- exposure count/duration/filter used;
- whether guiding was active;
- resulting log filename and SHA-256;
- representative line numbers or timestamps for target, sequence and exposure lifecycle evidence.

### 6.5 PASS / FAIL decision

**PASS** only when all of the following are true:

1. active C8 profile is evidenced;
2. logging level is evidenced as `Information` or more verbose;
3. a new post-change log is generated by a controlled test;
4. target/sequence context is present in the log;
5. at least one exposure lifecycle is directly evidenced;
6. emitted filter/duration/artifact-correlation metadata is retained when applicable;
7. no scientific metadata is invented to fill fields absent from the log;
8. evidence bundle path and SHA-256 are recorded in `AP14-W07-EAGLE-M27-OAT-Result.md`.

**FAIL / BLOCKED** if the installed N.I.N.A. build cannot expose the required informational events, if the wrong profile is active, if no new log is generated, or if the controlled test cannot be executed safely. In that case preserve evidence and open a remediation path; do not mark BKL-019 Done.

BKL-019 may move to `Done` only after the physical evidence is committed/referenced and independently reviewable.

## 7. M27 controlled replay

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

## 8. GitHub automatic chain

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

## 9. Acceptance evidence

Retain:

- deployment backup directory;
- old/new preflight and launcher hashes;
- task XML and post-deployment task definition;
- installed Reporting version/path;
- runtime repository branch/HEAD/clean status;
- automatic daily log and task result;
- BKL-019 N.I.N.A. profile/logging screenshots or equivalent immutable evidence;
- BKL-019 controlled-test log and SHA-256;
- actual M27 time window;
- preview/package status and evidence counts;
- session branch/commit SHA;
- promotion workflow run;
- analytics workflow run;
- Pages workflow run;
- resulting catalog/index commit;
- portal verification.

Record results in `docs/architecture/validation/AP14-W07-EAGLE-M27-OAT-Result.md`. The runtime `NO_SESSION` sub-gate is already PASS; BKL-019 and the overall OAT remain open until their physical/downstream evidence is complete.

## 10. Rollback

If the scheduled runtime fails before overall acceptance:

1. disable `Digital StarGate - Daily Session Upload` only when continued execution could create unsafe or corrupt state;
2. restore the previous task XML from the deployment backup only after inspecting it;
3. restore previous preflight/launcher files only from captured backup/hash;
4. do not delete any produced scientific/session evidence;
5. do not force-push or rewrite Git history;
6. record the failure and remediation evidence before retry.

For BKL-019, if the logging change causes unacceptable operational impact, restore the captured previous logging setting only after the controlled test is stopped and preserve both pre/post evidence. A failed AP-014 automation or logging deployment must not affect AP-013B XISF transport/import.
