# ARB-BKL-039-F4-A — Independent Architecture Re-Review — 2026-09-09

| Field | Value |
|---|---|
| Review ID | `ARB-BKL-039-F4-A` |
| Capability | BKL-039 — Equipment Performance Registry |
| Increment | F4-A — Machine-Readable Read-Only Consumer |
| PR | #130 |
| Reviewed HEAD | `468b16de3d2e420315b4eecf095788e42b57918c` |
| Accepted upstream | F3 merge `ce2482aa6b2da62296ebdc221f73f39c1acd3aa2` |
| GitHub ARB review | `5156625629` |
| Decision | **APPROVED** |
| Overall score | **98/100** |

## 1. Executive decision

The Architecture Review Board independently re-reviewed BKL-039 F4-A after remediation of M01 from review `5156438732`.

**Decision: APPROVED — 98/100.**

No Blocker, Major or Minor findings remain. F4-A is accepted architecturally as a deterministic repository/static read-only consumer projection of the accepted F3 evidence.

This approval does not authorize equipment health scoring, thresholds, ranking, anomaly diagnosis, prediction, maintenance recommendation, remediation, device command authority or current-time Safety inference.

## 2. Exact-head CI evidence

Reviewed exact HEAD: `468b16de3d2e420315b4eecf095788e42b57918c`.

- BKL-039 F4 Governance #3 — SUCCESS;
- Developer Foundation #1162 — SUCCESS;
- Validate documentation #781 — SUCCESS;
- Genera manuale Word #1206 — SUCCESS.

Developer Foundation independently executes the F4 deterministic generator, validator and negative regression suite.

## 3. Prior finding disposition

### M01 — Developer Foundation did not enforce F4

**RESOLVED.**

`.github/workflows/developer-foundation.yml` now:

- includes `docs/data/equipment-performance-registry-f4-read-model.json` in push and pull-request path filters;
- verifies the deterministic F4 generated read model;
- runs the F4 read-only consumer validator;
- runs the F4 fail-closed negative regression suite.

Developer Foundation #1162 executed those F4 steps successfully on the reviewed exact HEAD.

## 4. Source, identity and population binding

Approved.

F4-A remains bound to the accepted F3 population:

- `configuration_id=QUATTRO200_TOUPTEK294_BIN1`;
- `session_id=2026-07-14_2026-07-15`;
- target `LDN 1320`;
- filter `LPRO`;
- frame type `LIGHT`;
- exactly 19 measurements in deterministic source order.

The consumer copies accepted F3 values and statistics; it does not recalculate or reinterpret them.

## 5. Unit and calibration boundary

Approved.

The read model retains:

- `unit=NINA_FILENAME_FWHM_SOURCE_UNIT`;
- `unit_semantics=SOURCE_NATIVE_UNCALIBRATED`;
- `angular_calibration_state=NOT_PROVEN`.

No arcsecond, pixel, seeing, focus-quality or equipment-health interpretation is introduced.

## 6. Fail-closed consumer model

Approved.

The schema/validator/test package enforces strict root and view fields, deterministic population and values, exact method identifiers, source lineage, Citation/Provenance and non-authoritative semantics.

Negative regressions reject authority escalation, action authority, unknown properties, population/count mismatch, changed measurement/statistic values, unit/calibration escalation, method mutation, missing or duplicate lineage, missing Citation/Provenance and prohibited health/recommendation/Safety-authority fields.

## 7. Citation, Provenance and limitations

Approved.

The consumer retains repository-resolvable source references, Citation and Provenance and explicitly exposes limitations. Coverage is descriptive evidence coverage only and is not a health or Safety state.

## 8. Runtime, security and Safety

Approved.

F4-A is repository/static and read-only. It introduces no writable API, network listener, scheduler, EAGLE/PC command path, device action, remediation or present-time Safety inference.

`authority=projection` and `action_authority=NONE` remain mandatory. Local physical interlocks remain independent and authoritative.

## 9. Migration and rollback

Approved.

No runtime or persistent-data migration is required. Rollback is repository revert of the F4-A schema, generator, materialized read model, validator, tests, workflow integration and review artifacts.

## 10. Findings

### Blocker

None.

### Major

None.

### Minor

None.

### Observation O01 — Preserve structural semantic rejection

Forbidden assessment/remediation semantics must continue to be rejected by structural field names/schema. Do not replace this with substring scanning of legitimate limitation values.

## 11. Decision

**APPROVED — 98/100.**

F4-A may proceed to Release Quality after this ARB evidence artifact is committed and the new exact-head CI cycle is green.

## 12. Re-review criteria

ARB re-review is required if subsequent changes alter source/session/configuration binding, FWHM unit/calibration semantics, F3 value fidelity, method identifiers, Citation/Provenance, fail-closed behavior, assessment/ranking/threshold/recommendation semantics, runtime/command authority, or Safety Authority / physical-interlock boundaries.
