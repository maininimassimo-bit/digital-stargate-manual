# DSG-GOV-001 - Governance Enterprise

| Campo | Valore |
|---|---|
| Documento | Governance Enterprise |
| Identificativo | `DSG-GOV-001` |
| Roadmap | `DSG-MR-001` |
| Versione | 1.0 |
| Stato | Approvata per revisione |
| Owner | Massimo Mainini |
| Data baseline | 26/07/2026 |

## 1. Scopo

La governance definisce ruoli, processi decisionali, controlli di qualità, gestione delle modifiche e criteri di manutenzione della documentazione enterprise Digital StarGate.

## 2. Modello RACI

| Attività | Owner | Contributor | Reviewer | Approver |
|---|---|---|---|---|
| Roadmap enterprise | Governance Owner | Documentation Owner | Architecture Owner | Massimo Mainini |
| Architettura | Architecture Owner | Data Owner | Reviewer tecnico | Massimo Mainini |
| DSRA | Operations Owner | Infrastructure Owner | Governance Owner | Massimo Mainini |
| SOP | Operations Owner | Documentation Owner | Reviewer operativo | Massimo Mainini |
| Registri | Documentation Owner | Tutti gli owner | Governance Owner | Massimo Mainini |
| Release | Release Owner | Documentation Owner | Reviewer | Massimo Mainini |

## 3. Processi decisionali

| Tipo decisione | Strumento | Criterio |
|---|---|---|
| Architetturale | ADR | Impatta componenti, dati, deployment o confini di responsabilità |
| Operativa | SOP o capitolo manuale | Impatta avvio, chiusura, recovery o manutenzione |
| Documentale | Registro e PR | Impatta navigazione, struttura o template |
| Release | Release documentation | Impatta readiness, rollback o comunicazione |
| Rischio | DSRA | Impatta safety, continuità, dati o sicurezza |

## 4. Change management

Ogni cambiamento passa da:

1. identificazione;
2. classificazione;
3. valutazione impatti;
4. aggiornamento documentale;
5. aggiornamento registri;
6. validazione;
7. PR e review;
8. rilascio o follow-up.

## 5. Quality gate

| Gate | Applicazione | Bloccante |
|---|---|---|
| `DSG-QG-DOC-001` | Link e navigazione | Si |
| `DSG-QG-DOC-002` | Assenza marcatori aperti | Si |
| `DSG-QG-GOV-001` | Registri aggiornati | Si per modifiche enterprise |
| `DSG-QG-ADR-001` | ADR per decisione strutturale | Si quando applicabile |
| `DSG-QG-REL-001` | Release readiness | Si per release |
| `DSG-QG-SEC-001` | Assenza segreti | Sempre bloccante |

## 6. Review

La review deve controllare:

- coerenza con `DSG-MR-001`;
- correttezza tecnica;
- sufficienza delle evidenze;
- assenza di contenuti fuorvianti;
- coerenza tra registri e documenti;
- impatto sulla navigazione e sulla release.

## 7. Ciclo di riesame

| Oggetto | Frequenza minima | Evento straordinario |
|---|---|---|
| Roadmap | A ogni release | Cambio strategico |
| DSRA | Semestrale | Incidente o near miss |
| Registri | Ogni PR enterprise | Nuovo rischio o requisito |
| SOP | Semestrale | Procedura fallita o cambiamento operativo |
| ADR | Trimestrale | Decisione superata |
| Release documentation | Ogni release | Rollback o hotfix |

## 8. Criteri di accettazione

La governance è efficace quando:

- ogni documento enterprise ha owner e stato;
- le modifiche sono tracciate in PR e change log;
- i rischi hanno controlli;
- le decisioni strutturali hanno ADR;
- la release non procede senza readiness documentata.
