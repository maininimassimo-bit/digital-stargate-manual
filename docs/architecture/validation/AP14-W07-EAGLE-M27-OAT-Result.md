# AP-014 EAGLE M27 Operational Acceptance Test Result

| Campo | Valore |
|---|---|
| Documento | AP14-W07 EAGLE M27 OAT Result |
| Identificativo | AP14-W07-EAGLE-M27-OAT-RESULT |
| Versione | 1.9 |
| Data | 2026-08-21 |
| Stato | Pending |
| Owner | Digital StarGate Architecture Office |

## 1. Scope

Record the runtime and end-to-end acceptance evidence for the designated M 27 observing session of 10/11 August 2026 and reconcile that historical publication with the current automatic-session contract without inventing retroactive evidence.

Target current-state flow:

`EAGLE evidence -> COMPLETE session package -> session/<session-id> -> governed promotion -> analytics -> AP-014 projections -> GitHub Pages`.

The designated package was published on 13 August 2026 before the current `session/<session-id>` + `promote-session-package.yml` contract was introduced. Therefore a historical execution of that later workflow is **N/A for the designated publication baseline**, not an outstanding historical run.

Current summary:

- unattended `NO_SESSION`: **PASS**;
- BKL-019 informational logging outcome: **PASS / DONE**;
- BKL-020 scientific lineage: **PASS / DONE**;
- M27 repository copy/package presence: **PASS / DONE**;
- AP-014 projections and portal reconciliation (BKL-023/BKL-024): **PASS / DONE**;
- historical `session/<session-id>` promotion run for the 10/11 package: **N/A**;
- current-contract negative/fail-safe validation: **PASS contract-level**;
- real-session idempotency: **PENDING**;
- overall OAT: **Pending**.

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

Reporting 1.0.6 separates exact-window session discovery from wider evidence collection. When neither NINA nor PHD2 evidence exists in the candidate window it returns before staging creation and before CloudWatcher parsing.

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

Relevant history includes `480c3fe2a8d36cd315cb814e7af97f8d6aa3260b` and `5fd4b0ebae58bf558e1d4818bdfc8840f8ed7137`.

Decision: **PASS / DONE**.

## 4. Session package result

- Session ID: `2026-08-10_2026-08-11`.
- Controlled `Import-DSGSession` preview: **COMPLETE / PASS**.
- NINA files packaged: `1`.
- PHD2 files packaged: `2`.
- CloudWatcher weather package present.
- Repository copy/package publication: **PASS**.
- Published package commit: `4266f4249cda7b2a8c47c21fd5b69c890d3ff6ed`.
- Package structure on `main`: **PASS** (`README.md`, `manifest.json`, `raw/nina`, `raw/phd2`, `raw/weather`, normalized content).
- Manifest contains session identity, size and SHA-256 metadata: **PASS**.

The copy operation is complete and must not be repeated solely to satisfy stale documentation.

## 5. Historical publication vs current promotion contract

### Designated 10/11 August publication

- package present on `main`: **PASS**;
- `session/<session-id>` branch under current contract: **N/A historical baseline**;
- `promote-session-package.yml` for historical publication: **N/A historical baseline**;
- current workflow-specific fast-forward/hash/scope run ID for that historical publication: **N/A historical baseline**.

Rationale: commit `4266f424...` predates introduction of the current governed promotion workflow. A later workflow cannot be required retroactively as evidence of an earlier publication.

### Current contract

The current `promote-session-package.yml` delegates validation to `.github/scripts/validate-session-promotion.ps1`. The same validator is exercised by `.github/scripts/test-session-promotion.ps1` in Developer Foundation.

Developer Foundation #714 on exact head `ba3247aa891df3f11d43a0a808611956c0bb4ff5` completed **SUCCESS** and proved:

- nominal `COMPLETE` package: PASS;
- `PARTIAL` rejection: PASS;
- manifest size mismatch rejection: PASS;
- SHA-256 mismatch rejection: PASS;
- extraneous path/scope rejection: PASS;
- non-descendant ancestry rejection: PASS.

Decision: **current-contract negative/fail-safe validation PASS at contract level**.

This evidence validates the promotion guard implementation without fabricating a retroactive M27 promotion run. Real-session idempotency remains a separate operational gate.

