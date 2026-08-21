# AP-014 EAGLE M27 Operational Acceptance Test Result

| Campo | Valore |
|---|---|
| Documento | AP14-W07 EAGLE M27 OAT Result |
| Identificativo | AP14-W07-EAGLE-M27-OAT-RESULT |
| Versione | 2.1 |
| Data | 2026-08-21 |
| Stato | Accepted |
| Owner | Digital StarGate Architecture Office |

## 1. Scope

Record the runtime and end-to-end acceptance evidence for the designated M 27 observing session of 10/11 August 2026 and reconcile that historical publication with the current automatic-session contract without inventing retroactive evidence.

Target current-state flow:

`EAGLE evidence -> COMPLETE session package -> session/<session-id> -> governed promotion -> analytics -> AP-014 projections -> GitHub Pages`.

The designated package was published on 13 August 2026 before the current `session/<session-id>` promotion contract and before the current analytics workflow baseline. Historical execution of those later workflow contracts is therefore **N/A for the designated publication baseline**.

Current summary:

- unattended `NO_SESSION`: **PASS**;
- BKL-019 informational logging: **PASS / DONE**;
- BKL-020 scientific lineage: **PASS / DONE**;
- M27 repository package: **PASS / DONE**;
- AP-014 projections and portal reconciliation: **PASS / DONE**;
- historical promotion and analytics workflow run for the 10/11 package: **N/A historical baseline**;
- current-contract negative/fail-safe validation: **PASS**;
- real-session semantic idempotency: **PASS**;
- final governance CI: **PASS**;
- overall OAT: **Accepted**.

## 2. Runtime inspection and reconciliation evidence

Runtime inspection was executed on physical host `EAGLE30154` using governed read-only inspection and controlled runtime checks.

### Historical runtime

- Scheduled Task `Digital StarGate - Daily Session Upload`: FOUND / Ready.
- Principal: `PrimaLuceLab`, `LogonType = S4U`, `RunLevel = Highest`.
- Trigger: daily, `07:20` local.
- Historical run observed on 13 August 2026: `LastTaskResult = 1`.
- Historical launcher: `C:\DigitalStarGate\Automation\Invoke-DSGAutomaticSession.ps1`.
- Historical launcher SHA-256: `9C2F6B6010EB5A9268786E61D1AEAB123D6B7B56C51755B9B62B86B134A25AD8`.
- Historical automation configuration SHA-256: `BF1CDF0B8E313186E5B4283992ECE507B511DF8B6B66A5CFC241CC0C6DC11083`.
- Historical Reporting versions: `1.0.3`, `1.0.0`.
- Historical repository root: `C:\DigitalStarGate\digital-stargate-manual`.
- Historical deviations included `git pull --rebase`, direct publication to `main`, repository writes before proving `COMPLETE`, and legacy working-tree drift.

### Preserved rollback evidence

- Historical task exported before cutover.
- Historical launcher/config preserved under `C:\DigitalStarGate\SessionReports\deployment-backup\ap14-cutover-20260813-134642`.
- No destructive reset or history rewrite was used.

### Reconciled runtime

- Clean runtime clone: `C:\DigitalStarGate\digital-stargate-manual-ap14-runtime`.
- Required branch: `main`.
- Reporting `1.0.6` installed and verified.
- Effective configuration: `C:\DigitalStarGate\Automation\reporting.config.psd1`.
- NINA source: `C:\Users\PrimaLuceLab\AppData\Local\NINA\Logs`.
- PHD2 source: `C:\Users\PrimaLuceLab\Documents\PHD2`.
- CloudWatcher source: `C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv`.
- Preflight enforces clean `main`, fetch/pull fast-forward-only and `HEAD = origin/main`.

### `NO_SESSION` production acceptance

Controlled replay on 17 August 2026:

