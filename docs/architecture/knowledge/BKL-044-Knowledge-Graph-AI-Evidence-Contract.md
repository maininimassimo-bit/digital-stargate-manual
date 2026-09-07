# BKL-044 — Knowledge Graph / AI Evidence Contract

| Field | Value |
|---|---|
| Identifier | BKL-044 |
| Status | In Progress |
| Version | 0.4 |
| Date | 2026-09-07 |
| Predecessor | BKL-015 — Done / Accepted |
| Related capability | CAP-40 — Scientific Knowledge Layer |
| Authority | Repository governance contract |
| Runtime impact | None |

## 1. Purpose

BKL-044 defines the semantic and machine-readable contract required to represent scientific and AI-derived knowledge on top of the accepted BKL-015 repository foundation. The contract distinguishes observations, evidence, claims, inference, recommendations, confidence, citations, provenance, conflicts and unknowns without making derived projections authoritative.

## 2. Verified baseline

BKL-015 provides stable repository entity identities, typed/versioned relations, source locators, a non-authoritative Knowledge Graph projection and deterministic integrity/coverage gates. BKL-044 extends that baseline without reopening TD-008.

F1 is merged via PR #98. F2 is CLOSED / ACCEPTED via PR #100 and merge `ea36179882f05ce53581b80e5d5e8e70c560dcd9`, after independent ARB approval, Release Quality readiness and successful post-merge CI.

## 3. Authority model

Authoritative sources remain authoritative for their own facts. Knowledge/AI datasets are projections. Source disagreement is represented as conflict and is never silently resolved. AI remains advisory/read-only and outside Safety Authority.

## 4. Canonical semantic classes

| Class | Meaning | Authority rule |
|---|---|---|
| Observation | Directly recorded/governed measurement or event | Source and observation time required |
| Evidence | Source artifact or governed fact supporting derivation | Validated evidence must resolve a governed citation/locator |
| Claim | Statement asserted from evidence | Producer, method and provenance required |
| Inference | Derived interpretation | Never silently promoted to fact |
| Recommendation | Advisory proposed action/choice | Non-authoritative unless separately governed |
| Confidence | Contextual certainty/quality statement | Stable versioned interpretation contract required |
| Citation | Versioned locator to supporting authority | First-class record; must remain resolvable by governed consumers |
| Provenance | Versioned source/transformation/producer chain | First-class record; inputs, output, method and citations must resolve |
| Conflict | Incompatible/unresolved assertions | Remains explicit until governed resolution |
| Unknown | Insufficient evidence | Must not become inferred certainty |

## 5. F2 machine-readable contract

F2 introduced:

- `schemas/knowledge-ai-evidence-contract.schema.json` — JSON Schema 2020-12, version `1.0`;
- `docs/data/knowledge-ai-evidence-contract.json` — bounded contract fixture/projection, not repository authority;
- `.github/scripts/verify-knowledge-ai-evidence-contract.mjs` — deterministic semantic and referential validator;
- `.github/scripts/test-knowledge-ai-evidence-contract.mjs` — positive and negative fail-closed tests;
- Developer Foundation integration.

The root contract contains first-class `citations`, `provenance_records`, `confidence_contracts` and semantic `items`. Citation and Provenance identity is versioned as `<id>@<version>`. The F2 schema does not replace `schemas/knowledge-graph-foundation.schema.json`; BKL-015 repository traceability and BKL-044 scientific/AI evidence semantics remain separate contracts.

## 6. Lifecycle and fail-closed rules

Lifecycle states are `incomplete`, `unknown`, `draft`, `validated`, `superseded`, and `rejected`.

A `claim`, `inference`, or `recommendation` may exist without complete evidence only while non-validated. Promotion to `validated` requires resolvable evidence, citation and provenance references plus derivation method. Validated `evidence` requires at least one resolvable governed Citation containing source authority and locator. A validated AI-derived item additionally requires producer version metadata.

Missing mandatory evidence, citation, provenance or producer identity fails closed and cannot be represented as validated knowledge.

## 7. Citation contract

