# BKL-015 — Knowledge Graph Machine-Readable Foundation

**Identifier:** BKL-015-F1  
**Status:** Proposed  
**Version:** 0.1  
**Date:** 2026-09-04  
**Capability:** Repository Knowledge Graph foundation  
**Depends on:** BKL-029, BKL-030, Governance Foundation  
**Precedes:** BKL-044, BKL-035, BKL-040, BKL-014/AP-015

## 1. Purpose

BKL-015 introduces the minimum machine-readable Knowledge Graph contract needed to make repository architecture traceability queryable without replacing the authoritative sources already present in Digital StarGate.

The first increment is deliberately repository-centric. It models stable identities and typed relations for architecture/governance artifacts and establishes a validation gate. Scientific/AI evidence semantics are deferred to BKL-044.

## 2. Scope

F1 includes:

- stable entity identifiers;
- typed and versioned relations;
- source/citation locators back to authoritative repository artifacts;
- explicit authority and lifecycle metadata;
- a JSON Schema contract;
- an initial repository graph projection;
- deterministic validation for referential integrity, relation vocabulary and source locators.

F1 does **not** include:

- graph database selection;
- vector database, embeddings or RAG;
- AI claim/confidence semantics;
- automatic inference;
- mutation of authoritative repository sources from the graph;
- runtime EAGLE changes;
- Safety Authority or remediation functions.

## 3. Architectural Drivers

1. Resolve TD-008 by making AP/ADR/component/evidence traceability machine-readable.
2. Preserve GitHub documents, catalogs and registries as authoritative sources.
3. Provide a stable semantic foundation for BKL-044 and future Scientific Knowledge Layer work.
4. Prevent silent drift through CI validation.
5. Keep technology choice separate from the semantic contract.

## 4. Current State

Traceability exists primarily in Markdown tables, cross-references, architecture reviews, evidence documents and generated projections. Those links are useful to humans but are not consistently queryable as typed repository relations.

The approved Scientific Knowledge Layer vision already requires stable Knowledge Entities, typed/versioned Knowledge Relations, provenance and citation locators while keeping projections non-authoritative.

## 5. Target State

The repository contains a versioned graph projection with this shape:

```text
Authoritative repository artifacts
        |
        | deterministic extraction/curation
        v
Knowledge Graph projection
  - entities[]
  - relations[]
  - source locators
  - schema/version metadata
        |
        +--> CI referential-integrity validation
        +--> future query/projection adapters
        +--> BKL-044 scientific/AI evidence extension
```

The graph is a projection. If graph content conflicts with an authoritative artifact, the authoritative artifact wins and the graph must be regenerated or corrected.

## 6. Foundation Contract

### 6.1 Entity identity

Every entity MUST have:

- `id`: stable repository identifier;
- `type`: controlled vocabulary value;
- `title`: human-readable label;
- `status`: lifecycle status when applicable;
- `authority`: authority class for the represented fact;
- `source_locator`: repository-relative citation locator.

F1 entity types are:

- `architecture_package`;
- `adr`;
- `component`;
- `evidence`;
- `backlog_item`;
- `technical_debt`;
- `capability`.

Additional types require contract versioning and review.

### 6.2 Relation identity

Every relation MUST have:

- `id`: deterministic stable identifier;
- `type`: controlled relation vocabulary;
- `from`: existing entity ID;
- `to`: existing entity ID;
- `source_locator`: evidence for the relation;
- `version`: relation contract version.

F1 relation types are:

- `depends_on`;
- `implements`;
- `governs`;
- `addresses`;
- `evidenced_by`;
- `documents`;
- `supersedes`;
- `relates_to`.

The generic `relates_to` is allowed only when a more specific F1 relation cannot be supported by repository evidence. Its use should decrease over time.

### 6.3 Source locator

`source_locator` is repository-relative and MUST point to a tracked source artifact. Optional `anchor` and `line_hint` values may improve human navigation but are not authority by themselves.

### 6.4 Authority

F1 authority values:

- `repository_authority` — approved architecture/governance source;
- `evidence_authority` — accepted validation/runtime evidence;
- `projection` — derived view, never source authority.

The graph root MUST declare `authority = projection`.

## 7. Rules and Constraints

- No dangling relation endpoints.
- Entity IDs are unique.
- Relation IDs are unique.
- Relation vocabulary is closed by the schema version.
- Every entity and relation has a source locator.
- A projection cannot silently promote itself to authority.
- Missing or conflicting source evidence is represented as a validation failure or future knowledge-conflict record; it is not auto-resolved.
- No AI inference is stored as fact in BKL-015 F1.
- No health, safety or remediation decision is derived by this foundation.

## 8. Migration Strategy

1. Establish the contract and seed projection using high-value governance/architecture nodes.
2. Add deterministic CI validation.
3. Expand coverage across AP, ADR, components and evidence without changing the contract unnecessarily.
4. Introduce query adapters only after graph quality is measurable.
5. Hand off to BKL-044 for scientific claim/evidence and AI provenance semantics.

The migration is additive and reversible: deleting the projection does not alter authoritative repository artifacts.

## 9. Security, Safety and Operations

The graph is read-only with respect to observatory runtime systems. It contains repository metadata and references, not operational credentials. It must not contain secrets, bearer tokens or private runtime values.

Operational diagnostics for F1 are CI validation results: schema validity, duplicate IDs, dangling relations, unsupported vocabulary and invalid source locators.

No EAGLE Scheduled Task, Cloud Run service or Safety Authority component is changed by BKL-015 F1.

## 10. Risks and Trade-offs

| Risk | Mitigation |
|---|---|
| Entity/relation proliferation | Closed F1 vocabularies and versioning |
| Graph drifts from Markdown authority | CI source-locator and integrity validation |
| Premature graph technology lock-in | JSON projection first; storage technology deferred |
| Generic relationships reduce semantic value | `relates_to` permitted only as fallback |
| Future AI semantics contaminate factual graph | BKL-044 remains a separate contract |
| Historical metadata is incomplete | Missing coverage is explicit; no invented edges |

## 11. Traceability

- Backlog: `BKL-015`.
- Technical debt: `TD-008`.
- Vision: `docs/architecture/scientific-knowledge-layer-vision.md`.
- Roadmap authority: `.github/roadmap/roadmap-source.json`.
- Successor contract: `BKL-044 Knowledge Graph / AI Evidence Contract`.

## 12. Acceptance Criteria

F1 is accepted when:

1. the JSON Schema is versioned and valid;
2. the committed graph projection validates against the F1 structural rules;
3. duplicate entity/relation IDs fail CI;
4. dangling relation endpoints fail CI;
5. unsupported entity/relation types fail CI;
6. source locators are repository-relative and resolve to tracked files;
7. the projection declares itself non-authoritative;
8. TD-008 has measurable progress and is not closed until required AP/ADR/component/evidence coverage is demonstrated;
9. BKL-044 semantics are not implemented implicitly;
10. MkDocs strict build and repository quality gates remain green.

## 13. Open Issues

- Coverage threshold required before TD-008 can move to Resolved.
- Whether later extraction is curated, generated, or hybrid.
- Whether relation IDs should remain deterministic strings or move to content-derived identifiers.
- Query API shape for later portal/analytics consumers.
- Technology choice for AP-015 materialization.

## 14. Future Evolution

BKL-044 will extend this foundation with richer evidence provenance, scientific claims, AI recommendation provenance and confidence semantics. AP-015 may later select a graph/document/hybrid materialization strategy without changing the fundamental authority boundary established here.
