# CAP-WEA-001 - Requirements

## Requirement Rules

- Requirements derive from `DSG-MR-001`, DSRA, `EA-000`, Knowledge Framework, `CAP-000`, `REL-000`, `DOM-001` and existing Core Observatory capability packages.
- This capability defines conceptual weather state and operational assessment only.
- No requirement mandates a specific driver, sensor, vendor, database, API, frontend or forecasting engine.

## Business Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `WEA-BR-001` | The capability shall provide a trusted operational weather state for the Core Observatory domain. | Must | EA Observability / DOM-001 | Defined |
| `WEA-BR-002` | The capability shall support protection of observatory assets and scientific data from unsafe weather. | Must | DSRA / Chapter 26 | Defined |
| `WEA-BR-003` | The capability shall support scheduling and session decisions without replacing Observatory Safety. | Must | CAP-SCH-001 / CAP-OSM-001 | Defined |
| `WEA-BR-004` | The capability shall preserve evidence for weather-driven suspend, resume and recovery decisions. | Must | Knowledge Framework | Defined |

## Functional Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `WEA-FR-001` | Represent weather observations with source, timestamp and observed condition values. | Must | Data Architecture / Knowledge Framework | Defined |
| `WEA-FR-002` | Represent weather snapshots as point-in-time operational weather state evidence. | Must | CAP-OSM-001 manifest dependency | Defined |
| `WEA-FR-003` | Represent wind, humidity, temperature, cloud cover, rain, sky quality, seeing, transparency, lightning and roof safe state. | Must | User-approved scope / Chapter 26 | Defined |
| `WEA-FR-004` | Classify overall observatory weather state as safe, caution, unsafe or unknown, or equivalent governed states. | Must | EA Observability | Defined |
| `WEA-FR-005` | Detect stale weather evidence conceptually using governed freshness rules. | Must | DSRA / Observability | Defined |
| `WEA-FR-006` | Detect conflicting weather evidence conceptually when multiple sources disagree. | Should | Integration Architecture | Defined |
| `WEA-FR-007` | Publish weather state for scheduling approval and session readiness checks. | Must | CAP-SCH-001 / CAP-OSM-001 | Defined |
| `WEA-FR-008` | Record historical weather state changes relevant to schedule, session and safety decisions. | Must | Knowledge Framework | Defined |

## Operational Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `WEA-OR-001` | Operators shall be able to determine whether weather state is current, stale, conflicting or unavailable. | Must | SOP / Runbook need | Defined |
| `WEA-OR-002` | Unsafe weather shall trigger documented suspension or prevention procedure. | Must | DSRA / CAP-OSM-001 | Defined |
| `WEA-OR-003` | Recovery from offline weather source shall require explicit evidence of restored monitoring or manual fallback. | Must | Runbook need | Defined |
| `WEA-OR-004` | Resume after unsafe weather shall require revalidated state and session/schedule impact review. | Must | SOP need | Defined |

## Security Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `WEA-SR-001` | Weather state used for operational decisions shall be protected from unauthorized alteration. | Must | Security Architecture | Defined |
| `WEA-SR-002` | Operator overrides, if allowed by future governance, shall be traceable and auditable. | Should | Security Architecture / Open decision | Open |
| `WEA-SR-003` | Credentials or secrets for weather integrations shall not be documented in capability artefacts. | Must | Governance / Security Architecture | Defined |
| `WEA-SR-004` | Remote access to monitoring evidence shall follow approved VPN and access governance. | Must | Technology/Security Architecture | Defined |

## Performance Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `WEA-PR-001` | Weather state freshness targets shall be defined before implementation. | Must | Open Architectural Decision | Open |
| `WEA-PR-002` | Weather state publication shall be timely enough to support schedule and session safety gates. | Must | CAP-SCH-001 / CAP-OSM-001 | Defined |
| `WEA-PR-003` | Historical recording shall not delay immediate safety assessment. | Should | Operational need | Defined |

## Availability Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `WEA-AR-001` | Weather Monitoring shall expose `UNKNOWN` when authoritative assessment cannot be produced. | Must | DSRA safety posture | Defined |
| `WEA-AR-002` | Loss of primary weather evidence shall have a documented recovery path. | Must | Runbook need | Defined |
| `WEA-AR-003` | Weather state shall not be assumed safe during source outage, stale data or unresolved conflict. | Must | DSRA / Observatory Safety | Defined |

## Quality Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `WEA-QR-001` | Weather state definitions shall be consistent across capability, SOP, runbook and traceability documents. | Must | Knowledge Framework | Defined |
| `WEA-QR-002` | Threshold names and meanings shall be documented before implementation. | Must | ADR need | Defined |
| `WEA-QR-003` | Weather-related acceptance criteria shall be measurable and reviewable. | Must | REL-000 | Defined |

## Traceability Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `WEA-TR-001` | Every Weather Monitoring artefact shall reference roadmap, DSRA, EA, Knowledge Framework, DOM-001, CAP-000 and REL-000. | Must | Governance chain | Defined |
| `WEA-TR-002` | Schedule and session decisions shall reference the weather snapshot or alert that influenced them. | Must | CAP-SCH-001 / CAP-OSM-001 | Defined |
| `WEA-TR-003` | Open threshold, arbitration and retention topics shall be recorded as open decisions until approved. | Must | ADR governance | Defined |

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
