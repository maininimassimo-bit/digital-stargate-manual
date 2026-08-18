# Observation Session Management - Requirements

| Campo | Valore |
|---|---|
| Documento | Capability Requirements |
| Capability | `DSG-CAP-OSM-001` |
| Fonte gerarchica | `DSG-MR-001` -> DSRA -> Enterprise Architecture -> Knowledge Framework -> Design System |
| Stato | Controlled Baseline |

## Requirement Model

Ogni requisito e documentale e architetturale. Nessun requisito in questo documento autorizza implementazione software senza governance successiva.

## Business Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `OSM-BR-001` | La sessione osservativa shall be the governed unit for operational and scientific traceability. | Must | ADR-001, Data Architecture | Accepted |
| `OSM-BR-002` | La capability shall support repeatable remote observatory operation. | Must | Business/Application Architecture | Accepted |
| `OSM-BR-003` | Ogni sessione shall produce evidence usable by archive, analytics and knowledge update. | Must | Knowledge Framework | Accepted |
| `OSM-BR-004` | La capability shall become the reference documentation pattern for future capabilities. | Should | User objective | Accepted |

## Functional Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `OSM-FR-001` | The capability shall start from an Observation Request or documented operator intent. | Must | Domain Model | Accepted |
| `OSM-FR-002` | The capability shall link each session to a Target and Target Registry reference where available. | Must | Domain/Data Architecture | Open where registry is TBD |
| `OSM-FR-003` | The capability shall validate equipment readiness before execution. | Must | Application/Technology Architecture | Accepted |
| `OSM-FR-004` | The capability shall capture weather and safety validation before and during session execution. | Must | Observability Architecture | Accepted |
| `OSM-FR-005` | The capability shall produce or update a Session Manifest as the session evidence binder. | Must | ADR-001, Data Architecture | Open pending manifest schema |
| `OSM-FR-006` | The capability shall connect raw images to session, target, equipment and acquisition metadata. | Must | Data Architecture | Accepted |
| `OSM-FR-007` | The capability shall support session closing and archive readiness. | Must | Data/Technology Architecture | Accepted |
| `OSM-FR-008` | The capability shall record unresolved gaps as open decisions. | Must | Knowledge Framework | Accepted |

## Operational Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `OSM-OPR-001` | SOP shall exist for prepare, execute, abort, recover and close session. | Must | Capability package | Accepted |
| `OSM-OPR-002` | Runbooks shall exist for scheduler, weather, roof, camera, mount, N.I.N.A., ASCOM and emergency failures. | Must | Observability/Technology Architecture | Accepted |
| `OSM-OPR-003` | Operator actions shall be documented with timestamped evidence where feasible. | Should | Security/Observability Architecture | Accepted |
| `OSM-OPR-004` | Session state transitions shall be explicit and reviewable. | Must | Knowledge Framework | Accepted |

## Security Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `OSM-SEC-001` | Remote session operation shall respect VPN and access governance. | Must | Security Architecture | Open pending detailed access ADR |
| `OSM-SEC-002` | Session documentation shall not contain secrets or credentials. | Must | Security Architecture | Accepted |
| `OSM-SEC-003` | Safety-critical actions shall require human awareness and documented procedure. | Must | DSRA/Observability | Accepted |
| `OSM-SEC-004` | Publication of session evidence shall respect sensitivity classification where defined. | Should | Knowledge Framework | Open |

## Performance Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `OSM-PER-001` | Session readiness checks shall be concise enough for pre-session operations. | Should | Operational need | Accepted |
| `OSM-PER-002` | Session evidence shall be captured without blocking safe observatory operation. | Must | Observability Architecture | Accepted |
| `OSM-PER-003` | Dashboard or report views shall present session state without unnecessary visual latency when implemented. | Should | Design System | Future implementation |

## Availability Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `OSM-AVL-001` | The capability shall define behavior when scheduler, N.I.N.A., ASCOM, camera, mount or weather input is unavailable. | Must | Runbooks | Accepted |
| `OSM-AVL-002` | Session recovery shall preserve available evidence even if acquisition fails. | Must | Data Architecture | Accepted |
| `OSM-AVL-003` | Archive readiness shall not depend on successful publication. | Should | Data Architecture | Accepted |

## Quality Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `OSM-QLT-001` | Session documentation shall use Design System terminology and status conventions. | Must | Design System | Accepted |
| `OSM-QLT-002` | Tests shall include functional, operational, recovery, acceptance and regression checks. | Must | Capability package | Accepted |
| `OSM-QLT-003` | Missing evidence shall be marked open or not available, never invented. | Must | Knowledge Framework | Accepted |

## Traceability Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `OSM-TRC-001` | Every capability document shall reference Roadmap, DSRA, Enterprise Architecture, Knowledge Framework and Design System. | Must | Governance | Accepted |
| `OSM-TRC-002` | Every operational procedure shall map to at least one runbook or acceptance criterion. | Must | Traceability Matrix | Accepted |
| `OSM-TRC-003` | ADRs shall reference existing architecture decisions and avoid duplicating enterprise decisions. | Must | Architecture Decision Catalog | Accepted |

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
