# Digital StarGate — Current Technical Baseline — 2026-09-07

| Campo | Valore |
|---|---|
| Stato | Current |
| Repository authority | GitHub `main` |
| Baseline verificata | `8d9f47922de1536b424cdd29ca00fc61c5c9fa49` |
| Current governed package | BKL-044 Knowledge Graph / AI Evidence Contract |
| BKL-044 state | In Progress — F1/F2/F3 accepted; F4 next |
| BKL-015 | Done / Accepted |
| TD-008 | Resolved |
| Runtime EAGLE | unchanged |
| Safety Authority | local / outside Knowledge Graph and AI scope |

## 1. Current package

BKL-044 è il package corrente. F3 è integrato tramite PR #102 e merge `8d9f47922de1536b424cdd29ca00fc61c5c9fa49`.

Governance F3:

- `docs/architecture/reviews/ARB-BKL-044-F3-ReReview-2026-09-07.md` — APPROVED;
- `docs/architecture/reviews/RQ-BKL-044-F3-Release-Quality-Review-2026-09-07.md` — READY;
- `docs/project/BKL-044-F3-CLOSURE-2026-09-07.md` — closure record.

Post-merge: Developer Foundation #992, documentation #601, Word #1026 e Pages #695 — SUCCESS.

## 2. Machine-readable evidence baseline

F2 remains the accepted evidence contract: `schemas/knowledge-ai-evidence-contract.schema.json` and `docs/data/knowledge-ai-evidence-contract.json`, with deterministic validator/tests in Developer Foundation.

Semantic classes remain distinct: Observation, Evidence, Claim, Inference, Recommendation, with Confidence, Citation, Provenance, Conflict and Unknown governed explicitly.

## 3. F3 reconciliation baseline

F3 adds `docs/data/knowledge-ai-seed-reconciliation.json`, `.github/scripts/verify-knowledge-ai-seed-reconciliation.mjs` and `.github/scripts/test-knowledge-ai-seed-reconciliation.mjs`.

Accepted properties:

- bounded seed/source set: 3/3, governed maximum 5/5;
- exact approved-baseline anchoring;
- repository-authority source reconciliation;
- fail-closed source-fragment drift detection;
- seed-to-Citation repository locator identity;
- item-to-Citation identity;
- derived Provenance/Citation/output identity;
- negative tests for drift, unresolved references, semantic flattening, authority downgrade, bounds, source/Citation mismatch, Provenance/Citation mismatch and baseline mismatch.

F3 approval is not broad-ingestion authorization.

## 4. BKL-015 foundation

BKL-015 remains Done/Accepted. The repository Knowledge Graph remains a rebuildable projection and does not become authoritative merely by containing an item or relation.

## 5. Next governed increment — F4

**BKL-044 F4 — Consumer / Read-Model Contract.**

F4 must define machine-readable consumer/read-model behavior preserving:

- semantic type;
- lifecycle state;
- source authority;
- Citation identity/version/locator;
- Provenance identity and applicable chain;
- Confidence contract identity/value where present;
- explicit unknown/conflict/incomplete states.

Consumers must not silently flatten Evidence into Claim, Claim into fact, Inference into Observation, or AI output into repository authority.

## 6. Runtime, security and safety invariants

No BKL-044 F1-F3 change affects EAGLE runtime or local safety. F4 is expected to remain repository-only unless separately governed. No command endpoint, remediation, graph/vector persistence, RAG runtime, AI provider, inference engine or Safety Authority coupling is authorized by the current baseline.

## 7. Scientific/runtime invariants

Existing scientific transport, AP-013C cleanup exclusions, EAGLE Health read-only rules and session automation branch discipline remain unchanged. Runtime EAGLE must operate from `main`, not a feature/governance worktree.