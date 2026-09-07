# BKL-035 F3 — Deterministic Source Reconciliation and Conflict/Alias Validation

| Field | Value |
|---|---|
| Identifier | BKL-035-F3 |
| Status | In Progress |
| Version | 0.1 |
| Date | 2026-09-07 |
| Parent | BKL-035 — Target Knowledge Base |
| Baseline | `2d30962b1c51325361ffa448064930a79c915023` |
| Predecessor | BKL-035 F2 — CLOSED / ACCEPTED |
| Authority | Projection contract |
| Runtime impact | None |
| Safety impact | None |

## 1. Purpose and scope

F3 governs one additional repository source relation for exact target-identifier reconciliation: `data/analytics/metadata/session-scientific-metadata.csv`. The source is accepted only as `analytics_projection`; it does not replace the Scientific Session Catalog, DSDM/AP-013 scientific authority, or the F2 target projection.

F3 is deliberately bounded to at most five matches and five explicit conflicts. It performs no external catalog lookup, fuzzy name matching, transliteration, probabilistic merge, broad ingestion or autonomous correction.

## 2. Current state

F2 contains two validated projection identities (`LDN 1320`, `M 27`) and four `TARGET_HAS_SESSION` relations. It intentionally did not promote analytics `target_id` values. The metadata CSV contains exact session-scoped target evidence, including `target_name`, `target_id`, `metadata_state` and `session_id`.

## 3. Source contract

The only newly governed F3 source is:

- path: `data/analytics/metadata/session-scientific-metadata.csv`;
- authority: `analytics_projection`;
- record key: `session_id`;
- accepted evidence state: `REGISTERED` only.

`PARTIAL` rows cannot validate an identifier. A missing, blank or inconsistent identifier fails closed. F3 never upgrades analytics metadata into scientific/catalog authority.

## 4. Deterministic reconciliation method

Method `BKL035-F3-EXACT-ID-RECONCILIATION-1` operates only on an existing F2 `target_key` and its accepted canonical name.

For a match to be `validated`:

1. every selected metadata row must be `REGISTERED`;
2. every row must have the exact F2 `canonical_name` as `target_name`;
3. every row must carry the same non-empty `target_id`;
4. `target_id` must satisfy the bounded repository identifier syntax `TGT-[A-Z0-9-]+`;
5. each source reference must bind exactly to `analytics-metadata:<session_id>`;
6. one `target_id` cannot validate two different F2 target keys.

No normalization is performed on `target_id` or `target_name` during reconciliation.

## 5. Bounded fixture

The initial F3 projection validates exactly two matches:

- `dsg-target:ldn-1320` ↔ `TGT-LDN-1320`, backed by registered sessions `2026-07-14_2026-07-15` and `2026-07-15_2026-07-16`;
- `dsg-target:m-27` ↔ `TGT-MESSIER-M27`, backed by registered sessions `2026-08-14_2026-08-15` and `2026-08-15_2026-08-16`.

The M 27 `2026-08-10_2026-08-11` row is `PARTIAL` and is intentionally excluded from validating evidence.

## 6. Alias governance

F3 defines the validation boundary but does not invent aliases. `aliases[]` remains empty in the accepted fixture because the newly governed source does not provide a separate alias field or explicit alias assertion.

A human-readable synonym, compact spelling, Messier expansion, catalog nickname or external-catalog label must not be inferred from `target_id` or `canonical_name`. Any future alias requires an explicit governed source assertion and Citation/Provenance before `TARGET_ALIAS_OF` can be materialized.

An alias claimed for more than one target key is `ALIAS_COLLISION` and must fail closed until reconciled by a later governed increment.

## 7. Conflict model

F3 reserves explicit conflict reasons:

- `TARGET_ID_DISAGREEMENT` — registered evidence for one target key carries incompatible target IDs;
- `CANONICAL_NAME_DISAGREEMENT` — metadata target name differs from the accepted F2 canonical identity;
- `ALIAS_COLLISION` — one explicitly evidenced alias would identify multiple target keys.

The current repository fixture contains no genuine conflict, so `conflicts[]` is empty. Tests inject disagreement in memory; repository data is never falsified merely to exercise conflict handling.

## 8. Fail-closed rules

Validation rejects at minimum:

1. authority escalation;
2. source-path, key, state or authority widening;
3. `PARTIAL` or missing metadata evidence;
4. exact target-ID disagreement;
5. canonical-name disagreement;
6. identifier reuse across target keys;
7. source-reference/session misbinding;
8. arbitrary alias insertion without governed evidence;
9. mutation of the accepted F2 canonical identity;
10. bounded fixture expansion beyond 5 matches / 5 conflicts.

## 9. Migration and rollback

F3 is additive and repository-only. It does not modify source CSV records, the Scientific Session Catalog, F2 target identities, observatory runtime or EAGLE. Rollback is a repository revert of the F3 artifacts and CI entries.

## 10. Security, safety and operations

No secret, external provider, command path, scheduler, actuator, weather authority or Safety Authority is introduced. No persistent graph/vector/RAG or AI inference runtime is introduced. Runtime OAT and observability changes are Not Applicable.

## 11. Traceability

| Requirement | Evidence |
|---|---|
| F2 target identity preserved | `docs/data/target-knowledge-base.json` |
| Additional exact identifier evidence | `data/analytics/metadata/session-scientific-metadata.csv` |
| Machine-readable F3 contract | `schemas/target-identity-reconciliation.schema.json` |
| Bounded reconciliation | `docs/data/target-identity-reconciliation.json` |
| Fail-closed validator | `.github/scripts/verify-target-identity-reconciliation.mjs` |
| Negative regression suite | `.github/scripts/test-target-identity-reconciliation.mjs` |

## 12. Acceptance criteria

F3 is acceptable when the source relation is explicit and bounded; exact target IDs reconcile without authority escalation; unsupported aliases remain rejected; disagreement is fail-closed; fixture facts resolve to `REGISTERED` repository evidence; exact-head CI is green; and independent ARB approves the package before merge.

## 13. Future evolution

A later increment may materialize explicit conflict/alias relations into the Target Knowledge Base only after genuine governed evidence exists and the Citation/Provenance model is extended without weakening BKL-044/F1/F2 invariants. F3 itself remains a read-only reconciliation projection.
