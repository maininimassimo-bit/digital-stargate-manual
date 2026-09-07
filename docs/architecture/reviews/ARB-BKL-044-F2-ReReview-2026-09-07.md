# ARB-BKL-044-F2 — Independent Architecture Re-Review

**Decision:** Approved  
**Date:** 2026-09-07  
**Scope:** BKL-044 F2 — Machine-readable schema and fail-closed validation  
**Reviewed branch:** `architecture/bkl-044-f2-machine-readable-validation`  
**Reviewed head:** `9d6121d82758a244f5ebd448d7ddb1951991ee54`  
**PR:** #100

## 1. Executive decision

The Architecture Review Board approves BKL-044 F2 after remediation. The previous Major findings M-01 and M-02 and Minor finding m-01 are disposed on the reviewed head.

Citation and Provenance are now first-class versioned machine-readable records. Validated Evidence requires a resolvable governed Citation/locator. Validated claim/inference/recommendation records require resolvable evidence, citation and provenance references. The executable validator now enforces the same source-authority vocabulary as the schema.

No runtime, persistent graph/vector/RAG, inference provider, command-path or Safety Authority capability is introduced.

## 2. Reviewed evidence

- `docs/architecture/knowledge/BKL-044-Knowledge-Graph-AI-Evidence-Contract.md` v0.3;
- `schemas/knowledge-ai-evidence-contract.schema.json`;
- `docs/data/knowledge-ai-evidence-contract.json`;
- `.github/scripts/verify-knowledge-ai-evidence-contract.mjs`;
- `.github/scripts/test-knowledge-ai-evidence-contract.mjs`;
- `.github/workflows/developer-foundation.yml`;
- prior `ARB-BKL-044-F2-Independent-Review-2026-09-07.md`;
- PR #100 exact-head workflow evidence.

## 3. Finding disposition

| Finding | Disposition | Evidence |
|---|---|---|
| M-01 Citation/Provenance not first-class | Closed | Root contract now contains versioned `citations` and `provenance_records`; validated derived items resolve both. |
| M-02 Evidence locatability not fail-closed | Closed | Validated `evidence` requires `citation_refs`; referenced Citation includes governed locator and source authority. |
| m-01 source-authority validator parity | Closed | Executable validator uses the same governed authority vocabulary and negative test rejects unsupported authority. |

## 4. Architecture scorecard

| Dimension | Score | Assessment |
|---|---:|---|
| Repository-truth alignment | 100 | Review targets exact PR head and current F2 package. |
| F1 semantic fidelity | 99 | Observation/Evidence/Claim/Inference/Recommendation plus Citation, Provenance, Confidence, Conflict and Unknown remain distinguishable. |
| Fail-closed behavior | 100 | Materially incomplete validated evidence/derived/AI records are rejected. |
| Confidence governance | 99 | Stable versioned confidence contract resolution remains enforced. |
| Citation/evidence traceability | 99 | Governed Citation locator and reference resolution are explicit. |
| Provenance integrity | 99 | Versioned provenance resolves input, output and Citation references. |
| Contract integrity | 99 | Schema and executable semantic validator are aligned for the reviewed acceptance surface. |
| Technology neutrality | 100 | No graph/vector/RAG/provider technology selected. |
| Safety/security | 100 | No command path, remediation or Safety Authority coupling. |
| Testability/CI | 100 | Exact-head Developer Foundation and documentation/Word workflows are green. |

**Overall:** 99/100.

## 5. Validation evidence

### Executed on reviewed head

- Developer Foundation #979 — SUCCESS;
- `Verify Knowledge / AI evidence contract` — SUCCESS;
- `Test Knowledge / AI evidence fail-closed rules` — SUCCESS;
- MkDocs strict within Developer Foundation — SUCCESS;
- Validate documentation #588 — SUCCESS;
- Genera manuale Word #1013 — SUCCESS.

### Not Applicable

- EAGLE runtime OAT;
- observatory hardware validation;
- production runtime deployment validation.

F2 is repository contract/CI work only.

## 6. Safety and security disposition

Local physical Safety Authority remains independent. F2 does not authorize dome, mount, camera, power, network, cleanup, remediation or weather-safety commands. Citation metadata does not grant access to protected sources and no credentials are embedded in the contract.

## 7. Observations

- O-01 — F3 must seed only bounded governed examples and prove reconciliation against authoritative source material; F2 approval does not authorize broad ingestion.
- O-02 — F4 remains responsible for preserving semantic type, lifecycle, authority, citation and provenance in read models and UI/API consumers.
- O-03 — Any persistent graph/vector/RAG or inference-runtime selection remains outside this approval and requires separate governance.

## 8. Re-review criteria

ARB re-review is required if F2 scope changes after this reviewed head in a way that materially changes semantic classes, authority, Citation/Provenance identity, validation rules, storage technology, runtime behavior or Safety boundaries.

## 9. Decision

**APPROVED.** BKL-044 F2 may proceed to Release Quality review and merge readiness assessment on the exact reviewed head `9d6121d82758a244f5ebd448d7ddb1951991ee54` or a descendant containing only review/governance artifacts that do not alter the implementation contract.