```text
DSG PRECHECK OK main-head=bbaef3fafbef749ccf32e07bc1c2fe61238e0669
MODULE version=1.0.6
DISCOVERY session=2026-08-16_2026-08-17 status=NO_SESSION nina=0 phd2=0 weatherRows=0
END outcome=NO_SESSION
```

Scheduled unattended execution on 18 August 2026:

```text
START candidate-window=2026-08-17T19:00:00..2026-08-18T06:00:00
BASE main-head=bbaef3fafbef749ccf32e07bc1c2fe61238e0669
MODULE version=1.0.6
DISCOVERY session=2026-08-17_2026-08-18 status=NO_SESSION nina=0 phd2=0 weatherRows=0
END outcome=NO_SESSION
```

- `LastTaskResult = 0`.
- No false staging directory remained.
- `NO_SESSION` acceptance result: **PASS**.

## 3. Designated M27 source evidence

Evidence-derived observations for 10/11 August 2026:

- NINA log `20260810-204106-3.2.0.9001.7156-202608.log`.
- NINA activity through at least `2026-08-11T05:09:32`.
- PHD2 DebugLog and GuideLog present.
- PHD2 guiding approximately `22:18:22` -> `05:00:14`.
- CloudWatcher evidence present.
- Controlled replay window: `2026-08-10 20:00:00` -> `2026-08-11 06:00:00` local.

The designated session remains `PARTIAL` where its own source evidence does not attest instrument configuration or target coordinates. Later sessions are not used to backfill historical facts.

### BKL-019 informational logging reconciliation

Versioned N.I.N.A. evidence from M 27 on 14/15 August directly records `INFO` telemetry including QHY695A connection, Advanced Sequence, target/exposure lifecycle, 600 s LIGHT exposures, L-Pro, binning 1x1, image save paths and target-coordinate evidence.

Authoritative source:

`data/sessions/2026/08/2026-08-14_2026-08-15/raw/nina/20260814-201744-3.2.0.9001.3996-202608.log`

Decision: **PASS / DONE**.

### BKL-020 lineage reconciliation

- `2026-08-10_2026-08-11`: `PARTIAL` where evidence is insufficient.
- `2026-08-14_2026-08-15`: `REGISTERED` with governed C8/QHY695A metadata.
- `2026-08-15_2026-08-16`: `REGISTERED` with governed C8/QHY695A metadata.

Decision: **PASS / DONE**.

## 4. Session package result

- Session ID: `2026-08-10_2026-08-11`.
- Controlled `Import-DSGSession` preview: **COMPLETE / PASS**.
- NINA files packaged: `1`.
- PHD2 files packaged: `2`.
- CloudWatcher weather package present.
- Repository copy/package publication: **PASS**.
- Published package commit: `4266f4249cda7b2a8c47c21fd5b69c890d3ff6ed`.
- Package structure on `main`: **PASS**.
- Manifest contains session identity, size and SHA-256 metadata: **PASS**.

The copy operation is complete and must not be repeated solely to satisfy stale documentation.

## 5. Historical publication vs current contracts

### Designated 10/11 August publication

- package present on `main`: **PASS**;
- current `session/<session-id>` promotion run: **N/A historical baseline**;
- current `promote-session-package.yml` run: **N/A historical baseline**;
- current `analyze-session-automatic.yml` run attributable to the original publication: **N/A historical baseline**.

Rationale: the package publication commit `4266f424...` predates the current governed promotion and analytics workflow baselines. Later workflows cannot be required retroactively as evidence of an earlier publication. Historical analytics/catalog outputs are nevertheless materialized and were reconciled by BKL-023/BKL-024.

### Current promotion contract

Developer Foundation #714 on exact head `ba3247aa891df3f11d43a0a808611956c0bb4ff5` completed **SUCCESS** and proved:

- nominal `COMPLETE`: PASS;
- `PARTIAL` rejection: PASS;
- manifest size mismatch rejection: PASS;
- SHA-256 mismatch rejection: PASS;
- extraneous scope rejection: PASS;
- non-descendant ancestry rejection: PASS.

