# BKL-035 F4 — Target Knowledge Consumer / Read-Model and Closure Contract

| Field | Value |
|---|---|
| Package | BKL-035 — Target Knowledge Base |
| Increment | F4 — Target Knowledge consumer/read-model projection and closure |
| Status | Proposed |
| Date | 2026-09-07 |
| Baseline | `27bd88d55a1e2d963b02c9c59991ea9ebcb32272` |
| Authority | Projection only |
| Runtime impact | None |
| Safety impact | None |

## 1. Current state

F1 established source/semantic rules, F2 created the bounded target identity/session projection, and F3 reconciled exact governed `target_id` values from the analytics metadata projection with fail-closed Citation/Provenance and conflict semantics.

BKL-044 already established the platform-wide consumer invariant: a read model may project accepted knowledge but may not increase authority, lifecycle certainty or semantic certainty.

## 2. Target state

F4 adds `docs/data/target-knowledge-read-model.json`, a bounded target-centric consumer projection over the accepted F2 and F3 artifacts. It is suitable as a future UI/API input contract but is not itself an API, persistence technology or source of truth.

For each target the read model preserves:

- `target_key`, canonical name, aliases and identity state from F2;
- exact `target_id` and identifier state from F3;
- scientific session relations from F2;
- reconciliation-evidence sessions from F3 as a distinct field;
- both source-authority classes;
- F2/F3 Citation and Provenance identity lineage;
- explicit conflict references.

## 3. Semantic preservation rules

### 3.1 Authority

`authority` is always `projection`. `governed_scientific_projection` and `analytics_projection` remain source-authority labels and cannot be promoted by the consumer.

### 3.2 Scientific relation versus reconciliation evidence

A metadata row used by F3 to reconcile identity is not automatically a `TARGET_HAS_SESSION` scientific relation. Therefore `scientific_sessions` is derived only from accepted F2 relations, while `reconciliation_evidence_sessions` preserves the complete F3 evidence set. This prevents the F4 consumer from manufacturing scientific relationships.

### 3.3 Identity and aliases

Canonical names, aliases and identity state must equal F2. Exact target identifiers must equal F3. No fuzzy matching, transliteration or implicit alias is permitted.

### 3.4 Citation and Provenance

The consumer carries the union of the F2 identity Citation/Provenance refs and F3 reconciliation Citation/Provenance refs for the same `target_key`. References must resolve in their original source contract. F4 cannot substitute or synthesize lineage.

### 3.5 Conflicts

All F3 conflicts for a projected target must remain visible in `conflict_refs`. A consumer must not flatten a conflicted identifier into `validated`. The accepted bounded fixture currently contains no conflicts, so the rule is proved through fail-closed tests rather than invented production data.

## 4. Bounded fixture

F4 projects exactly the two currently reconciled targets, within `max_targets = 5`:

- `dsg-target:ldn-1320` / `TGT-LDN-1320`;
- `dsg-target:m-27` / `TGT-MESSIER-M27`.

The validator also rejects omission of an F2 target that has an accepted F3 reconciliation.

## 5. Executable contract

Normative executable gate:

- `.github/scripts/verify-target-knowledge-read-model.mjs`;
- `.github/scripts/test-target-knowledge-read-model.mjs`;
- Developer Foundation executes both on pull requests and relevant pushes.

Fail-closed tests cover authority promotion, canonical-name drift, invented aliases, analytics-evidence promotion into scientific relations, evidence omission, Citation/Provenance loss or substitution, target omission and conflict flattening.

## 6. Migration

F4 is additive. Existing F2/F3 artifacts remain unchanged and authoritative only within their already accepted projection roles. Future UI/API consumers may migrate to F4 after acceptance; direct consumers of F2/F3 are not removed by this increment.

Rollback is a repository revert of the F4 read-model, validator/tests, workflow integration and this architecture contract.

## 7. Benefits and trade-offs

Benefits: one bounded target-centric consumer shape; explicit separation of scientific facts from reconciliation evidence; preserved lineage; conflict visibility; deterministic CI gate.

Trade-off: consumers must retain multiple semantic fields rather than receive a flattened target object. This is intentional because flattening would lose authority/evidence semantics.

## 8. Risks

- semantic flattening by future UI/API adapters;
- treating reconciliation evidence as a scientific relation;
- lineage omission during future schema evolution;
- widening beyond the bounded fixture without governance.

The executable gate addresses these risks for the repository fixture. Wider ingestion remains separately governed.

## 9. Security and safety

Repository-only, read-only projection. No secrets, external enrichment, provider/inference runtime, persistent graph/vector/RAG choice, EAGLE change, observatory command path, automatic remediation or Safety Authority coupling is introduced. Local physical interlocks remain authoritative and independent.

## 10. Validation and closure gate

F4 may be accepted only after:

1. exact-head Developer Foundation, documentation and Word workflows are green;
2. independent ARB confirms semantic preservation and no authority escalation;
3. Release Quality returns Ready for Merge;
4. merge uses expected-head protection;
5. post-merge workflows on the actual merge SHA are green;
6. BKL-035 closure records the accepted F1-F4 chain.

Until those gates complete, BKL-035 remains `In Progress`.
