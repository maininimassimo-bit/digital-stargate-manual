# AP-014 EAGLE M27 Operational Acceptance Test Result

| Campo | Valore |
|---|---|
| Documento | AP14-W07 EAGLE M27 OAT Result |
| Identificativo | AP14-W07-EAGLE-M27-OAT-RESULT |
| Versione | 1.3 |
| Data | 2026-08-13 |
| Stato | Pending |
| Owner | Digital StarGate Architecture Office |

## 1. Scope

Record the runtime and end-to-end acceptance evidence for the M 27 observing session of 10/11 August 2026 and prove the permanent automatic flow:

`EAGLE evidence -> COMPLETE session package -> session branch -> governed promotion -> analytics -> AP-014 projections -> GitHub Pages`.

## 2. Runtime inspection and reconciliation evidence

Runtime inspection was executed on physical host `EAGLE30154` using the governed read-only collector.

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

1. Reporting `1.0.3` instead of governed `1.0.4`;
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
- Branch: `main`.
- Clone HEAD at creation/verification: `7e8a57884cf740ae1a3584e044144f7234c795b4`.
- `HEAD...origin/main = 0 0` at creation.
- Working tree was restored to clean after removing the obsolete untracked `templates/reporting/reporting.config.psd1` created by the pre-fix installer.

### Reporting runtime reconciliation

- Reporting `1.0.4` installed successfully at `C:\Users\PrimaLuceLab\Documents\WindowsPowerShell\Modules\DigitalStarGate.Reporting\1.0.4`.
- Reporting source repository advanced through:
  - `fedb5564fc1009dd356f20d7c5739fc4ca4cc1e6` — actual EAGLE CloudWatcher source path;
  - `0b7edd2f1d175b157d4ba52fb1cedbbdb52103ed` — runtime config kept outside Git working tree;
  - `518a91bd17c9d4dbb055c7febc158edeac03ae27` — task default aligned to external runtime config.
- Runtime config: `C:\DigitalStarGate\Automation\reporting.config.psd1`.
- Effective RepositoryRoot: `C:\DigitalStarGate\digital-stargate-manual-ap14-runtime`.
- NINA source: `C:\Users\PrimaLuceLab\AppData\Local\NINA\Logs`.
- PHD2 source: `C:\Users\PrimaLuceLab\Documents\PHD2`.
- CloudWatcher source: `C:\Users\PrimaLuceLab\Documents\CloudWatcher\CloudWatcher.csv`.
- CloudWatcher source existence check: PASS.
- Runtime repository remained clean after external-config installation: PASS.

### Scheduled Task cutover

Cutover completed successfully on the physical EAGLE.

- Task: `Digital StarGate - Daily Session Upload`.
- State: `Ready`.
- UserId: `PrimaLuceLab`.
- LogonType: `S4U`.
- RunLevel: `Highest`.
- Execute: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`.
- Arguments: `-NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "C:\DigitalStarGate\Automation\Invoke-DSGAutomaticSession.ps1" -ConfigPath "C:\DigitalStarGate\Automation\reporting.config.psd1"`.
- WorkingDirectory: `C:\DigitalStarGate\Automation`.
- Trigger: daily `07:20` local; enabled.
- Next run observed after final alignment: `2026-08-14 07:20:20` local.
- `LastTaskResult = 1` remains the historical pre-cutover result and is not evidence of the new runtime behavior.
- Runtime launcher SHA-256: `7CCA0699E880F5F416D535B24834B6EC8C413EE197EF3CFFAEE6EE60FAA4A110`.
- Governed source launcher SHA-256: `7CCA0699E880F5F416D535B24834B6EC8C413EE197EF3CFFAEE6EE60FAA4A110`.
- Source/runtime SHA-256 equality: PASS.

### Runtime conformance assessment after cutover

**Installed runtime configuration: CONFORMANT BY INSPECTION with AP14-INT-EAGLE-PUBLISH-001; scheduled operational execution evidence remains pending.**

Runtime evidence bundle from pre-cutover inspection:

`C:\DigitalStarGate\SessionReports\runtime-evidence\EAGLE-runtime-evidence-20260813-132013`

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
- Runtime Git working tree clean before repository-copy gate: PASS.
- Re-run behavior idempotent: PENDING.
- PARTIAL/NO_SESSION protection verified in production: PENDING.

## 9. CI/quality gates

- Reporting collector/locked-weather Quality Gate run `31694911434`: PASS on `591984ae9cbb6e7b4d54ef3ab6a696fb2a98e700`.
- Reporting repository-root installer Quality Gate run `31696735200`: PASS on `f27330da5f4e8363fcfea9af2ccfa808592091b7`.
- Reporting unattended-task semantics Quality Gate run `31697194103`: PASS on `5b82235bd1aab21bfac5f47a11c38538ee3f264b`.
- Reporting actual CloudWatcher path Quality Gate run `31698320816`: PASS on `fedb5564fc1009dd356f20d7c5739fc4ca4cc1e6`.
- Quality gates for external-runtime-config commits `0b7edd2f...` / `518a91bd...`: verification required before final OAT acceptance.
- Post-OAT Developer Foundation: PENDING.
- Post-OAT Pages: PENDING.

## 10. Decision

**Stato: Pending**

The EAGLE runtime is structurally reconciled and the M27 staging preview is COMPLETE with real NINA, PHD2 and CloudWatcher evidence. The next gate is a controlled repository copy followed by manifest/content/hash verification before any branch publication.

This record may be changed to `Accepted` only when all mandatory repository-copy, promotion, analytics, portal, idempotency and scheduled-runtime evidence is recorded and verifiable.
