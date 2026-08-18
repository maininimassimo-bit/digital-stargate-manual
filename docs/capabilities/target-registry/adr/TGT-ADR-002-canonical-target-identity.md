# TGT-ADR-002 - Canonical Target Identity

| Campo | Valore |
|---|---|
| ADR | `TGT-ADR-002` |
| Capability | CAP-TGT-001 Target Registry |
| Stato | Accepted with Open Implementation Detail |
| Data | 2026-07-27 |
| Owner | Lead Enterprise Solution Architect |
| Related Architecture | EA Data Architecture / Knowledge Framework |

## Context

Astronomical targets commonly have multiple identifiers, aliases and catalogue references. Some targets are static deep-sky objects, while comets, asteroids, planets, Moon, Sun and satellites require dynamic or contextual position evidence. Without canonical identity rules, Digital StarGate could publish duplicate or ambiguous targets.

## Decision

CAP-TGT-001 shall maintain a canonical target identity for each target managed by Digital StarGate. Catalogue references and aliases are attached to the canonical target record, not used as competing internal records.

Potential duplicates, unresolved identifiers and invalid coordinate evidence must block publication until resolved or explicitly documented as open.

## Consequences

- Target publication requires identity validation.
- Duplicate target risk is handled before scheduling.
- CAP-SCH-001 and CAP-OSM-001 consume canonical target references.
- Moving target ephemeris handling remains open for future governance.
- Final target identifier format remains open unless defined later by CAP-000 convention or future ADR.

## Alternatives Considered

| Alternative | Reason Not Selected |
|---|---|
| Allow each catalogue designation as separate target | Produces duplicates and weak observation history linkage. |
| Use target display name as identity | Names change and may be ambiguous. |
| Implement ephemeris-specific identity now | Unsupported by current repository evidence and outside scope. |

## Open Implementation Detail

| Decision | Reason | Required Input |
|---|---|---|
| Final target identifier format | Not yet defined in approved implementation artefacts. | Science/Knowledge identifier policy. |
| Moving target ephemeris model | Requires future astronomical data decision. | Science and integration decision. |
| Automated duplicate matching | Requires future implementation design. | Data/Engineering decision. |

## Traceability

- Roadmap: `DSG-MR-001`.
- DSRA: data quality and operational risk.
- Enterprise Architecture: Data Architecture and Knowledge Graph.
- Knowledge Framework: Target Identity, Catalogue Reference and Traceability.
- CAP-000: `CAP-TGT-001`.
- REL-000: ADR artefact and readiness evidence.
