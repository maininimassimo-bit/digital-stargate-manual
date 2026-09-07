# BKL-044 — Knowledge Graph / AI Evidence Contract

| Field | Value |
|---|---|
| Identifier | BKL-044 |
| Status | In Progress |
| Version | 0.5 |
| Date | 2026-09-07 |
| Predecessor | BKL-015 — Done / Accepted |
| Related capability | CAP-40 — Scientific Knowledge Layer |
| Authority | Repository governance contract |
| Runtime impact | None |

## 1. Purpose

BKL-044 defines the semantic and machine-readable contract required to represent scientific and AI-derived knowledge on top of the accepted BKL-015 repository foundation. It distinguishes observations, evidence, claims, inference, recommendations, confidence, citations, provenance, conflicts and unknowns without making derived projections authoritative.

## 2. Verified baseline

BKL-015 provides stable repository identities, typed/versioned relations, source locators and deterministic graph gates. F1 established knowledge semantics. F2 is CLOSED / ACCEPTED via PR #100 and merge `ea36179882f05ce53581b80e5d5e8e70c560dcd9`. The F2 closure/handover is integrated through PR #101; verified F3 starting baseline is `40f7854f7e662e5a9f0ddc577f3f6f0f30f98993`.

Post-merge validation of that baseline is green: Developer Foundation #984, Validate documentation #593, Word #1018 and Pages #694.

## 3. Authority model

Authoritative sources remain authoritative for their own facts. Knowledge/AI datasets and F3 reconciliation manifests are projections. Source disagreement remains explicit. AI remains advisory/read-only and outside Safety Authority.

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

## 5. F2 machine-readable baseline

F2 introduced `schemas/knowledge-ai-evidence-contract.schema.json`, `docs/data/knowledge-ai-evidence-contract.json`, deterministic validation/tests and Developer Foundation integration. Citation and Provenance identity is versioned as `<id>@<version>`. BKL-015 repository traceability and BKL-044 evidence semantics remain separate contracts.

## 6. Lifecycle and fail-closed rules

Lifecycle states are `incomplete`, `unknown`, `draft`, `validated`, `superseded`, and `rejected`. Validated Claim/Inference/Recommendation requires resolvable evidence, citation, provenance and method. Validated Evidence requires governed Citation. Validated AI-derived knowledge additionally requires producer version. Confidence must resolve a stable/versioned contract.

## 7. F3 governed seed projection

F3 adds a separate non-authoritative manifest:

`docs/data/knowledge-ai-seed-reconciliation.json`

The manifest intentionally does not extend or weaken the F2 schema. It maps a bounded set of F2 knowledge items to explicit repository-authoritative source files and small source assertions that can be reconciled deterministically.

The initial governed set is limited to three reconciliation seeds and three repository sources:

1. F2 closure state from `docs/project/BKL-044-F2-CLOSURE-2026-09-07.md`;
2. current BKL-044 state from `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-07.md`;
3. F3-next planning assertion from `docs/project/BACKLOG.md`.

The manifest declares `max_sources=5` and `max_seeds=5`. Exceeding those bounds fails closed. Expanding the bounds is a governed contract change, not ordinary ingestion.

## 8. F3 reconciliation algorithm

`.github/scripts/verify-knowledge-ai-seed-reconciliation.mjs` verifies deterministically that:

- manifest identity/version/authority are expected;
- baseline commit is explicit;
- source and seed counts stay within governed bounds;
- every source is repository-relative, exists and has `repository_authority`;
- every seed resolves a knowledge item in the F2 projection;
- semantic type, lifecycle and source authority agree between manifest and F2 item;
- every seed carries 1..3 bounded source fragments;
- each required fragment is still present in the authoritative source.

Any missing source, unresolved item, semantic flattening, authority downgrade, source drift or bound violation fails closed.

## 9. F3 knowledge items and provenance

F3 seeds the F2 projection with governed Citation records for closure, baseline and backlog, plus:

- `EVD-BKL044-F3-F2-CLOSURE` — validated Evidence;
- `OBS-BKL044-F3-CURRENT-STATE` — validated Observation;
- `EVD-BKL044-F3-BACKLOG` — validated Evidence supporting the planning claim;
- `CLM-BKL044-F3-NEXT-INCREMENT` — validated Claim with evidence, Citation, Provenance, method and deterministic confidence.

`PRV-BKL044-F3-NEXT-INCREMENT@1.0` records the evidence-to-claim derivation. F3 therefore exercises F2 Citation, Provenance and Confidence without inventing a new persistence model.

## 10. F3 fail-closed tests

`.github/scripts/test-knowledge-ai-seed-reconciliation.mjs` covers:

- positive bounded reconciliation;
- authoritative source assertion drift;
- unresolved knowledge item;
- semantic-type flattening;
- governed-bound overflow;
- source-authority downgrade.

Both validator and tests are Developer Foundation gates.

## 11. Observation vs inference boundary

```text
repository authority -> Citation -> Observation/Evidence -> Provenance + method -> Claim/Inference -> optional Recommendation
```

F3 includes no validated AI inference or recommendation because no such content is required to prove reconciliation. The pre-existing incomplete AI example remains incomplete and non-authoritative.

## 12. AI-specific governance

AI-produced content remains explicitly marked and cannot mutate authoritative sources through this contract. No graph DB, vector DB, RAG framework, inference runtime, model provider or autonomous remediation is selected or authorized.

## 13. Safety and security boundary

F3 is repository-only. It introduces no observatory command path, cleanup action, remediation, interlock override, weather-safety decision, EAGLE runtime change or Safety Authority coupling. Citation presence is not access authorization.

## 14. Transition increments

- **F1 — Semantic contract:** accepted.
- **F2 — Machine-readable schema and validation:** CLOSED / ACCEPTED.
- **F3 — Governed seed projection and reconciliation:** current implementation/review increment.
- **F4 — Consumer/read-model contract:** only after F3 acceptance.

## 15. Acceptance criteria for F3

F3 is acceptable only if:

1. seed/source bounds are explicit and enforced;
2. every seed resolves an F2 knowledge item;
3. source authority, semantic type and lifecycle are preserved;
4. source assertions reconcile deterministically and fail closed on drift;
5. Citation/Provenance/Confidence F2 semantics remain intact;
6. negative tests cover drift, unresolved references, flattening, authority downgrade and bound overflow;
7. Developer Foundation, documentation and manual gates are green on exact PR head;
8. independent ARB review approves the increment;
9. Release Quality marks the increment ready before merge;
10. post-merge validation on `main` is green before F3 closure.

## 16. Migration and rollback

F3 is additive repository contract/projection/CI work. No runtime or scientific source data is migrated. Rollback is a repository revert of the F3 change set.

## 17. Risks and open decisions

Source wording changes can intentionally trigger reconciliation drift and require a governed seed update. Broad ingestion remains prohibited. Persistent graph/vector storage, RAG, inference technology and F4 consumer behavior remain undecided. Historical incomplete provenance remains explicit rather than synthesized.

## 18. Decision

F2 remains accepted. F3 is now the current bounded repository-only increment. It proves that selected knowledge items remain reconciled to explicit authoritative source material while preserving F2 fail-closed Citation, Provenance, Confidence and semantic boundaries. BKL-044 remains In Progress.