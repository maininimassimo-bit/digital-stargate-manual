# AP-014 EAGLE Automatic Session Deployment Runbook

| Campo | Valore |
|---|---|
| Identificativo | AP14-OPS-EAGLE-AUTO-001 |
| Versione | 1.4 |
| Stato | Deployed; Reporting 1.0.7 runtime validated; historical AP-014 OAT preserved |
| Data | 2026-09-02 |
| Host | EAGLE / PrimaLuceLab |

## Objective

Operate and verify the governed automatic session producer on EAGLE so every future complete observing session is published through the AP-014 automatic portal pipeline, while no-observation nights terminate safely as `NO_SESSION`.

This runbook changes the physical EAGLE runtime and must therefore be executed on EAGLE. Repository commits alone do not prove deployment. Historical AP-014 validation records remain authoritative for the OAT they actually executed; this runbook records the later operational runtime baseline without rewriting historical evidence.

## Current production baseline

Before any runtime change verify:

- `maininimassimo-bit/DigitalStarGate.Reporting` is at or after merge `c5f1bd617eb7b256372f0257a3cf22b60d503d3b`;
- `DigitalStarGate.Reporting` runtime version is `1.0.7`;
- `maininimassimo-bit/digital-stargate-manual` runtime clone is synchronized to current `main` before launcher execution;
- runtime clone path is `C:\DigitalStarGate\digital-stargate-manual-ap14-runtime`;
- runtime config is `C:\DigitalStarGate\Automation\reporting.config.psd1`;
- EAGLE scientific repository clone is clean before any pull/install action.

Current evidence sources:

```text
C:\Users\PrimaLuceLab\AppData\Local\NINA\Logs
C:\Users\PrimaLuceLab\Documents\PHD2
C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv
C:\Users\PrimaLuceLab\AppData\Local\DigitalStarGate\telemetry\sqm-history.ndjson
```

The SQM history source is scientific evidence only and is never Safety Authority.

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
git fetch origin main
git pull --ff-only origin main
git branch --show-current
git rev-list --left-right --count HEAD...origin/main
git status --short
```

Expected steady state: branch `main`, divergence `0 0`, empty short status.

Reporting source repository:

```powershell
Set-Location 'C:\DigitalStarGate\DigitalStarGate.Reporting-src'
git status --porcelain
git switch main
git fetch origin
git pull --ff-only origin main
Get-Content .\VERSION
```

Expected Reporting version is `1.0.7` or a later explicitly governed release.

## 3. Install/upgrade Reporting

From `C:\DigitalStarGate\DigitalStarGate.Reporting-src`:

```powershell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass `
  -File .\Install-DSGReporting.ps1 `
  -RepositoryRoot 'C:\DigitalStarGate\digital-stargate-manual-ap14-runtime' `
  -RuntimeConfigPath 'C:\DigitalStarGate\Automation\reporting.config.psd1'
```

Verify the installed production baseline in a fresh Bypass process:

```powershell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -Command "& { Import-Module DigitalStarGate.Reporting -RequiredVersion 1.0.7 -Force; Get-Module DigitalStarGate.Reporting | Select-Object Name,Version,ModuleBase; Get-Command Import-DSGSession,Publish-DSGSession | Select-Object Name,Source,Version }"
```

The expected version for this runbook revision is `1.0.7`. Older installed module directories do not by themselves indicate an error; verify the actual loaded module in the production-like Bypass context.

Verify the effective configuration:

```powershell
$config = 'C:\DigitalStarGate\Automation\reporting.config.psd1'
Test-Path $config
Get-Content $config -Raw
```

The installer derives the destination version from the module manifest. Do not hard-code an installation destination or infer the active runtime merely from the highest directory name.

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

Any failed invariant stops before session import/publication. A preflight stop caused by a stale session branch or divergence is a fail-safe integrity response and must be diagnosed rather than bypassed with force/reset operations.

Verify task:

```powershell
Get-ScheduledTask -TaskName 'Digital StarGate - Daily Session Upload' | Format-List *
Get-ScheduledTaskInfo -TaskName 'Digital StarGate - Daily Session Upload' | Format-List LastRunTime,LastTaskResult,NextRunTime,NumberOfMissedRuns
```

Production trigger is daily at `07:20` local.

## 5. NO_SESSION behavior

For a night with no NINA/PHD2 observing evidence in the candidate window, `NO_SESSION` is a valid non-error outcome. Historical production acceptance of this path was recorded with Reporting 1.0.6 on 18 August 2026:

