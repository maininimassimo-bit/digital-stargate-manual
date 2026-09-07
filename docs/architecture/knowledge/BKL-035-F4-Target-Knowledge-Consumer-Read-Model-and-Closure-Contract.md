# BKL-035 F4 — Target Knowledge Consumer / Read-Model and Closure Contract

| Field | Value |
|---|---|
| Package | BKL-035 — Target Knowledge Base |
| Increment | F4 — Target Knowledge consumer/read-model projection and closure |
| Status | Proposed |
| Version | 0.2 |
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
- exact `target_id` from F3 and a consumer identifier state derived with explicit conflict precedence;
- scientific session relations from F2 together with their relation-level Citation/Provenance;
- reconciliation-evidence sessions from F3 as a distinct field;
- both source-authority classes;
- F2/F3 identity/reconciliation Citation and Provenance lineage;
- explicit complete conflict references.

## 3. Semantic preservation rules

### 3.1 Authority

`authority` is always `projection`. `governed_scientific_projection` and `analytics_projection` remain source-authority labels and cannot be promoted by the consumer.

### 3.2 Scientific relation versus reconciliation evidence

A metadata row used by F3 to reconcile identity is not automatically a `TARGET_HAS_SESSION` scientific relation. Therefore `scientific_sessions` is derived only from accepted F2 relations, while `reconciliation_evidence_sessions` preserves the complete F3 evidence set. This prevents the F4 consumer from manufacturing scientific relationships.

Every projected scientific session also carries exact F2 relation lineage through `scientific_session_citation_refs` and `scientific_session_provenance_refs`. The executable validator derives those sets from the accepted `TARGET_HAS_SESSION` records; missing or substituted relation evidence fails closed.

### 3.3 Identity and aliases

Canonical names, aliases and identity state must equal F2. The exact target identifier value must equal the accepted F3 match. No fuzzy matching, transliteration or implicit alias is permitted.

### 3.4 Citation and Provenance

Identity/reconciliation lineage is preserved separately from relation lineage. `citation_refs` and `provenance_refs` preserve the F2 target-identity plus F3 reconciliation evidence. `scientific_session_citation_refs` and `scientific_session_provenance_refs` preserve the exact F2 relation evidence for the projected scientific sessions. References must resolve in their original source contract. F4 cannot substitute or synthesize lineage.

### 3.5 Conflicts and identifier-state precedence

All F3 conflicts for a projected target must remain visible in `conflict_refs`.

Identifier-state precedence is deterministic:

1. if F3 exposes one or more conflicts for the target, F4 `target_id_state` is `conflicted` and `conflict_refs` is the complete set of those conflict IDs;
2. otherwise `target_id_state` equals the accepted F3 match `identity_state` (`validated` in the bounded accepted fixture).

The exact `target_id` value remains the accepted F3 match value; `conflicted` explicitly means that consumers must not treat that value as uncontested. A conflict therefore reduces semantic certainty rather than deleting source evidence or manufacturing a replacement identifier.

The accepted repository fixture currently contains no conflicts. Positive and negative synthetic tests prove that a conflict-preserving consumer projection can validate, while omitted conflict refs or a flattened `validated` state fail closed.

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

Fail-closed tests cover authority promotion, canonical-name drift, invented aliases, analytics-evidence promotion into scientific relations, scientific relation Citation/Provenance loss or substitution, reconciliation-evidence omission, identity/reconciliation lineage loss or substitution, target omission, conflict-ref omission and conflict flattening. A positive synthetic conflict test proves representability of the governed conflicted state.

## 6. ARB remediation

Independent ARB on exact head `856034949faf1e56f873a7403f617335cf3e4ae2` returned **REWORK REQUIRED — 92/100** (comment `5575291582`).

Remediation v0.2 closes:

- **M-01:** F4 now preserves and validates relation-level Citation/Provenance for every projected F2 `TARGET_HAS_SESSION` fact;
- **M-02:** conflict precedence is executable and non-contradictory; a correctly conflict-preserving synthetic F4 projection validates, while omission/flattening fails closed.

Final acceptance remains subject to new exact-head CI, independent ARB re-review and Release Quality.

## 7. Migration

F4 is additive. Existing F2/F3 artifacts remain unchanged and authoritative only within their already accepted projection roles. Future UI/API consumers may migrate to F4 after acceptance; direct consumers of F2/F3 are not removed by this increment.

Rollback is a repository revert of the F4 read-model, validator/tests, workflow integration and this architecture contract.

## 8. Benefits and trade-offs

Benefits: one bounded target-centric consumer shape; explicit separation of scientific facts from reconciliation evidence; relation and identity lineage preservation; conflict visibility; deterministic CI gate.

Trade-off: consumers must retain multiple semantic and lineage fields rather than receive a flattened target object. This is intentional because flattening would lose authority/evidence semantics.

## 9. Risks

- semantic flattening by future UI/API adapters;
- treating reconciliation evidence as a scientific relation;
- relation or identity lineage omission during future schema evolution;
- conflict-state flattening;
- widening beyond the bounded fixture without governance.

The executable gate addresses these risks for the repository fixture. Wider ingestion remains separately governed.

## 10. Security and safety

Repository-only, read-only projection. No secrets, external enrichment, provider/inference runtime, persistent graph/vector/RAG choice, EAGLE change, observatory command path, automatic remediation or Safety Authority coupling is introduced. Local physical interlocks remain authoritative and independent.

## 11. Validation and closure gate

F4 may be accepted only after:

1. exact-head Developer Foundation, documentation and Word workflows are green;
2. independent ARB confirms semantic preservation and no authority escalation;
3. Release Quality returns Ready for Merge;
4. merge uses expected-head protection;
5. post-merge workflows on the actual merge SHA are green;
6. BKL-035 closure records the accepted F1-F4 chain.

Until those gates complete, BKL-035 remains `In Progress`.
