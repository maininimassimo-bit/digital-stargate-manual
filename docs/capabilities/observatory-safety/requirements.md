# CAP-SAF-001 - Requirements

## Requirement Rules

- Requirements derive from approved governance and existing repository artefacts only.
- No requirement defines hardware implementation, PLC logic, driver behavior, API, database, frontend or backend.
- Every requirement uses a unique `SAF-*` identifier.

## Business Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `SAF-BR-001` | The capability shall be the conceptual safety authority for Core Observatory operational decisions. | Must | DSRA / DOM-001 / REV-001 | Defined |
| `SAF-BR-002` | The capability shall protect observatory assets, equipment and scientific continuity from unsafe operations. | Must | DSRA | Defined |
| `SAF-BR-003` | The capability shall provide auditable allow, suspend, abort, safe mode and recovery decision support. | Must | Knowledge Framework / REL-000 | Defined |
| `SAF-BR-004` | The capability shall complete the documented Core Observatory domain without introducing implementation. | Must | DOM-001 / REV-001 | Defined |

## Functional Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `SAF-FR-001` | Represent safety states: Unknown, Safe, Warning, Unsafe, Emergency, Recovery, Maintenance and Disabled. | Must | Capability scope | Defined |
| `SAF-FR-002` | Consume conceptual safety inputs from Weather Monitoring. | Must | CAP-WEA-001 | Defined |
| `SAF-FR-003` | Consume observation session state and active execution context from OSM. | Must | CAP-OSM-001 | Defined |
| `SAF-FR-004` | Consume equipment readiness, roof-related and lifecycle context from Equipment Registry. | Must | CAP-EQR-001 | Defined |
| `SAF-FR-005` | Consume schedule approval and planned observation context from Scheduling. | Must | CAP-SCH-001 | Defined |
| `SAF-FR-006` | Consume target and observation constraint context where relevant. | Should | CAP-TGT-001 | Defined |
| `SAF-FR-007` | Produce conceptual outputs: Allow Observation, Suspend Observation, Abort Observation, Close Roof Request, Safe Mode, Recovery Allowed, Operator Notification and Audit Event. | Must | Capability scope | Defined |
| `SAF-FR-008` | Record safety assessments, safety events, emergency actions and recovery actions. | Must | Knowledge Framework | Defined |

## Operational Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `SAF-OR-001` | Unknown or Disabled safety state shall block unattended observation start or continue. | Must | Fail-safe policy | Defined |
| `SAF-OR-002` | Unsafe state shall trigger suspend or abort decision support. | Must | DSRA / CAP-OSM-001 | Defined |
| `SAF-OR-003` | Emergency state shall trigger emergency shutdown procedure and audit event. | Must | DSRA / Runbook need | Defined |
| `SAF-OR-004` | Recovery shall require validation before operations resume. | Must | REL-000 / SOP need | Defined |

## Security Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `SAF-SR-001` | Safety policy, state and decisions shall be protected from unauthorized modification. | Must | Security Architecture | Defined |
| `SAF-SR-002` | Operator decisions and overrides shall be auditable. | Must | Security Architecture / Knowledge Framework | Defined |
| `SAF-SR-003` | Secrets, credentials and access tokens shall not be documented in capability artefacts. | Must | Governance | Defined |
| `SAF-SR-004` | Remote safety operations shall follow approved remote access and VPN governance. | Must | Security / Technology Architecture | Defined |

## Performance Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `SAF-PR-001` | Safety decision freshness targets shall be defined before implementation. | Must | Open decision | Open |
| `SAF-PR-002` | Emergency decision support shall be prioritized over non-safety workflows. | Must | DSRA | Defined |
| `SAF-PR-003` | Audit recording shall not delay immediate emergency posture. | Should | Operational safety | Defined |

## Availability Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `SAF-AR-001` | Loss of safety authority shall result in Disabled or Unknown, not Safe. | Must | Fail-safe policy | Defined |
| `SAF-AR-002` | Communications, power or roof status loss shall have documented runbook handling. | Must | Runbook need | Defined |
| `SAF-AR-003` | Safe mode shall be representable even when normal observation workflow is unavailable. | Must | DSRA / OSM recovery | Defined |

## Quality Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `SAF-QR-001` | Safety state vocabulary shall remain consistent across documents. | Must | Knowledge Framework | Defined |
| `SAF-QR-002` | Safety decisions shall be traceable to inputs, rule and assessment evidence. | Must | Traceability / REL-000 | Defined |
| `SAF-QR-003` | Acceptance criteria shall verify governance completeness and no implementation leakage. | Must | REL-000 | Defined |

## Traceability Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `SAF-TR-001` | Every Safety artefact shall reference Roadmap, DSRA, EA-000, Knowledge Framework, DOM-001, REV-001, CAP-000 and REL-000. | Must | Governance chain | Defined |
| `SAF-TR-002` | Safety outputs shall map to OSM, Scheduling, Weather and Equipment consumers. | Must | DOM-001 | Defined |
| `SAF-TR-003` | Open safety policy, rule priority and freshness decisions shall remain explicit until approved. | Must | ADR governance | Defined |

## Requirement Count

| Category | Count |
|---|---:|
| Business | 4 |
| Functional | 8 |
| Operational | 4 |
| Security | 4 |
| Performance | 3 |
| Availability | 3 |
| Quality | 3 |
| Traceability | 3 |
| **Total** | **32** |
