# BKL-044 — Knowledge Graph / AI Evidence Contract

| Field | Value |
|---|---|
| Identifier | BKL-044 |
| Status | In Progress |
| Version | 0.7 |
| Date | 2026-09-07 |
| Predecessor | BKL-015 — Done / Accepted |
| Related capability | CAP-40 — Scientific Knowledge Layer |
| Authority | Repository governance contract |
| Runtime impact | None |

## 1. Purpose

BKL-044 defines the semantic and machine-readable contract required to represent scientific and AI-derived knowledge on top of the accepted BKL-015 repository foundation. It distinguishes observations, evidence, claims, inference, recommendations, confidence, citations, provenance, conflicts and unknowns without making derived projections authoritative.

## 2. Accepted baseline

F1 established knowledge semantics. F2 established the machine-readable fail-closed evidence contract. F3 — Governed Seed Projection & Reconciliation — is CLOSED / ACCEPTED. The continuity closure was merged via PR #103 at `6ebe07c7316204fae04938587b10a1d0ff14583e`.

Post-merge closure validation is green: Developer Foundation #995, Validate documentation #604, Word #1029 and Pages #696.

## 3. Authority model

Authoritative sources remain authoritative for their own facts. Knowledge/AI datasets, reconciliation manifests and consumer/read models are projections. Source disagreement remains explicit. AI remains advisory/read-only and outside Safety Authority.

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

The accepted F3 set remains bounded to 3 seeds / 3 repository-authoritative sources with governed maxima 5 / 5. F3 approval does not authorize broad ingestion.

## 6. Lifecycle and fail-closed rules

Lifecycle states remain `incomplete`, `unknown`, `draft`, `validated`, `superseded`, and `rejected`. Validated Claim/Inference/Recommendation requires resolvable evidence, citation, provenance and method. Validated Evidence requires governed Citation. Validated AI-derived knowledge additionally requires producer version. Confidence must resolve a stable/versioned contract.

## 7. F4 — Consumer / Read-Model Contract

F4 is the current implementation increment. It introduces a separate downstream projection rather than altering the accepted F2 source contract:

- `schemas/knowledge-ai-read-model.schema.json` — versioned consumer projection shape;
- `docs/data/knowledge-ai-read-model.json` — bounded governed fixture;
- `.github/scripts/verify-knowledge-ai-read-model.mjs` — deterministic semantic/traceability preservation validator;
- `.github/scripts/test-knowledge-ai-read-model.mjs` — fail-closed regression tests;
- Developer Foundation integration.

The read model has component `DSG.KnowledgeConsumerReadModel` and authority `projection`. Its `source_contract` is the governed F2/F3 evidence dataset.

## 8. Consumer invariants

For every projected source item F4 preserves exactly:

- source item identity through `source_item_ref`;
- semantic type;
- lifecycle state;
- source authority;
- AI-derived marker;
- producer and producer version where present;
- ordered Citation identities plus governed source authority and locator;
- ordered Provenance identities, method, inputs, output and Citation references;
- Confidence contract identity and value where present.

A consumer cannot invent Confidence when absent, drop Confidence when present, mutate Citation locators, mutate Provenance chains, remove the AI marker, escalate source authority, promote lifecycle, or flatten semantic type.

## 9. F4 validation matrix

Positive validation proves the governed fixture preserves source semantics and traceability. Negative tests fail closed for:

1. semantic flattening;
2. authority escalation;
3. lifecycle promotion/loss;
4. Citation identity loss;
5. Citation locator mutation;
6. Provenance identity loss;
7. Provenance chain mutation;
8. Confidence contract loss;
9. AI-derived marker loss.

Developer Foundation executes both the deterministic validator and negative test suite.

## 10. Observation vs inference boundary

```text
repository authority -> Citation -> Observation/Evidence -> Provenance + method -> Claim/Inference -> optional Recommendation -> read-only consumer projection
```

The consumer boundary is downstream of the governed knowledge contract and cannot increase authority.

## 11. AI-specific governance

AI-produced content remains explicitly marked and cannot mutate authoritative sources through this contract. No graph DB, vector DB, RAG framework, inference runtime, model provider or autonomous remediation is selected or authorized.

## 12. Safety and security boundary

BKL-044 F4 remains repository/read-only governance. It introduces no observatory command path, cleanup action, remediation, interlock override, weather-safety decision, EAGLE runtime change or Safety Authority coupling. Citation presence is not access authorization.

## 13. Transition increments

- **F1 — Semantic contract:** CLOSED / ACCEPTED.
- **F2 — Machine-readable schema and validation:** CLOSED / ACCEPTED.
- **F3 — Governed seed projection and reconciliation:** CLOSED / ACCEPTED.
- **F4 — Consumer / Read-Model Contract:** IMPLEMENTED / PENDING INDEPENDENT REVIEW.

## 14. Acceptance criteria for F4

F4 is acceptable only if:

1. consumer/read-model contract is versioned and machine-readable;
2. semantic type and lifecycle are preserved exactly;
3. source authority cannot be escalated by projection;
4. Citation identity/version/locator remain traceable;
5. Provenance identity and chain remain traceable for derived items;
6. Confidence remains tied to its versioned contract;
7. unknown/conflict/incomplete states remain explicit when projected;
8. negative tests fail closed on semantic flattening, authority escalation and traceability loss;
9. Developer Foundation, documentation and manual gates are green on exact PR head;
10. independent ARB and Release Quality gates approve before merge;
11. post-merge validation is green before F4 closure.

## 15. Migration and rollback

F4 is additive repository contract/projection/CI work. No runtime or scientific source data migration is authorized. Rollback is a repository revert of the F4 change set.

## 16. Risks and open decisions

Persistent graph/vector storage, RAG, inference technology and runtime UI/API implementation remain undecided. Broad ingestion remains prohibited. Historical incomplete provenance remains explicit rather than synthesized. F4 does not create a second authority model.

The current fixture intentionally exercises evidence, observation, claim and an incomplete AI inference. It does not manufacture conflict/unknown/recommendation records merely to increase fixture coverage; those semantic classes remain governed by the source contract and must be preserved exactly when future governed source items of those types are projected.

## 17. Decision

F3 is accepted. F4 implementation is ready for exact-head CI and independent ARB review. BKL-044 remains `In Progress`.