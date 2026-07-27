# CAP-002 - Requirements

## Requirement Identification

Gli identificatori usano prefisso `OSD` per Observation Scheduling Documentation. Gli stati riflettono la baseline documentale della capability e non indicano implementazione software.

## Business Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `OSD-BR-001` | La capability deve trasformare Observation Request tracciabili in Scheduled Observation governate. | Must | DSG-MR-001 / EA | Approved |
| `OSD-BR-002` | La capability deve supportare priorita scientifiche e operative senza bypassare safety. | Must | DSRA / EA | Approved |
| `OSD-BR-003` | La capability deve ridurre conflitti tra target, risorse e finestre disponibili. | Should | EA / Knowledge Framework | Approved |
| `OSD-BR-004` | La capability deve produrre evidenza sufficiente per CAP-001 e per il repository di conoscenza. | Must | CAP-000 / CAP-001 | Approved |

## Functional Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `OSD-FR-001` | Registrare una Observation Request con target, vincoli, priorita e owner. | Must | Knowledge Framework | Approved |
| `OSD-FR-002` | Collegare ogni richiesta a Target Registry o registrare il motivo di sospensione. | Must | EA Data Architecture | Approved |
| `OSD-FR-003` | Valutare finestre astronomiche candidate per ogni target schedulabile. | Must | EA Application Architecture | Approved |
| `OSD-FR-004` | Verificare disponibilita risorse con Equipment Registry prima dell'approvazione. | Must | EA Application Architecture | Approved |
| `OSD-FR-005` | Verificare condizioni meteo e safety prima della pubblicazione. | Must | DSRA / Observability Architecture | Approved |
| `OSD-FR-006` | Identificare conflitti tra schedule candidate, risorse, finestre e priorita. | Must | CAP-000 | Approved |
| `OSD-FR-007` | Applicare una risoluzione di priorita documentata e auditabile. | Must | `OSD-ADR-002` | Approved |
| `OSD-FR-008` | Pubblicare solo schedule approvate verso Observation Session Management. | Must | CAP-001 | Approved |

## Operational Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `OSD-OR-001` | Ogni aggiornamento schedule deve mantenere storico decisionale minimo. | Must | Governance / Knowledge Framework | Approved |
| `OSD-OR-002` | Cancellazioni e recovery devono seguire SOP o runbook dedicati. | Must | REL-000 | Approved |
| `OSD-OR-003` | Il monitoraggio schedule deve rilevare perdita finestra meteo, risorsa indisponibile e safety unsafe. | Must | Observability Architecture | Approved |
| `OSD-OR-004` | La capability deve produrre evidenza di handover a CAP-001 quando la schedule e pubblicata. | Must | CAP-001 | Approved |

## Security Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `OSD-SR-001` | Solo ruoli autorizzati possono approvare o cancellare una schedule. | Must | Security Architecture | Approved |
| `OSD-SR-002` | Ogni approvazione o cancellazione deve avere owner e audit trail documentale. | Must | Governance | Approved |
| `OSD-SR-003` | La schedule non deve contenere segreti, credenziali o dati personali non necessari. | Must | Security Architecture | Approved |
| `OSD-SR-004` | Remote operations e accessi devono rispettare VPN e regole di sicurezza gia approvate. | Must | Technology / Security Architecture | Approved |

## Performance Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `OSD-PR-001` | La valutazione schedule deve essere completabile prima dell'inizio della finestra osservativa. | Must | Operational need | Approved |
| `OSD-PR-002` | La detection di conflitto deve essere abbastanza tempestiva da permettere recovery o cancellazione controllata. | Should | Observability Architecture | Approved |
| `OSD-PR-003` | Il processo deve supportare piu richieste candidate senza perdere tracciabilita. | Should | Knowledge Framework | Approved |

## Availability Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `OSD-AR-001` | La schedule pubblicata deve restare consultabile durante la preparazione CAP-001. | Must | CAP-001 | Approved |
| `OSD-AR-002` | In caso di indisponibilita di una fonte, la schedule deve restare in stato non pubblicato o recovery. | Must | DSRA | Approved |
| `OSD-AR-003` | Le evidenze di schedule devono essere preservate per audit e knowledge update. | Must | Knowledge Framework | Approved |

## Quality Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `OSD-QR-001` | Ogni schedule deve essere completa rispetto a target, finestra, risorse, vincoli, stato e approvazione. | Must | Data Architecture | Approved |
| `OSD-QR-002` | Le regole di priorita devono essere documentate e non ambigue per gli operatori. | Must | `OSD-ADR-002` | Approved |
| `OSD-QR-003` | Il contenuto deve rispettare glossary, taxonomy e design governance quando genera UI futura. | Should | Knowledge / Design System | Approved |

## Traceability Requirements

| ID | Requirement | Priority | Source | Status |
|---|---|---|---|---|
| `OSD-TR-001` | Ogni artefatto CAP-002 deve riferire Roadmap, DSRA, EA, Knowledge, CAP-000 e REL-000. | Must | Governance | Approved |
| `OSD-TR-002` | Ogni Scheduled Observation deve mantenere legame con Observation Request e CAP-001 handover. | Must | Knowledge Framework | Approved |
| `OSD-TR-003` | ADR, SOP, runbook, manuale, test e acceptance devono essere richiamati nella traceability matrix. | Must | REL-000 | Approved |

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
