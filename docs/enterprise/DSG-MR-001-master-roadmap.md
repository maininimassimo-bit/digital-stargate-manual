# DSG-MR-001 - Master Roadmap Enterprise

| Campo | Valore |
|---|---|
| Documento | Master Roadmap Enterprise |
| Identificativo | `DSG-MR-001` |
| Sistema | Digital StarGate |
| Versione | 1.0 |
| Stato | Approvata |
| Owner | Massimo Mainini |
| Data baseline | 26/07/2026 |
| Branch di lavoro | `docs/dsg-master-roadmap` |

## 1. Scopo

La roadmap `DSG-MR-001` definisce il percorso di completamento della documentazione enterprise del progetto Digital StarGate.

L'obiettivo è portare il repository `digital-stargate-manual` da manuale tecnico strutturato a sistema documentale enterprise, mantenendo MkDocs come canale di pubblicazione e usando GitHub come fonte primaria di tracciabilità.

## 2. Ambito

La roadmap copre:

- architettura enterprise e integrazione con i capitoli esistenti;
- DSRA e gestione dei rischi;
- ADR e decision log;
- requisiti, controlli, deliverable e change log;
- handbook e procedure operative standard;
- assessment, governance e release readiness;
- appendici, glossario, template e mapping.

Sono fuori ambito della roadmap:

- modifica del codice applicativo non necessaria alla documentazione;
- cambio di piattaforma di pubblicazione;
- inserimento di segreti, credenziali o configurazioni operative sensibili;
- certificazioni formali di terza parte.

## 3. Obiettivi

| ID | Obiettivo | Criterio di completamento |
|---|---|---|
| `DSG-MR-OBJ-001` | Rendere la documentazione enterprise navigabile | Sezione MkDocs dedicata e link interni risolti |
| `DSG-MR-OBJ-002` | Allineare architettura, rischi e requisiti | Matrici e registri con ID stabili |
| `DSG-MR-OBJ-003` | Formalizzare decisioni e governance | ADR, ruoli, workflow e quality gate pubblicati |
| `DSG-MR-OBJ-004` | Rendere le procedure eseguibili | SOP con trigger, ruoli, passi, output e controlli |
| `DSG-MR-OBJ-005` | Preparare la release documentale | Release documentation e checklist di readiness disponibili |

## 4. Milestone

| Milestone | ID | Deliverable | Stato | Evidenza |
|---|---|---|---|---|
| Roadmap e indice enterprise | `DSG-MR-M1` | `enterprise/index.md`, roadmap `DSG-MR-001` | Completata | Navigazione MkDocs |
| Architettura e decisioni | `DSG-MR-M2` | Enterprise Architecture, ADR-004 | Completata | Documenti `DSG-EA-001`, `DSG-ADR-004` |
| Rischi e controlli | `DSG-MR-M3` | DSRA e registri rischio/controlli | Completata | `DSG-DSRA-001`, `DSG-REG-001` |
| Operatività | `DSG-MR-M4` | Handbook, SOP, governance | Completata | `DSG-HBK-001`, `DSG-SOP-001`, `DSG-GOV-001` |
| Assessment e release | `DSG-MR-M5` | Assessment, release documentation, appendici | Completata | `DSG-ASMT-001`, `DSG-REL-001`, `DSG-APP-001` |

## 5. Deliverable minimi

| ID | Deliverable | Documento primario | Collegamenti |
|---|---|---|---|
| `DSG-DEL-001` | Master Roadmap | Questo documento | Registri, governance, release |
| `DSG-DEL-002` | Enterprise Architecture | `DSG-EA-001` | ADR, requisiti, manuale tecnico |
| `DSG-DEL-003` | DSRA | `DSG-DSRA-001` | FMEA, controlli, SOP |
| `DSG-DEL-004` | ADR enterprise | `DSG-ADR-004` | Architecture, governance |
| `DSG-DEL-005` | Registri | `DSG-REG-001` | Tutti i documenti enterprise |
| `DSG-DEL-006` | Handbook | `DSG-HBK-001` | SOP, governance |
| `DSG-DEL-007` | SOP | `DSG-SOP-001` | DSRA, release |
| `DSG-DEL-008` | Assessment | `DSG-ASMT-001` | Roadmap, controlli |
| `DSG-DEL-009` | Governance | `DSG-GOV-001` | Handbook, registri |
| `DSG-DEL-010` | Release documentation | `DSG-REL-001` | Release notes, checklist |
| `DSG-DEL-011` | Appendici | `DSG-APP-001` | Glossario e template |

## 6. Matrice di tracciabilità

| Obiettivo | Requisiti | Rischi | Controlli | Deliverable |
|---|---|---|---|---|
| `DSG-MR-OBJ-001` | `DSG-REQ-DOC-001`, `DSG-REQ-DOC-002` | `DSG-RSK-DOC-001` | `DSG-CTL-DOC-001` | `DSG-DEL-001`, `DSG-DEL-005` |
| `DSG-MR-OBJ-002` | `DSG-REQ-ARC-001`, `DSG-REQ-SAF-001` | `DSG-RSK-OPS-001`, `DSG-RSK-DATA-001` | `DSG-CTL-ARC-001`, `DSG-CTL-SAF-001` | `DSG-DEL-002`, `DSG-DEL-003` |
| `DSG-MR-OBJ-003` | `DSG-REQ-GOV-001`, `DSG-REQ-ADR-001` | `DSG-RSK-GOV-001` | `DSG-CTL-GOV-001`, `DSG-CTL-ADR-001` | `DSG-DEL-004`, `DSG-DEL-009` |
| `DSG-MR-OBJ-004` | `DSG-REQ-OPS-001`, `DSG-REQ-OPS-002` | `DSG-RSK-OPS-002` | `DSG-CTL-OPS-001`, `DSG-CTL-OPS-002` | `DSG-DEL-006`, `DSG-DEL-007` |
| `DSG-MR-OBJ-005` | `DSG-REQ-REL-001`, `DSG-REQ-QA-001` | `DSG-RSK-REL-001` | `DSG-CTL-REL-001`, `DSG-CTL-QA-001` | `DSG-DEL-008`, `DSG-DEL-010`, `DSG-DEL-011` |

## 7. Criteri di accettazione

La roadmap è completata quando:

- ogni deliverable minimo ha una pagina pubblicata;
- `mkdocs.yml` espone la sezione enterprise;
- i registri contengono ID, stato, owner e relazione con `DSG-MR-001`;
- le SOP indicano trigger, ruoli, passi, output e controlli;
- DSRA e assessment hanno criteri di valutazione espliciti;
- la release documentation definisce readiness, rollback e note di rilascio;
- la Pull Request verso `main` riporta milestone, commit e validazioni.

## 8. Manutenzione

La roadmap viene riesaminata:

- a ogni release documentale;
- dopo una modifica architetturale rilevante;
- dopo un incidente operativo con impatto su sicurezza o continuità;
- quando un registro segnala un rischio o un requisito non più allineato.

Ogni revisione deve aggiornare il change log nel registro enterprise.
