# AP-014 EAGLE M27 Operational Acceptance Test Result

| Campo | Valore |
|---|---|
| Documento | AP14-W07 EAGLE M27 OAT Result |
| Identificativo | AP14-W07-EAGLE-M27-OAT-RESULT |
| Versione | 1.1 |
| Data | 2026-08-13 |
| Stato | Pending |
| Owner | Digital StarGate Architecture Office |

## 1. Scope

Record the runtime and end-to-end acceptance evidence for the M 27 observing session of 10/11 August 2026 and prove the permanent automatic flow:

`EAGLE evidence -> COMPLETE session package -> session branch -> governed promotion -> analytics -> AP-014 projections -> GitHub Pages`.

## 2. Runtime inspection evidence

Runtime inspection was executed on physical host `EAGLE30154` using the governed read-only collector.

- Scheduled Task `Digital StarGate - Daily Session Upload`: FOUND / Ready.
- Task principal: `PrimaLuceLab`, `LogonType = S4U`, `RunLevel = Highest`.
- Trigger: daily; historical start boundary `2026-07-16T07:20:00+02:00`.
- Last observed run: `2026-08-13 12:22:22` local; `LastTaskResult = 1` (FAILED); next run observed for `2026-08-14 07:20:20`.
- Installed launcher path: `C:\DigitalStarGate\Automation\Invoke-DSGAutomaticSession.ps1`.
- Installed launcher SHA-256: `9C2F6B6010EB5A9268786E61D1AEAB123D6B7B56C51755B9B62B86B134A25AD8`.
- Installed launcher last modified: `2026-07-22 16:06:59` local.
- Task arguments: `-NoProfile -NonInteractive -ExecutionPolicy Bypass -File "C:\DigitalStarGate\Automation\Invoke-DSGAutomaticSession.ps1" -ConfigPath "C:\DigitalStarGate\Automation\automation.config.psd1"`.
- Effective automation config SHA-256: `BF1CDF0B8E313186E5B4283992ECE507B511DF8B6B66A5CFC241CC0C6DC11083`.
- Installed `DigitalStarGate.Reporting` versions: `1.0.3` and `1.0.0`.
- Version selected by a clean `powershell.exe -NoProfile -NonInteractive` lookup: `1.0.3` from `C:\Users\PrimaLuceLab\Documents\WindowsPowerShell\Modules\DigitalStarGate.Reporting\1.0.3`.
- Historical automation repository root: `C:\DigitalStarGate\digital-stargate-manual`.
- Historical repository branch: `main`.
- Historical repository observed HEAD before reconciliation: `0b00d1f23c825a2f753cef2a13fc41d2ea5e3b1a`; `0` local commits ahead and `44` behind `origin/main` at inspection time.
- Historical repository was not clean because three session README files were represented with CRLF/LF differences only; semantic diff check with `--ignore-space-at-eol` returned exit code `0`. Copies and Git stash evidence were retained before further work.
- Clean parallel AP-014 runtime clone created at `C:\DigitalStarGate\digital-stargate-manual-ap14-runtime`.
- Clean runtime clone branch/HEAD: `main` / `7e8a57884cf740ae1a3584e044144f7234c795b4`.
- Clean runtime clone status: clean; `HEAD...origin/main = 0 0` at creation.
- Runtime evidence bundle: `C:\DigitalStarGate\SessionReports\runtime-evidence\EAGLE-runtime-evidence-20260813-132013`.

Collector observations:

- Host: `EAGLE30154`.
- Task found: `True`.
- Launcher count: `1`.
- Reporting module count: `2`.
- Configuration found: `True`.
- NINA files in broad M27 inspection window: `1`.
- PHD2 files in broad M27 inspection window: `2`.
- Weather source found: `True`.
- Weather SHA-256 during live CloudWatcher operation: unavailable because the file is locked by the producer; collector records this as a non-fatal unavailable hash state.

Validated Reporting collector baseline before runtime execution:

`maininimassimo-bit/DigitalStarGate.Reporting@591984ae9cbb6e7b4d54ef3ab6a696fb2a98e700`

Reporting Quality Gate run `31694911434`: PASS.

### Runtime conformance assessment

**Current installed historical runtime: NON-CONFORMANT with AP14-INT-EAGLE-PUBLISH-001.**

Observed deviations requiring reconciliation before M27 publication:

1. installed Reporting runtime resolves to `1.0.3`, not governed `1.0.4`;
2. historical launcher performs `git pull --rebase`, while AP-014 requires fast-forward-only synchronization;
3. historical launcher commits and pushes the selected branch directly; its configured branch is `main`, while AP-014 requires publication to `session/<session-id>` and GitHub-owned promotion to `main`;
4. historical launcher writes directly into the repository before it has proved the package is `COMPLETE`; the governed launcher uses a staging pass first;
5. historical automation points to the legacy repository clone currently affected by line-ending/index drift;
6. last Scheduled Task run returned exit code/result `1`; exact failure reason must be confirmed from `C:\DigitalStarGate\AutomationLogs` before cutover.

No destructive correction of the historical clone or task has been performed during inspection.

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

- Scientific XISF files unchanged during inspection: PASS.
- AP-013B transport/import unchanged during inspection: PASS.
- No source NINA/PHD2/weather evidence deleted during inspection: PASS.
- No force push/history rewrite performed during inspection: PASS.
- Re-run behavior idempotent: PENDING.
- PARTIAL/NO_SESSION protection verified in production: PENDING.

## 9. CI/quality gates

- `digital-stargate-manual` baseline workflow gate before EAGLE inspection: PASS on the previously validated main baseline.
- `DigitalStarGate.Reporting` collector/locked-weather quality gate: PASS on `591984ae9cbb6e7b4d54ef3ab6a696fb2a98e700`, run `31694911434`.
- Post-runtime-reconciliation Reporting Quality Gate: PENDING.
- Post-OAT Developer Foundation: PENDING.
- Post-OAT Pages: PENDING.

## 10. Decision

**Stato: Pending**

Runtime inspection is complete enough to determine that the historical EAGLE automation must be reconciled before M27 replay. No M27 publication is authorized while the installed runtime remains non-conformant.

This record may be changed to `Accepted` only when all mandatory runtime, session, promotion, analytics, portal and safety evidence is recorded and verifiable. A repository-only implementation is insufficient for acceptance.
