# AP-014 EAGLE M27 Operational Acceptance Test Result

| Campo | Valore |
|---|---|
| Documento | AP14-W07 EAGLE M27 OAT Result |
| Identificativo | AP14-W07-EAGLE-M27-OAT-RESULT |
| Versione | 1.5 |
| Data | 2026-08-20 |
| Stato | Pending |
| Owner | Digital StarGate Architecture Office |

## 1. Scope

Record the runtime and end-to-end acceptance evidence for the M 27 observing session of 10/11 August 2026 and prove the permanent automatic flow:

`EAGLE evidence -> COMPLETE session package -> session branch -> governed promotion -> analytics -> AP-014 projections -> GitHub Pages`.

This version also records the production validation of the unattended `NO_SESSION` path completed on 18 August 2026 and the governed execution criteria for BKL-019. The `NO_SESSION` runtime sub-gate is accepted; BKL-019 and the overall M 27 OAT remain `Pending` until their required physical/downstream evidence is completed.

## 2. Runtime inspection and reconciliation evidence

Runtime inspection was executed on physical host `EAGLE30154` using the governed read-only collector and subsequent controlled runtime checks.

### Historical runtime

- Scheduled Task `Digital StarGate - Daily Session Upload`: FOUND / Ready.
- Historical task principal: `PrimaLuceLab`, `LogonType = S4U`, `RunLevel = Highest`.
- Historical trigger: daily, `07:20` local.
- Last historical run observed: `2026-08-13 12:22:22` local; `LastTaskResult = 1`.
- Historical launcher: `C:\DigitalStarGate\Automation\Invoke-DSGAutomaticSession.ps1`.
- Historical launcher SHA-256: `9C2F6B6010EB5A9268786E61D1AEAB123D6B7B56C51755B9B62B86B134A25AD8`.
- Historical automation configuration SHA-256: `BF1CDF0B8E313186E5B4283992ECE507B511DF8B6B66A5CFC241CC0C6DC11083`.
- Historical Reporting versions installed: `1.0.3`, `1.0.0`.
- Historical clean PowerShell resolution: `1.0.3`.
- Historical repository root: `C:\DigitalStarGate\digital-stargate-manual`.
- Historical repository state at inspection: `main`, HEAD `0b00d1f23c825a2f753cef2a13fc41d2ea5e3b1a`, `0` ahead / `44` behind `origin/main`, with three README line-ending-only working-tree differences.
- Historical automation log for `2026-08-13` stopped after `Sincronizzazione preventiva del repository`; this is consistent with the non-clean legacy working tree and the historical `git pull --rebase` behavior.

Historical deviations from AP14-INT-EAGLE-PUBLISH-001 were confirmed:

1. Reporting `1.0.3` instead of the governed baseline;
2. `git pull --rebase` instead of fast-forward-only synchronization;
3. direct publication to configured branch `main` instead of `session/<session-id>`;
4. repository writes before proving `COMPLETE`;
5. dependency on the legacy repository clone with line-ending/index drift.

### Preserved rollback evidence

- Historical task exported before cutover.
- Historical launcher/config copied to `C:\DigitalStarGate\SessionReports\deployment-backup\ap14-cutover-20260813-134642`.
- Backup launcher SHA-256: `9C2F6B6010EB5A9268786E61D1AEAB123D6B7B56C51755B9B62B86B134A25AD8`.
- Backup automation config SHA-256: `BF1CDF0B8E313186E5B4283992ECE507B511DF8B6B66A5CFC241CC0C6DC11083`.
- Historical README state separately backed up and preserved in Git stash; no destructive reset/history rewrite was used.

### Clean AP-014 runtime repository

- Runtime clone: `C:\DigitalStarGate\digital-stargate-manual-ap14-runtime`.
- Required branch: `main`.
- Runtime HEAD during the 17/18 August validation: `bbaef3fafbef749ccf32e07bc1c2fe61238e0669`.
- Runtime preflight proved local `HEAD = origin/main` before launching the automatic session flow.
- Working tree was clean during the accepted unattended run.

