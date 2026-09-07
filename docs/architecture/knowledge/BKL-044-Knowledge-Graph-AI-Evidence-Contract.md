# BKL-044 — Knowledge Graph / AI Evidence Contract

| Field | Value |
|---|---|
| Identifier | BKL-044 |
| Status | In Progress |
| Version | 0.6 |
| Date | 2026-09-07 |
| Predecessor | BKL-015 — Done / Accepted |
| Related capability | CAP-40 — Scientific Knowledge Layer |
| Authority | Repository governance contract |
| Runtime impact | None |

## 1. Purpose

BKL-044 defines the semantic and machine-readable contract required to represent scientific and AI-derived knowledge on top of the accepted BKL-015 repository foundation. It distinguishes observations, evidence, claims, inference, recommendations, confidence, citations, provenance, conflicts and unknowns without making derived projections authoritative.

## 2. Accepted baseline

F1 established knowledge semantics. F2 established the machine-readable fail-closed evidence contract. F3 — Governed Seed Projection & Reconciliation — is CLOSED / ACCEPTED via PR #102 and merge `8d9f47922de1536b424cdd29ca00fc61c5c9fa49`.

F3 governance is recorded by the independent ARB re-review (APPROVED 99/100), Release Quality review (READY), and `docs/project/BKL-044-F3-CLOSURE-2026-09-07.md`.

Post-merge validation on the F3 merge commit is green: Developer Foundation #992, Validate documentation #601, Word #1026 and Pages #695.

## 3. Authority model

Authoritative sources remain authoritative for their own facts. Knowledge/AI datasets, reconciliation manifests and future consumer/read models are projections. Source disagreement remains explicit. AI remains advisory/read-only and outside Safety Authority.

## 4. Canonical semantic classes

| Class | Meaning | Authority rule |
|---|---|---|
| Observation | Directly recorded/governed measurement or event | Source and observation time required |
| Evidence | Source artifact or governed fact supporting derivation | Validated evidence must resolve a governed citation/locator |
| Claim | Statement asserted from evidence | Producer, method and provenance required |
| Inference | Derived interpretation | Never silently promoted to fact |
| Recommendation | Advisory proposed action/choice | Non-authoritative unless separately governed |
| Confidence | Contextual certainty/quality statement | Stable versioned interpretation contract required |
| Citation | Versioned locator to supporting authority | First-class record; must remain resolvable |
| Provenance | Versioned source/transformation/producer chain | First-class record; inputs, output, method and citations resolve |
| Conflict | Incompatible/unresolved assertions | Explicit until governed resolution |
| Unknown | Insufficient evidence | Must not become inferred certainty |

## 5. Accepted F2/F3 machine-readable contracts

F2 provides `schemas/knowledge-ai-evidence-contract.schema.json`, `docs/data/knowledge-ai-evidence-contract.json`, deterministic validation/tests and Developer Foundation integration.

F3 provides `docs/data/knowledge-ai-seed-reconciliation.json`, `.github/scripts/verify-knowledge-ai-seed-reconciliation.mjs` and `.github/scripts/test-knowledge-ai-seed-reconciliation.mjs`.

The accepted F3 set is bounded to 3 seeds / 3 repository-authoritative sources with governed maxima 5 / 5. F3 enforces approved-baseline identity, source drift detection, semantic/lifecycle/authority parity, seed-to-Citation locator identity, item-to-Citation identity and derived Provenance/Citation/output identity.

F3 approval does not authorize broad ingestion.

## 6. Lifecycle and fail-closed rules

Lifecycle states remain `incomplete`, `unknown`, `draft`, `validated`, `superseded`, and `rejected`. Validated Claim/Inference/Recommendation requires resolvable evidence, citation, provenance and method. Validated Evidence requires governed Citation. Validated AI-derived knowledge additionally requires producer version. Confidence must resolve a stable/versioned contract.

## 7. F4 — Consumer / Read-Model Contract

F4 is the current increment. Its purpose is to define and validate a consumer-facing projection contract that preserves F1-F3 semantics when knowledge items are exposed to API, UI, portal or other read-only consumers.

F4 must preserve at minimum:

- item identity;
- semantic type;
- lifecycle state;
- source authority;
- AI-derived marker and producer identity/version when applicable;
- Citation identity/version and governed locator;
- Provenance identity/version and applicable chain;
- Confidence contract identity/value when present;
- explicit unknown/conflict/incomplete states.

## 8. Consumer invariants

A consumer/read model must not:

- flatten Observation, Evidence, Claim, Inference and Recommendation into an undifferentiated fact;
- promote Claim or Inference to Observation;
- promote AI-derived material to repository authority;
- omit lifecycle state in a way that makes incomplete/unknown material appear validated;
- replace Citation identity with display text only;
- replace Provenance with an untraceable summary;
- expose Confidence without its interpretation contract identity;
- resolve Conflict or Unknown by presentation convention alone.

## 9. F4 expected validation

F4 should introduce a versioned machine-readable read-model schema/fixture plus deterministic validator/tests. Tests must include positive preservation and negative cases for semantic flattening, authority escalation, lifecycle loss, Citation loss, Provenance loss and Confidence-contract loss.

The implementation remains repository-only unless a later explicitly governed increment introduces runtime consumers.

## 10. Observation vs inference boundary

```text
repository authority -> Citation -> Observation/Evidence -> Provenance + method -> Claim/Inference -> optional Recommendation -> read-only consumer projection
```

The consumer boundary is downstream of the governed knowledge contract and cannot increase authority.

## 11. AI-specific governance

AI-produced content remains explicitly marked and cannot mutate authoritative sources through this contract. No graph DB, vector DB, RAG framework, inference runtime, model provider or autonomous remediation is selected or authorized.

## 12. Safety and security boundary

BKL-044 remains repository/read-only governance. It introduces no observatory command path, cleanup action, remediation, interlock override, weather-safety decision, EAGLE runtime change or Safety Authority coupling. Citation presence is not access authorization.

## 13. Transition increments

- **F1 — Semantic contract:** CLOSED / ACCEPTED.
- **F2 — Machine-readable schema and validation:** CLOSED / ACCEPTED.
- **F3 — Governed seed projection and reconciliation:** CLOSED / ACCEPTED.
- **F4 — Consumer / Read-Model Contract:** CURRENT.

## 14. Acceptance criteria for F4

F4 is acceptable only if:

1. consumer/read-model contract is versioned and machine-readable;
2. semantic type and lifecycle are preserved exactly;
3. source authority cannot be escalated by projection;
4. Citation identity/version/locator remain traceable;
5. Provenance identity and chain remain traceable for derived items;
6. Confidence remains tied to its versioned contract;
7. unknown/conflict/incomplete states remain explicit;
8. negative tests fail closed on semantic flattening, authority escalation and traceability loss;
9. Developer Foundation, documentation and manual gates are green on exact PR head;
10. independent ARB and Release Quality gates approve before merge;
11. post-merge validation is green before F4 closure.

## 15. Migration and rollback

F4 is expected to be additive repository contract/projection/CI work. No runtime or scientific source data migration is authorized. Rollback is a repository revert of the F4 change set.

## 16. Risks and open decisions

Persistent graph/vector storage, RAG, inference technology and runtime UI/API implementation remain undecided. Broad ingestion remains prohibited. Historical incomplete provenance remains explicit rather than synthesized. F4 must not accidentally create a second authority model through presentation or serialization shortcuts.

## 17. Decision

F3 is accepted. F4 is now the current BKL-044 increment. BKL-044 remains `In Progress` until the governed increment sequence is completed.