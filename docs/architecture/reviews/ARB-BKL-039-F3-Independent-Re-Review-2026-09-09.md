# ARB-BKL-039-F3 — Independent Architecture Re-Review — 2026-09-09

| Field | Value |
|---|---|
| Review ID | `ARB-BKL-039-F3` |
| Capability | BKL-039 — Equipment Performance Registry |
| Increment | F3 — Descriptive Performance Measurement and Aggregation |
| PR | #129 |
| Reviewed HEAD | `1cae682a7f62e1cc2ca0d9f0a76066e47690d93e` |
| Accepted upstream | F2-A merge `96e0e7197d1b729b5ae0b2e0cec402b81baac17f` |
| GitHub ARB review | `5155601715` |
| Decision | **APPROVED** |
| Overall score | **98/100** |

## 1. Executive decision

The Architecture Review Board independently re-reviewed BKL-039 F3 after remediation of the prior findings M01, M02 and m01.

**Decision: APPROVED — 98/100.**

No Blocker, Major or Minor findings remain. F3 is accepted architecturally as a bounded historical/read-only projection of source-backed FWHM measurements and descriptive statistics for one accepted F2-A session/configuration population.

This approval does not authorize health scoring, thresholding, ranking, anomaly interpretation, prediction, maintenance recommendation, remediation, device command authority or current-time Safety inference.

## 2. Exact-head CI evidence

Reviewed exact HEAD: `1cae682a7f62e1cc2ca0d9f0a76066e47690d93e`.

- BKL-039 F3 Governance #19 — SUCCESS;
- Genera manuale Word #1197 — SUCCESS;
- Validate documentation #772 — SUCCESS;
- Developer Foundation #1153 — SUCCESS.

The F3 governance checks are also integrated into Developer Foundation.

## 3. Prior finding disposition

### M01 — Method identifiers and rounding diverged from the governed contract

**RESOLVED.**

Generator, schema, validator and projection now use the governed `BKL039-F3-*` method identifiers.

The descriptive statistics follow the governed four-decimal precision:

- MEAN `7.5995`;
- MINIMUM `6.78`;
- MAXIMUM `9.05`;
- SAMPLE_STDDEV `0.5771`.

The underlying per-measurement FWHM values remain source-native values extracted from repository evidence and are not reinterpreted as calibrated physical units.

### M02 — Fail-closed behavior did not explicitly prove rejection of arbitrary unknown properties

**RESOLVED.**

The validator now uses explicit allowed-field sets for `PERFORMANCE_MEASUREMENT` and `DESCRIPTIVE_PERFORMANCE_STATISTIC` records and rejects unexpected properties.

The negative regression suite explicitly verifies rejection of arbitrary unknown properties on both semantic record types.

### m01 — COMPLETE statistics did not independently prove exact source-population lineage

**RESOLVED.**

The validator derives the exact ordered source population from the declared bounded session and requires each `COMPLETE_FOR_DECLARED_POPULATION` statistic to reference exactly those 19 source rows.

Negative regressions prove rejection when:

- one source row is omitted;
- a source row is duplicated in place of another row.

## 4. Source, identity and population binding

Approved.

F3 remains bound to:

- `configuration_id=QUATTRO200_TOUPTEK294_BIN1`;
- `session_id=2026-07-14_2026-07-15`;
- target `LDN 1320`;
- filter `LPRO`;
- frame type `LIGHT`;
- exactly 19 repository-resolvable source exposures.

The accepted F2-A usage observation remains the upstream configuration/session identity authority.

## 5. Measurement semantics

Approved.

F3 authorizes only:

- `PERFORMANCE_MEASUREMENT`;
- `DESCRIPTIVE_PERFORMANCE_STATISTIC`.

FWHM is treated only as a historical descriptive image-quality quantity. No field or method claims that the value represents equipment health, focus quality state, collimation state, seeing quality, mount health, camera health or threshold compliance.

## 6. Unit and calibration boundary

Approved.

The projection retains:

- `unit=NINA_FILENAME_FWHM_SOURCE_UNIT`;
- `unit_semantics=SOURCE_NATIVE_UNCALIBRATED`;
- `angular_calibration_state=NOT_PROVEN`.

No implicit conversion to arcseconds or pixels is introduced. The negative suite rejects angular-unit or calibration-state overclaims.

## 7. Method, determinism and aggregation

Approved.

The bounded method set is versioned and deterministic:

- source extraction — `BKL039-F3-FWHM-NINA-FILENAME-EXTRACT-V1`;
- mean — `BKL039-F3-FWHM-MEAN-V1`;
- minimum — `BKL039-F3-FWHM-MIN-V1`;
- maximum — `BKL039-F3-FWHM-MAX-V1`;
- sample standard deviation — `BKL039-F3-FWHM-SAMPLE-STDDEV-V1`.

The statistic population is explicit, `sample_count=19`, and COMPLETE coverage requires exact source-row lineage.

## 8. Fail-closed validation

Approved.

The validator and negative regression suite cover, among other cases:

- unexpected properties;
- unit/calibration escalation;
- authority escalation;
- changed source values;
- incorrect sample count;
- incorrect statistic value;
- changed/unversioned method;
- incomplete coverage claim;
- incomplete or duplicated COMPLETE lineage;
- unresolved provenance;
- duplicate record identifiers;
- extra records;
- changed bounded session.

## 9. Citation, Provenance and quality

Approved.

Measurement and statistic records require non-empty source, Citation and Provenance references that resolve to repository evidence. COMPLETE quality remains an evidence-coverage statement only and is not an equipment-health state.

## 10. Runtime, operations and Safety

Approved.

F3 is repository/analytics-only, historical and read-only. It introduces no collector, API, service, scheduler, EAGLE live dependency, device command, focusing action, cooling action, mount action, USB/power/network remediation or present-time Safety inference.

`authority=projection` and `action_authority=NONE` remain mandatory.

Local physical interlocks remain independent and authoritative.

## 11. Migration and rollback

Approved.

No runtime or persistent-data migration is required. Existing source evidence is unchanged. Rollback is repository revert of the F3 schema, projection, generator, validator, tests, workflow integration and review artifacts.

## 12. Findings

### Blocker

None.

### Major

None.

### Minor

None.

### Observation O01 — Future comparability and interpretation boundary

Future extensions must preserve explicit unit, method, population and environmental comparability boundaries.

Cross-configuration ranking, health scoring, thresholding, anomaly interpretation, failure prediction or maintenance recommendation remain outside this approved increment and require separate governance.

## 13. Decision

**APPROVED — 98/100.**

F3 may proceed to Release Quality after this ARB evidence artifact is committed and the new exact-head CI cycle is green.

## 14. Re-review criteria

ARB re-review is required if subsequent F3 changes alter:

- source/session/configuration identity binding;
- FWHM unit or calibration semantics;
- method identifiers or calculation semantics;
- declared source population or coverage rules;
- Citation/Provenance requirements;
- fail-closed schema/validator behavior;
- allowed semantic record types;
- performance assessment/ranking/threshold/anomaly/prediction/recommendation semantics;
- runtime or command authority;
- Safety Authority or physical-interlock boundaries.