### Reporting runtime reconciliation

- Reporting `1.0.6` installed at `C:\Users\PrimaLuceLab\Documents\WindowsPowerShell\Modules\DigitalStarGate.Reporting\1.0.6`.
- Effective runtime configuration: `C:\DigitalStarGate\Automation\reporting.config.psd1`.
- Effective RepositoryRoot: `C:\DigitalStarGate\digital-stargate-manual-ap14-runtime`.
- NINA source: `C:\Users\PrimaLuceLab\AppData\Local\NINA\Logs`.
- PHD2 source: `C:\Users\PrimaLuceLab\Documents\PHD2`.
- CloudWatcher source: `C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv`.
- CloudWatcher source existence check: PASS.
- Reporting source fix for exact-window `NO_SESSION` discovery: `2b64617db4e757c0e361300af7be7bc77086b1b2`.
- Reporting post-OAT installer/Windows-checkout hardening: `c902c51ddaae7493cbfecc019fef554ffc22ca7a`.
- Reporting source clone on EAGLE was realigned to `c902c51ddaae7493cbfecc019fef554ffc22ca7a`, `VERSION = 1.0.6`, clean working tree.

### NO_SESSION defect and remediation evidence

The scheduled run of 17 August 2026 exposed two independent conditions:

1. the runtime repository was initially on a feature branch, correctly rejected by the fail-safe preflight;
2. after restoring `main`, Reporting 1.0.5 could falsely discover a session because previous-night NINA/PHD2 logs inside the evidence collection boundary `+/-12h` were also used to decide whether a new session existed.

The false-positive evidence came from the previous 15/16 August session and caused the import path to enter CloudWatcher processing despite there being no observing session on 16/17 August.

Reporting 1.0.6 separates:

- **session discovery:** exact candidate window using NINA/PHD2 `CreationTime` or `LastWriteTime`;
- **evidence collection:** the wider `+/-12h` boundary, only after a real candidate session is established.

When neither NINA nor PHD2 evidence exists in the exact candidate window, `Import-DSGSession` returns `NO_SESSION` before staging creation and before CloudWatcher parsing.

### Controlled manual runtime replay — 17 August 2026

After installing Reporting 1.0.6 and removing only the previously inspected false staging directory, the governed preflight was executed manually against candidate window `2026-08-16 19:00` -> `2026-08-17 06:00`.

Observed evidence:

```text
DSG PRECHECK OK main-head=bbaef3fafbef749ccf32e07bc1c2fe61238e0669
MODULE version=1.0.6
DISCOVERY session=2026-08-16_2026-08-17 status=NO_SESSION nina=0 phd2=0 weatherRows=0
END outcome=NO_SESSION
```

- Process exit code: `0`.
- False staging path after replay: absent.
- Result: PASS.

### Scheduled unattended runtime execution — 18 August 2026

The production Scheduled Task executed automatically at the configured daily trigger.

Task evidence:

- Task: `Digital StarGate - Daily Session Upload`.
- `LastRunTime = 2026-08-18 07:20:20` local.
- `LastTaskResult = 0`.
- `NextRunTime = 2026-08-19 07:20:20` local.

Automation log evidence for candidate window `2026-08-17 19:00` -> `2026-08-18 06:00`:

```text
[2026-08-18T07:20:10.7943233+02:00] START candidate-window=2026-08-17T19:00:00..2026-08-18T06:00:00 repository=C:\DigitalStarGate\digital-stargate-manual-ap14-runtime
[2026-08-18T07:20:16.1832118+02:00] BASE main-head=bbaef3fafbef749ccf32e07bc1c2fe61238e0669
[2026-08-18T07:20:16.8548706+02:00] MODULE version=1.0.6 path=C:\Users\PrimaLuceLab\Documents\WindowsPowerShell\Modules\DigitalStarGate.Reporting\1.0.6
[2026-08-18T07:20:17.2454051+02:00] DISCOVERY session=2026-08-17_2026-08-18 status=NO_SESSION nina=0 phd2=0 weatherRows=0
[2026-08-18T07:20:17.2610282+02:00] END outcome=NO_SESSION
```