- `LastRunTime = 2026-08-18 07:20:20` local;
- `LastTaskResult = 0`;
- candidate session `2026-08-17_2026-08-18` -> `NO_SESSION`;
- NINA files `0`;
- PHD2 files `0`;
- weather rows `0`;
- final outcome `NO_SESSION`.

That evidence remains historical and valid. Current operations use Reporting 1.0.7; do not rewrite the historical log as if it had executed on 1.0.7.

## 6. Reporting 1.0.7 SQM packaging

For a real session, Reporting 1.0.7 exports the session-bounded SQM evidence before manifest generation. Unless overridden by governed configuration, the source is:

```text
%LOCALAPPDATA%\DigitalStarGate\telemetry\sqm-history.ndjson
```

Expected package paths:

```text
raw\sqm\sqm-history.ndjson
raw\sqm\sqm-summary.json
```

A non-destructive runtime test on EAGLE30154 for `2026-09-01_2026-09-02` verified `1306` valid samples, quality `AVAILABLE`, temporal coverage `0.9886`, min `8.91`, mean `17.738`, max `20.92` and median `18.755` mag/arcsec².

Do not infer safety from SQM. It remains scientific telemetry/history.

## 7. Reporting 1.0.7 publish contract

`Publish-DSGSession` must emit one structured result object rather than native Git stdout plus the result object. Runtime validation on EAGLE30154 verified, without `-CreateBranch` or `-Push`:

```text
System.Management.Automation.PSCustomObject
COUNT = 1
SessionId = 2026-09-01_2026-09-02
Committed = False
Pushed = False
```

This is the runtime regression check for the 02/09 `$publish.Committed` incident.

## 8. Controlled replay / manual diagnostic

Do not use the daily wrapper blindly for a historical session. Determine the actual session start/end from source evidence first. For diagnostics that do not need repository publication, omit `-CopyToRepository` and do not call `Publish-DSGSession`.

If testing PowerShell code containing multiple variables/continuations from an interactive shell, prefer a temporary `.ps1` invoked with `powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File ...` rather than a deeply nested multiline `-Command` string. This avoids false parameter prompts caused by quoting/backtick parsing.

Proceed to `-CopyToRepository`, `-CreateBranch` or `-Push` only when the session is intentionally being governed/published.

## 9. GitHub automatic chain

After EAGLE intentionally pushes `session/<session-id>`, no manual catalog or page edit is permitted.

Expected automatic chain:

1. `promote-session-package.yml` validates COMPLETE evidence, manifest hashes, scope and fast-forward ancestry;
2. package is promoted to `main`;
3. `analyze-session-automatic.yml` is explicitly dispatched;
4. analytics/history/target projections are regenerated;
5. `scientific-session-catalog.json` is regenerated;
6. `scientific-observation-index.json` is regenerated;
7. `deploy-pages.yml` is explicitly dispatched;
8. Session Explorer, Session Detail, Mission Control and enterprise search reflect the shared updated projections.

## 10. Acceptance and runtime evidence

Retain as applicable:

- deployment backup directory;
- task XML and post-deployment task definition;
- installed Reporting version/path;
- runtime repository branch/HEAD/clean status;
- automatic daily log and task result;
- NINA/PHD2/weather/SQM source evidence;
- session time window;
- package status/evidence counts;
- session branch/commit SHA when publication occurs;
- promotion/analytics/Pages workflow runs;
- resulting catalog/index commit;
- portal verification.

Historical AP-014 OAT evidence remains in the existing validation records. Reporting 1.0.7 runtime remediation evidence is recorded separately in the 02/09/2026 handover and runtime validation record.

## 11. Rollback and recovery

If the scheduled runtime fails:

1. preserve produced scientific/session evidence;
2. inspect runtime branch, clean state and divergence before changing anything;
3. return to `main` and use fast-forward synchronization when the working tree is clean and the failure is understood;
4. do not use force-push or history rewrite as normal recovery;
5. disable the Scheduled Task only when continued execution could create corrupt state or when diagnosis requires it;
6. restore task/preflight/launcher only from captured backup/hash after inspection;
7. record failure and remediation evidence before retry.

A failed AP-014 automation deployment must not affect AP-013B XISF transport/import or the independent local Safety Authority.

## 12. Known hardening debt

The current 1.0.7 runtime validation does not close two separate hardening items:

- guarantee restore-to-main in the launcher even if an exception occurs before normal cleanup;
- restore the historical Reporting quality-gate checks that were reduced in the 1.0.7 PR while retaining the new SQM/publish regression tests.

Track these as runtime/quality hardening; do not reinterpret them as evidence that the validated 1.0.7 SQM exporter or publish output contract failed.
