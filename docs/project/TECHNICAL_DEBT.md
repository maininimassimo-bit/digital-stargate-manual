# Technical Debt Register

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-DEBT-001 |
| Versione | 1.7 |
| Stato | Active |
| Data review | 06/09/2026 |

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
| TD-002 | Portal JS | Presenza di logica inline in alcune pagine | Duplicazione, coupling e incompatibilità con Instant Navigation | P1 | Resolved | JavaScript eseguibile inline eliminato dalla baseline documentale; gate `.github/scripts/verify-no-inline-portal-js.mjs` applicato sia a `docs.yml` sia a `deploy-pages.yml`; validation #383 e Pages #558 PASS; BKL-010 closure 30/08/2026 |
| TD-003 | Repository Entry Point | README root descrive soprattutto il manuale storico | Onboarding incompleto e rappresentazione non aggiornata della piattaforma | P1 | Resolved | README root riallineato alla piattaforma Digital StarGate: manuale, Enterprise Architecture, Portal, Developer Foundation, Observatory Status, scientific platform, governance e CI/CD; BKL-008 closure 29/08/2026; commit `9da5ec55bd7f995ad602bbcd3db92058176c3a4c` |
| TD-004 | CI/CD | Coesistenza di workflow documentali attivi, disabilitati e storici | Ownership ambigua e rischio di pubblicazioni duplicate | P1 | Resolved | `deploy-pages.yml` designato unico owner GitHub Pages; `docs.yml` validation-only senza Pages write permission; legacy `docs.yml.disabled` rimosso; BKL-007 closure baseline 28/08/2026 |
| TD-005 | Projections | Roadmap e dashboard JSON possono divergere dalle fonti autorevoli | Stato visualizzato obsoleto | P1 | Resolved | Consistency gate AMP-002/roadmap/backlog attivo nel Developer Foundation; BKL-009 Done sulla baseline 28/08/2026 |
| TD-006 | Documentation IA | Project Governance Center non integrato nella nav MkDocs | Documenti canonici difficili da scoprire | P1 | Resolved | `mkdocs.yml` contiene la sezione `Project Governance`; Governance Center e registri canonici sono navigabili; BKL-002 Done |
| TD-007 | Release History | Guide e release storiche in root non sempre contestualizzate | Possibile confusione con baseline corrente | P2 | Accepted | Creare indice storico e dichiarare stato/supersession — BKL-016 |
| TD-008 | Knowledge Traceability | Collegamenti AP/ADR/componenti/evidence non machine-readable | Analisi manuale e rischio di gap | P2 | Resolved | BKL-015 F1-F3: schema/IDs/source locator, AP+ADR identity coverage 100%, component+evidence identity e material-relation coverage 100% sull'Architecture Artifact Register; merge F3 `c1a9f96b34a23407c5804e7fd6facfbad226f8fc`; post-merge DF #963, docs #572, Pages #685, Word #997 SUCCESS |
| TD-009 | EAGLE Reporting Automation | Launcher EAGLE inizialmente non governato dalla source of truth | Rischio di configuration drift e regressioni non tracciate | P1 | Mitigated | Runtime inspection, SHA/task definition e AP-014 OAT completati; Reporting 1.0.8 ha corretto Git stderr PS5.1 e drift evidence window; mantenere baseline governata e change control. |
| TD-010 | EAGLE Session Launcher | Un'eccezione dopo la creazione del session branch può lasciare il runtime clone fuori da `main` | Il preflight del run successivo fallisce chiuso e richiede recovery manuale; rischio di interruzione della pipeline automatica | P1 | Accepted | Evidence reale 03/09/2026: failure dopo `git checkout -b` ha lasciato `session/2026-09-02_2026-09-03`; introdurre restore-to-main governato in `finally` o equivalente preservando package/evidence e senza reset distruttivi; regression test obbligatorio. |
| TD-011 | Reporting CI | Copertura quality gate 1.0.7/1.0.8 non ancora riconciliata formalmente con tutti i check storici pre-remediation | Possibile perdita silenziosa di controlli installer/launcher/task/runtime pur con regression test incident-specific verdi | P2 | Accepted | Confrontare gate storico e corrente; ripristinare i check applicabili mantenendo test SQM, exact evidence selection e PS5.1 publish; chiudere solo con workflow evidence. |

## 4. Criteri di rimozione

Una voce può essere chiusa solo quando:

- la modifica è implementata;
- i test applicabili sono eseguiti;
- non sono introdotti debiti equivalenti;
- documentazione, backlog e decision log sono aggiornati o verificati non applicabili;
- esiste un commit o una evidence verificabile.

## 5. Review 06/09/2026

La review riconcilia il registro con la closure BKL-015:

- TD-001–TD-006 restano `Resolved`;
- TD-007 resta `Accepted` e mappato a BKL-016;
- **TD-008 passa a `Resolved`**: BKL-015 F1-F3 copre le quattro classi dichiarate dal debito — AP, ADR, componenti, evidence — con identità/source locator machine-readable e gate CI di coverage/material relations;
- la closure TD-008 non include scientific claim, AI confidence, recommendation provenance, graph DB, vector DB o RAG; tali evoluzioni restano BKL-044 o package successivi;
- TD-009 resta `Mitigated`;
- TD-010 e TD-011 restano `Accepted` e indipendenti da BKL-015;
- nessun nuovo debito equivalente di Knowledge Traceability è stato identificato nella closure review;
- il Decision Log non richiede una nuova decisione: la closure applica roadmap e governance già approvate senza cambiare authority, boundary, safety, security o contratto pubblico.
