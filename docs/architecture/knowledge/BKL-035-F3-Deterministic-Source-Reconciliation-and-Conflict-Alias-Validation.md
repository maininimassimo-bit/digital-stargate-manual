# BKL-035 F3 — Deterministic Source Reconciliation and Conflict/Alias Validation

| Field | Value |
|---|---|
| Identifier | BKL-035-F3 |
| Status | In Progress |
| Version | 0.3 |
| Date | 2026-09-07 |
| Parent | BKL-035 — Target Knowledge Base |
| Baseline | `2d30962b1c51325361ffa448064930a79c915023` |
| Predecessor | BKL-035 F2 — CLOSED / ACCEPTED |
| Authority | Projection contract |
| Runtime impact | None |
| Safety impact | None |

## 1. Purpose and scope

F3 governs one additional repository source relation for exact target-identifier reconciliation: `data/analytics/metadata/session-scientific-metadata.csv`. The source is accepted only as `analytics_projection`; it does not replace the Scientific Session Catalog, DSDM/AP-013 scientific authority, or the F2 target projection. F3 is bounded to five matches/five explicit conflicts and performs no external lookup, fuzzy matching, transliteration, probabilistic merge, broad ingestion or autonomous correction.

## 2. Source and eligibility contract

The source contract is exact: path `data/analytics/metadata/session-scientific-metadata.csv`, authority `analytics_projection`, record key `session_id`, accepted state `REGISTERED`, eligibility rule `ALL_REGISTERED_ROWS_FOR_SESSION_CATALOG_EXACT_CANONICAL_TARGET`.

For every existing F2 target being reconciled, all `REGISTERED` metadata rows whose `target_name` exactly equals the accepted F2 `canonical_name` are eligible evidence. The match must enumerate the complete eligible set; cherry-picking a consistent subset fails closed. `PARTIAL` rows are non-validating and cannot strengthen a match.

## 3. Deterministic reconciliation method

`BKL035-F3-EXACT-ID-RECONCILIATION-1` requires: exact F2 canonical name; complete eligible `REGISTERED` evidence; one identical non-empty `target_id` across that complete set; identifier syntax `TGT-[A-Z0-9-]+`; exact source refs `analytics-metadata:<session_id>`; and no reuse of one target ID by different F2 target keys. No name/identifier normalization or guessing occurs.

## 4. Citation and Provenance

Every validated mapping carries versioned Citation and Provenance compatible with the BKL-044/F1/F2 evidence invariants. Each Citation locator binds exactly to the metadata CSV, `session_id`, and source row value. Provenance method is `BKL035-F3-EXACT-ID-RECONCILIATION-1`; inputs equal the complete eligible source-ref set; output is exactly `target-id-map:<target_key>=<target_id>`; Provenance Citation refs equal the match Citation set. Existing-but-wrong Citation or Provenance binding fails closed.

A materialized conflict is subject to the same semantic evidence discipline: `session_ids` deterministically imply source refs `analytics-metadata:<session_id>`; Citation locators must resolve exactly to that ordered session set; exactly one Provenance record must resolve; its `input_refs` must equal the conflict evidence set; its `output_ref` must be exactly `conflict:<conflict_id>`; and its Citation refs must equal the conflict Citation set. Referential existence without semantic binding is insufficient and fails closed.

## 5. Bounded fixture

The projection contains two matches and no manufactured conflict:

- `dsg-target:ldn-1320` ↔ `TGT-LDN-1320`, complete eligible sessions `2026-07-14_2026-07-15`, `2026-07-15_2026-07-16`, `2026-07-16_2026-07-17`;
- `dsg-target:m-27` ↔ `TGT-MESSIER-M27`, complete eligible sessions `2026-08-14_2026-08-15`, `2026-08-15_2026-08-16`.

M 27 session `2026-08-10_2026-08-11` is `PARTIAL` and deliberately non-validating.

## 6. Alias and conflict governance

Aliases remain empty because no governed alias assertion exists. Nicknames, compact spellings, Messier expansions or external labels are not inferred. Future aliases require explicit governed evidence plus Citation/Provenance. Conflict reasons remain `TARGET_ID_DISAGREEMENT`, `CANONICAL_NAME_DISAGREEMENT`, and `ALIAS_COLLISION`. The current repository contains no genuine conflict, so `conflicts[]` remains empty; tests inject synthetic conflict evidence in memory only and never falsify repository data.

## 7. Executable structural and semantic contract

The published JSON Schema and normative semantic validator describe the same closed structure. CI enforces root/source/bounds/match/Citation/Provenance/conflict required fields, closed property sets, bounds, uniqueness, identifier patterns, candidate-ID cardinality and governance constants. It additionally proves match and conflict evidence binding, so an existing Citation or Provenance record belonging to another fact cannot satisfy a new mapping or conflict.

## 8. Fail-closed rules

Validation rejects authority escalation; source-contract widening; omitted eligible REGISTERED evidence; PARTIAL evidence used for validation; target-ID or canonical-name disagreement; target-ID reuse; source/Citation/Provenance misbinding; unsupported alias insertion; F2 identity mutation; malformed conflict records; conflict Citation/session misbinding; conflict Provenance input/output/Citation misbinding; and fixture expansion beyond 5/5.

## 9. Migration, rollback, security and safety

F3 is additive and repository-only. It modifies neither source CSV nor Scientific Session Catalog nor F2 identities. Rollback is repository revert. No secret, provider, scheduler, actuator, observatory command path, persistent graph/vector/RAG, AI inference authority, EAGLE change or Safety Authority coupling is introduced. Runtime OAT/observability are Not Applicable.

## 10. ARB remediation record

Independent ARB on exact head `7acfcaf961369aa3d4c16d18d757c95b87f20c58` returned **REWORK REQUIRED — 88/100** (PR #110 governance comment `5574302017`). M-01, M-02 and M-03 were remediated by complete evidence enumeration, machine-readable Citation/Provenance and executable structural validation.

ARB re-review on exact head `c8f3a1b1c13d1b59c8a33b05ddaaf4e925df0169` returned **REWORK REQUIRED — 97/100** (PR #110 governance comment `5574835069`). Its sole Minor R-01 required conflict Citation/Provenance to be semantically bound rather than merely referentially valid. Version 0.3 closes R-01 by executable session-to-Citation binding, exact conflict Provenance inputs, `conflict:<conflict_id>` output binding, exact Provenance Citation binding, and positive/negative synthetic conflict tests.

A new exact-head CI run and final independent ARB re-review remain required before Release Quality and merge.

## 11. Traceability

| Requirement | Evidence |
|---|---|
| F2 target identity preserved | `docs/data/target-knowledge-base.json` |
| Additional exact identifier evidence | `data/analytics/metadata/session-scientific-metadata.csv` |
| Machine-readable F3 contract | `schemas/target-identity-reconciliation.schema.json` |
| Bounded reconciliation + Citation/Provenance | `docs/data/target-identity-reconciliation.json` |
| Complete-evidence and conflict-binding validator | `.github/scripts/verify-target-identity-reconciliation.mjs` |
| Negative/positive regression suite | `.github/scripts/test-target-identity-reconciliation.mjs` |

## 12. Acceptance criteria

F3 is acceptable only when complete eligible evidence is executable; exact target IDs reconcile without authority escalation; match and conflict Citation/Provenance bindings are exact; aliases remain unsupported without evidence; structural and semantic drift fail closed; exact-head CI is green; and independent ARB approves before Release Quality and merge.
