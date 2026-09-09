# BKL-039 F3 — Descriptive Performance Measurement and Aggregation Contract

| Field | Value |
|---|---|
| Identifier | `BKL-039-F3` |
| Capability | BKL-039 — Equipment Performance Registry |
| Status | In Progress — source/unit discovery locked |
| Version | 0.2 |
| Date | 2026-09-09 |
| Base | F2-A merge `96e0e7197d1b729b5ae0b2e0cec402b81baac17f` |
| Runtime impact | None — repository/analytics only |
| Safety impact | None — local physical Safety Authority unchanged |

## 1. Entry condition

BKL-039 F2-A is repository-integrated and post-merge green on merge SHA `96e0e7197d1b729b5ae0b2e0cec402b81baac17f`.

Verified post-merge workflows:

- BKL-039 F2 Governance #16 — SUCCESS;
- Genera manuale Word #1180 — SUCCESS;
- Deploy MkDocs artifact to GitHub Pages #723 — SUCCESS;
- Validate documentation #755 — SUCCESS;
- Developer Foundation #1136 — SUCCESS.

Therefore F2-A is accepted as the machine-readable identity/session-usage foundation for F3.

## 2. Objective

F3 introduces deterministic, source-backed **descriptive performance measurements and statistics** for equipment/configuration history.

F3 is not a health-scoring, ranking, anomaly, prediction or maintenance-policy increment. It may only compute quantities whose source values, unit, population and method are explicitly repository-resolvable.

## 3. Source discovery — verified current path

The accepted repository contains an executable warehouse quality path in `dsg-analytics/warehouse/datasets/quality.py`.

The implementation:

- reads `data/analytics/history/target-exposures.csv` and `data/analytics/history/target-summary.csv`;
- accepts only `LIGHT` exposures for quality aggregation;
- extracts a positive numeric FWHM value from the `_FWHM_<value>_` token embedded in the source N.I.N.A. image filename;
- groups values by `(session_id, target_name, filter_name)`;
- requires the number of extracted FWHM values to equal the declared `image_count` in `target-summary.csv`;
- computes arithmetic mean, minimum, maximum and sample standard deviation;
- rounds the derived values to four decimal places;
- emits `average_fwhm`, `minimum_fwhm`, `maximum_fwhm`, `fwhm_stddev`, `image_count`, average camera temperature, integration hours and time bounds.

The existing warehouse tests contain deterministic known-answer assertions for this transformation.

This is the accepted calculation reference for the first F3 slice; F3 must not silently change its mathematics.

## 4. Bounded source population — LOCKED

The smallest source population that cleanly maps to an accepted F2-A identity is:

| Field | Locked value |
|---|---|
| `configuration_id` | `QUATTRO200_TOUPTEK294_BIN1` |
| `session_id` | `2026-07-14_2026-07-15` |
| target | `LDN 1320` |
| filter | `LPRO` |
| binning | `1` |
| session state | `REGISTERED` |
| declared LIGHT image count | `19` |
| declared integration | `11400.00 s` / `3.1667 h` |
| source exposure dataset | `data/analytics/history/target-exposures.csv` |
| source summary dataset | `data/analytics/history/target-summary.csv` |
| identity/session binding | `data/analytics/metadata/session-scientific-metadata.csv` |

The F2-A contract and independent review already bind session `2026-07-14_2026-07-15` to `QUATTRO200_TOUPTEK294_BIN1`.

`target-summary.csv` independently declares exactly 19 images for `(2026-07-14_2026-07-15, LDN 1320, LPRO)`. The exposure dataset contains the corresponding N.I.N.A. records and FWHM-bearing filenames.

The first executable F3 fixture must use this population only. Expanding to the C8 session or any other configuration is a later compatible increment after this slice is accepted.

## 5. Unit discovery — LOCKED FAIL-CLOSED DECISION

Repository evidence does **not** prove that the numeric `_FWHM_<value>_` token consumed by the current executable warehouse path is already calibrated in arcseconds.