## 6. Analytics and AP-014 projections

Repository reconciliation establishes:

- `sessions.csv` contains M 27: **PASS**;
- `target-exposures.csv` uses governed evidence/provenance: **PASS**;
- `targets.csv` reflects M 27: **PASS**;
- `scientific-session-catalog.json` contains the sessions with governed metadata state: **PASS**;
- `scientific-observation-index.json` contains M 27 and separates metadata completeness from analytics quality: **PASS**;
- `latest-observation.json` identifies the current latest scientific session without inheriting stale target state: **PASS**;
- Enterprise Search consumes the observation index: **PASS**;
- Mission Control and Session Detail consume shared governed projections: **PASS**.

The historical `analyze-session-automatic.yml` run ID attributable specifically to the original 13 August M27 publication has not been identified. Its output state is materialized and reconciled, but the workflow-run criterion remains **PENDING** until either a traceable run is found or the acceptance authority explicitly classifies that historical run requirement as N/A based on workflow timeline.

## 7. Portal deployment and correlated pages

- BKL-025 Pages integrity baseline: **PASS** (`deploy-pages` run 381 and published-site integrity PASS).
- Session Explorer / Session Detail / Mission Control / Enterprise Search semantic reconciliation: **PASS** through BKL-023.
- Observatory Status vs historical latest observation separation: **PASS** through BKL-024.
- Session Reports latest-session ordering: **PASS**.
- Power and Network remain `UNKNOWN` without verified realtime sources: **PASS fail-safe behavior**.

No acceptance claim depends on manually editing a catalog to fabricate M27 visibility.

## 8. Safety, fail-safe and idempotency matrix

| Check | State | Evidence |
|---|---|---|
| Scientific XISF unchanged by AP-014 inspection/import | PASS | runtime/OAT evidence |
| AP-013B path unaffected | PASS | separated architecture boundary |
| Source NINA/PHD2/weather not deleted | PASS | runtime/OAT evidence |
| No force-push/history rewrite | PASS | governance evidence |
| Clean `main` preflight | PASS | production preflight evidence |
| `NO_SESSION` rejected from publication path | PASS | 18/08 unattended production run |
| Historical M27 metadata incompleteness preserved | PASS | `PARTIAL` lineage in governed metadata/projections |
| `PARTIAL` rejected by current automatic promotion path | PASS contract-level | Developer Foundation #714 |
| Non-descendant branch rejected | PASS contract-level | Developer Foundation #714 |
| Manifest size/hash mismatch rejected | PASS contract-level | Developer Foundation #714 |
| Extraneous path rejected | PASS contract-level | Developer Foundation #714 |
| Scientific metrics not synthesized from XISF filenames/transfer plan | PASS | BKL-020/BKL-022 governance |
| Real-session rerun/idempotency | PENDING | no traceable real-session double-run evidence identified |

## 9. CI and quality evidence

Exact-head CI used for fail-safe acceptance:

- head `ba3247aa891df3f11d43a0a808611956c0bb4ff5`;
- Developer Foundation #714: **SUCCESS**;
- `Test session promotion fail-safe contract`: **SUCCESS**;
- all Developer Foundation quality-gate steps: **SUCCESS**;
- Genera manuale Word #595: **SUCCESS**.

The fail-safe suite is therefore accepted as traceable CI evidence for the current promotion validator.

## 10. Decision

**Overall OAT state: Pending**

Accepted sub-gates:

- runtime `NO_SESSION`: PASS;
- BKL-019: DONE;
- BKL-020: DONE;
- repository copy/package presence: PASS;
- BKL-023 projections/portal consistency: DONE;
- BKL-024 status/report alignment: DONE;
- current promotion negative/fail-safe validation: PASS contract-level.

Historical current-contract promotion requirements are explicitly **N/A** for the 13 August M27 publication and are no longer treated as impossible historical blockers.

Remaining acceptance blockers are now limited to:

1. real-session idempotency;
2. final disposition of the historical `analyze-session-automatic.yml` run criterion.

This record remains `Pending` until those two items are resolved with traceable evidence or an explicit, evidence-based N/A decision by the acceptance authority.