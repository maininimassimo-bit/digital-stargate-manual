# BKL-044 — Knowledge Graph / AI Evidence Contract

| Field | Value |
|---|---|
| Identifier | BKL-044 |
| Status | Closed / Accepted |
| Version | 1.0 |
| Date | 2026-09-07 |
| Predecessor | BKL-015 — Done / Accepted |
| Successor | BKL-035 — Target Knowledge Base |
| Related capability | CAP-40 — Scientific Knowledge Layer |
| Authority | Repository governance contract |
| Runtime impact | None |

## 1. Purpose

BKL-044 defines the semantic and machine-readable contract required to represent scientific and AI-derived knowledge on top of the accepted BKL-015 repository foundation. It distinguishes observations, evidence, claims, inference, recommendations, confidence, citations, provenance, conflicts and unknowns without making derived projections authoritative.

## 2. Accepted baseline

All four increments are CLOSED / ACCEPTED:

- F1 — Semantic Contract;
- F2 — Machine-readable Schema & Validation;
- F3 — Governed Seed Projection & Reconciliation;
- F4 — Consumer / Read-Model Contract.

F4 was integrated via PR #104 with merge `b7c01ba7221818e1971403ab3befe38c8e40cc54`. Independent ARB re-review approved F4 100/100 and Release Quality declared it READY. Post-merge Developer Foundation #1004, Docs #613, Word #1038 and Pages #697 completed successfully.

Final closure: `docs/project/BKL-044-CLOSURE-2026-09-07.md`.

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

## 5. Accepted machine-readable contracts

F2 provides `schemas/knowledge-ai-evidence-contract.schema.json`, `docs/data/knowledge-ai-evidence-contract.json`, deterministic validation/tests and Developer Foundation integration.

F3 provides `docs/data/knowledge-ai-seed-reconciliation.json`, `.github/scripts/verify-knowledge-ai-seed-reconciliation.mjs` and `.github/scripts/test-knowledge-ai-seed-reconciliation.mjs`. The accepted F3 set remains bounded to 3 seeds / 3 repository-authoritative sources with governed maxima 5 / 5; acceptance does not authorize broad ingestion.

F4 provides `schemas/knowledge-ai-read-model.schema.json`, `docs/data/knowledge-ai-read-model.json`, `.github/scripts/verify-knowledge-ai-read-model.mjs` and `.github/scripts/test-knowledge-ai-read-model.mjs`.

## 6. Lifecycle and fail-closed rules

Lifecycle states remain `incomplete`, `unknown`, `draft`, `validated`, `superseded`, and `rejected`. Validated Claim/Inference/Recommendation requires resolvable evidence, citation, provenance and method. Validated Evidence requires governed Citation. Validated AI-derived knowledge additionally requires producer version. Confidence must resolve a stable/versioned contract.

## 7. Consumer invariants

Every governed projection must preserve source item identity, semantic type, lifecycle state, source authority, AI-derived marker, applicable producer/version, Citation identity/authority/locator, Provenance identity/method/input/output/citations and Confidence contract/value where present.

A consumer cannot invent or drop Confidence, mutate Citation locators or Provenance chains, remove the AI marker, escalate source authority, promote lifecycle or flatten semantic type.

## 8. Observation vs inference boundary

```text
repository authority -> Citation -> Observation/Evidence -> Provenance + method -> Claim/Inference -> optional Recommendation -> read-only consumer projection
```

The consumer boundary is downstream of the governed knowledge contract and cannot increase authority.

## 9. AI-specific governance

AI-produced content remains explicitly marked and cannot mutate authoritative sources through this contract. No graph DB, vector DB, RAG framework, inference runtime, model provider or autonomous remediation is selected or authorized by BKL-044.

## 10. Safety and security boundary

BKL-044 is repository/read-only governance. It introduces no observatory command path, cleanup action, remediation, interlock override, weather-safety decision, EAGLE runtime change or Safety Authority coupling. Citation presence is not access authorization.

## 11. Acceptance result

All BKL-044 acceptance criteria are satisfied for the approved scope: machine-readable/versioned contracts, exact semantic/lifecycle/authority preservation, Citation/Provenance/Confidence traceability, explicit incomplete/unknown/conflict semantics, fail-closed tests, exact-head CI, independent ARB, Release Quality and post-merge validation.

## 12. Migration and rollback

BKL-044 is additive repository contract/projection/CI work. No runtime or scientific source data migration was authorized. Rollback remains repository revert of the applicable change set.

## 13. Residual decisions transferred forward

Persistent graph/vector storage, RAG, inference technology and runtime UI/API implementation remain undecided. Broad ingestion remains prohibited unless separately governed. Historical incomplete provenance remains explicit rather than synthesized. These decisions are not closure blockers and transfer to successor packages when relevant.

## 14. Successor

The next governed package is **BKL-035 Target Knowledge Base**. It must build on BKL-015/BKL-044, preserve all authority and provenance invariants, and begin with source discovery and a bounded semantic contract before any broader projection or UI implementation.

## 15. Decision

**BKL-044 is CLOSED / ACCEPTED.** F1-F4 constitute the accepted Knowledge Graph / AI Evidence Contract baseline.