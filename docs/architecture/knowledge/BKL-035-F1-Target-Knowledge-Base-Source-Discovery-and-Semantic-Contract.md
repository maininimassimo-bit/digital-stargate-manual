# BKL-035 F1 — Target Knowledge Base Source Discovery & Semantic Contract

| Field | Value |
|---|---|
| Identifier | BKL-035-F1 |
| Status | In Progress |
| Version | 0.2 |
| Date | 2026-09-07 |
| Parent backlog item | BKL-035 — Target Knowledge Base |
| Baseline | `d550427c7acf0fd03e6e79fcfba32d6f17597dcb` |
| Dependencies | BKL-015; BKL-044; AP-013; AP-014; BKL-029; AP14-W06 |
| Authority | Repository governance contract |
| Runtime impact | None |

## 1. Purpose

Define the authoritative source inventory and semantic boundary for a target-centric knowledge projection without creating a second source of truth. BKL-035 must correlate existing governed facts about astronomical targets, sessions, SQM/conditions, setups, scientific assets and processing provenance while preserving the authority and lifecycle semantics of each source.

## 2. Current state

The repository already contains governed scientific/session projections and architecture contracts that expose target-related information. The scientific observation index is generated from the scientific session catalog and currently contains 14 reconciled observation-session documents. Search documents already expose target labels together with session date, telescope, camera, filter and integration summary.

The AP-013 conceptual model already defines `SCIENTIFIC_TARGET` as a first-class concept related to `SCIENTIFIC_PROJECT` and downstream observation sessions. AP-013 remains the architecture authority for scientific asset/storage lineage; AP-014 remains the authority for observation catalog/search projections.

BKL-029 provides SQM realtime/history semantics. AP14-W06 provides a governed PixInsight manifest/import/reconciliation boundary and explicitly treats processing projections as derived/read-only rather than scientific asset authority.

BKL-044 is CLOSED / ACCEPTED and supplies the semantic rules that BKL-035 must inherit: projection authority, explicit Citation/Provenance/Confidence, no semantic flattening, no implicit AI authority and no broad ingestion authorization.

## 3. Deterministic source discovery inventory

F1 source discovery is an ordered, bounded repository contract. A later validator must resolve these paths exactly; family labels are not sufficient.

| Order | Canonical repository path / record | Role for BKL-035 | Authority classification | F1 disposition |
|---:|---|---|---|---|
| 1 | `docs/data/scientific-session-catalog.json` — session record keyed by canonical `session_id` | session-level scientific facts, target label, coordinates where present, setup/configuration and source-metrics linkage | governed scientific projection | **primary factual source for session-bound target evidence** |
| 2 | `docs/data/scientific-observation-index.json` — `catalogItems[].entityId` / matching `searchDocuments[].catalogItemId` | searchable target/session representation generated from source 1 | projection | discovery/read optimization only; never wins a conflict against source 1 |
| 3 | `docs/architecture/scientific-assets/DSDM-001-Scientific-Data-Manager-Conceptual-Model.md` | `SCIENTIFIC_TARGET -> SCIENTIFIC_PROJECT -> OBSERVATION_SESSION` conceptual lineage | repository architecture authority | semantic authority for target/project/session relation meaning |
| 4 | `docs/architecture/packages/AP-013-Scientific-Image-Repository-Architecture.md` and `docs/architecture/scientific-assets/DSDM-003-Contract-and-Manifest-Model.md` | scientific asset identity, repository/storage lineage and manifest semantics | repository architecture authority | semantic authority for `TARGET_HAS_ASSET`; does not supply target identity by itself |
| 5 | `docs/architecture/packages/AP-014-Scientific-Observation-Catalog-and-Search.md` | observation catalog identity, search, reconciliation and index boundaries | repository architecture authority | semantic authority for observation/catalog indexing behavior |
| 6 | `data/sessions/<YYYY>/<MM>/<session_id>/normalized/session-metrics.json` — `scientific.target_name`, scientific/setup fields and `sqm.*` | canonical per-session normalized scientific and SQM evidence | governed scientific projection | primary per-session environmental/setup evidence; exact file is resolved from source-1 `session_id` / source metrics path |
| 7 | `data/analytics/history/sessions.csv` — row keyed by `session_id`, including `target_name`, setup and `sqm_*` columns | historical aggregate/read model over source 6 | analytics projection | read optimization / aggregate evidence only; cannot override source 6 |
| 8 | `docs/architecture/telemetry/BKL-029-SQM-Source-Discovery-and-Architecture-Contract.md` | SQM source/quality semantics and provenance rules | repository architecture authority | semantic authority for interpretation of SQM evidence |
| 9 | `docs/architecture/integration/AP14-W06-PixInsight-Synchronization-Adapter.md` | processing manifest/import/reconciliation boundary | repository architecture authority | semantic authority for processing synchronization and candidate-vs-reconciled state |
| 10 | `.github/scripts/pixinsight-manifest.mjs`, `.github/scripts/pixinsight-ledger.mjs`, `.github/scripts/pixinsight-reconciliation.mjs` and `.github/scripts/pixinsight-processing-projection.mjs` | executable governed manifest/ledger/reconciliation/processing-projection contracts | governed processing projection/tooling | processing provenance source only after reconciliation succeeds |
| 11 | `docs/data/knowledge-ai-evidence-contract.json` and `docs/data/knowledge-ai-read-model.json` | Citation, Provenance, Confidence, lifecycle and consumer-preservation semantics | repository governance authority/projection | mandatory cross-cutting BKL-044 rules; no target facts sourced here |

