# AP-014 Session Package to Scientific Portal Automation

- **Identifier:** AP14-W07-AUTO-001
- **Status:** Downstream implemented; EAGLE producer OAT pending
- **Version:** 1.2
- **Target:** AP-014 / RC3 readiness
- **Dependencies:** DigitalStarGate.Reporting, versioned session packages, DSG Analytics v2.8, AP-014 catalog projections

## Purpose

Close the governed automation gap between the EAGLE-produced session package and the AP-014 Scientific Portal without making XISF transport or the operational image repository an AP-014 source of truth.

## Architecture rule

The EAGLE is the producer of NINA, PHD2 and CloudWatcher evidence and of the governed session package. The PC Principale remains the development/integration and downstream analytics environment. AP-013B XISF transport is a separate data path.

## Target flow

```mermaid
flowchart TD
    A[NINA + PHD2 + CloudWatcher on EAGLE] --> B[DigitalStarGate.Reporting Import-DSGSession]
    B --> C{Package COMPLETE?}
    C -- No --> D[PARTIAL / NO_SESSION: no AP-014 promotion]
    C -- Yes --> E[Versioned data/sessions manifest]
    E --> F[Automatic analytics]
    F --> G[sessions.csv]
    F --> H[target-exposures.csv]
    H --> I[targets.csv]
    G --> J[scientific-session-catalog.json]
    I --> J
    J --> K[scientific-observation-index.json]
    K --> L[GitHub Pages]
```

## Verified producer

The certified `maininimassimo-bit/DigitalStarGate.Reporting` module is the existing session-package producer. Its configuration uses the EAGLE `PrimaLuceLab` NINA/PHD2 paths and the local CloudWatcher CSV. `Import-DSGSession` copies the three evidence streams into the session package, writes `manifest.json` and sets `COMPLETE`, `PARTIAL` or `NO_SESSION` according to actual evidence.

The detailed alignment and M 27 OAT sequence are recorded in `AP14-W07-EAGLE-Session-Package-Producer.md`.

## Downstream implementation

1. A versioned `data/sessions/**/manifest.json` is the trigger boundary for AP-014 processing.
2. `.github/workflows/analyze-session-automatic.yml` validates package completeness, runs analytics/report/history/target projections, regenerates the scientific session catalog and observation index, verifies deterministic output, and commits only derived versioned projections.
3. `.github/scripts/generate-scientific-session-catalog.mjs` deterministically derives the AP-014 session catalog from `sessions.csv` and `targets.csv`.
4. `.github/scripts/generate-scientific-catalog.mjs` remains the observation-index generator from the session catalog.
5. AP-013B continues to transport XISF files independently to `F:\Astrofotografia`; those files are not used to synthesize missing NINA/PHD2/weather evidence.

## Superseded implementation note

The PC-side collector introduced in commit `5d9f954e0cff39b5ac85a5f7db64e6a8d0891a4f` was based on an incorrect ownership assumption and is superseded by this architecture correction. It must not be deployed or scheduled. The authoritative producer is the existing EAGLE reporting flow.

## Fail-safe and idempotency rules

- `PARTIAL` and `NO_SESSION` are not promoted into AP-014 analytics/catalog projections.
- Missing NINA, PHD2 or weather evidence is never inferred from XISF filenames or AP-013B transport metadata.
- No quality metric is synthesized when analytics does not provide it.
- Scientific XISF files are never deleted, overwritten or moved by AP-014.
- AP-013B transport/import behavior remains unchanged.
- Re-running deterministic downstream projections with unchanged inputs produces no new projection commit.

## Validation matrix

| Check | Status |
| --- | --- |
| EAGLE responsibility documented in EA-001 | VERIFIED |
| DigitalStarGate.Reporting EAGLE paths | VERIFIED |
| Import-DSGSession package/evidence behavior | VERIFIED |
| AP-013B XISF transport separation | VERIFIED |
| AP-014 downstream analytics/catalog automation | IMPLEMENTED |
| Actual EAGLE scheduled reporting task/script | TO INSPECT / OAT |
| M 27 EAGLE package | OAT PENDING |
| M 27 end-to-end analytics/catalog | Pending package publication |

## Acceptance criteria

The slice is operationally accepted only when the existing EAGLE reporting automation produces a real `COMPLETE` M 27 session package, versions it to the authoritative repository, and the downstream automatic chain creates analytics containing that session, regenerates both AP-014 projections, passes CI, deploys Pages, and shows M 27 without manual catalog edits.
