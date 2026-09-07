# ARB-BKL-044-F1 — Independent Architecture Review

**Decision:** Approved with Conditions  
**Date:** 2026-09-07  
**Scope:** BKL-044 F1 — Knowledge Graph / AI Evidence Semantic Contract  
**Reviewed branch:** `architecture/bkl-044-knowledge-ai-evidence-contract`  
**Reviewed head:** `056bb03a79466fa69074ccd1d3cd750dc312f0cd`

## 1. Executive decision

The Architecture Review Board approves BKL-044 F1 with conditions. No Blocker or Major findings were identified.

The proposal is consistent with the accepted BKL-015 machine-readable foundation and with `SKL-VIS-001`. It establishes a clear semantic distinction between observations, evidence, claims, inference, recommendations, confidence, citations, provenance, conflicts and unknowns while preserving repository/source authority and keeping AI advisory/read-only.

The package correctly avoids premature selection of graph database, vector database, embedding, RAG or AI-provider technology and introduces no observatory runtime or Safety Authority behavior.

## 2. Reviewed evidence

- `docs/architecture/knowledge/BKL-044-Knowledge-Graph-AI-Evidence-Contract.md`
- `docs/architecture/scientific-knowledge-layer-vision.md`
- accepted BKL-015 F1/F2/F3 contracts and closure state
- `docs/project/BACKLOG.md`
- roadmap state with BKL-044 as current package
- branch ancestry from accepted `main` merge `714f32a7aff55d4c6ea05fa5bcf66e72c29b4abd`

## 3. Architecture scorecard

| Dimension | Score | Assessment |
|---|---:|---|
| Repository-truth alignment | 99 | Extends the accepted BKL-015 foundation and current backlog/roadmap state. |
| Semantic clarity | 98 | Observation/evidence/claim/inference/recommendation boundaries are explicit. |
| Authority integrity | 100 | Derived projections and AI output remain non-authoritative. |
| Scientific provenance | 98 | Minimum provenance envelope and citation requirements are explicit. |
| AI governance | 98 | AI-derived output is distinguishable, advisory and uncertainty-aware. |
| Confidence semantics | 97 | Contextual confidence contract avoids unqualified numeric certainty. |
| Technology neutrality | 100 | Storage, vector and model/provider choices remain intentionally undecided. |
| Safety/security | 100 | No command path, remediation or Safety Authority coupling. |
| Migration/rollback | 100 | Documentation-only additive increment with trivial revert. |
| Future extensibility | 99 | F2-F4 sequence cleanly separates schema, seed projection and consumers. |

**Overall:** 99/100.

## 4. Findings

### Blocker

None.

### Major

None.

### Minor

**M-01 — Evidence-less AI output must remain explicitly incomplete.**  
Section 6 requires every claim, inference or recommendation to carry evidence/citation references, while section 9 says AI should preserve references “where available”. F2 must encode a fail-closed lifecycle rule so an AI-derived item lacking mandatory evidence/citations cannot be represented as complete/validated knowledge.

**Required disposition:** machine-readable F2 schema/validator MUST classify missing mandatory provenance as `incomplete`, `unknown` or equivalent non-authoritative state and reject promotion to a completed/validated claim.

**M-02 — Confidence contracts require versioned identity.**  
F1 correctly makes confidence contextual, but F2 must ensure the scale/method/calibration semantics are referenced by a stable/versioned contract identifier rather than free text alone.

**Required disposition:** define a versioned machine-readable confidence-contract reference in F2.

### Observations

**O-01 — Conflict semantics are correctly explicit.** Source disagreements remain represented rather than auto-resolved.

**O-02 — BKL-044 does not reopen TD-008.** This package adds scientific/AI semantics beyond the repository traceability debt already resolved by BKL-015.

**O-03 — No ADR is required in F1.** No irreversible technology or runtime decision is taken. A future storage/inference technology selection must trigger a separate ADR/review.

## 5. Safety and security disposition

The package is read-only with respect to observatory operations. It does not authorize dome, mount, camera, power, network, cleanup, remediation or weather-safety commands. Local physical interlocks remain independent.

Security boundaries are appropriate for F1: graph presence does not imply universal source authorization, and credentials/secrets are explicitly excluded from knowledge projections.

## 6. Migration and rollback

F1 is contract/documentation-only. Rollback is a repository revert. No scientific source data, configuration or runtime state is mutated.

## 7. Validation status

### Executed

- repository truth inspection against BKL-015 closure state;
- consistency review against `SKL-VIS-001`;
- backlog/roadmap dependency review;
- branch ancestry verification against accepted `main`.

### Not yet executed

- exact-head documentation CI;
- MkDocs strict build on the final reviewed branch head;
- post-merge validation.

These validations remain merge conditions and are not treated as passed by this review.

## 8. Conditions for continuation

1. F2 must fail closed on missing mandatory evidence/provenance.
2. F2 must provide stable/versioned confidence-contract identity.
3. Exact-head documentation/quality gates must be green before F1 merge.
4. Any persistent graph/vector/RAG/model-provider selection requires separate architecture decision and review.
5. AI remains advisory/read-only and outside Safety Authority unless a future separately governed capability explicitly changes that boundary.

## 9. Re-review criteria

ARB re-review is required if BKL-044 introduces persistent graph/vector storage, inference runtime, autonomous source mutation, operational command authority, Safety Authority coupling, or materially changes the semantic classes/authority model defined in F1.

## 10. Decision

**APPROVED WITH CONDITIONS.** BKL-044 F1 may proceed to Release Quality review and PR validation. Merge remains conditional on exact-head CI and the conditions above being carried into F2.