A Citation is a first-class versioned record with stable ID, version, source authority, governed locator, producer and production timestamp. Locator kinds are technology-neutral (`repository_path`, `uri`, `catalog_id`, `external_asset_id`). Citation references use `<citation-id>@<version>` and must resolve deterministically. Citation is evidence location metadata, not a grant of authority or access.

## 8. Provenance contract

A Provenance record is a first-class versioned transformation record with producer, timestamp, method, one or more input item references, one output item reference and one or more governed Citation references. All referenced items and citations must resolve in the bounded contract dataset.

## 9. Confidence contract

Confidence is valid only through a stable versioned reference using `<contract-id>@<version>`. Each referenced confidence contract defines at minimum scale, method and producer, with calibration version, population/window and timestamp available when applicable. The validator rejects unresolved confidence contract references. A bare value has no compliant meaning.

## 10. Observation vs inference boundary

```text
observation/evidence -> governed citation -> derivation method + provenance -> claim/inference -> optional recommendation
```

Consumers must preserve semantic type, lifecycle, source authority, citation and provenance identity. F4 remains responsible for downstream read-model/API presentation rules.

## 11. AI-specific governance

AI-produced content is explicitly marked `ai_derived`, remains distinguishable from observations and repository facts, exposes incomplete/unknown states, and cannot mutate authoritative sources through this contract. No graph DB, vector DB, RAG framework, inference runtime, model provider or autonomous remediation is selected or authorized.

## 12. Safety and security boundary

BKL-044 introduces no observatory command path, cleanup action, remediation, interlock override, weather-safety decision or Safety Authority coupling. Knowledge projections contain no credentials and graph presence does not grant access to protected sources.

## 13. F2 acceptance evidence

Independent governance:

- `docs/architecture/reviews/ARB-BKL-044-F2-ReReview-2026-09-07.md` — APPROVED;
- `docs/architecture/reviews/RQ-BKL-044-F2-Release-Quality-Review-2026-09-07.md` — READY.

Post-merge on `ea36179882f05ce53581b80e5d5e8e70c560dcd9`:

- Developer Foundation #982 — SUCCESS;
- Validate documentation #591 — SUCCESS;
- Genera manuale Word #1016 — SUCCESS;
- Deploy MkDocs artifact to GitHub Pages #693 — SUCCESS.

Closure record: `docs/project/BKL-044-F2-CLOSURE-2026-09-07.md`.

## 14. Transition increments

- **F1 — Semantic contract:** merged via PR #98; accepted baseline.
- **F2 — Machine-readable schema and validation:** CLOSED / ACCEPTED via PR #100; merge `ea36179882f05ce53581b80e5d5e8e70c560dcd9`.
- **F3 — Governed seed projection and reconciliation:** next governed increment.
- **F4 — Consumer/read-model contract:** after F3.

## 15. F3 scope guardrails

F3 must seed only a bounded set of governed examples needed to prove the F2 contract against real authoritative source material. It must not become a broad ingestion initiative.

F3 must:

- select explicit authoritative repository source material;
- create only the minimum Observation/Evidence/Claim/Inference/Recommendation examples necessary for reconciliation coverage;
- use resolvable Citation and Provenance records;
- preserve source authority, lifecycle and semantic type;
- use confidence only through stable/versioned confidence contracts;
- expose incomplete, unknown or conflicting material explicitly;
- provide deterministic reconciliation/validation evidence;
- keep all projection content non-authoritative.

F3 must not select persistent graph/vector storage, RAG, model provider or inference runtime and must not introduce runtime EAGLE or Safety Authority behavior.

## 16. Migration and rollback

F2 is additive repository contract/CI work. No scientific source data or runtime configuration was migrated. F3 remains repository-only unless a separately governed decision changes that boundary. Rollback remains a repository revert of the applicable change set.

## 17. Risks and open decisions

Uncontrolled vocabulary growth, source conflicts, historical incomplete provenance, downstream flattening, access-control leakage and premature storage/AI technology selection remain risks. Persistent graph/vector storage, RAG and inference technology remain explicitly undecided and require separate governance.

## 18. Decision

F2 is accepted and closed as the machine-readable fail-closed contract baseline. BKL-044 remains In Progress. F3 may begin only from a verified post-F2 baseline and must remain bounded, source-reconciled, technology-neutral, advisory/read-only and outside Safety Authority.