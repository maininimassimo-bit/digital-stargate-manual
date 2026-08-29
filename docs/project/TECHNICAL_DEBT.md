# Technical Debt Register

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-DEBT-001 |
| Versione | 1.4 |
| Stato | Active |
| Data review | 29/08/2026 |

## 1. Scopo

Registrare esclusivamente debito tecnico noto, accettato e tracciato. Problemi operativi, difetti aperti e attività pianificate appartengono rispettivamente a incident management, bug tracking e backlog.

## 2. Regole

Ogni voce deve includere: identificativo, descrizione, causa, impatto, rischio, area, priorità, owner, strategia di rimozione, dipendenze, stato e data di revisione.

Stati ammessi: `Proposed`, `Accepted`, `Mitigated`, `Scheduled`, `Resolved`, `Rejected`.

Priorità: `P0` critica, `P1` alta, `P2` media, `P3` bassa.

## 3. Registro

| ID | Area | Debito | Impatto/Rischio | Priorità | Stato | Strategia / evidence |
|---|---|---|---|---|---|---|
| TD-001 | Portal Theme | Gestione tema accoppiata al DOM interno di Material in `page-enhancements.js` | Pulsante fragile e responsabilità errata | P0 | Resolved | WP-03 Enterprise Theme Framework `Completed / Accepted`; Theme Service centralizzato in `dsg-theme-manager.js`, separato da `page-enhancements.js`; commit funzionale `5cb6cd3454b2b1d95fcf8ede3b42352e41514d88` |
| TD-002 | Portal JS | Presenza di logica inline in alcune pagine | Duplicazione, coupling e incompatibilità con Instant Navigation | P1 | Accepted | Migrare progressivamente in moduli proprietari — BKL-010 |
| TD-003 | Repository Entry Point | README root descrive soprattutto il manuale storico | Onboarding incompleto e rappresentazione non aggiornata della piattaforma | P1 | Resolved | README root riallineato alla piattaforma Digital StarGate: manuale, Enterprise Architecture, Portal, Developer Foundation, Observatory Status, scientific platform, governance e CI/CD; BKL-008 closure 29/08/2026; commit `9da5ec55bd7f995ad602bbcd3db92058176c3a4c` |
| TD-004 | CI/CD | Coesistenza di workflow documentali attivi, disabilitati e storici | Ownership ambigua e rischio di pubblicazioni duplicate | P1 | Resolved | `deploy-pages.yml` designato unico owner GitHub Pages; `docs.yml` validation-only senza Pages write permission; legacy `docs.yml.disabled` rimosso; BKL-007 closure baseline 28/08/2026 |
| TD-005 | Projections | Roadmap e dashboard JSON possono divergere dalle fonti autorevoli | Stato visualizzato obsoleto | P1 | Resolved | Consistency gate AMP-002/roadmap/backlog attivo nel Developer Foundation; BKL-009 Done sulla baseline 28/08/2026 |
| TD-006 | Documentation IA | Project Governance Center non integrato nella nav MkDocs | Documenti canonici difficili da scoprire | P1 | Resolved | `mkdocs.yml` contiene la sezione `Project Governance`; Governance Center e registri canonici sono navigabili; BKL-002 Done |
| TD-007 | Release History | Guide e release storiche in root non sempre contestualizzate | Possibile confusione con baseline corrente | P2 | Accepted | Creare indice storico e dichiarare stato/supersession — BKL-016 |
| TD-008 | Knowledge Traceability | Collegamenti AP/ADR/componenti/evidence non ancora machine-readable | Analisi manuale e rischio di gap | P2 | Accepted | GP-003 Knowledge Graph e schema di relazione versionato — BKL-015 |
| TD-009 | EAGLE Reporting Automation | Launcher EAGLE inizialmente non governato dalla source of truth | Rischio di configuration drift e regressioni non tracciate | P1 | Mitigated | Runtime inspection, SHA/task definition e AP-014 OAT completati; mantenere la baseline governata e il change control. Non riaprire AP-014 salvo drift o modifica runtime. |

## 4. Criteri di rimozione

Una voce può essere chiusa solo quando:

- la modifica è implementata;
- i test applicabili sono eseguiti;
- non sono introdotti debiti equivalenti;
- documentazione, backlog e decision log sono aggiornati;
- esiste un commit o una evidence verificabile.

## 5. Review 29/08/2026

La review ha riconciliato il registro con la repository truth:

- TD-001 e TD-006 restano `Resolved`;
- TD-003 è `Resolved`: il README root rappresenta ora il repository come piattaforma Digital StarGate e indirizza alle fonti canoniche senza duplicare lo stato dinamico del programma;
- TD-004 è `Resolved`: `deploy-pages.yml` è l'unico workflow autorizzato a pubblicare GitHub Pages, mentre `docs.yml` è esplicitamente validation-only; il workflow legacy disabilitato è stato ritirato;
- TD-005 è `Resolved`: il consistency gate AMP-002/roadmap/backlog è attivo e BKL-009 è Done;
- TD-009 resta `Mitigated` dalle runtime inspection e acceptance AP-014, pur restando soggetto a change control;
- TD-002/007/008 restano debito reale e sono mappati ai rispettivi backlog item;
- BKL-027/BKL-028 Power/Network sono Done e non costituiscono debito tecnico aperto.
