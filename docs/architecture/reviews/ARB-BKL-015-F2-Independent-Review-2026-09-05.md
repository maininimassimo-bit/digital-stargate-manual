# ARB-BKL-015-F2 — Independent Architecture Review

**Decision:** Approved with Conditions  
**Date:** 2026-09-05  
**Scope:** BKL-015 F2 — Knowledge Graph Coverage & Reconciliation  
**Reviewed branch:** `architecture/bkl-015-f2-coverage-reconciliation`  
**Reviewed head:** `98a725f60aeee1587b6abbcb8dd8f9358d5f730a`

## 1. Executive decision

The Architecture Review Board approves BKL-015 F2 with conditions. No Blocker or Major findings were identified.

F2 correctly extends the accepted F1 contract from structural validity to measurable repository coverage. The implementation derives canonical Architecture Package and ADR inventories from repository truth, requires 100% identity coverage for those two families, and preserves the Knowledge Graph as a non-authoritative projection.

The increment remains repository-only and does not introduce graph-database lock-in, vector search, RAG, AI inference, EAGLE runtime changes, Safety Authority coupling or remediation behavior.

## 2. Reviewed evidence

- `docs/architecture/knowledge/BKL-015-F2-Coverage-Reconciliation.md`
- `docs/data/knowledge-graph.json`
- `.github/scripts/verify-knowledge-graph-coverage.mjs`
- `.github/workflows/developer-foundation.yml`
- BKL-015 F1 contract and accepted review evidence
- `.github/roadmap/roadmap-source.json`
- repository ADR files under `docs/architecture`
- `docs/project/TECHNICAL_DEBT.md` — TD-008
- CI on head `98a725f60aeee1587b6abbcb8dd8f9358d5f730a`

## 3. Architecture scorecard

| Dimension | Score | Assessment |
|---|---:|---|
| Repository-truth alignment | 98 | AP and ADR inventories are derived from governed repository sources rather than duplicated lists. |
| Contract continuity with F1 | 97 | F1 entity/relation semantics and authority boundaries are preserved. |
| Traceability quality | 96 | AP/ADR identities and F1 review evidence are represented explicitly. |
| Validation design | 98 | CI fails on missing IDs, wrong types and integrity regressions. |
| Technology neutrality | 100 | No persistent graph technology is selected. |
| Safety/security | 100 | No runtime control, credential handling, remediation or Safety Authority change. |
| Migration/rollback | 98 | Repository-only additive change with straightforward revert. |
| Operational impact | 99 | No observatory runtime impact; only CI validation cost is introduced. |
| Documentation quality | 95 | Purpose, coverage policy, TD-008 boundary and acceptance criteria are explicit. |
| Future extensibility | 96 | BKL-044 and later component/evidence coverage remain cleanly separated. |

**Overall:** 98/100.

## 4. Findings

### Blocker

None.

### Major

None.

### Minor

**M-01 — TD-008 remains open.**  
F2 proves complete AP/ADR identity coverage but does not yet prove repository-wide component, evidence and material-relation coverage.

**Required disposition:** keep TD-008 open and define a later reviewed coverage increment before marking the debt resolved.

### Observations

**O-01 — Identity coverage is not relation completeness.** The 100% AP/ADR result must not be presented as full semantic traceability.

**O-02 — Generic graph storage remains deferred.** This is appropriate; JSON projection is sufficient for this increment.

**O-03 — BKL-044 separation is preserved.** Scientific claim, confidence and AI evidence semantics remain out of scope.

## 5. Safety and security disposition

No observatory runtime component, EAGLE Scheduled Task, N.I.N.A. flow, Cloud Run service, device command path or Safety Authority is modified. The package is safe to merge from an observatory-operations perspective.

## 6. Migration and rollback

F2 is additive and repository-only. Rollback is the revert of the projection, validator, workflow gate and package documentation. No operational or scientific source data is mutated.

## 7. Validation evidence

On reviewed head `98a725f60aeee1587b6abbcb8dd8f9358d5f730a`:

- Developer Foundation #956 — PASS;
- Validate documentation #565 — PASS;
- Genera manuale Word #989 — PASS;
- `Verify repository knowledge graph coverage` step — PASS;
- MkDocs strict step inside Developer Foundation — PASS.

The branch is currently behind `main` only by the isolated session-workflow hotfix PR #95 and its merge. Those commits do not modify F2 artifacts. Re-running CI after this review evidence is committed remains required before merge.

## 8. Conditions for continuation

1. Keep TD-008 open after F2.
2. Do not equate identity coverage with relation completeness.
3. Re-run all applicable CI gates after ARB/RQ evidence is committed.
4. Re-review is required before persistent graph infrastructure, generated inference or new authority semantics are introduced.

## 9. Re-review criteria

A new ARB review is required if BKL-015 later introduces:

- persistent graph/document/vector storage;
- automatically generated semantic relations promoted to repository fact;
- authority-boundary changes;
- component/evidence closure thresholds for TD-008;
- runtime integration beyond repository projections.

## 10. Decision

**APPROVED WITH CONDITIONS.** BKL-015 F2 may proceed to Release Quality review and merge once the final branch quality gates are green with the review evidence included.