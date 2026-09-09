# ARB-BKL-039-F2-A — Independent Architecture Re-Review — 2026-09-09

| Field | Value |
|---|---|
| Review ID | `ARB-BKL-039-F2-A` |
| Capability | BKL-039 — Equipment Performance Registry |
| Increment | F2-A — Machine-Readable Registry Contract and Bounded Fixture |
| PR | #128 |
| Reviewed HEAD | `88085f5cf5abd035811ea781230dc9ad291b7071` |
| Accepted upstream | BKL-039 F1 merge `a5f2b6bffd2590fc6c0958fe266515ff84cc5c20` |
| Prior ARB decision | REWORK REQUIRED — 88/100 on `0300900bd56bafe9edcc9ada0131991feee1d621` |
| Decision | **APPROVED** |
| Overall score | **99/100** |

## 1. Executive decision

The Architecture Review Board independently re-reviewed BKL-039 F2-A after remediation of the prior findings M01, M02 and m01.

**Decision: APPROVED — 99/100.**

No Blocker, Major or Minor findings remain. F2-A is accepted architecturally as a bounded repository projection that proves equipment/configuration identity binding and REGISTERED session usage lineage without introducing performance assessment, threshold, prediction, remediation or Safety Authority.

F3 remains blocked until F2-A completes Release Quality, exact-head CI, merge and post-merge verification.

## 2. Exact-head CI evidence

Reviewed exact HEAD: `88085f5cf5abd035811ea781230dc9ad291b7071`.

- BKL-039 F2 Governance #13 — SUCCESS;
- Genera manuale Word #1177 — SUCCESS;
- Validate documentation #752 — SUCCESS;
- Developer Foundation #1133 — SUCCESS.

Developer Foundation executes both the positive bounded-registry validator and the F2 fail-closed regression suite in addition to the dedicated BKL-039 F2 Governance workflow.

## 3. Prior finding disposition

### M01 — Required identity distinction was prose-only

**RESOLVED.**

The strict schema now requires, for every `EQUIPMENT_IDENTITY` record:

- `identity_namespace=DSG_ANALYTICS_CONFIGURATION_ID`;
- `dsdm_materialization_state=NOT_SEPARATELY_PROVEN`.

Both fields are materialized in the fixture, checked explicitly by the validator and covered by negative tests for missing/mutated values.

This preserves the distinction between the existing operational `configuration_id` namespace and a separately proven DSDM entity materialization. No synthetic `instrumentConfigurationId` is introduced.

### M02 — Strict schema was not completely enforced by CI

**RESOLVED for the bounded F2-A schema.**

The validator derives and enforces the structural constraints used by the published schema, including required/allowed properties, constants, enumerations, string/integer constraints and bounded arrays. `additionalProperties:false` is therefore fail-closed for the F2-A objects actually materialized.

The negative suite now includes an arbitrary unknown-property regression in addition to the explicit performance-rating rejection. The same positive and negative checks run in both the dedicated F2 Governance workflow and Developer Foundation.

### m01 — Contract/fixture selected-session mismatch

**RESOLVED.**

The architecture contract and fixture consistently select:

- `2026-07-14_2026-07-15` → `QUATTRO200_TOUPTEK294_BIN1`;
- `2026-08-14_2026-08-15` → `C8_QHY695A_BIN1`.

No source evidence is rewritten.

## 4. Identity and source authority

Approved.

F2-A reuses the accepted operational `configuration_id` values from `data/analytics/configurations/equipment-registry.csv` and binds usage observations to `REGISTERED` session metadata in `data/analytics/metadata/session-scientific-metadata.csv`.

The projection explicitly records that DSDM separate materialization is not proven. Display labels are not treated as stable identifiers, and unknown/PARTIAL source state is not promoted to REGISTERED.

## 5. Machine-readable semantic boundary

Approved.

F2-A authorizes only:

- `EQUIPMENT_IDENTITY`;
- `EQUIPMENT_USAGE_OBSERVATION`.

It does not materialize:

- `PERFORMANCE_MEASUREMENT`;
- `DESCRIPTIVE_PERFORMANCE_STATISTIC`;
- `PERFORMANCE_ASSESSMENT`;
- `RECOMMENDATION`.

Usage frequency or session presence is therefore not a performance score or equipment-health statement.

## 6. Citation, Provenance and quality

Approved.

Every bounded record requires non-empty, repository-resolvable source/Citation/Provenance references. Usage observations resolve against REGISTERED session metadata and source evidence. A PARTIAL session remains excluded and the validator fails closed on unresolved or mutated source binding.

Projection authority remains `projection` and `action_authority=NONE`.

## 7. Runtime, operations and Safety

Approved.

F2-A is repository-only and historical/read-only. It introduces no collector, API, service, scheduler, EAGLE filesystem dependency, device command, maintenance action, remediation path or present-time Safety inference.

Local physical interlocks remain independent and authoritative.

## 8. Migration and rollback

Approved.

No runtime or persistent-data migration is required. Existing source CSV evidence is unchanged. Rollback is repository revert of the F2-A projection/schema/validation artifacts.

## 9. Findings

### Blocker

None.

### Major

None.

### Minor

None.

### Observation O01 — F3 measurement semantics

F3 may introduce only genuinely source-backed quantitative measurements/statistics with explicit unit, method/version, sample population and quality/coverage semantics.

Usage count, completion percentage, guiding RMS, FWHM, SQM or any other available metric must not be promoted to equipment health, ranking, threshold breach, failure prediction or maintenance recommendation without separate governance defining comparability and interpretation policy.

## 10. Decision

**APPROVED — 99/100.**

F2-A may proceed to Release Quality after this ARB artifact is committed and the new exact-head CI is green.

F3 remains blocked until F2-A is merged and applicable post-merge workflows succeed on the real merge SHA.

## 11. Re-review criteria

ARB re-review is required if subsequent F2-A changes alter:

- equipment/configuration identity semantics;
- source/session binding rules;
- DSDM materialization claims;
- machine-readable record types;
- Citation/Provenance requirements;
- schema enforcement/fail-closed behavior;
- performance assessment/ranking/threshold semantics;
- runtime or command authority;
- Safety Authority or physical-interlock boundaries.
