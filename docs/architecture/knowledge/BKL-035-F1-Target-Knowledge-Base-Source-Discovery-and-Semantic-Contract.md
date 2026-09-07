# BKL-035 F1 — Target Knowledge Base Source Discovery & Semantic Contract

| Field | Value |
|---|---|
| Identifier | BKL-035-F1 |
| Status | In Progress |
| Version | 0.1 |
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

## 3. Source discovery inventory

| Source | Role for BKL-035 | Authority classification | F1 disposition |
|---|---|---|---|
| `docs/data/scientific-session-catalog.json` | session-level scientific facts and metadata | governed scientific projection | primary session source |
| `docs/data/scientific-observation-index.json` | searchable target/session projection generated from session catalog | projection | discovery/read optimization only |
| AP-013 scientific asset contracts / DSDM model | scientific target/project/session/asset conceptual lineage | repository architecture authority | semantic authority for asset relations |
| AP-014 catalog/search contracts | observation catalog identity, search and reconciliation | repository architecture authority | semantic authority for observation indexing |
| BKL-029 SQM contracts/history | sky-quality facts and session-linked SQM metrics | governed telemetry/scientific projection | environmental evidence source |
| AP14-W06 PixInsight manifest/reconciliation | processing manifest, ledger and processing projection | governed processing projection | processing provenance source |
| BKL-044 evidence/read-model contracts | evidence semantics, citation, provenance, confidence, authority boundaries | repository governance authority | mandatory cross-cutting semantic rules |

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
- `canonical_name` — selected from governed source evidence;
- `aliases[]` — governed aliases with explicit source/citation;
- `identity_state` — `validated`, `conflicted`, `incomplete`, or `unknown`;
- `source_refs[]` — references to source records supporting identity;
- `citation_refs[]` — BKL-044 compliant citations;
- `provenance_refs[]` — required when identity is derived by normalization/reconciliation.

### 5.1 Identity rules

1. exact governed identifiers are preferred over display names;
2. normalization may remove formatting differences but must not merge scientifically distinct objects;
3. an alias is not accepted only because text similarity is high;
4. conflicting names/identifiers remain explicit and block `validated` identity;
5. unknown catalog identity remains `unknown` rather than inferred;
6. a target projection cannot overwrite the underlying session or asset source.

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

## 8. Bounded F1 seed strategy

F1 authorizes only a small proof set for contract validation. Maximum initial seed:

- up to 5 target identities;
- up to 10 session relations total;
- only repository/governed sources already present on the accepted baseline;
- no external catalog enrichment;
- no broad repository ingestion.

The initial seed must include at least one normal validated identity and one incomplete/conflicted/unknown case if such evidence exists in current governed data. Missing conflict evidence must not be manufactured merely to satisfy coverage.

## 9. Fail-closed rules

Validation must reject:

1. target identity without source reference;
2. validated identity without Citation;
3. alias merge without deterministic rule/evidence;
4. relation to an unresolved session/asset/provenance record;
5. source-authority escalation;
6. loss of BKL-044 semantic/lifecycle state;
7. duplicate target keys resolving to incompatible governed identities;
8. broad seed expansion beyond configured bounds;
9. synthesized SQM/setup/processing facts not present in governed sources;
10. external facts lacking separate governance and citation.

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

1. authoritative and projection sources are explicitly separated;
2. canonical target identity and alias rules are defined;
3. session/SQM/setup/asset/processing relation semantics are defined;
4. observation vs derived boundaries are explicit;
5. BKL-044 Citation/Provenance/Confidence/authority rules are inherited;
6. bounds and fail-closed criteria are documented;
7. no second source of truth or runtime/safety authority is introduced;
8. documentation/CI gates pass;
9. independent architecture review approves the semantic model before F2.

## 15. Open decisions for later increments

- exact machine-readable target key encoding;
- whether a future external astronomical catalog adapter is useful and under what authority/access contract;
- aggregate statistic definitions across heterogeneous sessions;
- API/UI shape for target-centric navigation;
- persistent storage technology, if ever justified.

These decisions are intentionally deferred and are not required to accept F1.

## 16. Decision

Proceed with a target-centric **projection over existing governed sources**, not a new catalog authority. BKL-035 F1 is ready for exact-head CI and independent architecture review.