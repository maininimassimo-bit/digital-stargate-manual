# AP-014 EAGLE Session Publisher Runtime Contract

- **Identifier:** AP14-INT-EAGLE-PUBLISH-001
- **Status:** Approved runtime contract; EAGLE conformance evidence pending
- **Version:** 1.0
- **Date:** 2026-08-13
- **Target release:** RC3
- **Owner:** Digital StarGate Architecture Office

## Purpose

Define the minimum observable behavior required from the EAGLE scheduled launcher `Invoke-DSGAutomaticSession.ps1` without replacing or inventing its implementation before the installed runtime has been inspected.

## Authoritative components

The runtime launcher orchestrates existing governed components only:

- `DigitalStarGate.Reporting` on EAGLE is the session-package producer;
- `Import-DSGSession` creates the governed package and returns `COMPLETE`, `PARTIAL` or `NO_SESSION`;
- `Publish-DSGSession -CreateBranch -Push` publishes `session/<session-id>`;
- GitHub workflow `.github/workflows/promote-session-package.yml` is the promotion authority from a session branch to `main`;
- `.github/workflows/analyze-session-automatic.yml` is the downstream analytics/catalog projection boundary.

The launcher must not implement an independent parser, analytics engine, catalog generator or XISF importer.

## Required preconditions

Before creating a new session branch, the launcher must establish a clean, current repository base:

1. repository path resolves to `C:\DigitalStarGate\digital-stargate-manual`;
2. no unrelated working-tree changes are present;
3. current branch is `main` before synchronization;
4. `git fetch origin main` succeeds;
5. local `main` is synchronized by fast-forward only (`git pull --ff-only origin main` or an equivalent non-rewriting operation);
6. no force checkout, reset of unrelated work, force push or history rewrite is permitted.

If any precondition fails, the launcher must stop before `Import-DSGSession`/publication.

## Session-window contract

The scheduler may determine a candidate previous-night window, but the package must correspond to real NINA/PHD2 evidence. Historical sessions used `19:00 -> 06:00`; this is evidence of past operation, not a universal scientific rule.

For replay/OAT, start and end must be chosen from the real evidence for the observing night. A guessed time window must not be used to manufacture a package.

## Producer contract

The launcher must invoke the certified reporting module and configuration, logically equivalent to:

```powershell
Import-Module DigitalStarGate.Reporting -Force
$config = 'C:\DigitalStarGate\digital-stargate-manual\templates\reporting\reporting.config.psd1'
$result = Import-DSGSession -SessionStart $sessionStart -SessionEnd $sessionEnd -ConfigPath $config -CopyToRepository
```

State handling is mandatory:

- `NO_SESSION` -> no branch, no push, successful no-op or explicitly recorded no-session outcome;
- `PARTIAL` -> no promotion candidate; retain/report evidence for diagnosis;
- `COMPLETE` -> eligible for `Publish-DSGSession`.

The launcher must never convert `PARTIAL` into `COMPLETE` and must never synthesize missing weather/guiding/scientific metrics.

## Publication contract

For `COMPLETE` only, publication must be logically equivalent to:

```powershell
Publish-DSGSession -SessionId $result.SessionId -ConfigPath $config -CreateBranch -Push
```

Expected branch:

```text
session/<YYYY-MM-DD_YYYY-MM-DD>
```

The EAGLE does not push directly to `main`. GitHub owns promotion to `main`.

## GitHub promotion contract

The promotion workflow must remain fail-safe:

- exact session branch naming;
- exact matching manifest path;
- `report_status = COMPLETE`;
- non-empty NINA/PHD2/weather evidence;
- size/SHA-256 validation for manifest-declared files;
- changes scoped to the selected session/report path;
- current `main` must be an ancestor of the session branch;
- promotion by fast-forward only;
- explicit downstream workflow dispatch after promotion.

If `main` advanced after the session branch was created, promotion must fail rather than merge or overwrite automatically. The EAGLE package must be recreated/rebased through a controlled procedure after synchronizing to current `main`.

## Idempotency

Repeated execution for a previously published session must not create divergent evidence or overwrite conflicting files. Existing package/branch state must be inspected before retry. Any differing evidence for the same stable session ID requires reconciliation, not overwrite.

## Safety and non-destructive rules

The launcher and promotion path must not:

- delete or move scientific XISF files;
- alter AP-013B OneDrive transport state;
- remove source NINA/PHD2/CloudWatcher logs;
- perform `git push --force`;
- perform destructive cleanup of unrelated repository changes;
- derive catalog/quality values directly from XISF filenames or transfer plans.

## Observability and evidence

Each scheduled execution must make the following diagnosable through task/runtime output or a retained log:

- execution timestamp;
- candidate session window;
- repository HEAD before import;
- Reporting module version;
- result state (`NO_SESSION`, `PARTIAL`, `COMPLETE`);
- session ID when present;
- NINA/PHD2/weather counts/status;
- publication branch when pushed;
- Git command failure/non-zero result when applicable.

Secrets/tokens must never be written to logs.

## EAGLE conformance evidence required

AP14-W07 runtime conformance remains pending until the installed EAGLE launcher is inspected and compared with this contract. Required evidence:

1. Scheduled Task definition for `Digital StarGate - Daily Session Upload`;
2. installed `Invoke-DSGAutomaticSession.ps1` path, source and SHA-256;
3. installed Reporting module version/path;
4. effective Reporting configuration;
5. Git synchronization behavior before session branch creation;
6. real M 27 evidence inventory;
7. complete M 27 package and pushed session branch;
8. successful GitHub promotion, analytics/catalog pipeline and Pages deployment.

## Acceptance criteria

This contract is satisfied only when runtime inspection shows that the EAGLE launcher conforms or has been reconciled to these rules, and an end-to-end real-session OAT proves:

`EAGLE evidence -> COMPLETE package -> session branch -> governed fast-forward promotion -> analytics -> AP-014 projections -> Pages`.
