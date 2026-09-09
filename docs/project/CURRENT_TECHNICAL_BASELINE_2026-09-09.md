# Digital StarGate Current Technical Baseline — 09/09/2026

| Campo | Valore |
|---|---|
| Stato | Current technical continuity baseline — reconciled through BKL-039 F5-A |
| Data | 09/09/2026 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Main HEAD before F5 | `e4ccecb3bc52af4a5baaa27cbc8df7178fd239ea` |
| Current governed package | BKL-039 — Equipment Performance Registry |
| Current PR | #132 |
| Current branch | `architecture/bkl-039-f5-dynamic-multisession-registry` |

## 1. Accepted BKL-039 baseline

BKL-039 F4-A machine-readable read-only consumer was merged through PR #130 as `c9ccf2bdfd849a4ae7305a4a7d134572353aa45e`. F4-B portal projection was merged through PR #131 as `e4ccecb3bc52af4a5baaa27cbc8df7178fd239ea`.

The accepted F4 population was bounded to session `2026-07-14_2026-07-15`, target `LDN 1320`, configuration `QUATTRO200_TOUPTEK294_BIN1`, filter `LPRO`, frame `LIGHT`, with 19 source-backed FWHM measurements. Accepted descriptive statistics were MEAN 7.5995, MINIMUM 6.78, MAXIMUM 9.05 and SAMPLE_STDDEV 0.5771.

## 2. Measurement semantics and authority

FWHM source values are not physically calibrated. Required semantics remain:

- `unit=NINA_FILENAME_FWHM_SOURCE_UNIT`;
- `unit_semantics=SOURCE_NATIVE_UNCALIBRATED`;
- `angular_calibration_state=NOT_PROVEN`;
- `authority=projection`;
- `action_authority=NONE`.

They must not be reinterpreted automatically as arcsec, pixel, seeing, focus quality or equipment health. No GOOD/BAD, RAG, ranking, threshold, percentile, score, anomaly diagnosis, predictive maintenance, recommendation, remediation or command/control semantics are authorized.

## 3. F5 target state

F5 evolves the bounded F4 projection into a dynamic multi-session registry. A future COMPLETE scientific session containing eligible source-backed data must become visible in Equipment Performance through the existing AP-014 publication/analytics chain without per-session manual edits.

The architecture contract is `docs/architecture/telemetry/BKL-039-F5-Dynamic-Multi-Session-Equipment-Performance-Registry-Contract.md`.

## 4. F5-A implementation baseline

PR #132 is open on `architecture/bkl-039-f5-dynamic-multisession-registry`.

F5-A provides governed discovery, tests and workflow. Repository discovery currently yields five eligible populations: three LDN 1320 / LPRO populations on 14–15, 15–16 and 16–17 July with counts 19, 32 and 31; M27 / Blu on 15–16 August with count 2; M27 / Green on 15–16 August with count 12.

Fail-closed exclusions are M27 14–15 August / L-Pro and M27 15–16 August / Red as `FWHM_SOURCE_VALUE_UNRESOLVED`, plus PARTIAL M27 10–11 August as `METADATA_NOT_REGISTERED`. These exclusions must not be overridden by invented evidence.

At exact HEAD `b123d6a28fd7cdc70483ce7a6f7004769f26bcfb`, all four applicable F5-A workflows are SUCCESS:

- BKL-039 F5 Governance #4;
- Developer Foundation #1174;
- Validate documentation #793;
- Genera manuale Word #1218.

## 5. F5-B entry condition

F5-A is green and F5-B is authorized. F5-B must generate a deterministic collection read model from the eligible populations and update the Equipment Performance portal to select/render populations dynamically. Each view preserves population/configuration/session/target/filter/frame identity, measurement count and values, descriptive statistics, measurement semantics, source record references, Citation, Provenance, limitations and projection-only authority. The browser must not recompute authoritative metrics.

## 6. F5-C automation requirement

After F5-B, integrate discovery and F3/F4 regeneration into `.github/workflows/analyze-session-automatic.yml` after target/history rebuild and also inside retry `regenerate()` paths following `git reset --hard origin/main`. Governed generated paths must be committed with the existing scientific projections so regeneration remains deterministic and idempotent.

## 7. Safety/runtime boundary

No EAGLE/PC command or runtime change is required for F5. AP-014 remains the ingestion/publication path. No device control, remediation or Safety Authority coupling is introduced; local physical interlocks and local Safety Authority remain independent and authoritative.