### 3.1 Source precedence by fact class

Precedence is **fact-class specific**, not a universal ranking across all domains:

- session identity and session-bound target evidence: source 1, then source 6 as supporting evidence; source 2 is discovery-only;
- target/project/session conceptual relation meaning: source 3;
- asset relation meaning and asset identity semantics: sources 4;
- observation index/catalog semantics: source 5;
- per-session SQM/setup evidence: source 6; source 7 is downstream aggregate/read optimization; source 8 defines SQM semantics;
- processing provenance: source 9 plus source 10 after successful governed reconciliation;
- Citation/Provenance/Confidence/lifecycle semantics: source 11.

A lower-precedence projection may add discoverability or derived summaries but must not overwrite a conflicting higher-precedence fact.

## 4. Non-sources / prohibited authority promotion

The following must not become authoritative merely because BKL-035 can read them:

- UI labels or free-text search summaries;
- inferred aliases generated only from string similarity;
- AI-generated target classifications or recommendations;
- PixInsight candidate/import payloads before governed reconciliation;
- static documentation examples;
- filenames when a governed catalog identifier exists;
- browser/client state;
- external catalog data not separately governed and cited.

## 5. Canonical target identity

BKL-035 introduces a **Target Knowledge Identity** as a projection key, not a replacement scientific catalog.

Required shape:

- `target_key` — stable repository-local projection key;
- `canonical_name` — deterministically selected from governed source evidence;
- `aliases[]` — governed aliases with explicit source/citation;
- `identity_state` — `validated`, `conflicted`, `incomplete`, or `unknown`;
- `source_refs[]` — references to source records supporting identity;
- `citation_refs[]` — BKL-044 compliant citations;
- `provenance_refs[]` — required when identity is derived by normalization/reconciliation.

### 5.1 Deterministic identity-equivalence and precedence policy

Identity resolution is executed in this order and stops/fails closed when a higher-precedence rule conflicts:

1. **Governed exact object identifier**: when the accepted session/source record exposes a governed astronomical object/catalog identifier, exact normalized identifier equality is the strongest identity evidence. Different exact governed identifiers are never auto-merged.
2. **Governed coordinates associated with the same declared target**: coordinates may corroborate identity but cannot merge two different exact governed identifiers. Coordinate tolerance/epoch reconciliation is not authorized in F1; any required tolerance is a later governed method.
3. **Governed target name from the primary session source**: when no exact object identifier exists, `scientific-session-catalog.json` / its linked normalized session evidence provides the candidate canonical name.
4. **Downstream/index/analytics names**: observation-index titles, `sessions.csv target_name`, UI/search text and other read models may corroborate or provide aliases only; they cannot supersede source-1/source-6 evidence.
5. **Repository-local identity fallback**: when no external/catalog identifier exists but one or more governed session records contain the same deterministically normalized target name and no incompatible identifier/coordinate evidence exists, BKL-035 may create a repository-local `target_key`. The exact key encoding is deferred to F2, but the equivalence class is the normalized governed name plus its source record set, never free-text similarity.

### 5.2 Allowed name normalization

For identity comparison only, F1 permits deterministic normalization limited to:

- Unicode normalization;
- trim leading/trailing whitespace;
- collapse repeated internal whitespace to one ASCII space;
- case-insensitive comparison;
- normalize separator-only presentation differences such as `M27` vs `M 27` **only when a deterministic catalog-prefix plus numeric-token rule is explicitly encoded in F2 tests**.

F1 does **not** authorize fuzzy similarity, phonetic matching, semantic/AI matching, coordinate-nearness merging, prefix guessing, catalog crosswalk inference or removal of arbitrary punctuation that could change scientific identity.

The original source spelling remains preserved as evidence even when a normalized comparison form is used.

### 5.3 Identity-state decision table

| State | Deterministic condition |
|---|---|
| `validated` | all material governed evidence in the bounded source set is compatible; at least one source reference and Citation exist; no competing exact governed identifier exists; any alias relation is justified by the allowed deterministic normalization or the same exact governed identifier |
| `incomplete` | a candidate target can be formed from governed evidence but required supporting fields/relations for the current increment are missing; there is no contradictory evidence |
| `conflicted` | two or more governed records in scope provide incompatible exact identifiers or materially incompatible identity evidence; no automatic merge or precedence override is allowed |
| `unknown` | evidence is insufficient to form even a stable repository-local equivalence class, or the source explicitly reports target identity as unknown/absent |

### 5.4 Collision and disagreement rules

- two candidate identities that generate the same future `target_key` but carry incompatible governed identifiers must fail validation and become explicit conflict evidence;
- different exact governed identifiers are never collapsed because names normalize alike;
- a display/index/analytics label cannot resolve a conflict in primary governed evidence;
- when authoritative sources for different fact classes disagree on a fact outside their authority, BKL-035 preserves both source facts and marks the relevant projection relation/identity `conflicted` or `incomplete`; it does not choose a winner by file order;
- no automatic alias relation is created from string similarity alone;
- collision resolution requires a later governed reconciliation rule plus Citation/Provenance and cannot be silently implemented in F2.

### 5.5 Canonical-name selection

For a non-conflicted equivalence class, `canonical_name` is selected deterministically:

1. name attached to the highest-precedence exact governed object identifier, if such an identifier is present and the name is available in the same governed record;
2. otherwise the target name in the earliest source-1 session record in deterministic ascending `session_id` order;
3. downstream names that differ only by allowed normalization become aliases; materially different names remain unresolved/conflicted until separately governed.

This rule selects a projection label only; it does not change the underlying scientific source.

## 6. Core relation semantics

The initial BKL-035 relation vocabulary is intentionally small:

- `TARGET_HAS_SESSION` — target projection to governed observation session;
- `TARGET_HAS_SQM_EVIDENCE` — target/session to SQM evidence applicable to that session;
- `TARGET_USES_SETUP` — target/session to governed telescope/camera/filter/setup facts;
- `TARGET_HAS_ASSET` — target/session to scientific asset identity governed by AP-013;
- `TARGET_HAS_PROCESSING_PROVENANCE` — target/asset to reconciled processing provenance;
- `TARGET_ALIAS_OF` — governed alias relation within one target identity;
- `TARGET_IDENTITY_CONFLICT` — explicit unresolved identity conflict.

Relations are projection facts. They must carry source/citation/provenance information sufficient to trace them back to the governed source record.

`TARGET_HAS_SQM_EVIDENCE` is session-scoped in F1/F2. A target-wide SQM statistic is a later derived fact and must declare method, inputs, Citation and Provenance.

`TARGET_HAS_ASSET` and `TARGET_HAS_PROCESSING_PROVENANCE` are valid only when the referenced AP-013/AP14-W06 record is in an acceptable reconciled/governed state; candidate or unresolved import payloads are excluded.

## 7. Observation vs derivation boundary

### Direct/source-backed facts

Examples include session identifier, source target label, telescope, camera, filter, integration metadata, SQM metric and reconciled processing manifest identity when present in governed source records.

### Derived facts

Examples include normalized target key, cross-session target grouping, alias reconciliation and aggregate target statistics. Derived facts must:

- remain `projection` authority;
- identify the derivation method;
- preserve input references;
- expose Citation and Provenance;
- fail closed when source evidence conflicts or is incomplete.

Confidence is not mandatory for every target identity. If F2 or later represents confidence/quality, it must resolve a versioned BKL-044 Confidence contract and must not invent confidence merely to satisfy schema shape.

## 8. Bounded F1 seed strategy

F1 authorizes only a small proof set for contract validation. Maximum initial seed:

