# ARB-BKL-044-F3 — Independent Architecture Review

**Decision:** Rework Required  
**Date:** 2026-09-07  
**Scope:** BKL-044 F3 — Governed Seed Projection & Reconciliation  
**Reviewed branch:** `architecture/bkl-044-f3-governed-seed-reconciliation`  
**Reviewed head:** `772f3c9b8f38096d7c32f06a04d6f51e4adfd5b3`  
**PR:** #102

## 1. Executive decision

BKL-044 F3 demonstrates a sound bounded approach: three governed seeds, three repository-authoritative sources, explicit `max_sources=5` / `max_seeds=5`, deterministic source-fragment drift checks, semantic-type/lifecycle/source-authority parity checks, F2-compatible Citation/Provenance/Confidence records and successful exact-head CI.

The package is not yet approvable because the reconciliation manifest and validator do not prove that the authoritative source used for a seed is the same source represented by the knowledge item's governed Citation/Provenance chain. In addition, `baseline_commit` is syntax-validated only and therefore does not currently anchor the reconciliation to the declared baseline snapshot.

No runtime, EAGLE, persistent graph/vector/RAG, command-path or Safety Authority concern is introduced.

## 2. Reviewed evidence

- `docs/data/knowledge-ai-seed-reconciliation.json`;
- `docs/data/knowledge-ai-evidence-contract.json`;
- `.github/scripts/verify-knowledge-ai-seed-reconciliation.mjs`;
- `.github/scripts/test-knowledge-ai-seed-reconciliation.mjs`;
- `.github/workflows/developer-foundation.yml`;
- `docs/architecture/knowledge/BKL-044-Knowledge-Graph-AI-Evidence-Contract.md` v0.5;
- PR #102 exact-head workflow evidence.

## 3. Findings

### M-01 — Major — Seed source is not bound to governed Citation/Provenance

The validator resolves `seed.source_ref`, reads that repository file and verifies required fragments. Separately, it resolves `seed.knowledge_item_ref` and compares semantic type, lifecycle and source authority. It does **not** verify that the selected manifest source path equals a Citation locator referenced by the knowledge item or by its required evidence/provenance chain.

Therefore a seed can theoretically reconcile against authoritative file A while its knowledge item is governed by Citation B, and still pass if semantic metadata matches.

**Required remediation:** introduce deterministic linkage from each seed to the governed Citation identity or derive the expected Citation(s) from the item. Verify that at least one resolved Citation has `source_authority=repository_authority` and `locator.kind=repository_path` with `locator.value` exactly equal to the resolved manifest source path. For validated derived items, also verify the referenced Provenance chain resolves and points back to the governed Citation/source used by the seed.

Add negative tests that intentionally swap a seed to another valid authoritative source and prove the validator fails on Citation/source mismatch; add a provenance/citation mismatch test for the validated Claim seed.

### M-02 — Major — Declared baseline commit is not an effective reconciliation anchor

`baseline_commit` is only checked against a 40-character hexadecimal regular expression. Source files are read from the current checkout. The validator does not establish that the declared baseline commit is the expected starting baseline or that the authoritative source material being reconciled is anchored to that baseline.

This weakens the evidence behind the phrase "reconciled against baseline `40f7854...`" because any syntactically valid SHA could be substituted without affecting validation.

**Required remediation:** make baseline anchoring deterministic without adding network/runtime dependencies. At minimum, bind the manifest to a governed expected baseline identity supplied by repository state/contract and fail if the manifest baseline differs. Prefer a repository-local baseline contract or an explicit validator argument/environment value derived by CI from the PR base/approved baseline; alternatively persist bounded source digests for the baseline source files and verify them before reconciliation. The implementation must remain reproducible in CI and must not depend on mutable external services.

Add a negative test proving that changing `baseline_commit` to another syntactically valid SHA fails closed.

### O-01 — Observation — Bounds are effective and appropriately conservative

The manifest contains 3 sources and 3 seeds with explicit maximums of 5/5. The validator rejects over-bound datasets and prevents silent broad ingestion. This is aligned with the F3 scope guardrail.

### O-02 — Observation — Semantic flattening and authority downgrade are correctly fail-closed

Tests explicitly reject semantic-type mismatch and downgrade of authoritative source classification. This is a useful permanent property for F4 consumers.

## 4. Architecture scorecard

| Dimension | Score | Assessment |
|---|---:|---|
| Repository-truth alignment | 94 | Real repository sources are used, but baseline identity is not yet enforced. |
| Bounded scope / anti-ingestion | 100 | 3/3 seed set with hard 5/5 bounds and fail-closed overflow. |
| F2 semantic fidelity | 98 | Semantic types/lifecycle/authority remain distinct and validated. |
| Citation/evidence traceability | 78 | Citations exist but reconciliation source is not deterministically bound to them. |
| Provenance integrity | 82 | F2 provenance resolves, but F3 does not prove source/provenance reconciliation identity. |
| Drift detection | 92 | Required source fragments detect content drift in the current checkout. |
| Baseline reproducibility | 72 | Baseline SHA is declarative rather than enforced. |
| CI/testability | 98 | Exact-head gates are green and negative tests cover several material failure modes. |
| Technology neutrality | 100 | No graph/vector/RAG/provider selection. |
| Safety/security | 100 | No runtime command path, remediation or Safety Authority coupling. |

**Overall:** 91/100.

## 5. Validation evidence

Exact reviewed head `772f3c9b8f38096d7c32f06a04d6f51e4adfd5b3`:

- Developer Foundation #985 — SUCCESS;
- Validate documentation #594 — SUCCESS;
- Genera manuale Word #1019 — SUCCESS.

These successful gates prove the implemented tests pass; they do not dispose M-01/M-02 because those properties are not yet tested/enforced.

## 6. Safety and operational disposition

F3 remains repository-only. No EAGLE runtime deployment, observatory hardware OAT, command endpoint, cleanup/remediation path or Safety Authority change is present. Runtime OAT is Not Applicable.

## 7. Re-review criteria

ARB re-review may approve F3 when all of the following are demonstrated on an exact head:

1. every seed's authoritative `source_ref` is deterministically linked to a governed Citation repository locator for the corresponding knowledge item/evidence chain;
2. validated derived items also prove the governed Provenance/Citation chain reaches the same reconciled source;
3. the declared baseline commit is fail-closed and cannot be replaced by another valid-looking SHA without failure;
4. negative tests cover source/Citation mismatch, provenance/Citation mismatch and baseline mismatch;
5. existing bounds, semantic parity, source-authority parity and source-drift checks remain green;
6. Developer Foundation, documentation and Word gates pass;
7. no expansion into broad ingestion, persistent graph/vector/RAG/runtime AI, EAGLE runtime or Safety Authority scope occurs.

## 8. Decision

**REWORK REQUIRED.** F3 architecture is directionally correct and bounded, but merge must not proceed until M-01 and M-02 are remediated and independently re-reviewed.