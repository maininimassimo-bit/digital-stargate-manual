# AP-014 EAGLE Automatic Session Deployment Runbook

| Campo | Valore |
|---|---|
| Identificativo | AP14-OPS-EAGLE-AUTO-001 |
| Versione | 1.3 |
| Stato | Deployed; NO_SESSION runtime validated; BKL-019 evidence reconciled |
| Data | 2026-08-20 |
| Host | EAGLE / PrimaLuceLab |

## Objective

Operate and verify the governed automatic session producer on EAGLE so every future complete observing session is published through the AP-014 automatic portal pipeline, while no-observation nights terminate safely as `NO_SESSION`.

This runbook changes the physical EAGLE runtime and must therefore be executed on EAGLE. Repository commits alone do not prove deployment. Conversely, already-versioned runtime evidence may satisfy a gate when it directly proves the required operational outcome; a redundant retrospective test must not be introduced solely to recreate evidence that already exists.

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

## 6. BKL-019 — N.I.N.A. C8 informational logging evidence

BKL-019 is satisfied by direct, versioned runtime evidence already present in the repository. No additional controlled physical test is required solely to prove that N.I.N.A. can emit the informational telemetry required by the governed analytics pipeline.

Authoritative source evidence:

```text
data/sessions/2026/08/2026-08-14_2026-08-15/raw/nina/20260814-201744-3.2.0.9001.3996-202608.log
```

The 14/15 August M 27 log directly records, at `INFO` level:

- N.I.N.A. version and normal informational logging output;
- QHY695A camera discovery/connection;
- filter wheel, focuser, CPWI mount, PHD2, CloudWatcher and dome connections;
- Advanced Sequence start and sequence-container execution;
- target-context evidence for M 27;
- exposure lifecycle including `TakeExposure` start and completion;
- 600 s LIGHT exposures, gain/offset and binning 1x1;
- L-Pro filter switching;
- successful XISF save paths containing M 27 / Celestron C8 acquisition context;
- plate solving and target coordinates, including M 27 coordinates used by the meridian-flip workflow.

Related governed metadata/equipment evidence is maintained in:

```text
data/analytics/metadata/session-scientific-metadata.csv
data/analytics/configurations/session-configuration-map.csv
data/analytics/configurations/equipment-registry.csv
```

Relevant repository history includes:

- `480c3fe2a8d36cd315cb814e7af97f8d6aa3260b` — register C8/QHY695A for the 14/15 August M 27 session;
- `5fd4b0ebae58bf558e1d4818bdfc8840f8ed7137` — register the 15/16 August M 27 scientific configuration.

### 6.1 Acceptance interpretation

BKL-019 proves the operational outcome “N.I.N.A. informational telemetry is available and usable for governed analytics”. It does **not** prove that the designated 10/11 August OAT session itself contained those informational records.

Therefore:

- BKL-019 may be `Done` from the 14/15 August versioned N.I.N.A. evidence;
- the 10/11 August session remains historically incomplete where its own source evidence does not attest fields;
- later evidence must not be copied backward to claim an instrument configuration or coordinates for the 10/11 August session unless a separate governed source explicitly attests them;
- no screenshot of a current profile setting is required to recreate a fact already proven by versioned runtime output;
- future regressions in N.I.N.A. logging are operational defects and should be handled as new incidents/remediations, not by reopening historical BKL-019 without evidence of regression.

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
- versioned N.I.N.A. source evidence and governed metadata references used for BKL-019/BKL-020;
- actual M27 time window;
- preview/package status and evidence counts;
- session branch/commit SHA;
- promotion workflow run;
- analytics workflow run;
- Pages workflow run;
- resulting catalog/index commit;
- portal verification.

Record results in `docs/architecture/validation/AP14-W07-EAGLE-M27-OAT-Result.md`. The runtime `NO_SESSION` sub-gate and BKL-019/BKL-020 evidence reconciliation are complete; the overall OAT remains open until its downstream publication, promotion, analytics, portal, PARTIAL and idempotency evidence is complete.

## 10. Rollback

If the scheduled runtime fails before overall acceptance:

1. disable `Digital StarGate - Daily Session Upload` only when continued execution could create unsafe or corrupt state;
2. restore the previous task XML from the deployment backup only after inspecting it;
3. restore previous preflight/launcher files only from captured backup/hash;
4. do not delete any produced scientific/session evidence;
5. do not force-push or rewrite Git history;
6. record the failure and remediation evidence before retry.

A failed AP-014 automation deployment must not affect AP-013B XISF transport/import.
