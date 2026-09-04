# ARB-BKL-015-F1 — Independent Architecture Review

**Decision:** Approved with Conditions  
**Date:** 2026-09-04  
**Scope:** BKL-015 F1 — Knowledge Graph Machine-Readable Foundation  
**Reviewed branch:** `architecture/bkl-015-knowledge-graph-foundation`  
**Reviewed head:** `6dea3a48107ed6d761dcebb63e9df662d657c615`

## 1. Executive decision

The Architecture Review Board approves BKL-015 F1 with conditions. No Blocker or Major findings were identified. The increment is repository-centric, additive, reversible at projection level and consistent with the approved Scientific Knowledge Layer vision.

The proposal correctly separates repository traceability from future scientific/AI evidence semantics and does not introduce runtime control, Safety Authority coupling, EAGLE changes, graph-database lock-in or vector/RAG technology.

## 2. Reviewed evidence

- `docs/architecture/knowledge/BKL-015-Knowledge-Graph-Machine-Readable-Foundation.md`
- `docs/architecture/contracts/knowledge-graph.schema.json`
- `docs/data/knowledge-graph.json`
- `.github/scripts/verify-knowledge-graph.mjs`
- `.github/workflows/developer-foundation.yml`
- `docs/project/BACKLOG.md`
- `docs/architecture/scientific-knowledge-layer-vision.md`
- `docs/project/TECHNICAL_DEBT.md` — TD-008
- CI on head `6dea3a48107ed6d761dcebb63e9df662d657c615`

## 3. Architecture scorecard

| Dimension | Score | Assessment |
|---|---:|---|
| Repository-truth alignment | 96 | Directly addresses BKL-015/TD-008 and preserves authority boundaries. |
| Domain/layer integrity | 95 | Graph is explicitly a projection; authoritative systems remain authoritative. |
| Contract clarity | 94 | Closed F1 entity/relation vocabularies, stable IDs and source locators are explicit. |
| Safety/security | 100 | No runtime control, credentials, remediation or Safety Authority changes. |
| Operability/observability | 92 | CI exposes duplicate IDs, dangling endpoints, unsupported vocabulary and bad locators. |
| Migration/rollback | 97 | Additive projection; removal does not mutate source artifacts. |
| Traceability | 95 | BKL-015, TD-008, CAP-40, AP-015 and BKL-044 boundaries are explicit. |
| Technology neutrality | 100 | Graph/vector/RAG materialization deliberately deferred. |
| Documentation quality | 94 | Scope, rules, risks, acceptance and future evolution are clear. |
| Validation evidence | 96 | Developer Foundation, documentation and Word workflows are green. |

**Overall:** 96/100.

## 4. Findings

### Blocker

None.

### Major

None.

### Minor

**M-01 — Coverage closure threshold not yet defined.**  
F1 proves the contract and seed projection but does not establish the minimum AP/ADR/component/evidence coverage required to resolve TD-008.

**Required disposition:** define a measurable coverage criterion before TD-008 is marked Resolved or BKL-015 is closed.

### Observations

**O-01 — `relates_to` remains a generic fallback.** Its use is acceptable in F1 but should decrease as richer relations become supported by evidence.

**O-02 — Materialization remains intentionally open.** This is architecturally correct; no graph DB selection should be inferred from the JSON projection.

**O-03 — BKL-044 boundary is correctly preserved.** Scientific claims, AI recommendation provenance and confidence semantics remain out of F1.

## 5. Safety and security disposition

BKL-015 F1 is read-only with respect to observatory runtime systems. It introduces no command path and contains no operational secrets. Local physical interlocks and Safety Authority remain independent.

## 6. Migration and rollback

The increment is additive. If the projection or validator is removed, authoritative repository artifacts are unchanged. There is no data migration or operational rollback requirement.

## 7. Validation evidence

On head `6dea3a48107ed6d761dcebb63e9df662d657c615`:

- Developer Foundation #951 — PASS;
- Validate documentation #560 — PASS;
- Genera manuale Word #984 — PASS.

The review does not claim runtime validation because F1 does not modify runtime behavior.

## 8. Conditions for continuation

1. Define and validate a measurable coverage threshold before BKL-015 closure / TD-008 resolution.
2. Keep BKL-044 scientific/AI evidence semantics in a separate reviewed increment.
3. Do not select graph/vector storage technology implicitly through this projection.
4. Preserve repository authority and fail validation rather than inventing missing edges.

## 9. Re-review criteria

A new ARB review is required if a later BKL-015 increment:

- introduces a persistent graph service or external database;
- changes authority boundaries;
- introduces generated inference as repository fact;
- adds runtime integrations beyond read-only projections;
- materially changes entity/relation vocabularies.

## 10. Decision

**APPROVED WITH CONDITIONS.** BKL-015 F1 may merge after current branch quality gates remain green with this review included.