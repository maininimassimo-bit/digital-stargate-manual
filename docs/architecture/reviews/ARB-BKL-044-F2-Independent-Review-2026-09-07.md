# ARB-BKL-044-F2 — Independent Architecture Review

**Decision:** Rework Required  
**Date:** 2026-09-07  
**Scope:** BKL-044 F2 — Machine-readable schema and fail-closed validation  
**Reviewed branch:** `architecture/bkl-044-f2-machine-readable-validation`  
**Reviewed head:** `e38342adb023e9bd3080aac6b669af8ac7d341ee`  
**PR:** #100

## 1. Executive decision

BKL-044 F2 is directionally correct and exact-head CI is green, but the current machine-readable contract does not yet fully encode the F1 semantic surface required for F2. The review therefore requires rework before merge.

The implementation successfully addresses the two explicit F1 carry-over conditions for evidence-less AI promotion and versioned confidence identity. However, Citation and Provenance are still represented only as opaque references rather than governed machine-readable records, and Evidence locatability is not enforced end-to-end.

No Safety, runtime, storage-technology, graph/vector/RAG or command-path issue was identified.

## 2. Reviewed evidence

- `docs/architecture/knowledge/BKL-044-Knowledge-Graph-AI-Evidence-Contract.md` v0.2
- `schemas/knowledge-ai-evidence-contract.schema.json`
- `docs/data/knowledge-ai-evidence-contract.json`
- `.github/scripts/verify-knowledge-ai-evidence-contract.mjs`
- `.github/scripts/test-knowledge-ai-evidence-contract.mjs`
- `.github/workflows/developer-foundation.yml`
- BKL-044 F1 ARB/RQ conditions
- PR #100 exact-head workflows

## 3. Architecture scorecard

| Dimension | Score | Assessment |
|---|---:|---|
| Repository-truth alignment | 100 | Branch and PR are based on the verified `main` baseline. |
| F1 semantic fidelity | 86 | Core item types and lifecycle are present, but Citation/Provenance are not first-class machine-readable records. |
| Fail-closed behavior | 96 | Validated derived/AI items fail closed when evidence/citation requirements are absent. |
| Confidence governance | 99 | Stable versioned confidence-contract resolution is implemented. |
| Evidence traceability | 82 | Evidence references exist, but evidence locatability and citation resolution are not fully governed. |
| Contract integrity | 88 | JSON Schema and validator exist, but several semantic constraints are only partially cross-validated. |
| Technology neutrality | 100 | No graph/vector/RAG/provider choice. |
| Safety/security | 100 | No runtime command or Safety Authority coupling. |
| Migration/rollback | 100 | Additive repository-only change with repository revert rollback. |
| Testability/CI | 99 | Exact-head CI is green and positive/negative fail-closed tests execute. |

**Overall:** 95/100.

## 4. Findings

### Blocker

None.

### Major

**M-01 — Citation and Provenance are not first-class machine-readable F2 contracts.**  
F1 defines Citation and Provenance as canonical governed concepts, and the F2 target is to encode the accepted semantic contract machine-readably. The current schema exposes `citation_refs` and evidence references but no governed Citation record and no governed Provenance record/chain. A consumer cannot inspect locator, source authority, producer/transformation lineage or resolve the provenance chain from the contract alone.

**Required disposition:** introduce versioned machine-readable Citation and Provenance record definitions, stable IDs, reference resolution and deterministic validation. Validated derived items must resolve their citation/provenance references.

**M-02 — Evidence locatability is not fail-closed.**  
F1 requires Evidence to be locatable and attributable. The generic `evidence` item currently has no mandatory citation/source locator or equivalent resolvable reference. A validated Evidence item can therefore pass without a governed locator.

**Required disposition:** require validated Evidence to resolve at least one governed Citation (or equivalent governed locator) and validate that reference deterministically.

### Minor

**m-01 — Source authority parity should be enforced by the executable validator.**  
The JSON Schema enumerates allowed `source_authority` values, while the executable validator currently checks only for a non-empty string. This creates avoidable schema/validator drift.

**Required disposition:** enforce the same authority vocabulary in the executable validator and add a negative test.

### Observations

- O-01 — F1 M-01/RQ-01 is correctly addressed for validated derived and AI-derived items.
- O-02 — F1 M-02/RQ-02 is correctly addressed through `<contract-id>@<version>` confidence resolution.
- O-03 — `incomplete` AI inference without evidence remains representable, which is the required fail-closed behavior rather than an error.
- O-04 — Runtime OAT is Not Applicable because F2 is repository contract/CI work only.

## 5. Validation status

### Executed

- Developer Foundation #973 — SUCCESS;
- Validate documentation #582 — SUCCESS;
- Word #1007 — SUCCESS;
- `Verify Knowledge / AI evidence contract` step — SUCCESS;
- `Test Knowledge / AI evidence fail-closed rules` step — SUCCESS;
- MkDocs strict step inside Developer Foundation — SUCCESS.

### Not applicable

- EAGLE runtime OAT;
- observatory hardware validation;
- production deployment validation.

## 6. Safety/security disposition

No command path, remediation, device access, Safety Authority coupling, secret embedding or persistent graph/vector technology is introduced. Local physical safety remains independent.

## 7. Re-review criteria

ARB re-review is required after:

1. first-class Citation contract is added;
2. first-class Provenance contract/chain is added;
3. validated Evidence requires a resolvable citation/locator;
4. source-authority vocabulary parity is enforced in the executable validator;
5. positive/negative tests cover the new fail-closed rules;
6. exact-head CI is green on the remediated head.

## 8. Decision

**REWORK REQUIRED.** PR #100 must not merge at reviewed head `e38342adb023e9bd3080aac6b669af8ac7d341ee`. The remediation remains within the already approved F2 scope and requires no new ADR, runtime technology or Safety decision.
