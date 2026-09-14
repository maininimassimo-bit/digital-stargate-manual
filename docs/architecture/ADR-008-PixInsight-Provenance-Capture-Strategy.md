# ADR-008 — PixInsight Provenance Capture Strategy

**Status:** Accepted — applied by BKL-045 F3/F4 and closure; native successor planned by BKL-049  
**Date:** 09/09/2026  
**Decision owner:** Digital StarGate Architecture  
**Related package:** BKL-045 F2  

## Context

BKL-045 requires reproducible, machine-readable PixInsight processing provenance while preserving the accepted AP-013/AP-014 authority boundaries. F1 established that processing facts are classified as `OBSERVED`, `DECLARED` or `SUGGESTED`, and that missing provenance must never be reconstructed as observed fact.

The repository already has AP14-W06 synchronization, a PixInsight manifest schema, deterministic validation/digest, ledger, reconciliation and processing projection. The missing capability is detailed workflow capture.

Three mechanisms were assessed:

1. native PCL module;
2. governed PJSR script/package;
3. hybrid native-evidence capture plus governed exporter.

## Decision

Digital StarGate will use a **hybrid provenance capture strategy** for the first BKL-045 implementation.

### Observed evidence

PixInsight-native Project/processing-history artifacts are the preferred source for `OBSERVED` workflow evidence when the relevant fields are present and can be validated.

No field is promoted to `OBSERVED` solely because it is plausible or can be inferred from an output image.

### Governed exporter

A local governed PixInsight script/package will provide the controlled export boundary. Its responsibilities are limited to:

- correlate the workflow with Digital StarGate session/asset identifiers;
- collect supported native evidence and source locators;
- record explicit user `DECLARED` operations/notes;
- capture bounded environment/version metadata;
- generate a versioned deterministic provenance sidecar;
- validate the sidecar before handoff;
- pass the sidecar through the existing AP14-W06 validation/reconciliation path.

The exporter is not authoritative for scientific-asset identity/checksum/lifecycle and cannot directly accept or mutate catalog records.

### Native module

A PCL native module is **deferred**, not prohibited. It may be introduced only through a later ADR amendment if real F3 evidence demonstrates a required provenance-observation capability that cannot be implemented safely and maintainably with native history/project evidence plus the governed exporter.

## Rationale

The hybrid strategy provides the best balance between evidence fidelity and operational simplicity:

- PixInsight itself persists project/history context, so that evidence can remain the source for facts actually captured by PixInsight;
- a PJSR package is appropriate for explicit export, correlation and manual declarations;
- a script-only implementation would risk claiming complete observation where universal process interception has not been proven;
- a native C++ module would impose significant build/version/maintenance cost before a concrete need for that depth of integration has been demonstrated;
- the strategy reuses AP14-W06 rather than introducing a parallel ingestion authority.

## Consequences

### Positive

- local-first provenance capture;
- clear mapping between source evidence and `OBSERVED` claims;
- explicit support for manual `DECLARED` steps;
- deterministic sidecar boundary suitable for Git/repository governance;
- minimal coupling to PixInsight native module ABI/API;
- straightforward rollback: disable/remove exporter without changing PixInsight image-processing capabilities.

### Negative / trade-offs

- F3 must validate which history/project fields are actually extractable;
- capture completeness can vary by native process, script or third-party module;
- incomplete histories must be represented as incomplete rather than silently filled;
- more than one bounded source adapter may eventually be needed.

## Authority boundaries

- AP-013 remains authoritative for scientific asset identity, checksum, storage locator and lifecycle.
- AP-014/AP14-W06 remains the synchronization and reconciliation boundary.
- PixInsight is a processing-evidence source, not a Digital StarGate catalog authority.
- `SUGGESTED` AI/advisor steps are never part of executed provenance until separately supported by `OBSERVED` or `DECLARED` evidence.
- no observatory Safety Authority, device command path or autonomous image-processing authority is introduced.

## Failure behavior

- missing history => provenance marked incomplete/unavailable, not reconstructed;
- unsupported process => retain bounded identifier/source evidence and explicit unresolved detail state;
- invalid sidecar => reject/quarantine before reconciliation;
- unresolved asset correlation => no authoritative link is created;
- exporter failure => PixInsight processing remains unaffected and no partial catalog mutation occurs.

## Validation obligations

F3 must produce real evidence for:

1. at least one ordered processing history;
2. process identifiers and parameter availability;
3. scripts/third-party behavior;
4. masks/reference relationships where exposed;
5. deterministic repeated export;
6. manual `DECLARED` steps;
7. incomplete-history fail-closed behavior;
8. no image mutation caused by export.

## Rejected alternatives

### Native PCL module as first implementation

Rejected for the initial release because its complexity and compatibility burden are not justified by a proven requirement for deeper integration.

### PJSR script/package as the sole evidence authority

Rejected because the repository and technical evidence do not prove universal observation of arbitrary PixInsight process execution from a script-only layer.

## Planned native successor — BKL-049 (14/09/2026)

The retained BKL-045 F3-B evidence demonstrated the essential gap anticipated by this ADR: the governed PJSR probe produced repeatable evidence but could not automatically observe an ordered processing history and therefore correctly reported `completeness=UNAVAILABLE` with zero observed steps.

That evidence activates the native-module revisit path. BKL-049 now plans an end-to-end PCL native capability with the following intent:

- automatically observe every process execution and relationship that the supported PixInsight/PCL interfaces can expose;
- preserve ordered process identifiers, versions, parameters, inputs, outputs, masks, references and environment context;
- maintain a crash-resilient local journal and deterministic export to the existing PXP/AP14-W06 boundary;
- correlate evidence with Digital StarGate sessions and scientific assets without taking catalog authority;
- publish a sanitized, read-only workflow archive and step-by-step visualization in the portal;
- represent unsupported, opaque or missing activity explicitly as `PARTIAL` or `UNAVAILABLE`, never as inferred `OBSERVED` evidence.

BKL-049 is `Planned`, not current and not implemented. The accepted hybrid exporter remains the operational baseline until a future BKL-049 increment passes SDK/licensing feasibility, detailed architecture, real PixInsight OAT, independent review and governed release acceptance. This planning amendment does not authorize code, installation, catalog writes, image mutation, autonomous processing, AI apply or Safety Authority.

## Revisit triggers

Reconsider this ADR if:

- PixInsight introduces a stable supported history/event API that materially changes the trade-off;
- F3 demonstrates an essential provenance gap requiring PCL;
- Project/history persistence semantics change incompatibly;
- a supported structured provenance API becomes available.
