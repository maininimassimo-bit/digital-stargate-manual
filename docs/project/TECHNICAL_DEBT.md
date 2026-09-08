# Technical Debt Register

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-DEBT-001 |
| Versione | 1.8 |
| Stato | Active |
| Data review | 08/09/2026 |

## 1. Scopo

Registrare esclusivamente debito tecnico noto, accettato e tracciato. Problemi operativi, difetti aperti e attività pianificate appartengono rispettivamente a incident management, bug tracking e backlog.

## 2. Regole

Ogni voce deve includere: identificativo, descrizione, causa, impatto, rischio, area, priorità, owner, strategia di rimozione, dipendenze, stato e data di revisione.

Stati ammessi: `Proposed`, `Accepted`, `Mitigated`, `Scheduled`, `Resolved`, `Rejected`. Priorità: `P0` critica, `P1` alta, `P2` media, `P3` bassa.

## 3. Registro

| ID | Area | Debito | Impatto/Rischio | Priorità | Stato | Strategia / evidence |
|---|---|---|---|---|---|---|
| TD-001 | Portal Theme | Gestione tema accoppiata al DOM interno di Material in `page-enhancements.js` | Pulsante fragile e responsabilità errata | P0 | Resolved | WP-03 Enterprise Theme Framework `Completed / Accepted`; Theme Service centralizzato in `dsg-theme-manager.js` |
| TD-002 | Portal JS | Presenza di logica inline in alcune pagine | Duplicazione, coupling e incompatibilità con Instant Navigation | P1 | Resolved | JavaScript eseguibile inline eliminato; gate `verify-no-inline-portal-js.mjs`; BKL-010 closure 30/08/2026 |
| TD-003 | Repository Entry Point | README root descriveva soprattutto il manuale storico | Onboarding incompleto | P1 | Resolved | README root riallineato alla piattaforma; BKL-008 closure 29/08/2026 |
| TD-004 | CI/CD | Coesistenza di workflow documentali attivi, disabilitati e storici | Ownership ambigua | P1 | Resolved | `deploy-pages.yml` unico owner Pages; `docs.yml` validation-only; BKL-007 closure |
| TD-005 | Projections | Roadmap e dashboard JSON possono divergere dalle fonti autorevoli | Stato visualizzato obsoleto | P1 | Resolved | Consistency gate AMP-002/roadmap/backlog attivo nel Developer Foundation; BKL-009 Done |
| TD-006 | Documentation IA | Project Governance Center non integrato nella nav MkDocs | Documenti canonici difficili da scoprire | P1 | Resolved | `mkdocs.yml` include Project Governance; BKL-002 Done |
| TD-007 | Release History | Guide e release storiche in root non sempre contestualizzate | Possibile confusione con baseline corrente | P2 | Accepted | Creare indice storico e dichiarare stato/supersession — BKL-016 |
| TD-008 | Knowledge Traceability | Collegamenti AP/ADR/componenti/evidence non machine-readable | Analisi manuale e rischio di gap | P2 | Resolved | BKL-015 F1-F3 accepted; merge F3 `c1a9f96b34a23407c5804e7fd6facfbad226f8fc` |
| TD-009 | EAGLE Reporting Automation | Launcher EAGLE inizialmente non governato dalla source of truth | Configuration drift | P1 | Mitigated | Runtime inspection, SHA/task definition e AP-014 OAT completati; mantenere change control |
| TD-010 | EAGLE Session Launcher | Un'eccezione dopo la creazione del session branch può lasciare il runtime clone fuori da `main` | Preflight successivo fail-closed e recovery manuale | P1 | Accepted | Introdurre restore-to-main governato in `finally` o equivalente, senza reset distruttivi; regression test obbligatorio |
| TD-011 | Reporting CI | Copertura quality gate 1.0.7/1.0.8 non ancora riconciliata formalmente con tutti i check storici pre-remediation | Possibile perdita silenziosa di controlli | P2 | Accepted | Confrontare gate storico/corrente e ripristinare check applicabili con workflow evidence |
| TD-012 | BKL-040 Timeline Contract | F2 accepted contract non riproduce tutti i minimum-envelope field dichiarati in F1 e usa il proprio tie-break deterministico basato su `replay_event_id` anziché il F1 `source_event_id` | Futuri consumer possono assumere una envelope uniforme inesistente o introdurre incompatibilità retroattiva | P2 | Accepted | Non retrofit silenzioso della F2 accepted baseline. Qualunque normalizzazione deve essere un incremento/versione compatibile, con migration contract, fail-closed tests e ARB review. Closure BKL-040 documenta esplicitamente il boundary. |

## 4. Criteri di rimozione

Una voce può essere chiusa solo quando la modifica è implementata, i test applicabili sono eseguiti, non sono introdotti debiti equivalenti, documentazione/backlog/decision log sono aggiornati o verificati non applicabili ed esiste evidence verificabile.

## 5. Review 08/09/2026

La review riconcilia il registro con BKL-040 e le foundation precedenti:

- TD-001–TD-006 e TD-008 restano `Resolved`;
- TD-007, TD-010 e TD-011 restano `Accepted`;
- TD-009 resta `Mitigated`;
- viene registrato **TD-012** per rendere esplicita la compatibilità bounded tra BKL-040 F1 e l'accepted F2 contract, evitando di nascondere o retrofittare il debito durante la closure;
- TD-012 non mette in discussione l'acceptance F2/F3/F4: governa una futura eventuale normalizzazione compatibile;
- la copertura eseguibile BKL-040 resta bounded: NINA/PHD2/CloudWatcher e session projection dove definita; nessuna dichiarazione implicita di materializzazione Power/Network/Safety;
- nessuna nuova authority, command path, remediation authority o Safety Authority coupling viene introdotta dalla closure.