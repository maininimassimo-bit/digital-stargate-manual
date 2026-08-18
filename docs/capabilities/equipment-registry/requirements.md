# CAP-003 - Requirements

## Requirement Identification

Gli identificatori usano prefisso `EQR` per Equipment Registry. Gli stati indicano baseline documentale, non implementazione software.

## Business Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `EQR-BR-001` | La capability deve essere single source of truth per asset fisici e logici dell'osservatorio. | Must | EA / CAP-000 | Approved |
| `EQR-BR-002` | La capability deve supportare scheduling e session management con disponibilita e configurazione attendibili. | Must | CAP-001 / CAP-002 | Approved |
| `EQR-BR-003` | La capability deve preservare storico di configurazioni, manutenzioni e retirement. | Must | Knowledge Framework | Approved |
| `EQR-BR-004` | La capability deve ridurre rischio operativo causato da asset non censiti o non verificati. | Must | DSRA | Approved |

## Functional Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `EQR-FR-001` | Registrare equipment con identificatore unico, tipo, owner, posizione e lifecycle state. | Must | Knowledge Framework | Approved |
| `EQR-FR-002` | Supportare Optical Tubes, Mounts, Cameras, Filter Wheels, Focusers, Guidescopes, Guide Cameras, Rotators and Flat Panels. | Must | User scope / EA | Approved |
| `EQR-FR-003` | Supportare Weather Stations, Roof Controllers, UPS, Power Distribution, Network Devices, Mini PCs and Storage. | Must | User scope / Technology Architecture | Approved |
| `EQR-FR-004` | Registrare firmware, drivers e logical equipment groups come elementi logici tracciabili. | Must | Knowledge Framework | Approved |
| `EQR-FR-005` | Collegare configuration, dependency, capability and assignment a ogni asset rilevante. | Must | EA Data Architecture | Approved |
| `EQR-FR-006` | Esporre concettualmente availability and health status per CAP-002 e CAP-001. | Must | CAP-001 / CAP-002 | Approved |
| `EQR-FR-007` | Registrare maintenance records e impatti operativi. | Must | Maintenance Portal | Approved |
| `EQR-FR-008` | Preservare retirement record senza eliminare storico. | Must | Knowledge Framework | Approved |

## Operational Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `EQR-OR-001` | Ogni asset operativo deve avere stato `Verified` o `Available` prima dell'assegnazione. | Must | Business Process | Approved |
| `EQR-OR-002` | Equipment offline deve attivare runbook e rimuovere disponibilita operativa. | Must | DSRA / Observability | Approved |
| `EQR-OR-003` | Configuration mismatch deve impedire uso operativo finche non risolto o accettato con evidenza. | Must | Quality / Safety | Approved |
| `EQR-OR-004` | Ogni update deve mantenere storico minimo: chi, quando, cosa, perche, impatto. | Must | Governance | Approved |

## Security Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `EQR-SR-001` | Solo ruoli autorizzati possono registrare, aggiornare, verificare o ritirare equipment. | Must | Security Architecture | Approved |
| `EQR-SR-002` | Il registry non deve contenere segreti, password o credenziali. | Must | Security Architecture | Approved |
| `EQR-SR-003` | Asset di rete e remote access devono essere registrati senza esporre dati sensibili non necessari. | Must | DSRA / Security | Approved |
| `EQR-SR-004` | Ogni cambiamento safety-critical deve essere auditabile. | Must | Observatory Safety | Approved |

## Performance Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `EQR-PR-001` | Stato e disponibilita devono essere consultabili in tempo utile per scheduling e session preparation. | Must | CAP-001 / CAP-002 | Approved |
| `EQR-PR-002` | La verifica configurazione deve essere completabile prima dell'uso operativo pianificato. | Should | Operations | Approved |
| `EQR-PR-003` | Il registry deve supportare piu asset e gruppi logici senza perdere tracciabilita. | Should | Knowledge Framework | Approved |

## Availability Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `EQR-AR-001` | Evidenza equipment critica deve restare disponibile durante scheduling e session management. | Must | CAP-001 / CAP-002 | Approved |
| `EQR-AR-002` | In caso di registry inconsistente, deve essere attivabile recovery documentale. | Must | DSRA | Approved |
| `EQR-AR-003` | Lo storico asset deve essere preservato anche dopo retirement. | Must | Knowledge Framework | Approved |

## Quality Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `EQR-QR-001` | Ogni record deve essere completo rispetto ai campi obbligatori definiti nel modello concettuale. | Must | Data Model | Approved |
| `EQR-QR-002` | Stati equipment e lifecycle devono usare vocabolario controllato. | Must | `EQR-ADR-002` | Approved |
| `EQR-QR-003` | Il registry deve distinguere asset fisici, logici, firmware, driver and logical groups. | Must | Architecture Mapping | Approved |

## Traceability Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `EQR-TR-001` | Ogni artefatto CAP-003 deve riferire Roadmap, DSRA, EA, Knowledge, CAP-000 and REL-000. | Must | Governance | Approved |
| `EQR-TR-002` | Ogni assignment deve essere tracciabile verso capability consumatrice quando applicabile. | Must | CAP-001 / CAP-002 | Approved |
| `EQR-TR-003` | ADR, SOP, runbook, manuale, test e acceptance devono essere nella traceability matrix. | Must | REL-000 | Approved |

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