Evidence is deliberately separated:

1. `docs/architecture/warehouse/datasets-and-schema.md` requires measurements to have explicit units and lists `fwhm_arcsec` as an example of a well-named unit-bearing field.
2. Historical `.bak` warehouse prototypes also contain a field named `fwhm_arcsec`, but those files are non-authoritative historical design material under the BKL-039 F1 governance boundary.
3. The **current executable** quality implementation extracts the filename token as a raw positive float and emits fields named `average_fwhm`, `minimum_fwhm`, `maximum_fwhm` and `fwhm_stddev`; it performs no pixel-scale or angular-unit conversion and carries no source-unit assertion.
4. DSDM-002 can model `pixelScaleArcsecPerPixel`, but the presence of a logical pixel-scale field is not proof that the historical filename token was expressed in pixels or converted to arcseconds.

Therefore F3 must not label these values `arcsec`, `pixels`, or any other physical unit.

The initial machine-readable F3 unit is locked as:

`NINA_FILENAME_FWHM_SOURCE_UNIT`

with:

- `unit_semantics = SOURCE_NATIVE_UNCALIBRATED`;
- `angular_calibration_state = NOT_PROVEN`;
- no conversion factor;
- no cross-unit normalization.

This is an explicit evidence-preserving semantic label, not a new physical unit claim.

Any future conversion to arcseconds requires a separately governed mapping that proves the native token semantics and applicable pixel scale for the exact configuration/session population.

## 6. Authorized semantic types

F3 may add:

- `PERFORMANCE_MEASUREMENT`;
- `DESCRIPTIVE_PERFORMANCE_STATISTIC`.

F3 must preserve existing F2-A `EQUIPMENT_IDENTITY` and `EQUIPMENT_USAGE_OBSERVATION` semantics and must not add `PERFORMANCE_ASSESSMENT` or `RECOMMENDATION`.

## 7. First metric family — FWHM only

The first executable F3 slice may emit only the following descriptive quantities for the locked population:

- source sample count;
- arithmetic mean FWHM;
- minimum FWHM;
- maximum FWHM;
- sample standard deviation FWHM.

No numeric value may be interpreted as GOOD/BAD, healthy/degraded, acceptable/unacceptable, nominal/outlier or failure evidence.

Camera temperature and integration time remain provenance/context for this first slice; they are not separate equipment-performance metrics yet.

## 8. Method contract — LOCKED

The first executable method family must be versioned and must reproduce the accepted warehouse calculation semantics exactly.

Reserved method identifiers for the implementation slice:

- `BKL039-F3-FWHM-MEAN-V1` — arithmetic mean over all source-backed FWHM values in the declared population, rounded to 4 decimals;
- `BKL039-F3-FWHM-MIN-V1` — minimum over the same population, rounded to 4 decimals;
- `BKL039-F3-FWHM-MAX-V1` — maximum over the same population, rounded to 4 decimals;
- `BKL039-F3-FWHM-SAMPLE-STDDEV-V1` — sample standard deviation with denominator `n-1`; returns `0.0` only for a valid one-element population, matching current warehouse semantics; rounded to 4 decimals.

The implementation must derive these values from source exposure records; it must not copy precomputed display/report values as calculation authority.

## 9. Population and sample semantics

Every statistic must declare:

- `configuration_id`;
- `session_id`;
- `target_name`;
- `filter_name`;
- population selector;
- `sample_count`;
- source record references;
- `method_id`;
- `unit`;
- unit semantics/calibration state;
- quality/coverage;
- Citation references;
- Provenance references;
- `authority=projection`;
- `action_authority=NONE`.

For the locked first fixture, `sample_count` must equal `19`. Any mismatch against the source summary or extracted LIGHT population must fail closed.

`sample_count=0` is not a valid statistic. Missing source images or unresolved FWHM values must produce no statistic or an explicit unavailable/insufficient state, never a fabricated zero.

## 10. Quality and coverage rules

F3 must distinguish at least:

- `COMPLETE_FOR_DECLARED_POPULATION`;
- `PARTIAL_FOR_DECLARED_POPULATION`;
- `UNKNOWN_COVERAGE`;
- `INSUFFICIENT_SAMPLE`.

These are evidence/coverage states only, not equipment-health states.

For the initial fixture, `COMPLETE_FOR_DECLARED_POPULATION` is permitted only when all 19 declared LIGHT records resolve, contain valid positive FWHM tokens and participate in the aggregation. Otherwise generation/validation must fail closed rather than silently downgrade a supposedly complete fixture.

## 11. Comparability boundary

F3 may aggregate only within the declared equipment configuration and compatible method/unit population.

The first slice contains exactly one configuration and therefore performs no cross-configuration comparison or ranking.

Different optics, cameras, binning, filters, focal scales or acquisition conditions must not be normalized implicitly.

## 12. Environmental context boundary

Temperature, SQM, guiding RMS, seeing or weather may be referenced as contextual evidence only if repository-resolvable and session-aligned.

F3 must not claim that environmental correlation establishes equipment causation. The first executable slice does not combine environmental metrics with FWHM.

## 13. FWHM interpretation boundary

FWHM is treated only as a historical descriptive image-quality measurement.

F3 must not infer optical health, focus quality state, collimation state, seeing quality, mount performance, camera performance, threshold breach, anomaly, failure prediction or maintenance recommendation.

Any such interpretation requires separate governed methods and evidence.

## 14. Authority and Safety

All F3 derived records remain historical/read-only with `authority=projection` and `action_authority=NONE`.

F3 introduces no device commands, service restart, focusing action, cooling adjustment, mount action, USB/power/network remediation, scheduler action or current-time Safety inference.

Local physical interlocks remain independent and authoritative.

## 15. Executable artifact set — next implementation step

The next commit set must produce:

1. a machine-readable F3 schema/contract for the descriptive statistic projection;
2. a bounded fixture generated from the locked 19-record population;
3. a deterministic generator/aggregator implementing the four locked method identifiers;
4. a fail-closed validator;
5. negative regression tests covering missing/changed unit, false `arcsec` claim, missing/changed method, zero/incorrect sample count, unresolved source record, population mismatch, unexpected property and forbidden assessment/ranking fields;
6. a dedicated F3 Governance workflow or an explicit F3 extension to the existing governance workflow;
7. Developer Foundation integration;
8. independent ARB and Release Quality before merge.

## 16. Acceptance criteria

F3 is reviewable only when:

- every emitted statistic resolves to `QUATTRO200_TOUPTEK294_BIN1` and session `2026-07-14_2026-07-15`;
- the population is exactly `(LDN 1320, LPRO, LIGHT)` with 19 source-backed records;
- every FWHM source value resolves to repository evidence;
- unit is exactly `NINA_FILENAME_FWHM_SOURCE_UNIT` with uncalibrated/not-proven semantics;
- no physical FWHM unit is invented;
- aggregation methods reproduce the locked deterministic warehouse mathematics;
- sample population/count is explicit and validated;
- Citation/Provenance are non-empty and repository-resolvable;
- no performance assessment, threshold, ranking, anomaly, prediction or recommendation is introduced;
- runtime and Safety Authority remain unchanged;
- exact-head governance/documentation/build gates are green;
- independent ARB approves the executable F3 slice.

## 17. Open items

The source population, unit decision and method semantics are now closed for the first slice.

Remaining implementation questions are limited to artifact structure and CI wiring. They must not reopen the physical-unit question without new repository evidence.

## 18. Decision summary

BKL-039 F3 starts with one bounded, deterministic historical FWHM population: 19 LIGHT exposures from `2026-07-14_2026-07-15`, mapped to `QUATTRO200_TOUPTEK294_BIN1`. The current executable source does not prove a physical FWHM unit, so F3 preserves the source-native numeric semantics explicitly and fail-closed instead of claiming arcseconds or pixels. This establishes a safe basis for the machine-readable implementation.