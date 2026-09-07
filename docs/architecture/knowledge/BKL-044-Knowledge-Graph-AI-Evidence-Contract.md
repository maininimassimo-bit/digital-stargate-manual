# BKL-044 — Knowledge Graph / AI Evidence Contract

| Field | Value |
|---|---|
| Identifier | BKL-044 |
| Status | In Progress |
| Version | 0.2 |
| Date | 2026-09-07 |
| Predecessor | BKL-015 — Done / Accepted |
| Related capability | CAP-40 — Scientific Knowledge Layer |
| Authority | Repository governance contract |
| Runtime impact | None |

## 1. Purpose

BKL-044 defines the semantic and machine-readable contract required to represent scientific and AI-derived knowledge on top of the accepted BKL-015 repository foundation. The contract distinguishes observations, evidence, claims, inference, recommendations, confidence, citations, provenance, conflicts and unknowns without making derived projections authoritative.

## 2. Verified baseline

BKL-015 provides stable repository entity identities, typed/versioned relations, source locators, a non-authoritative Knowledge Graph projection and deterministic integrity/coverage gates. BKL-044 extends that baseline without reopening TD-008.

## 3. Authority model

Authoritative sources remain authoritative for their own facts. Knowledge/AI datasets are projections. Source disagreement is represented as conflict and is never silently resolved. AI remains advisory/read-only and outside Safety Authority.

## 4. Canonical semantic classes

| Class | Meaning | Authority rule |
|---|---|---|
| Observation | Directly recorded/governed measurement or event | Source and observation time required |
| Evidence | Source artifact or governed fact supporting derivation | Must be attributable/locatable |
| Claim | Statement asserted from evidence | Producer, method and provenance required |
| Inference | Derived interpretation | Never silently promoted to fact |
| Recommendation | Advisory proposed action/choice | Non-authoritative unless separately governed |
| Confidence | Contextual certainty/quality statement | Stable versioned interpretation contract required |
| Citation | Locator to supporting authority | Must remain resolvable by governed consumers |
| Provenance | Source/transformation/producer chain | Must be inspectable end-to-end |
| Conflict | Incompatible/unresolved assertions | Remains explicit until governed resolution |
| Unknown | Insufficient evidence | Must not become inferred certainty |

## 5. F2 machine-readable contract

F2 introduces:

- `schemas/knowledge-ai-evidence-contract.schema.json` — JSON Schema 2020-12, version `1.0`;
- `docs/data/knowledge-ai-evidence-contract.json` — bounded contract fixture/projection, not repository authority;
- `.github/scripts/verify-knowledge-ai-evidence-contract.mjs` — deterministic semantic validator;
- `.github/scripts/test-knowledge-ai-evidence-contract.mjs` — positive and negative fail-closed tests;
- Developer Foundation integration.

The F2 schema does not replace `schemas/knowledge-graph-foundation.schema.json`; BKL-015 repository traceability and BKL-044 scientific/AI evidence semantics remain separate contracts.

## 6. Lifecycle and fail-closed rules

Lifecycle states are `incomplete`, `unknown`, `draft`, `validated`, `superseded`, and `rejected`.

A `claim`, `inference`, or `recommendation` may exist without complete evidence only when its lifecycle remains non-validated, such as `incomplete` or `unknown`. Promotion to `validated` requires evidence references, citation references and derivation method.

A validated AI-derived item additionally requires producer version metadata. Missing mandatory provenance therefore fails closed: it cannot be represented as validated knowledge.

This directly disposes ARB F1 finding M-01 and Release Quality condition RQ-01.

## 7. Confidence contract

Confidence is valid only through a stable versioned reference using the form `<contract-id>@<version>`. Each referenced confidence contract defines at minimum scale, method and producer, with calibration version, population/window and timestamp available when applicable.

The validator rejects an unresolved confidence contract reference. A bare value such as `0.92` has no compliant meaning.

This directly disposes ARB F1 finding M-02 and Release Quality condition RQ-02.

## 8. Observation vs inference boundary

```text
observation/evidence -> derivation method -> claim/inference -> optional recommendation
```

Consumers must preserve semantic type, lifecycle and authority classification. F4 remains responsible for downstream read-model/API presentation rules.

## 9. AI-specific governance

AI-produced content is explicitly marked `ai_derived`, remains distinguishable from observations and repository facts, exposes incomplete/unknown states, and cannot mutate authoritative sources through this contract. No graph DB, vector DB, RAG framework, inference runtime, model provider or autonomous remediation is selected or authorized.

## 10. Safety and security boundary

F2 introduces no observatory command path, cleanup action, remediation, interlock override, weather-safety decision or Safety Authority coupling. Knowledge projections contain no credentials and graph presence does not grant access to protected sources.

## 11. Validation behavior

The CI validator checks at minimum:

- contract version/component/authority;
- unique item and confidence-contract identities;
- semantic and lifecycle vocabulary;
- observation timestamp requirement;
- derivation method for claim/inference/recommendation;
- evidence and citations for validated derived items;
- evidence, citations and producer version for validated AI items;
- stable/versioned confidence-contract resolution;
- explicit conflict references.

Negative tests prove that evidence-less validated AI inference and unresolved confidence references fail. Positive tests prove that incomplete AI inference remains representable and that fully evidenced validated derivation passes.

## 12. Transition increments

- **F1 — Semantic contract:** merged via PR #98.
- **F2 — Machine-readable schema and validation:** current increment.
- **F3 — Governed seed projection and reconciliation:** next after F2 acceptance.
- **F4 — Consumer/read-model contract:** after F3.

## 13. F2 acceptance criteria

F2 is acceptable when:

- the machine-readable schema is versioned and technology-neutral;
- canonical semantic classes remain distinguishable;
- lifecycle state and source authority are explicit;
- validated derived knowledge cannot omit evidence/citations/method;
- validated AI-derived knowledge cannot omit evidence/citations/producer version;
- confidence values resolve to stable/versioned confidence contracts;
- deterministic positive/negative tests are integrated into Developer Foundation;
- MkDocs/documentation gates pass;
- independent ARB and Release Quality reviews approve continuation;
- no runtime or Safety Authority capability is introduced.

## 14. Migration and rollback

F2 is additive repository contract/CI work. No scientific source data or runtime configuration is migrated. Rollback is a repository revert of the F2 change set.

## 15. Risks and open decisions

Uncontrolled vocabulary growth, source conflicts, historical incomplete provenance, downstream flattening, access-control leakage and premature storage/AI technology selection remain risks. Persistent graph/vector storage, RAG and inference technology remain explicitly undecided and require separate governance.

## 16. Decision

BKL-044 F2 encodes the accepted F1 semantics as a fail-closed machine-readable contract while preserving repository authority, explicit unknown/conflict states, technology neutrality and advisory/read-only AI boundaries. F3 seed/reconciliation work must not begin until F2 exact-head CI, independent review and merge acceptance are complete.
