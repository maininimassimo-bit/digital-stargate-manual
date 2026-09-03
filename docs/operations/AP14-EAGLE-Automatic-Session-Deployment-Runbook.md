# AP-014 EAGLE Automatic Session Deployment Runbook

| Campo | Valore |
|---|---|
| Identificativo | AP14-OPS-EAGLE-AUTO-001 |
| Versione | 1.5 |
| Stato | Deployed; Reporting 1.0.8 runtime validated; historical AP-014 OAT preserved |
| Data | 2026-09-03 |
| Host | EAGLE / PrimaLuceLab |

## Objective

Operate and verify the governed automatic session producer on EAGLE so every future complete observing session is published through the AP-014 automatic portal pipeline, while no-observation nights terminate safely as `NO_SESSION`.

This runbook changes the physical EAGLE runtime and must therefore be executed on EAGLE. Repository commits alone do not prove deployment. Historical AP-014 validation records remain authoritative for the OAT they actually executed; this runbook records the later operational runtime baseline without rewriting historical evidence.

## Current production baseline

Before any runtime change verify:

- `maininimassimo-bit/DigitalStarGate.Reporting` is at or after merge `0f9bffb5a9e6192dbf0302b563b10ec7e451bd8b`;
- `DigitalStarGate.Reporting` runtime version is `1.0.8`;
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

Expected Reporting version is `1.0.8` or a later explicitly governed release.

## 3. Install/upgrade Reporting

From `C:\DigitalStarGate\DigitalStarGate.Reporting-src`:

```powershell
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass `
  -File .\Install-DSGReporting.ps1 `
  -RepositoryRoot 'C:\DigitalStarGate\digital-stargate-manual-ap14-runtime' `
  -RuntimeConfigPath 'C:\DigitalStarGate\Automation\reporting.config.psd1'
```

Verify the installed production baseline in a fresh process:

```powershell
powershell.exe -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command "& { Import-Module DigitalStarGate.Reporting -RequiredVersion 1.0.8 -Force; Get-Module DigitalStarGate.Reporting | Select-Object Name,Version,ModuleBase; Get-Command Import-DSGSession,Publish-DSGSession | Select-Object Name,Source,Version }"
```

The expected version for this runbook revision is `1.0.8`. Older installed module directories do not by themselves indicate an error; verify the actually loaded module.

## 4. Governed preflight and Scheduled Task

Production chain:

```text
Scheduled Task
  -> C:\DigitalStarGate\Automation\Invoke-DSGSessionPreflight.ps1
  -> C:\DigitalStarGate\Automation\Invoke-DSGAutomaticSession.ps1
  -> DigitalStarGate.Reporting
```

The preflight must require runtime clone valid, clean, branch exactly `main`, successful `git fetch origin main`, successful fast-forward pull and local `HEAD == origin/main`.

Any failed invariant stops before session import/publication. Diagnose rather than bypass with force/reset operations.

Verify task:

```powershell
Get-ScheduledTaskInfo -TaskName 'Digital StarGate - Daily Session Upload' | Format-List LastRunTime,LastTaskResult,NextRunTime,NumberOfMissedRuns
```

Production trigger is daily at `07:20` local.

## 5. NO_SESSION behavior

`NO_SESSION` remains a valid non-error outcome when no observing evidence exists. Historical production acceptance with Reporting 1.0.6 on 18/08/2026 remains valid and must not be rewritten as 1.0.8 evidence.

## 6. SQM packaging

Reporting 1.0.8 retains session-bounded SQM packaging before manifest generation. Default source:

```text
%LOCALAPPDATA%\DigitalStarGate\telemetry\sqm-history.ndjson
```

Expected package paths:

```text
raw\sqm\sqm-history.ndjson
raw\sqm\sqm-summary.json
```

Real recovery evidence for `2026-09-02_2026-09-03`: 1295 valid samples, quality `AVAILABLE`, coverage `0.9803`, min `8.91`, mean `18.1931`, max `20.84`, median `19.14` mag/arcsec².

Do not infer safety from SQM.

## 7. Exact NINA/PHD2 evidence selection

Reporting 1.0.8 packages the NINA/PHD2 files selected by discovery rather than re-scanning with the legacy ±12 hour copy window.

Operational consequence:

- a previous-session PHD2 file whose activity ended outside the session window must not be included merely because it falls in an adjacent tolerance window;
- a long-lived NINA log may legitimately be included when it contains/writes current-session events inside the discovery window.

Do not remove a file solely from its filename/date. Inspect actual timestamps/content when diagnosing boundary cases.

## 8. Windows PowerShell 5.1 publish contract

`Publish-DSGSession` must emit one structured result and must judge native Git success from its exit code even when Git writes normal informational text to stderr.

The 03/09 recovery on EAGLE30154 with Reporting 1.0.8 verified:

```text
SessionId = 2026-09-02_2026-09-03
Committed = True
Pushed = True
COUNT = 1
```

This is the runtime evidence for the PowerShell 5.1 stderr hardening.

## 9. Controlled recovery of a materialized package

When discovery/package generation has already completed and failure occurred only during publication:

1. preserve the package and inspect branch/working tree;
2. verify package evidence and manifest before modifying anything;
3. do not rerun discovery merely to repair a publication failure;
4. after installing the governed Reporting fix, call `Publish-DSGSession` on the existing session branch without `-CreateBranch` and with `-Push` only when the branch/package have been verified;
5. verify the single structured result, commit SHA and remote branch;
6. verify GitHub promotion/analytics before returning runtime to `main`;
7. switch to `main`, fetch/pull fast-forward and require clean `0 0` steady state.

Do not use force reset/push as routine recovery.

## 10. GitHub automatic chain

After EAGLE intentionally pushes `session/<session-id>`, no manual catalog or page edit is permitted.

Expected chain: promote session package -> main -> automatic analysis -> analytics/history/target projections -> scientific catalog/index -> Pages.

For `2026-09-02_2026-09-03`, session commit `0023553bf300a1536663a6ee01f7d6a5c3745514` was promoted successfully and analytics reached `d4feb68e89e39977d7b34b15acce69a0065dedb0`.

## 11. Acceptance and runtime evidence

Retain as applicable: deployment backup, task definition, installed Reporting version/path, runtime branch/HEAD/clean state, automatic log/task result, source evidence, session window, package evidence counts, session branch/commit, promotion/analytics/Pages runs and resulting catalog/index commit.

Historical AP-014 OAT remains in existing validation records. Reporting 1.0.7 remediation is recorded in the 02/09 handover; Reporting 1.0.8 incident/recovery is recorded in the 03/09 handover.

## 12. Rollback and recovery

If scheduled runtime fails:

1. preserve produced evidence;
2. inspect branch, clean state and divergence;
3. diagnose the failure before switching/resetting;
4. use fast-forward synchronization only when working tree state is understood;
5. never use force-push/history rewrite as normal recovery;
6. record failure/remediation evidence before retry.

The independent local Safety Authority is unaffected by this reporting recovery process.

## 13. Known hardening debt

Reporting 1.0.8 closes the observed Git stderr PowerShell 5.1 bug and exact evidence-selection drift. It does **not** close:

- guaranteed restore-to-main in the launcher if an exception occurs after session branch creation; track as `TD-010`;
- formal reconciliation/restoration of all historical Reporting quality-gate checks while retaining current regression tests; track as `TD-011`.

Do not reinterpret these open hardening items as failure of the validated 1.0.8 recovery.
