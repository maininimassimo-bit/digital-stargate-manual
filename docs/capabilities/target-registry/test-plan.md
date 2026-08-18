# CAP-TGT-001 - Test Plan

## Purpose

Il test plan definisce verifiche documentali e funzionali future per Target Registry. Non crea test automatici, codice o tooling.

## Registration Tests

| ID | Test | Requirement | Expected Result |
|---|---|---|---|
| `TGT-RT-001` | Register static deep-sky target. | `TGT-FR-001` | Target record created as Proposed. |
| `TGT-RT-002` | Register moving target reference. | `TGT-FR-005` | Target record includes moving-target metadata note. |
| `TGT-RT-003` | Register custom target. | `TGT-FR-005` | Custom target is clearly marked and traceable. |
| `TGT-RT-004` | Associate catalogue reference. | `TGT-FR-003` | Catalogue Reference linked without replacing canonical identity. |

## Identity Validation Tests

| ID | Test | Requirement | Expected Result |
|---|---|---|---|
| `TGT-IVT-001` | Resolve alias to existing target. | `TGT-FR-002` | Alias is linked and duplicate avoided. |
| `TGT-IVT-002` | Detect potential duplicate target. | `TGT-OR-003` | Duplicate Target runbook applies. |
| `TGT-IVT-003` | Unknown identifier cannot be resolved. | `TGT-OR-001` | Unresolved Identifier runbook applies. |
| `TGT-IVT-004` | Canonical identity remains stable after adding catalogue reference. | `TGT-QR-002` | Target ID and canonical identity persist. |

## Classification Tests

| ID | Test | Requirement | Expected Result |
|---|---|---|---|
| `TGT-CLT-001` | Classify galaxy target. | `TGT-FR-004` | Target Type and Scientific Classification recorded. |
| `TGT-CLT-002` | Classify comet or asteroid. | `TGT-FR-005` | Moving target classification recorded. |
| `TGT-CLT-003` | Classify custom target. | `TGT-FR-005` | Custom type metadata remains explicit. |

## Constraint Validation Tests

| ID | Test | Requirement | Expected Result |
|---|---|---|---|
| `TGT-CVT-001` | Validate coordinates and epoch. | `TGT-FR-006` | Coordinates become validated or invalid runbook applies. |
| `TGT-CVT-002` | Record observation constraints. | `TGT-FR-007` | Constraints available to CAP-SCH-001. |
| `TGT-CVT-003` | Record visibility profile. | `TGT-FR-008` | Visibility evidence available to scheduling. |
| `TGT-CVT-004` | Invalid coordinates block publication. | `TGT-OR-002` | Target remains not published. |

## Recovery Tests

| ID | Test | Requirement | Expected Result |
|---|---|---|---|
| `TGT-REC-001` | Duplicate target recovery. | `TGT-OR-003` | Duplicate resolved or documented open. |
| `TGT-REC-002` | Unknown catalogue identifier. | `TGT-FR-003` | Identifier remains unresolved and target not published. |
| `TGT-REC-003` | Registry inconsistency. | `TGT-AR-002` | Registry Recovery runbook applies. |

## Acceptance Tests

| ID | Test | Acceptance Link | Expected Result |
|---|---|---|---|
| `TGT-AT-001` | End-to-end registration to published target. | `TGT-AC-001` | Target is complete, validated and schedulable. |
| `TGT-AT-002` | Duplicate prevented before publication. | `TGT-AC-006` | No duplicate published target. |
| `TGT-AT-003` | Target retirement preserves observation history. | `TGT-AC-011` | History remains archived. |
| `TGT-AT-004` | Registry and release evidence complete. | `TGT-AC-015` | CAP-000, REL-000 and MkDocs are updated. |

## Regression Tests

- CAP-OSM-001, CAP-SCH-001 and CAP-EQR-001 references remain valid.
- CAP-000 contains exactly one `CAP-TGT-001` registry entry.
- Requirement IDs with prefix `TGT` are unique.
- Mermaid diagrams use supported syntax.
- No implementation code, backend, frontend, API or database is introduced.

## Exit Criteria

- All requirement categories have tests or acceptance criteria.
- ADR, SOP and runbooks are linked in traceability.
- Open decisions are explicit and not implemented by assumption.
