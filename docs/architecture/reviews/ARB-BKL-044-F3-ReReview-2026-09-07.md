# ARB-BKL-044-F3 — Independent Architecture Re-Review

**Decision:** Approved  
**Date:** 2026-09-07  
**Scope:** BKL-044 F3 — Governed Seed Projection & Reconciliation  
**Reviewed branch:** `architecture/bkl-044-f3-governed-seed-reconciliation`  
**Reviewed head:** `c2abc8c49e703ba3e669686f6167fa8c838b7d2c`  
**PR:** #102

## 1. Executive decision

The Architecture Review Board approves BKL-044 F3 after remediation. Major findings M-01 and M-02 from the prior review are disposed on the reviewed head.

Each governed seed now resolves a versioned Citation identity and proves exact equality between the Citation repository locator and the selected repository-authoritative source path. The corresponding knowledge item must reference that Citation. Validated derived items additionally prove their governed Provenance record resolves, cites the same reconciled Citation and emits the same knowledge item as output.

The declared F3 baseline is now fail-closed against the approved baseline commit `40f7854f7e662e5a9f0ddc577f3f6f0f30f98993`; substituting another syntactically valid SHA fails validation.

The package remains bounded to 3 seeds / 3 sources with hard 5/5 maximums. No broad ingestion, persistent graph/vector/RAG technology, inference runtime, EAGLE runtime change, command path or Safety Authority capability is introduced.

## 2. Finding disposition

| Finding | Disposition | Evidence |
|---|---|---|
| M-01 Seed source not bound to Citation/Provenance | Closed | Manifest includes `citation_ref`; validator enforces Citation locator/source equality, item Citation membership and derived Provenance/Citation/output identity. |
| M-02 Baseline commit not effective | Closed | Validator compares manifest baseline to the approved F3 baseline constant; negative test rejects another valid-looking 40-char SHA. |

## 3. Architecture scorecard

| Dimension | Score | Assessment |
|---|---:|---|
| Repository-truth alignment | 99 | Explicit repository sources and approved baseline are fail-closed. |
| Bounded scope / anti-ingestion | 100 | 3/3 set with 5/5 hard upper bounds. |
| F2 semantic fidelity | 99 | Semantic type, lifecycle and source authority remain preserved. |
| Citation/evidence traceability | 100 | Seed source and governed Citation locator identity are deterministic. |
| Provenance integrity | 99 | Validated derived item provenance must cite the reconciled source and match output identity. |
| Drift detection | 98 | Bounded authoritative fragments fail closed on source drift. |
| Baseline reproducibility | 98 | Approved baseline identity is enforced deterministically. |
| CI/testability | 100 | Positive and negative tests execute under Developer Foundation. |
| Technology neutrality | 100 | No storage/RAG/provider/runtime selection. |
| Safety/security | 100 | No command path or Safety Authority coupling. |

**Overall:** 99/100.

## 4. Validation evidence

Exact remediation head `c2abc8c49e703ba3e669686f6167fa8c838b7d2c`:

- Developer Foundation #989 — SUCCESS;
- Validate documentation #598 — SUCCESS;
- Genera manuale Word #1023 — SUCCESS.

Negative tests now prove fail-closed behavior for source/Citation mismatch, item/Citation mismatch, Provenance/Citation mismatch and baseline replacement, while retaining source drift, semantic flattening, authority downgrade and bound overflow checks.

## 5. Safety and operational disposition

Runtime OAT is Not Applicable. F3 remains repository-only and non-authoritative. No EAGLE deployment, observatory hardware assumption, command endpoint, cleanup/remediation path or local interlock/Safety Authority change is present.

## 6. Observations

- O-01 — F4 must preserve semantic type, lifecycle, authority, Citation and Provenance identities in consumer/read-model contracts rather than flattening them.
- O-02 — Any expansion beyond the bounded F3 seed set requires separate governance; F3 approval is not permission for broad ingestion.
- O-03 — Persistent graph/vector/RAG or inference technology remains explicitly undecided.

## 7. Decision

**APPROVED.** BKL-044 F3 may proceed to Release Quality review on this exact implementation head or a descendant containing governance-only review artifacts that do not alter the implementation contract.