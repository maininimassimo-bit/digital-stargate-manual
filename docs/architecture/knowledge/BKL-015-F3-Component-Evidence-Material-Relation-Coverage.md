# BKL-015 F3 — Component, Evidence and Material Relation Coverage

| Field | Value |
|---|---|
| Identifier | BKL-015-F3 |
| Status | Proposed |
| Version | 0.1 |
| Date | 2026-09-05 |
| Parent | BKL-015 |
| Addresses | TD-008 |
| Authority | Repository documentation; this package defines a projection and validation contract |

## Purpose

Extend BKL-015 from AP/ADR identity coverage to measurable component, evidence and material-relation coverage using the existing Architecture Traceability Register as repository authority.

## Repository truth

F2 established 100% identity coverage for the governed AP and ADR inventories. The Architecture Traceability Register already exposes an Architecture Artifact Register containing stable artifact IDs, package ownership and evidence/review classification. F3 consumes that register rather than inventing a second inventory.

## Governed inventory

For F3, every row in `docs/architecture/traceability-register.md` section `Architecture Artifact Register` is governed as follows:

- IDs beginning with `ARB-` are projected as `evidence` entities;
- all other registered architecture artifacts are projected as `component` entities;
- the `Package` column is the authoritative material association for this increment;
- component-to-package association is represented by `documents`;
- package-to-review association is represented by `evidenced_by`.

The Knowledge Graph remains a non-authoritative projection. The register remains authoritative.

## Coverage thresholds

F3 is accepted only when both metrics are 100% for the governed Architecture Artifact Register:

1. **Artifact identity coverage** — every registered row has an entity of the expected type.
2. **Material relation coverage** — every registered row has the required typed relation to its declared package.

The validator fails closed on missing identities, wrong entity types, missing package endpoints, missing relations or an undiscoverable/empty register.

## CI reconciliation

`.github/scripts/verify-knowledge-graph-material-relations.mjs` derives the inventory directly from the register and reconciles it against `docs/data/knowledge-graph.json`. Developer Foundation executes this validator after the base Knowledge Graph integrity and AP/ADR coverage gates.

## Boundaries

F3 does not introduce a graph database, vector database, RAG, AI inference, scientific claim/confidence semantics, runtime telemetry, EAGLE changes, Safety Authority changes, command/remediation paths or cleanup authorization. BKL-044 remains the owner of the future AI Evidence Contract.

## TD-008 disposition

Passing F3 materially advances TD-008 by proving machine-readable identity and material relations for the governed architecture artifact/review register. TD-008 MUST remain open until independent architecture/release-quality review confirms that the combined F1/F2/F3 coverage is sufficient for closure and no material traceability class remains outside the governed inventories.

## Acceptance criteria

- Architecture Artifact Register is the single F3 inventory authority.
- 100% artifact identity coverage.
- 100% material relation coverage.
- Existing F1 schema/integrity validation remains green.
- Existing F2 AP/ADR coverage remains green.
- F3 validator runs in Developer Foundation.
- Independent ARB and Release Quality review completed before merge.
- BKL-044 boundary remains intact.