Acceptance result for unattended `NO_SESSION`: **PASS**.

### Runtime conformance assessment after production validation

**Installed runtime configuration and unattended `NO_SESSION` behavior: CONFORMANT / PASS for the validated path.**

This acceptance does not prove `PARTIAL`, real-session publication, downstream promotion, analytics, Pages, full idempotency behavior, or BKL-019 N.I.N.A. informational logging.

Runtime evidence bundle from pre-cutover inspection remains:

`C:\DigitalStarGate\SessionReports\runtime-evidence\EAGLE-runtime-evidence-20260813-132013`

The 17/18 August automation evidence is retained in the daily automation logs under:

`C:\DigitalStarGate\SessionReports\automation\`

## 3. M27 source evidence

Evidence-derived observations for the M 27 session:

- NINA log found: `20260810-204106-3.2.0.9001.7156-202608.log`.
- NINA log header timestamp: `2026-08-10T20:46:45`.
- NINA activity observed through at least `2026-08-11T05:09:32`.
- PHD2 DebugLog and GuideLog found for the same night.
- PHD2 guiding begins: `2026-08-10 22:18:22`.
- PHD2 guiding ends: `2026-08-11 05:00:14`.
- CloudWatcher source confirmed at `C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv`.
- CloudWatcher source is a long-running historical CSV containing Date/Time, cloud/rain/brightness conditions, ambient temperature, wind, humidity, dew point, pressure and Safe Status.
- Broad M27 weather check found `3960` rows between `2026-08-10 20:00` and `2026-08-11 06:59`.
- First inspected M27 weather row: `2026-08-10 20:00:05`.
- Last inspected M27 weather row: `2026-08-11 06:59:56`.

Controlled package window selected for replay:

- SessionStart: `2026-08-10 20:00:00` local.
- SessionEnd: `2026-08-11 06:00:00` local.

This window safely contains the real NINA/PHD2 observing activity while avoiding the non-scientific PHD2 application-open tail through 09:42.

### BKL-019 N.I.N.A. C8 logging evidence

Repository review on 20 August 2026 found no independent evidence that the active C8 N.I.N.A. profile has already been changed to `Information` logging. Later Observatory Status telemetry and later observing sessions do not substitute for this proof.

Current state:

- governed execution procedure: DEFINED in `AP14-OPS-EAGLE-AUTO-001` v1.2;
- physical C8 profile inspection: PENDING;
- pre-change setting evidence: PENDING;
- post-change `Information` or more verbose setting evidence: PENDING;
- new controlled-test N.I.N.A. log: PENDING;
- log SHA-256: PENDING;
- target/sequence/exposure lifecycle evidence: PENDING;
- BKL-019 acceptance: **PENDING**.

BKL-019 must not be closed from historical M27 evidence or repository documentation alone.

## 4. Session package result

Controlled preview executed on the EAGLE without `-CopyToRepository`.

- Session ID: `2026-08-10_2026-08-11`.
- Staging root: `C:\DigitalStarGate\SessionReports\incoming\2026\08\2026-08-10_2026-08-11`.
- `Import-DSGSession` preview status: **COMPLETE / PASS**.
- NINA files packaged: `1`.
- PHD2 files packaged: `2`.
- Weather file: `raw\weather\CloudWatcher_2026-08-10_2026-08-11.csv`.
- Weather rows exported for the controlled 20:00-06:00 package window: `3600`.
- Source weather coverage in the broader 20:00-06:59 inspection window: `3960` rows.
- `Import-DSGSession -CopyToRepository` status: PENDING.
- Manifest SHA-256 verification: PENDING.
- Repository package content/hash verification against staging: PENDING.

Acceptance gate `Status = COMPLETE` is satisfied for the staging preview.

## 5. Publication and promotion

- Session branch: PENDING
- Session commit SHA: PENDING
- EAGLE push result: PENDING
- `promote-session-package.yml` run: PENDING
- Manifest/hash/scope validation: PENDING
- Fast-forward promotion to `main`: PENDING

## 6. Analytics and portal projections

- `analyze-session-automatic.yml` run: PENDING
- `sessions.csv` contains M 27: PENDING
- `target-exposures.csv` contains derived M 27 metrics: PENDING
- `targets.csv` contains M 27: PENDING
- `scientific-session-catalog.json` contains M 27: PENDING
- `scientific-observation-index.json` contains M 27: PENDING
- `latest-observation.json` updated where applicable: PENDING

No quality/scientific metric may be inferred from XISF filenames or AP-013B transfer metadata.

## 7. Portal deployment and correlated pages

- `deploy-pages.yml` run: PENDING
- Session Explorer reflects M 27: PENDING
- Session Detail resolves M 27: PENDING
- Mission Control reflects updated shared projections: PENDING
- Enterprise Search returns M 27/target projection: PENDING

No manual catalog or page edit is permitted for acceptance.

## 8. Safety and idempotency checks

- Scientific XISF files unchanged through inspection/cutover/preview: PASS.
- AP-013B transport/import unchanged: PASS.
- No source NINA/PHD2/weather evidence deleted: PASS.
- No force push/history rewrite: PASS.
- Historical runtime rollback package retained: PASS.
- Preview performed only in staging: PASS.
- Runtime Git working tree clean before automatic execution: PASS.
- Fail-safe preflight requires clean `main` aligned to `origin/main`: PASS in production execution.
- `NO_SESSION` protection verified in production: **PASS**.
- `NO_SESSION` creates no staging and bypasses weather processing: **PASS**.
- BKL-019 C8 `Information` logging controlled test: **PENDING**.
- `PARTIAL` protection verified in production: PENDING.
- Re-run behavior idempotent for a real session package: PENDING.

## 9. CI/quality gates

- Reporting collector/locked-weather Quality Gate run `31694911434`: PASS on `591984ae9cbb6e7b4d54ef3ab6a696fb2a98e700`.
- Reporting repository-root installer Quality Gate run `31696735200`: PASS on `f27330da5f4e8363fcfea9af2ccfa808592091b7`.
- Reporting unattended-task semantics Quality Gate run `31697194103`: PASS on `5b82235bd1aab21bfac5f47a11c38538ee3f264b`.
- Reporting actual CloudWatcher path Quality Gate run `31698320816`: PASS on `fedb5564fc1009dd356f20d7c5739fc4ca4cc1e6`.
- Reporting 1.0.6 NO_SESSION regression: PASS before merge of `2b64617db4e757c0e361300af7be7bc77086b1b2`.
- Reporting 1.0.6 post-OAT runtime-hardening regression, Quality Gate and NO_SESSION regression: PASS before merge of `c902c51ddaae7493cbfecc019fef554ffc22ca7a`.
- BKL-019 documentation gate CI: PENDING for this update.
- BKL-019 physical runtime gate: PENDING; cannot be replaced by CI.

## 10. Decision

**Stato complessivo: Pending**

**Runtime sub-gate: PASS for unattended `NO_SESSION`.**

**BKL-019 N.I.N.A. C8 logging sub-gate: PENDING.**

The EAGLE runtime is structurally reconciled, Reporting 1.0.6 is installed and the scheduled unattended execution of 18 August 2026 completed with `LastTaskResult = 0` and `END outcome=NO_SESSION`. The M27 staging preview remains COMPLETE with real NINA, PHD2 and CloudWatcher evidence.

The next dependency-ordered physical gate is BKL-019: inspect the active C8 profile, evidence the current logging setting, set `Information` or more verbose if required, execute a safe controlled sequence, and retain the new N.I.N.A. log plus SHA-256 and representative lifecycle evidence. Only then may BKL-019 be considered for `Done` and BKL-020 lineage closure proceed on that evidence.

The designated M27 OAT remains Pending. This record may be changed to `Accepted` only when all mandatory BKL-019-dependent lineage, repository-copy, promotion, analytics, portal, real-session idempotency and remaining required runtime evidence is recorded and verifiable.
