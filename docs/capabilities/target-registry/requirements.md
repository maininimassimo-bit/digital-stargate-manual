# CAP-TGT-001 - Requirements

## Requirement Identification

Gli identificatori usano prefisso `TGT` per Target Registry. Gli stati indicano baseline documentale, non implementazione software.

## Business Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `TGT-BR-001` | La capability deve essere single conceptual source of truth per target gestiti da Digital StarGate. | Must | EA / CAP-000 | Approved |
| `TGT-BR-002` | La capability deve supportare scheduling e session management con target validati. | Must | CAP-SCH-001 / CAP-OSM-001 | Approved |
| `TGT-BR-003` | La capability deve preservare identita, alias, riferimenti catalogo e storia osservativa. | Must | Knowledge Framework | Approved |
| `TGT-BR-004` | La capability non deve sostituire cataloghi esterni, ma referenziarli in modo governato. | Must | Mission statement | Approved |

## Functional Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `TGT-FR-001` | Registrare Target con identita canonica, owner, lifecycle state and metadata. | Must | Knowledge Framework | Approved |
| `TGT-FR-002` | Gestire Target Identity, alias and duplicate detection evidence. | Must | `TGT-ADR-002` | Approved |
| `TGT-FR-003` | Gestire Catalogue Reference per Messier, NGC, IC, Sharpless, Barnard, LBN and Abell where applicable. | Must | Target Coverage | Approved |
| `TGT-FR-004` | Supportare Planetary Nebulae, Galaxies, Globular Clusters, Open Clusters, Nebulae and Dark Nebulae. | Must | Target Coverage | Approved |
| `TGT-FR-005` | Supportare Comets, Asteroids, Planets, Moon, Sun, Artificial Satellites and Custom Targets. | Must | Target Coverage | Approved |
| `TGT-FR-006` | Registrare coordinates, epoch and constellation when applicable. | Must | Data Model | Approved |
| `TGT-FR-007` | Registrare scientific classification, observation priority and observation constraints. | Must | CAP-SCH-001 | Approved |
| `TGT-FR-008` | Collegare visibility profile and observation history reference to target metadata. | Must | Data / Knowledge Framework | Approved |

## Operational Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `TGT-OR-001` | Target non validati non devono essere pubblicati per scheduling. | Must | Business Process | Approved |
| `TGT-OR-002` | Coordinate invalide devono attivare runbook dedicato. | Must | Quality / Safety | Approved |
| `TGT-OR-003` | Duplicati potenziali devono essere risolti o documentati prima della pubblicazione. | Must | `TGT-ADR-002` | Approved |
| `TGT-OR-004` | Ogni update deve preservare storico minimo: chi, quando, cosa, perche, impatto. | Must | Governance | Approved |

## Security Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `TGT-SR-001` | Solo ruoli autorizzati possono approvare, ritirare or pubblicare target. | Must | Security Architecture | Approved |
| `TGT-SR-002` | Il registry non deve contenere segreti, credenziali or dati personali non necessari. | Must | Security Architecture | Approved |
| `TGT-SR-003` | Custom targets devono essere documentati senza introdurre informazioni sensibili non richieste. | Should | Governance | Approved |
| `TGT-SR-004` | Ogni decisione di merge, retirement or identity override deve essere auditabile. | Must | Knowledge Framework | Approved |

## Performance Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `TGT-PR-001` | Target identity and coordinates devono essere consultabili in tempo utile per scheduling. | Must | CAP-SCH-001 | Approved |
| `TGT-PR-002` | Identity validation deve essere completabile prima dell'approvazione target. | Should | Business Process | Approved |
| `TGT-PR-003` | Il registry deve supportare piu alias e riferimenti senza perdere tracciabilita. | Should | Knowledge Framework | Approved |

## Availability Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `TGT-AR-001` | Target pubblicati devono restare consultabili durante scheduling e session preparation. | Must | CAP-SCH-001 / CAP-OSM-001 | Approved |
| `TGT-AR-002` | In caso di registry inconsistente, deve essere attivabile recovery documentale. | Must | DSRA | Approved |
| `TGT-AR-003` | Lo storico target deve essere preservato anche dopo retirement. | Must | Knowledge Framework | Approved |

## Quality Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `TGT-QR-001` | Ogni target pubblicato deve avere identita, coordinate/ephemeris reference where applicable, type and lifecycle state. | Must | Data Model | Approved |
| `TGT-QR-002` | Target identity deve usare regole canoniche documentate. | Must | `TGT-ADR-002` | Approved |
| `TGT-QR-003` | Il registry deve distinguere catalogue identity, target type and scientific classification. | Must | Data Model | Approved |

## Traceability Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `TGT-TR-001` | Ogni artefatto CAP-TGT-001 deve riferire Roadmap, DSRA, EA, Knowledge, CAP-000 and REL-000. | Must | Governance | Approved |
| `TGT-TR-002` | Ogni target pubblicato deve essere tracciabile verso scheduling, sessioni or observation history quando applicabile. | Must | CAP-SCH-001 / CAP-OSM-001 | Approved |
| `TGT-TR-003` | ADR, SOP, runbook, manuale, test e acceptance devono essere nella traceability matrix. | Must | REL-000 | Approved |

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
| Total | 32 |
