# BKL-045 F4 — Provenance Reconciliation Adapter

**Status:** In development  
**Package:** BKL-045 — PixInsight Workflow Provenance Plugin  
**Authority boundary:** AP-013 / AP-014 remain authoritative; PixInsight is processing evidence only.

## Objective

F4 connects the accepted F3 provenance sidecar contract to the existing AP14-W06 PixInsight Synchronization Adapter without creating a parallel catalog or provenance path.

The vertical slice is:

`PixInsight provenance sidecar -> deterministic candidate manifest -> existing manifest validation/idempotency -> read-only reconciliation -> derived processing projection`.

## Mapping rules

1. `authority` must be `processing_evidence` and `actionAuthority` must be `NONE`.
2. `PXP-*` capture identity is deterministically mapped to `PXM-*`; capture time is preserved.
3. Missing optional observation identifiers are mapped to the existing manifest vocabulary `unknown`; they are never inferred.
4. Only sidecar steps classified `OBSERVED` may populate `processingRun.processes`.
5. `DECLARED` steps remain counted evidence metadata and are never promoted to observed process evidence.
6. Asset references use an existing resolved `assetId` when present, otherwise the explicit source reference; no fuzzy matching is introduced.
7. `capture.completeness`, limitations and evidence counts are carried as non-authoritative manifest parameters so downstream consumers cannot lose the F3 evidence boundary.
8. `UNAVAILABLE` remains fail-closed: an empty process list is valid evidence of unavailable history, not proof that no processing occurred.

## Reconciliation boundary

The adapter output enters the existing AP14-W06 contract and `PixInsightReconciliationService`. Reconciliation remains exact/read-only against AP-014 session identifiers and AP-013 asset identifiers. `matched`, `partially-matched`, `unresolved`, `conflict`, `rejected` and `duplicate-noop` retain their existing meanings.

No F4 component may:

- write AP-013 asset identity, checksum, storage locator or authoritative provenance;
- promote a session, processing run or output to accepted;
- execute PixInsight processing;
- issue observatory/device commands;
- turn DECLARED/SUGGESTED information into OBSERVED evidence;
- infer missing historical processing.

## Acceptance criteria

F4 is acceptable when automated evidence demonstrates that:

- the F3 sidecar maps deterministically to a valid AP14-W06 candidate manifest;
- the real F3-B `UNAVAILABLE` case produces zero observed processes and preserves limitations;
- DECLARED steps are not promoted;
- action authority is rejected;
- existing manifest validation, idempotency, read-only reconciliation and processing-projection tests remain green;
- repository documentation and governance checks are green.

This increment does **not** close the known PixInsight complete-history observation gap. A future richer native-history adapter requires separate runtime evidence and governance under ADR-008.
