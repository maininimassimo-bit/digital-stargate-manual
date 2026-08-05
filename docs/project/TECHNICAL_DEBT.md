# Technical Debt Register

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-DEBT-001 |
| Versione | 1.0 |
| Stato | Active |

## 1. Scopo

Registrare esclusivamente debito tecnico noto, accettato e tracciato. Problemi operativi, difetti aperti e attività pianificate appartengono rispettivamente a incident management, bug tracking e backlog.

## 2. Regole

Ogni voce deve includere: identificativo, descrizione, causa, impatto, rischio, area, priorità, owner, strategia di rimozione, dipendenze, stato e data di revisione.

Stati ammessi: `Proposed`, `Accepted`, `Mitigated`, `Scheduled`, `Resolved`, `Rejected`.

Priorità: `P0` critica, `P1` alta, `P2` media, `P3` bassa.

## 3. Registro iniziale

| ID | Area | Debito | Impatto/Rischio | Priorità | Stato | Strategia |
|---|---|---|---|---|---|---|
| TD-001 | Portal Theme | Gestione tema accoppiata al DOM interno di Material in `page-enhancements.js` | Pulsante fragile e responsabilità errata | P0 | Scheduled | RC1-HF01: introdurre `dsg-theme-manager.js` e rimuovere l'handler fragile |
| TD-002 | Portal JS | Presenza di logica inline in alcune pagine | Duplicazione, coupling e incompatibilità con Instant Navigation | P1 | Accepted | Migrare progressivamente in moduli proprietari |
| TD-003 | Repository Entry Point | README root descrive soprattutto il manuale storico | Onboarding incompleto e rappresentazione non aggiornata della piattaforma | P1 | Accepted | Riallineare README dopo completamento Governance Foundation |
| TD-004 | CI/CD | Coesistenza di workflow documentali attivi, disabilitati e storici | Ownership ambigua e rischio di pubblicazioni duplicate | P1 | Accepted | Inventariare, designare workflow autorevoli e ritirare i duplicati |
| TD-005 | Projections | Roadmap e dashboard JSON possono divergere dalle fonti autorevoli | Stato visualizzato obsoleto | P1 | Accepted | Aggiungere controlli di coerenza e generation pipeline tracciata |
| TD-006 | Documentation IA | Project Governance Center non ancora integrato nella nav MkDocs | Documenti canonici difficili da scoprire | P1 | Scheduled | Aggiornare `mkdocs.yml` nello stesso package di chiusura |
| TD-007 | Release History | Guide e release storiche in root non sempre contestualizzate | Possibile confusione con baseline corrente | P2 | Accepted | Creare indice storico e dichiarare stato/supersession |
| TD-008 | Knowledge Traceability | Collegamenti AP/ADR/componenti/evidence non ancora machine-readable | Analisi manuale e rischio di gap | P2 | Accepted | GP-003 Knowledge Graph e schema di relazione versionato |

## 4. Criteri di rimozione

Una voce può essere chiusa solo quando:

- la modifica è implementata;
- i test applicabili sono eseguiti;
- non sono introdotti debiti equivalenti;
- documentazione, backlog e decision log sono aggiornati;
- esiste un commit o una evidence verificabile.

## 5. Review

Il registro deve essere riesaminato a ogni release, hotfix, Architecture Package o modifica di governance.