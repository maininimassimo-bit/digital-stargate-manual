# WEA-ADR-002 - Operational Safety Thresholds

| Campo | Valore |
|---|---|
| ADR | `WEA-ADR-002` |
| Capability | `CAP-WEA-001` Weather Monitoring |
| Stato | Accepted with Open Inputs |
| Data | 2026-07-27 |
| Owner | Lead Enterprise Solution Architect / Safety Reviewer |
| Decision scope | Capability-specific |

## Context

Weather Monitoring must evaluate environmental evidence against operational safety criteria. The repository supports the need for weather safety and monitoring, but final numeric thresholds and arbitration rules are not all approved in the architecture baseline.

## Decision

Weather Monitoring SHALL use governed operational safety thresholds or qualitative rules to classify weather state. Thresholds are architecture-governed configuration concepts, not hard-coded implementation details.

Until final values are approved, the capability package documents threshold governance, test categories and open decisions rather than inventing unsafe numeric limits.

## Threshold Domains

Threshold governance applies to:

- wind;
- humidity;
- temperature;
- cloud cover;
- rain;
- sky quality;
- seeing;
- transparency;
- lightning;
- roof safe state;
- overall observatory weather state.

## Consequences

- Future implementation must reference approved threshold definitions.
- SOP and runbooks can operate on `SAFE`, `CAUTION`, `UNSAFE` and `UNKNOWN` states without requiring final numeric values in this package.
- Historical records must preserve enough context to know which threshold version informed a decision.
- Threshold changes require governance review because they affect safety and scheduling behavior.

## Alternatives Considered

| Alternative | Reason not selected |
|---|---|
| Define numeric thresholds now | Repository evidence is insufficient; inventing values would violate governance. |
| Leave thresholds outside governance | Would weaken DSRA alignment and operational safety traceability. |
| Embed thresholds in individual SOP only | Would fragment decision logic across procedures. |

## Open Decisions

| Decision | Impact | Required Input |
|---|---|---|
| Numeric threshold values | Required before implementation. | Approved operational safety table. |
| Threshold versioning | Required for historical auditability. | Data Platform / Knowledge governance input. |
| Operator override policy | Affects `UNKNOWN` and `CAUTION` handling. | Security and Operations approval. |
| Weather-to-roof-safe mapping | Affects Observatory Safety and roof/cupola procedure. | Safety Reviewer / Operations input. |

## References

- `docs/capabilities/weather-monitoring/requirements.md`
- `docs/capabilities/weather-monitoring/data-model.md`
- `docs/capabilities/weather-monitoring/test-plan.md`
- `docs/enterprise-architecture/observability-architecture.md`
- `docs/enterprise/DSRA-risk-assessment.md`
