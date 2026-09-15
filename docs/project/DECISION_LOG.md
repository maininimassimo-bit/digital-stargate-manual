# Decision Log

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-DEC-001 |
| Versione | 1.6 |
| Stato | Active |
| Data baseline | 15/09/2026 |

## 1. Scopo

Registrare decisioni operative, di governance e di implementazione che devono essere tracciate ma non modificano principi architetturali, authority, boundary o invarianti al punto da richiedere un ADR.

## 2. Quando usare il Decision Log

Usare questo registro per decisioni reversibili, circoscritte a processo, naming, organizzazione o implementazione, senza modifica dei contratti pubblici, dei boundary tra layer/bounded context o di safety/security authority e command model.

Creare invece un ADR quando la decisione modifica un principio architetturale, introduce o cambia un boundary, modifica contratti pubblici o compatibilità, introduce una tecnologia strutturale difficilmente reversibile, modifica authority/safety/security/data ownership o condiziona più release/capability.

## 3. Stati

- `Proposed`
- `Accepted`
- `Superseded`
- `Rejected`
- `Retired`

## 4. Registro

| ID | Data | Decisione | Motivazione | Ambito | Stato | Riferimenti |
|---|---|---|---|---|---|---|
| DLG-001 | 04/08/2026 | Il repository GitHub è la fonte autorevole; le conversazioni sono solo contesto ausiliario | Ridurre dipendenza dalla memoria e garantire tracciabilità | Governance | Accepted | `ENTERPRISE_ARCHITECTURE_CONTEXT.md` |
| DLG-002 | 04/08/2026 | Introdurre `docs/project/` come Project Governance Center | Centralizzare baseline, standard, backlog e registri senza duplicare AP/ADR | Documentation IA | Accepted | `docs/project/index.md` |
| DLG-003 | 04/08/2026 | Usare `ENTERPRISE_ARCHITECTURE_CONTEXT.md` come bootstrap di ogni nuova sessione | Prima regola di bootstrap, successivamente sostituita dal root bootstrap universale | Governance | Superseded | Superseded by DLG-010; DSG-CTX-001 resta mandatory context dopo `AI_BOOTSTRAP.md` |
| DLG-004 | 04/08/2026 | Mantenere separati Context, Knowledge Map, Backlog, Technical Debt e Decision Log | Evitare ownership sovrapposte e ambiguità | Governance | Accepted | GP-001 |
| DLG-005 | 04/08/2026 | Il Navigation Manager resta in `page-enhancements.js`; la gestione tema ha un componente dedicato | Applicare responsabilità singola ed eliminare coupling fragile | Portal JS | Accepted | RC1-HF01, TD-001 |
| DLG-006 | 04/08/2026 | Lo Scientific Data Engine è l'unico access layer condiviso per i componenti scientifici del portale | Evitare parsing e accessi paralleli ai dataset | Scientific Portal | Accepted | `scientific-data-engine.js` |
| DLG-007 | 04/08/2026 | I dataset JSON del portale sono proiezioni e non fonti primarie | Preservare data authority e ricostruibilità | Data Governance | Accepted | AP-002, AMP-002 |
| DLG-008 | 04/08/2026 | Il Governance Framework viene completato prima di RC1-HF01 | Stabilizzare contesto e processo prima della hotfix | Sequencing | Accepted | GP-001, RC1-HF01 |
| DLG-009 | 04/08/2026 | I documenti governance vengono creati incrementalmente con commit coerenti | Ridurre rischio e consentire review puntuale | Delivery | Accepted | `DEVELOPMENT_WORKFLOW.md` |
| DLG-010 | 04/08/2026 | `AI_BOOTSTRAP.md` è il punto di ingresso root per persone e assistenti AI | Rendere immediatamente visibile il percorso di lettura e subordinare i documenti di contesto a un entry point universale | Onboarding | Accepted | `AI_BOOTSTRAP.md`; supersedes DLG-003 as entry point |
| DLG-011 | 05/08/2026 | Il Chief Architect AI è autorizzato a utilizzare autonomamente il connettore GitHub fino al completamento del progetto, entro roadmap e boundary approvati | Eliminare approvazioni ripetitive e consentire esecuzione end-to-end delle milestone | Delivery Governance | Accepted | `DEVELOPMENT_WORKFLOW.md` v2.0 |
| DLG-012 | 05/08/2026 | Le milestone approvate vengono eseguite autonomamente fino alla chiusura tecnica e documentale | Ridurre handoff e mantenere responsabilità unitaria sulla delivery | Delivery Governance | Accepted | `DEVELOPMENT_WORKFLOW.md` v2.0 |
| DLG-013 | 05/08/2026 | Per file grandi o change set controllati si adottano le Git Database API (`blob -> tree -> commit -> ref`) | Evitare limiti e rischi delle sostituzioni complete tramite Contents API | Repository Operations | Accepted | commit `801c6246983af85fba571515f48fc038cccfcbcf` |

