# CAP-002 - Test Plan

## Purpose

Il test plan definisce verifiche documentali e funzionali future per Observation Scheduling. Non implementa test automatici e non prescrive tooling.

## Test Scope

Incluso:

- functional tests;
- scheduling rule tests;
- conflict resolution tests;
- recovery tests;
- acceptance tests;
- regression tests documentali.

Escluso:

- codice di test;
- framework di test;
- simulazioni non documentate;
- criteri non tracciati a requisiti.

## Functional Tests

| ID | Test | Requirement | Expected Result |
|---|---|---|---|
| `OSD-FT-001` | Create schedule from valid Observation Request. | `OSD-FR-001` | Schedule created in Draft/Candidate with traceability. |
| `OSD-FT-002` | Link schedule to Target Registry entry. | `OSD-FR-002` | Target reference present or suspension reason recorded. |
| `OSD-FT-003` | Evaluate astronomical window. | `OSD-FR-003` | Candidate window has start, end and constraints. |
| `OSD-FT-004` | Validate resource availability. | `OSD-FR-004` | Allocation is valid or conflict is created. |
| `OSD-FT-005` | Publish approved schedule to CAP-001. | `OSD-FR-008` | Published schedule contains handover evidence. |

## Scheduling Rule Tests

| ID | Test | Requirement | Expected Result |
|---|---|---|---|
| `OSD-SRT-001` | Reject publication without weather validation. | `OSD-FR-005` | Schedule remains not published. |
| `OSD-SRT-002` | Reject publication without safety validation. | `OSD-FR-005` | Schedule remains not published. |
| `OSD-SRT-003` | Apply priority resolution to competing requests. | `OSD-FR-007` | Decision rationale recorded. |
| `OSD-SRT-004` | Preserve previous schedule state after update. | `OSD-OR-001` | Historical evidence remains available. |

## Conflict Resolution Tests

| ID | Test | Requirement | Expected Result |
|---|---|---|---|
| `OSD-CRT-001` | Resource double booking conflict. | `OSD-FR-006` | Conflict Record created. |
| `OSD-CRT-002` | Target not observable in selected window. | `OSD-FR-003` | Schedule returns to Candidate or Conflict. |
| `OSD-CRT-003` | Weather window lost before handover. | `OSD-OR-003` | Weather Window Lost runbook applies. |
| `OSD-CRT-004` | Priority conflict unresolved. | `OSD-FR-007` | Schedule cannot be approved. |

## Recovery Tests

| ID | Test | Requirement | Expected Result |
|---|---|---|---|
| `OSD-RT-001` | Recover schedule after source evidence unavailable. | `OSD-AR-002` | Schedule moves to recovery or not published. |
| `OSD-RT-002` | Resource becomes unavailable after approval. | `OSD-OR-003` | Resource Unavailable runbook applies. |
| `OSD-RT-003` | Schedule recovery after cancellation candidate. | `OSD-OR-002` | Recovery evidence and new decision recorded. |

## Acceptance Tests

| ID | Test | Acceptance Link | Expected Result |
|---|---|---|---|
| `OSD-AT-001` | End-to-end request to published schedule. | `OSD-AC-001` | Complete traceable schedule package. |
| `OSD-AT-002` | Safety override over priority. | `OSD-AC-006` | Unsafe schedule not approved/published. |
| `OSD-AT-003` | Registry and release evidence complete. | `OSD-AC-012` | CAP-000 and REL-000 references available. |

## Regression Tests

- Existing CAP-001 links remain valid.
- CAP-000 navigation and status remain internally consistent.
- REL-000 governance language remains unchanged except CAP-002 reference.
- Mermaid diagrams render with supported syntax.
- No duplicate requirement or ADR identifiers exist in CAP-002.

## Exit Criteria

Testing is acceptable when:

- all requirements have at least one mapped test or acceptance criterion;
- all runbooks have at least one recovery scenario;
- all SOP are referenced by process or traceability;
- all validation findings are recorded before release movement.
