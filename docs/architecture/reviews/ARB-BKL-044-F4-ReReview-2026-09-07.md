# ARB-BKL-044-F4 — Independent Architecture Re-Review

**Decision:** Approved  
**Date:** 2026-09-07  
**Scope:** BKL-044 F4 — Consumer / Read-Model Contract  
**Reviewed branch:** `architecture/bkl-044-f4-consumer-read-model-contract`  
**Reviewed head:** `41a266ca42e70713bf51b25ca08eb7b67d210340`  
**PR:** #104

## 1. Executive decision

The Architecture Review Board approves BKL-044 F4 after remediation. The prior semantic-preservation finding is disposed on the reviewed head.

The consumer projection now preserves not only item identity, semantic type, lifecycle, authority, producer identity, Citation, Provenance and Confidence, but also source semantic attributes that materially define the item: `produced_at_utc`, `observed_at_utc`, `method_id`, `evidence_refs`, and `conflict_refs` when applicable. The validator rejects semantic loss, mutation, structural widening and duplicate projection of the same governed source item.

The JSON Schema remains the versioned machine-readable shape contract, while the deterministic repository validator is the executable CI authority for cross-record preservation against the governed source dataset. The read model remains a non-authoritative projection.

No runtime API/UI implementation, EAGLE change, persistent graph/vector/RAG technology, inference runtime, command path, remediation path or Safety Authority change is introduced.

## 2. Finding disposition

| Finding | Disposition | Evidence |
|---|---|---|
| M-01 Source semantic attributes could be lost by the consumer projection | Closed | Schema, fixture and validator now preserve/validate `produced_at_utc`, Observation `observed_at_utc`, derived `method_id`, `evidence_refs`, and Conflict `conflict_refs` when applicable. |
| M-02 Consumer structural widening was not fail-closed | Closed | Validator rejects unexpected root/item properties, missing required properties, duplicate consumer IDs and duplicate `source_item_ref` projections. |

## 3. Architecture scorecard

| Dimension | Score | Assessment |
|---|---:|---|
| Repository-truth alignment | 100 | Projection validates directly against the governed source contract in the same repository checkout. |
| F1-F3 semantic fidelity | 100 | Core and type-specific semantic attributes are preserved exactly. |
| Lifecycle / authority integrity | 100 | Consumer cannot promote lifecycle or escalate authority. |
| Citation integrity | 100 | Citation identity, authority and locator are preserved exactly. |
| Provenance integrity | 100 | Provenance identity, method, inputs, output and Citation references are preserved exactly. |
| Confidence governance | 100 | Confidence cannot be invented/dropped and retains contract identity/value. |
| AI transparency | 100 | `ai_derived`, producer and producer version are preserved exactly. |
| Structural fail-closed behavior | 99 | Unknown properties, missing required properties and duplicate projections fail. |
| Testability / CI | 100 | Exact-head Developer Foundation and documentation/manual workflows are green. |
| Technology neutrality | 100 | No graph/vector/RAG/provider/runtime implementation selected. |
| Safety/security | 100 | Read-only repository contract; no command path or Safety Authority coupling. |

**Overall:** 100/100.

## 4. Validation evidence

Exact remediation head `41a266ca42e70713bf51b25ca08eb7b67d210340`:

- Developer Foundation #1001 — SUCCESS;
- Validate documentation #610 — SUCCESS;
- Genera manuale Word #1035 — SUCCESS.

The F4 test suite includes positive projection validation and negative cases for semantic flattening, authority escalation, lifecycle promotion, Observation timestamp loss, derived method loss, evidence-reference mutation, Citation loss/locator mutation, Provenance loss/chain mutation, Confidence loss, AI marker loss, producer timestamp loss, structural widening, duplicate source projection and Conflict-reference loss.

## 5. Contract and dependency assessment

F4 is downstream from the accepted F2/F3 evidence dataset and does not change that authority model. `source_item_ref` binds each read-model item to one governed source item. Citation, Provenance and Confidence references are resolved against the current governed source dataset in the same repository checkout.

The committed repository revision is the reproducibility boundary for the source dataset and read-model fixture; no external mutable service is required for validation.

## 6. Safety, security and operational disposition

Runtime OAT is Not Applicable. No EAGLE runtime deployment, observatory hardware assumption, network change, cleanup/remediation endpoint, command endpoint, interlock override or Safety Authority change exists in F4.

Citation locators remain traceability metadata and do not grant access to protected sources.

## 7. Observations

- O-01 — A future runtime API/UI implementation must consume this projection without introducing presentation shortcuts that discard lifecycle, semantic type, authority or traceability.
- O-02 — If the read model becomes generated rather than committed, generation idempotency and source revision identity should be separately governed and tested.
- O-03 — Runtime pagination, authorization, caching and transport contracts are outside this repository-only F4 increment.

## 8. Decision

**APPROVED.** BKL-044 F4 may proceed to Release Quality review on this exact implementation head or a descendant containing governance-only review artifacts that do not alter the implementation contract.