- up to 5 target identities;
- up to 10 session relations total;
- exact sources only from the ordered inventory in section 3 on the accepted baseline;
- no external catalog enrichment;
- no broad repository ingestion.

The initial seed must include at least one normal validated identity and one incomplete/conflicted/unknown case if such evidence exists in current governed data. Missing conflict evidence must not be manufactured merely to satisfy coverage.

## 9. Fail-closed rules

Validation must reject:

1. target identity without source reference;
2. validated identity without Citation;
3. alias merge without the deterministic rules/evidence in section 5;
4. relation to an unresolved session/asset/provenance record;
5. source-authority escalation;
6. loss of BKL-044 semantic/lifecycle state;
7. duplicate/colliding target keys resolving to incompatible governed identities;
8. broad seed expansion beyond configured bounds;
9. synthesized SQM/setup/processing facts not present in governed sources;
10. external facts lacking separate governance and citation;
11. source-family labels that cannot resolve to the exact inventory paths in section 3;
12. use of observation index, analytics history or UI/search text to override primary source evidence;
13. automatic merging of different exact governed identifiers;
14. fuzzy/AI/coordinate-nearness identity merge not explicitly governed by a later approved method.

## 10. Security and safety boundary

BKL-035 F1 is repository-only and read-only. It introduces no EAGLE runtime code, hardware command path, automatic remediation, scheduling authority, roof/interlock control, weather Safety Authority decision or protected-source bypass.

Target knowledge may support future planning/advisory capabilities, but it cannot by itself authorize an observatory action.

## 11. Operational and observability impact

Runtime observability is Not Applicable for F1. Repository validation must provide deterministic diagnostics for unresolved identities, missing relations, alias conflicts, bounds violations and source drift.

## 12. Migration strategy

F1 is additive:

1. keep all accepted source datasets unchanged;
2. define target projection semantics separately;
3. build a bounded fixture in F2 only after F1 review;
4. add deterministic reconciliation before any wider projection;
5. add API/UI consumer work only after machine-readable projection acceptance.

Rollback is repository revert; no scientific or runtime data migration is required.

## 13. Proposed increments

- **F1 — Source Discovery & Semantic Contract:** current.
- **F2 — Machine-Readable Target Identity/Relation Schema + bounded fixture.**
- **F3 — Deterministic Source Reconciliation and conflict/alias validation.**
- **F4 — Target Knowledge consumer/read-model projection and closure.**

No persistent graph/vector/RAG technology decision is implied by these increments.

## 14. Acceptance criteria for F1

F1 is acceptable when:

1. exact canonical source paths/record keys and authority roles are explicitly separated;
2. canonical target identity, deterministic precedence/equivalence and alias rules are defined;
3. session/SQM/setup/asset/processing relation semantics are defined;
4. observation vs derived boundaries are explicit;
5. BKL-044 Citation/Provenance/Confidence/authority rules are inherited;
6. bounds and fail-closed criteria are documented;
7. no second source of truth or runtime/safety authority is introduced;
8. documentation/CI gates pass;
9. independent architecture re-review approves the semantic model before F2.

## 15. Open decisions for later increments

- exact machine-readable `target_key` encoding syntax, provided F2 implements the equivalence/precedence policy in section 5 exactly;
- whether a future external astronomical catalog adapter is useful and under what authority/access contract;
- aggregate statistic definitions across heterogeneous sessions;
- API/UI shape for target-centric navigation;
- persistent storage technology, if ever justified.

These decisions are intentionally deferred and are not required to accept F1.

## 16. ARB remediation traceability

| Finding | Remediation |
|---|---|
| M-01 — source inventory not deterministic enough | Section 3 now defines an ordered bounded set of exact canonical paths, record keys, authority roles and precedence by fact class. |
| M-02 — identity/alias precedence under-specified | Section 5 now defines exact-identifier precedence, allowed normalization, repository-local fallback, state conditions, collision/disagreement behavior and canonical-name selection. |
| O-01 — Confidence semantics | Section 7 clarifies Confidence is optional but, when represented, must use the versioned BKL-044 contract. |
| O-02 — SQM scope | Section 6 fixes SQM evidence to session scope; target-wide statistics remain later derived facts. |
| O-03 — asset/processing reconciliation | Section 6 requires acceptable governed reconciliation before asset/processing relations are emitted. |

## 17. Decision

Proceed with a target-centric **projection over exact existing governed sources**, not a new catalog authority. BKL-035 F1 remediation is ready for exact-head CI and independent ARB re-review.