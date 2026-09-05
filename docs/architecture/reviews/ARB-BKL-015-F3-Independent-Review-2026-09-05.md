# ARB-BKL-015-F3 — Independent Architecture Review

**Decision:** Approved with Conditions  
**Date:** 2026-09-05  
**Scope:** BKL-015 F3 — Component, Evidence and Material Relation Coverage  
**Reviewed branch:** `architecture/bkl-015-f3-component-evidence-relations`  
**Reviewed head:** `417040c303195a120a8c56b28b0d31732cca8f6c`

## 1. Executive decision

The Architecture Review Board approves BKL-015 F3 with conditions. No Blocker or Major findings were identified.

F3 correctly advances the accepted F1/F2 Knowledge Graph foundation from identity coverage to material traceability. The Architecture Artifact Register remains authoritative; the graph is a derived projection. The implementation derives the governed inventory from that register and fails closed when a registered artifact or review lacks the expected entity type, package endpoint or typed material relation.

## 2. Reviewed evidence

- `docs/architecture/knowledge/BKL-015-F3-Component-Evidence-Material-Relation-Coverage.md`
- `docs/architecture/traceability-register.md`, section 4
- `docs/data/knowledge-graph.json`
- `.github/scripts/verify-knowledge-graph-material-relations.mjs`
- `.github/workflows/developer-foundation.yml`
- accepted BKL-015 F1/F2 architecture and review evidence
- CI on head `417040c303195a120a8c56b28b0d31732cca8f6c`

## 3. Architecture scorecard

| Dimension | Score | Assessment |
|---|---:|---|
| Repository-truth alignment | 99 | Inventory is derived from the existing governed traceability register. |
| Contract continuity | 98 | F1 authority/vocabulary and F2 coverage principles remain intact. |
| Material traceability | 98 | Registered components/reviews require explicit package relations. |
| Validation design | 99 | Fail-closed validation covers missing identity, type, endpoint and relation. |
| Technology neutrality | 100 | No graph/vector/RAG materialization decision is introduced. |
| Safety/security | 100 | No runtime, command, remediation, credential or Safety Authority change. |
| Migration/rollback | 99 | Repository-only additive change; rollback is a source revert. |
| Operability | 98 | CI produces deterministic reconciliation failure rather than silent drift. |
| Documentation quality | 97 | Scope, authority, thresholds and TD-008 boundary are explicit. |
| Future extensibility | 98 | BKL-044 remains cleanly separated from repository traceability semantics. |

**Overall:** 99/100.

## 4. Findings

### Blocker

None.

### Major

None.

### Minor

**M-01 — TD-008 closure still requires a dedicated disposition.**  
F3 proves 100% coverage for the currently governed Architecture Artifact Register, but the technical-debt closure must explicitly confirm that no material traceability class required by TD-008 remains outside the combined F1/F2/F3 inventories.

**Required disposition:** perform a dedicated closure review after F3 merge; do not mark TD-008 Resolved within this review artifact.

### Observations

**O-01 — Register quality is now a direct graph-quality dependency.** This is intentional and preferable to duplicate inventories, but future changes to the register format must preserve deterministic extraction or version the contract.

**O-02 — Identity coverage and material relation coverage are correctly distinguished.** Both are required at 100% for F3.

**O-03 — BKL-044 remains out of scope.** No scientific claim, AI confidence, inferred relation or RAG semantics are introduced.

## 5. Safety and security disposition

No EAGLE runtime, N.I.N.A., Cloud Run, telemetry transport, device command path, cleanup authorization, local interlock or Safety Authority component is changed. There is no operational observatory risk introduced by this package.

## 6. Migration and rollback

The change is additive and repository-only. Rollback consists of reverting the graph projection additions, validator, CI step and package documentation. Authoritative architecture sources are not mutated by graph execution.

## 7. Validation evidence

On reviewed head `417040c303195a120a8c56b28b0d31732cca8f6c`:

- Developer Foundation #960 — PASS;
- Validate documentation #569 — PASS;
- Genera manuale Word #994 — PASS;
- F1 graph integrity gate — exercised within Developer Foundation;
- F2 AP/ADR coverage gate — exercised within Developer Foundation;
- F3 material-relation gate — exercised within Developer Foundation;
- MkDocs strict — exercised within Developer Foundation.

No runtime validation is claimed because F3 changes no runtime behavior.

## 8. Conditions for continuation

1. Keep TD-008 open until a dedicated combined F1/F2/F3 closure review is completed.
2. Treat the Architecture Artifact Register as authority; do not silently infer missing relations.
3. Re-run all applicable CI gates after ARB/RQ evidence is committed.
4. Re-review before changing register semantics, relation authority, persistent graph infrastructure or generated inference behavior.

## 9. Re-review criteria

A new ARB review is required if subsequent work introduces persistent graph/vector storage, auto-generated relations promoted to fact, new authority classes, AI evidence semantics, runtime integrations, or changes to the F3 governed inventory contract.

## 10. Decision

**APPROVED WITH CONDITIONS.** F3 may proceed to Release Quality review and merge after the exact-head quality gates remain green with review evidence included.