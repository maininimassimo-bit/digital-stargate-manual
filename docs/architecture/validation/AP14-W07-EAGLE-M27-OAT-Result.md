# AP-014 EAGLE M27 Operational Acceptance Test Result

| Campo | Valore |
|---|---|
| Documento | AP14-W07 EAGLE M27 OAT Result |
| Identificativo | AP14-W07-EAGLE-M27-OAT-RESULT |
| Versione | 1.0 |
| Data | 2026-08-13 |
| Stato | Pending |
| Owner | Digital StarGate Architecture Office |

## 1. Scope

Record the runtime and end-to-end acceptance evidence for the M 27 observing session of 10/11 August 2026 and prove the permanent automatic flow:

`EAGLE evidence -> COMPLETE session package -> session branch -> governed promotion -> analytics -> AP-014 projections -> GitHub Pages`.

## 2. Runtime inspection evidence

- Scheduled Task `Digital StarGate - Daily Session Upload`: PENDING
- Task principal/trigger/action: PENDING
- Installed launcher path: PENDING
- Installed launcher SHA-256: PENDING
- Installed `DigitalStarGate.Reporting` version/path: PENDING
- Effective Reporting configuration: PENDING
- EAGLE repository branch/HEAD/working tree: PENDING
- Runtime evidence bundle reference: PENDING

Collector baseline:

`maininimassimo-bit/DigitalStarGate.Reporting@Get-DSGEagleRuntimeEvidence.ps1`

Validated Reporting commit:

`27f3c0a9a2c034f7f47b486f7df87ee10b8f3465`

Reporting Quality Gate run `31693642267`: PASS.

## 3. M27 source evidence

- Actual session start: PENDING
- Actual session end: PENDING
- NINA evidence count: PENDING
- PHD2 evidence count: PENDING
- CloudWatcher evidence status/rows: PENDING
- Source evidence observations: PENDING

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

- Scientific XISF files unchanged: PENDING
- AP-013B transport/import unchanged: PENDING
- No source NINA/PHD2/weather evidence deleted: PENDING
- No force push/history rewrite: PENDING
- Re-run behavior idempotent: PENDING
- PARTIAL/NO_SESSION protection verified: PENDING

## 9. CI/quality gates

- `digital-stargate-manual` baseline workflow gate before deployment: PASS on `8c107cdd03adb7543a4257ff3fada32d6302b57a`.
- `DigitalStarGate.Reporting` quality gate before runtime inspection: PASS on `27f3c0a9a2c034f7f47b486f7df87ee10b8f3465`.
- Post-OAT Developer Foundation: PENDING
- Post-OAT Pages: PENDING

## 10. Decision

**Stato: Pending**

This record may be changed to `Accepted` only when all mandatory runtime, session, promotion, analytics, portal and safety evidence is recorded and verifiable. A repository-only implementation is insufficient for acceptance.
