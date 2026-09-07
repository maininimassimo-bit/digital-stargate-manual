# BKL-044 F4 — ARB Remediation

- Date: 2026-09-07
- PR: #104
- Initial ARB decision: REWORK REQUIRED (96/100)
- Scope: repository-only consumer/read-model contract

## M-01 — Semantic preservation

Remediated. The F4 read model now preserves and deterministically compares semantic-type-specific source attributes in addition to the original common fields: `produced_at_utc`, `observed_at_utc`, `method_id`, `evidence_refs`, and `conflict_refs` where applicable. The validator fails closed on omission or mutation and does not synthesize absent source semantics.

Negative tests cover Observation timestamp loss, derived method loss, evidence-reference mutation, and Conflict reference loss using a bounded synthetic source item only inside the test.

## m-01 — Executable structural gate

Disposition: the JSON Schema remains the versioned machine-readable shape contract; the repository's normative executable CI gate for F4 is `.github/scripts/verify-knowledge-ai-read-model.mjs`. No new JSON-Schema runtime dependency is introduced in this increment. The executable validator now enforces root/item required shape, rejects unexpected root/item properties, rejects duplicate consumer identities/source projections, and continues deterministic source-semantic reconciliation. This keeps CI dependency-free while making the structural constraints used by the governed fixture executable.

## Boundaries

No runtime consumer, broad ingestion, graph/vector/RAG/provider selection, EAGLE change, hardware command path, autonomous remediation, or Safety Authority change is introduced.

## Re-review request

Re-review should verify M-01 and m-01 against the exact current PR head and require Developer Foundation, documentation, and Word gates to be green before approval.
