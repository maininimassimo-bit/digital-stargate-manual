# BKL-015-F2 — Knowledge Graph Coverage & Reconciliation

| Field | Value |
|---|---|
| Identifier | BKL-015-F2 |
| Status | In Progress |
| Version | 0.1 |
| Date | 2026-09-05 |
| Parent | BKL-015 |
| Predecessor | BKL-015-F1 — Accepted |
| Technical debt | TD-008 — Knowledge Traceability |

## 1. Purpose

F2 turns the F1 machine-readable contract into measurable repository coverage. It reconciles canonical repository inventories with `docs/data/knowledge-graph.json` and fails CI when mandatory architectural identities are missing.

The graph remains a non-authoritative projection. Repository documents and governed datasets remain authoritative.

## 2. Scope

F2 covers:

- canonical Architecture Package inventory from `.github/roadmap/roadmap-source.json`;
- canonical ADR inventory from repository ADR files;
- graph coverage measurement by entity type;
- deterministic missing-ID reporting;
- CI enforcement of mandatory coverage thresholds;
- explicit evidence links for the accepted F1 increment.

## 3. Out of scope

F2 does not introduce:

- graph database, semantic database or vector database;
- embeddings, RAG or AI inference;
- scientific claim/confidence semantics governed by BKL-044;
- automatic creation of repository facts from inferred relationships;
- EAGLE, NINA, Cloud Run or observatory runtime changes;
- Safety Authority or remediation changes.

## 4. Coverage policy

### 4.1 Mandatory identity coverage

The F2 gate requires:

| Entity family | Canonical inventory | Threshold |
|---|---|---:|
| Architecture Package | roadmap source, IDs matching `AP-001`…`AP-015` | 100% |
| ADR | repository files named `ADR-*.md` under `docs/architecture` | 100% |

An entity is covered only when its ID is present in the graph with the correct F1 entity type and its source locator resolves inside the repository.

### 4.2 Measured but not closure-authoritative

`component`, `evidence`, `capability`, `backlog_item` and `technical_debt` entities remain measured by the graph integrity gate but do not yet have a repository-wide percentage threshold in F2.

This prevents a nominal AP/ADR identity inventory from being used to close TD-008 prematurely.

## 5. Reconciliation rules

1. Inventory is derived from repository truth, not duplicated as a hard-coded list in the validator.
2. Missing mandatory IDs fail the coverage gate.
3. Wrong entity type fails the coverage gate.
4. Extra graph entities are permitted when valid under F1.
5. Missing relations are reported separately from identity coverage and are not silently inferred.
6. Repository conflicts are surfaced; the graph does not choose a winner automatically.
7. Coverage success does not mean TD-008 is resolved.

## 6. F2 baseline

The initial reconciliation expands the F1 seed projection to include:

- AP-001 through AP-015;
- ADR-001 through ADR-007;
- F1 ARB and Release Quality evidence entities;
- explicit `evidenced_by` relations from the F1 contract increment.

## 7. TD-008 closure boundary

TD-008 MUST remain open after F2 unless a later reviewed increment defines and demonstrates sufficient repository-wide traceability across at least:

- architecture packages;
- ADRs;
- implementation components;
- governed evidence;
- the material relations connecting those entities.

F2 therefore resolves the ARB F1 condition about measurable AP/ADR coverage, but not the complete technical debt.

## 8. Acceptance criteria

F2 is acceptable when:

- AP canonical inventory is discovered from repository truth;
- ADR canonical inventory is discovered from repository truth;
- AP identity coverage is 100%;
- ADR identity coverage is 100%;
- missing/wrong-type entities cause non-zero validation exit;
- F1 integrity validation remains green;
- F1 evidence is represented explicitly;
- BKL-044 remains separate;
- MkDocs strict and repository quality gates are green;
- independent ARB and Release Quality reviews are recorded before merge.

## 9. Migration and rollback

F2 is additive and repository-only. Rollback consists of reverting the projection, coverage validator and documentation commits. No authoritative operational data is mutated.

## 10. Safety and security

No runtime integration, command path, credential, device operation, Safety Authority or remediation behavior is introduced.

## 11. Future evolution

A later BKL-015 increment may define component/evidence relation coverage sufficient to close TD-008. BKL-044 will separately govern scientific and AI evidence semantics.
