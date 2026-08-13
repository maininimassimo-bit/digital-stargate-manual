# AP-014 EAGLE M27 Operational Acceptance Test Result

| Campo | Valore |
|---|---|
| Documento | AP14-W07 EAGLE M27 OAT Result |
| Identificativo | AP14-W07-EAGLE-M27-OAT-RESULT |
| Versione | 1.2 |
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
- `HEAD...origin/main = 0 0` at verification.
- Working tree clean at verification.

### Reporting runtime reconciliation

- Governed Reporting source repository synchronized to commit `f27330da5f4e8363fcfea9af2ccfa808592091b7` for installation logic and later `5b82235bd1aab21bfac5f47a11c38538ee3f264b` for task deployment logic.
- Reporting `1.0.4` installed successfully at `C:\Users\PrimaLuceLab\Documents\WindowsPowerShell\Modules\DigitalStarGate.Reporting\1.0.4`.
- Effective Reporting configuration installed at `C:\DigitalStarGate\digital-stargate-manual-ap14-runtime\templates\reporting\reporting.config.psd1`.
- Effective `RepositoryRoot`: `C:\DigitalStarGate\digital-stargate-manual-ap14-runtime`.
- NINA source: `C:\Users\PrimaLuceLab\AppData\Local\NINA\Logs`.
- PHD2 source: `C:\Users\PrimaLuceLab\Documents\PHD2`.
- Weather source: `C:\DigitalStarGate\Weather\CloudWatcher.csv`.

### Scheduled Task cutover

Cutover completed successfully on the physical EAGLE.

- Task: `Digital StarGate - Daily Session Upload`.
- State after cutover: `Ready`.
- UserId: `PrimaLuceLab`.
- LogonType: `S4U`.
- RunLevel: `Highest`.
- Execute: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`.
- Arguments: `-NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "C:\DigitalStarGate\Automation\Invoke-DSGAutomaticSession.ps1" -ConfigPath "C:\DigitalStarGate\digital-stargate-manual-ap14-runtime\templates\reporting\reporting.config.psd1"`.
- WorkingDirectory: `C:\DigitalStarGate\Automation`.
- Trigger start boundary after cutover: `2026-08-13T07:20:00+02:00`; enabled.
- Next run observed: `2026-08-14 07:20:20` local.
- `LastTaskResult = 1` remains the historical pre-cutover run result and is not evidence of the new runtime behavior.
- Runtime launcher SHA-256 after cutover: `7CCA0699E880F5F416D535B24834B6EC8C413EE197EF3CFFAEE6EE60FAA4A110`.
- Governed source launcher SHA-256: `7CCA0699E880F5F416D535B24834B6EC8C413EE197EF3CFFAEE6EE60FAA4A110`.
- Source/runtime SHA-256 equality: PASS.

### Runtime conformance assessment after cutover

**Installed runtime configuration: CONFORMANT BY INSPECTION with AP14-INT-EAGLE-PUBLISH-001; operational execution evidence remains pending.**

The installed launcher/task/config now satisfy the structural runtime contract for unattended execution, governed repository root, Reporting 1.0.4, and governed launcher identity. M27 replay and a successful scheduled execution are still required before operational acceptance.

Runtime evidence bundle from pre-cutover inspection:

`C:\DigitalStarGate\SessionReports\runtime-evidence\EAGLE-runtime-evidence-20260813-132013`

## 3. M27 source evidence

- Actual session start: PENDING — must be derived from NINA/PHD2 evidence.
- Actual session end: PENDING — must be derived from NINA/PHD2 evidence.
- NINA evidence count in broad inspection window: `1` file.
- PHD2 evidence count in broad inspection window: `2` files.
- CloudWatcher evidence: source exists and is actively locked by CloudWatcher; hash unavailable while producer holds the file.
- Source evidence observations: evidence presence is confirmed, but the exact scientific session window has not yet been derived from content/timestamps and no package has yet been generated.

The actual observing window must be derived from NINA/PHD2 evidence. A nominal 19:00-06:00 window must not be treated as authoritative without confirmation.

## 4. Session package result

- Session ID: PENDING
- `Import-DSGSession` preview status: PENDING
- `Import-DSGSession -CopyToRepository` status: PENDING
- Manifest path: PENDING
- Manifest SHA-256 verification: PENDING
- NINA package evidence: PENDING
- PHD2 package evidence: PENDING
- Weather package evidence: PENDING

Acceptance requires `Status = COMPLETE`.

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

- Scientific XISF files unchanged through inspection/cutover: PASS.
- AP-013B transport/import unchanged through inspection/cutover: PASS.
- No source NINA/PHD2/weather evidence deleted: PASS.
- No force push/history rewrite: PASS.
- Historical runtime rollback package retained: PASS.
- Re-run behavior idempotent: PENDING.
- PARTIAL/NO_SESSION protection verified in production: PENDING.

## 9. CI/quality gates

- `digital-stargate-manual` baseline workflow gate before EAGLE inspection: PASS on the previously validated main baseline.
- Reporting collector/locked-weather Quality Gate run `31694911434`: PASS on `591984ae9cbb6e7b4d54ef3ab6a696fb2a98e700`.
- Reporting repository-root installer Quality Gate run `31696735200`: PASS on `f27330da5f4e8363fcfea9af2ccfa808592091b7`.
- Reporting unattended-task semantics Quality Gate run `31697194103`: PASS on `5b82235bd1aab21bfac5f47a11c38538ee3f264b`.
- Post-OAT Developer Foundation: PENDING.
- Post-OAT Pages: PENDING.

## 10. Decision

**Stato: Pending**

EAGLE runtime inspection and structural reconciliation are complete. The new task/runtime is conformant by inspection but has not yet produced accepted operational evidence. The next gate is the controlled M27 replay using the actual session window derived from real NINA/PHD2 evidence.

This record may be changed to `Accepted` only when all mandatory session, promotion, analytics, portal and safety evidence is recorded and verifiable.
