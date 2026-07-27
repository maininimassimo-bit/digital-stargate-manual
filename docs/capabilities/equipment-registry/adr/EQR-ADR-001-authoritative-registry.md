# EQR-ADR-001 - Authoritative Registry

| Campo | Valore |
|---|---|
| ADR | `EQR-ADR-001` |
| Capability | CAP-003 Equipment Registry |
| Stato | Accepted |
| Data | 2026-07-27 |
| Owner | Lead Enterprise Solution Architect |
| Related Architecture | EA Application/Data Architecture |

## Context

Observation Scheduling, Observation Session Management, Maintenance, Engineering and Observatory Safety require consistent equipment identity, configuration and state evidence. Without an authoritative registry, future implementation could create parallel asset lists with conflicting status or configuration.

## Decision

CAP-003 Equipment Registry is the authoritative documentation source for physical and logical observatory equipment records. Capability consumers may reference or consume registry evidence, but they do not redefine equipment identity, lifecycle state, configuration history or registry ownership.

## Consequences

- CAP-002 consumes availability and assignment constraints from Equipment Registry.
- CAP-001 consumes verified readiness and configuration from Equipment Registry.
- Maintenance and Engineering updates must preserve registry traceability.
- Future implementation must either implement or integrate with this authority model through governed ADR.
- No vendor-specific registry product is selected by this decision.

## Alternatives Considered

| Alternative | Reason Not Selected |
|---|---|
| Separate asset lists per capability | Creates inconsistent state and weak traceability. |
| Store equipment only in technical manuals | Manuals are not sufficient for lifecycle, assignment and state governance. |
| Select a registry product now | Unsupported by current repository evidence and outside documentation scope. |

## Traceability

- Roadmap: `DSG-MR-001`.
- DSRA: operational and asset risk context.
- Enterprise Architecture: Equipment Registry in Application/Data Architecture.
- Knowledge Framework: Equipment, Engineering Asset, Configuration.
- CAP-000: `CAP-EQR-001`.
- REL-000: ADR artefact and readiness evidence.
