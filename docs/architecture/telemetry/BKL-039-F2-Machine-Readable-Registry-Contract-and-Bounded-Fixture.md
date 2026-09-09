# BKL-039 F2 — Machine-Readable Registry Contract and Bounded Fixture

| Field | Value |
|---|---|
| Identifier | `BKL-039-F2` |
| Capability | BKL-039 — Equipment Performance Registry |
| Status | In Progress — F2-A |
| Version | 0.2 |
| Date | 2026-09-09 |
| Accepted upstream | BKL-039 F1 merge `a5f2b6bffd2590fc6c0958fe266515ff84cc5c20` |
| Authority | Projection only |
| Runtime impact | None |
| Safety impact | None — local physical Safety Authority unchanged |

## 1. Purpose

Materialize the first bounded machine-readable Equipment Performance Registry projection from repository-resolvable equipment/configuration and session evidence. F2-A proves source binding and semantic integrity only; it does not create a scoring engine, performance rating, health state, anomaly policy, predictive-maintenance policy or remediation path.

## 2. F1 ARB observation O01 disposition

F1 ARB O01 distinguished the DSDM logical identity model from identities actually materialized in current session records. Repository discovery on the accepted F1 baseline found an existing operational configuration namespace and explicit session binding:

- `data/analytics/configurations/equipment-registry.csv` contains `configuration_id` values `QUATTRO200_TOUPTEK294_BIN1` and `C8_QHY695A_BIN1`, with equipment/configuration attributes and ACTIVE state;
- `data/analytics/metadata/session-scientific-metadata.csv` binds REGISTERED sessions to those same `configuration_id` values and preserves a `source_reference` to repository-resolvable N.I.N.A./governed evidence;
- `data/analytics/history/sessions.csv` and the analytics history contract already carry `session_id`, `configuration_id`, telescope, camera and related historical fields.

F2-A therefore does **not** synthesize a new `instrumentConfigurationId`. It uses the existing `configuration_id` namespace as the source operational identity and records its semantic role explicitly. DSDM remains the logical semantic authority for versioned instrument configuration; F2-A does not claim that the operational `configuration_id` string is already a separately materialized DSDM entity instance.

Any future canonical DSDM identity migration must be separately governed and must preserve the existing operational identifier as provenance/alias rather than silently rewriting historical records.

## 3. Bounded source set

F2-A uses only repository-resolvable accepted source records:

1. `data/analytics/configurations/equipment-registry.csv` — equipment/configuration source registry;
2. `data/analytics/metadata/session-scientific-metadata.csv` — session-to-configuration binding and source reference;
3. the source record referenced by each selected metadata row, used as provenance evidence rather than reinterpreted by F2-A.

The initial fixture selects exactly two REGISTERED sessions, one for each currently ACTIVE operational configuration:

- `2026-07-14_2026-07-15` -> `QUATTRO200_TOUPTEK294_BIN1`;
- `2026-08-14_2026-08-15` -> `C8_QHY695A_BIN1`.

The PARTIAL session `2026-08-10_2026-08-11` is deliberately excluded because its instrument metadata is unresolved by design.

## 4. Machine-readable record types

F2-A materializes two bounded semantic record types.

### 4.1 `EQUIPMENT_IDENTITY`

Projection of an existing operational configuration row. Required semantics:

- `configuration_id` exactly equals the source registry key;
- source registry path;
- configuration label and source-backed equipment attributes;
- source status;
- `identity_namespace=DSG_ANALYTICS_CONFIGURATION_ID`;
- `dsdm_materialization_state=NOT_SEPARATELY_PROVEN`;
- Citation/Provenance;
- `authority=projection`;
- `action_authority=NONE`.

The two identity-distinction fields above are mandatory machine-readable fields in schema and fixture and must fail closed if missing or changed. They prevent the operational `configuration_id` from being silently promoted to a separately proven DSDM entity.

### 4.2 `EQUIPMENT_USAGE_OBSERVATION`

Historical source-backed binding between one REGISTERED session and one existing configuration. Required semantics:

- exact `session_id`;
- exact `configuration_id`;
- metadata state `REGISTERED`;
- telescope/camera/binning copied from accepted metadata;
- source metadata path;
- source evidence reference exactly preserved;
- Citation/Provenance;
- `authority=projection`;
- `action_authority=NONE`.