Decision: **PASS contract-level**.

## 6. Analytics, projections and idempotency

Repository reconciliation establishes:

- `sessions.csv` contains M 27: **PASS**;
- `target-exposures.csv` uses governed provenance: **PASS**;
- `targets.csv` reflects M 27: **PASS**;
- scientific session catalog and observation index: **PASS**;
- latest scientific observation projection: **PASS**;
- Enterprise Search, Mission Control and Session Detail consume governed projections: **PASS**.

The current real-session analytics/projection contract is validated by Developer Foundation #723 on exact head `88ea7b1f915177906e5d514ee8254ef91ff5e45d`.

The gate executes the real downstream pipeline twice against the versioned `COMPLETE` session `2026-08-15_2026-08-16` and compares canonical governed scientific/projection state. Result: **semantic idempotency PASS**.

Volatile generation timestamps, line endings and PDF binary metadata are not scientific state. Byte-for-byte no-op hardening, if desired, is separate technical debt and is not an AP-014 acceptance blocker.

## 7. Portal deployment and correlated pages

- BKL-025 Pages integrity baseline: **PASS** (`deploy-pages` run 381 and published-site integrity PASS).
- Session Explorer / Session Detail / Mission Control / Enterprise Search reconciliation: **PASS**.
- Observatory Status vs historical latest observation separation: **PASS**.
- Session Reports latest-session ordering: **PASS**.
- Power and Network remain `UNKNOWN` without verified realtime sources: **PASS fail-safe behavior**.

## 8. Safety, fail-safe and idempotency matrix

| Check | State | Evidence |
|---|---|---|
| Scientific XISF unchanged by AP-014 inspection/import | PASS | runtime/OAT evidence |
| AP-013B path unaffected | PASS | separated architecture boundary |
| Source NINA/PHD2/weather not deleted | PASS | runtime/OAT evidence |
| No force-push/history rewrite | PASS | governance evidence |
| Clean `main` preflight | PASS | production preflight evidence |
| `NO_SESSION` rejected from publication path | PASS | 18/08 unattended production run |
| Historical M27 metadata incompleteness preserved | PASS | `PARTIAL` lineage |
| `PARTIAL` rejected by current automatic promotion path | PASS | Developer Foundation #714 |
| Non-descendant branch rejected | PASS | Developer Foundation #714 |
| Manifest size/hash mismatch rejected | PASS | Developer Foundation #714 |
| Extraneous path rejected | PASS | Developer Foundation #714 |
| Scientific metrics not synthesized from XISF filenames/transfer plan | PASS | BKL-020/BKL-022 |
| Real-session semantic rerun/idempotency | PASS | Developer Foundation #723, session `2026-08-15_2026-08-16` |

## 9. CI and quality evidence

Technical acceptance evidence:

- Developer Foundation #714: **SUCCESS** — promotion fail-safe contract;
- Developer Foundation #723: **SUCCESS** — real-session semantic idempotency and full applicable quality gate;
- Genera manuale Word #604: **SUCCESS**;
- exact technical head for #723/#604: `88ea7b1f915177906e5d514ee8254ef91ff5e45d`.

Final governance reconciliation evidence:

- exact head `a52c678ba6f3b498bc711ec7b8d5fad7359c7709`;
- Developer Foundation #725: **SUCCESS**;
- Genera manuale Word #606: **SUCCESS**.

## 10. Decision

**Overall OAT state: Accepted**

All technical/operational gates are **PASS** or explicitly **N/A historical baseline**. No acceptance blocker remains.

AP-014 OAT is formally accepted. No further physical EAGLE test or technical OAT rerun is required for this baseline. The historical M27 evidence remains immutable in meaning: fields unsupported by the original evidence remain `PARTIAL`, and later workflow contracts are not retroactively attributed to the 13 August publication.