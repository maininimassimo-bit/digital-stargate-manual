# EQR-ADR-002 - Equipment State Model

| Campo | Valore |
|---|---|
| ADR | `EQR-ADR-002` |
| Capability | CAP-003 Equipment Registry |
| Stato | Accepted with Open Implementation Detail |
| Data | 2026-07-27 |
| Owner | Lead Enterprise Solution Architect |
| Related Architecture | EA Data/Observability Architecture |

## Context

Equipment state influences scheduling, session readiness, maintenance and observatory safety. The repository requires a governed conceptual state model, but does not yet define automated telemetry ingestion or a physical registry implementation.

## Decision

CAP-003 adopts a controlled conceptual state vocabulary: `Unknown`, `Registered`, `Verified`, `Available`, `Assigned`, `In Use`, `Degraded`, `Offline`, `Maintenance`, `Retired`, `Archived`.

Only `Available`, and conditionally `Verified`, `Assigned` or `In Use`, may support operational use. `Unknown`, `Offline`, `Maintenance`, `Retired` and `Archived` must not be treated as available.

## Consequences

- CAP-002 cannot schedule an asset marked unavailable by the registry state model.
- CAP-001 must treat unavailable or unverified equipment as readiness risk.
- Maintenance actions can intentionally move equipment out of availability.
- Future implementation must preserve state transitions and evidence.

## Alternatives Considered

| Alternative | Reason Not Selected |
|---|---|
| Binary available/unavailable only | Too weak for maintenance, safety and recovery governance. |
| Vendor-native state models only | Would make the registry vendor-specific and non-canonical. |
| Automated state inference now | Not supported by current repository evidence and outside scope. |

## Open Implementation Detail

| Decision | Reason | Required Input |
|---|---|---|
| Automated vs manual state source | Current repository does not define telemetry ingestion. | Observability/integration ADR. |
| Exact transition authorization | Owner roles need final operational approval. | Governance/SOP evolution. |
| Health scoring granularity | No approved metric scale yet. | Engineering and safety input. |

## Traceability

- Roadmap: `DSG-MR-001`.
- DSRA: operational safety and availability risk.
- Enterprise Architecture: Observability, Technology and Data Architecture.
- Knowledge Framework: Equipment State, Health Status, Lifecycle State.
- CAP-000: `CAP-EQR-001`.
- REL-000: ADR artefact and readiness evidence.