F2-A does not materialize `PERFORMANCE_MEASUREMENT`, `DESCRIPTIVE_PERFORMANCE_STATISTIC`, `PERFORMANCE_ASSESSMENT` or `RECOMMENDATION`. Those require later bounded evidence/method contracts.

## 5. Identity and binding invariants

The validator must fail closed when:

- a usage observation references a `configuration_id` absent from the equipment registry;
- the configuration is not present in the selected source registry row;
- session metadata is not `REGISTERED`;
- session/configuration/telescope/camera/binning differs from the source metadata row;
- a source evidence reference is missing;
- an identity is silently rewritten into a synthetic DSDM identifier;
- `identity_namespace` or `dsdm_materialization_state` is missing or changed;
- Citation or Provenance is empty/unresolvable;
- authority differs from `projection`;
- action authority differs from `NONE`;
- any property outside the published bounded schema is introduced.

No inference from display label alone is permitted.

## 6. Quality and unknown handling

F2-A preserves source metadata state. A PARTIAL or unresolved session cannot be promoted to REGISTERED and cannot receive an inferred configuration merely because adjacent sessions use the same hardware.

Unknown data remains explicit. Empty or missing values are not converted to zero, healthy, nominal, default equipment or a guessed configuration.

## 7. Performance semantics boundary

The existence or frequency of a configuration in session history is usage evidence, not a performance score. F2-A must not infer:

- GOOD/BAD performance;
- HEALTHY/DEGRADED state;
- reliability percentage;
- comparative ranking;
- threshold breach;
- maintenance need;
- root cause;
- predicted failure.

F3 may introduce deterministic descriptive measurements/statistics only after their source fields, units, method version, sample population and quality/coverage rules are explicitly governed.

## 8. Environmental context boundary

No environmental correlation is materialized in F2-A. SQM/weather context remains eligible for a later increment only where session-aligned repository evidence and compatible timestamp/quality semantics are proven. Environmental evidence is not equipment causation and never Safety Authority.

## 9. Safety and operational boundary

F2-A is repository-only and historical/read-only. It introduces no collector, scheduler, API, service, EAGLE filesystem dependency, device command, process restart, maintenance action or remediation authority.

Local physical interlocks remain independent and authoritative. Historical equipment usage cannot be used to infer present-time Safety state.

## 10. Deliverables and validation plan

The bounded F2-A implementation includes:

- strict machine-readable schema for the two authorized record types;
- bounded fixture containing the two source equipment identities and two source-backed usage observations;
- positive validator resolving source registry rows, session bindings, source evidence references, Citation/Provenance and authority fields;
- schema-derived structural enforcement for required, allowed, constant, enum, string, integer and bounded-array semantics used by this F2-A schema;
- negative regression suite covering unresolved configuration, PARTIAL-session promotion, source mismatch, synthetic identity substitution, missing lineage, identity-distinction mutation, arbitrary unknown property and authority mutation;
- dedicated BKL-039 F2 Governance plus Developer Foundation execution of the same positive and negative checks.

Independent ARB approval remains mandatory before F3.

## 11. Migration and rollback

There is no runtime or persistent-data migration. F2-A adds a projection over existing repository evidence and does not modify source CSV records.

Rollback is repository revert of the F2 projection artifacts. Existing analytics source records remain unchanged.

## 12. Acceptance criteria

F2-A is review-ready when:

- every fixture `configuration_id` resolves to the existing equipment registry;
- every usage observation resolves to a REGISTERED session metadata row using the same configuration;
- source evidence references remain repository-resolvable;
- no synthetic DSDM identity is created;
- `identity_namespace=DSG_ANALYTICS_CONFIGURATION_ID` and `dsdm_materialization_state=NOT_SEPARATELY_PROVEN` are machine-readable and fail closed;
- the operational namespace and DSDM logical semantic distinction is explicit;
- PARTIAL/unresolved sessions fail closed;
- Citation/Provenance and authority boundaries fail closed;
- unknown properties outside the bounded schema fail closed;
- no performance rating/threshold/health/prediction/remediation semantics are introduced;
- no EAGLE/runtime/Safety Authority change occurs;
- positive and negative validation is integrated into dedicated CI and Developer Foundation;
- exact-head CI is green;
- independent ARB approves before F3 begins.

## 13. Next slice

After F2-A acceptance, F3 may select a minimal set of genuinely source-backed quantitative historical fields and define deterministic descriptive aggregation. It must not treat usage count, completion percentage, guiding RMS, FWHM, SQM or any other metric as an equipment health score without separately governed comparability and interpretation policy.