| DLG-014 | 15/09/2026 | Promuovere BKL-031 F3-A1 come package documentale e definire normativamente gli intervalli UTC half-open prima di ogni materializzazione | Rimuovere l'ambiguità di ARB-191-MI02 senza anticipare schema, dati o runtime | BKL-031 F3-A1 | Accepted | F3-A1 handoff/contract/validation plan |
| DLG-015 | 15/09/2026 | Selezionare BKL-031 F3-A2 Setup Authority Contract come successore, iniziando da un Program Assessment/Handoff esclusivamente documentale | Completare in dependency order l'autorità setup dopo il contratto sito, senza anticipare materializzazione, provider o runtime | BKL-031 F3-A2 | Accepted | BKL-031-F3-A2-PROGRAM-001 |
| DLG-016 | 15/09/2026 | Attivare il mandato continuativo `DSG-AEM-001` e la deroga condizionata `W-DSG-AEM-RULESET-001` fino a completamento o revoca | Ridurre handoff autorizzativi mantenendo exact-head CI, review applicabile, rollback, privacy, safety, audit e post-merge | Delivery Governance | Accepted | `DSG-AEM-001-CONTINUOUS-AUTONOMOUS-EXECUTION-MANDATE-2026-09-15.md`; owner authorization 15/09/2026 |
| DLG-017 | 15/09/2026 | F3-A2 usa un reference envelope version-pinned verso una concrete approved baseline, distinta da AP-006 architecture authority e dall'observed state | Risolvere ARB-195-MI01 senza inventare baseline, owner o materializzazione e mantenere S09 fail-closed | BKL-031 F3-A2 | Proposed | `BKL-031-F3-A2-CONTRACT-001`; `BKL-031-F3-A2-VAL-001` |

## 5. Delega operativa GitHub

La delega comprende, entro lo scope approvato: lettura e ricerca nel repository; creazione/aggiornamento/ritiro di file; commit e aggiornamenti fast-forward; controllo GitHub Actions, job, log e artifact; verifica GitHub Pages; correzione autonoma di errori coerenti con la milestone; review AI-assistite; merge condizionati; post-merge verification; aggiornamento dei registri di governance. `DSG-AEM-001` è la definizione operativa corrente.

Richiedono sempre approvazione esplicita: force push o aggiornamento non fast-forward; operazioni distruttive non previste; ampliamento dello scope o deviazione dalla roadmap; nuove integrazioni o dipendenze strutturali; cambi di boundary, authority, safety, security o contratti pubblici.

## 6. Relazioni con altri registri

- un compromesso accettato con costo futuro va in `TECHNICAL_DEBT.md`;
- un'attività da eseguire va in `BACKLOG.md`;
- un difetto va nel sistema di issue/bug tracking;
- una decisione strutturale va in un ADR;
- una variazione di roadmap va prima nella source governata applicabile e poi nelle proiezioni.

## 7. Review 08/09/2026

La closure BKL-040 e la promozione dependency-driven di BKL-038 non introducono una nuova decisione architetturale: applicano dipendenze e governance già approvate. La review elimina invece l'ambiguità storica tra DLG-003 e DLG-010: `AI_BOOTSTRAP.md` è l'unico root entry point; Enterprise Architecture Context e Repository Knowledge Map restano documenti obbligatori nella sequenza di bootstrap.
