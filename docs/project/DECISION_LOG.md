# Decision Log

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-DEC-001 |
| Versione | 1.1 |
| Stato | Active |
| Data baseline | 05/08/2026 |

## 1. Scopo

Registrare decisioni operative, di governance e di implementazione che devono essere tracciate ma non modificano principi architetturali, authority, boundary o invarianti al punto da richiedere un ADR.

## 2. Quando usare il Decision Log

Usare questo registro per decisioni:

- reversibili;
- circoscritte a processo, naming, organizzazione o implementazione;
- senza impatto sui contratti pubblici;
- senza modifica dei boundary tra layer o bounded context;
- senza modifica di safety, security authority o command model.

Creare invece un ADR quando la decisione:

- modifica un principio architetturale;
- introduce o cambia un boundary;
- modifica contratti pubblici o compatibilità;
- introduce una tecnologia strutturale difficilmente reversibile;
- modifica authority, safety, security o data ownership;
- condiziona più release o capability.

## 3. Stati

- `Proposed`
- `Accepted`
- `Superseded`
- `Rejected`
- `Retired`

## 4. Registro iniziale

| ID | Data | Decisione | Motivazione | Ambito | Stato | Riferimenti |
|---|---|---|---|---|---|---|
| DLG-001 | 04/08/2026 | Il repository GitHub è la fonte autorevole; le conversazioni sono solo contesto ausiliario | Ridurre dipendenza dalla memoria e garantire tracciabilità | Governance | Accepted | `ENTERPRISE_ARCHITECTURE_CONTEXT.md` |
| DLG-002 | 04/08/2026 | Introdurre `docs/project/` come Project Governance Center | Centralizzare baseline, standard, backlog e registri senza duplicare AP/ADR | Documentation IA | Accepted | `docs/project/index.md` |
| DLG-003 | 04/08/2026 | Usare `ENTERPRISE_ARCHITECTURE_CONTEXT.md` come bootstrap di ogni nuova sessione | Rendere ripetibile la ripresa del progetto | Governance | Accepted | DSG-CTX-001 |
| DLG-004 | 04/08/2026 | Mantenere separati Context, Knowledge Map, Backlog, Technical Debt e Decision Log | Evitare ownership sovrapposte e ambiguità | Governance | Accepted | GP-001 |
| DLG-005 | 04/08/2026 | Il Navigation Manager resta in `page-enhancements.js`; la gestione tema ha un componente dedicato | Applicare responsabilità singola ed eliminare coupling fragile | Portal JS | Accepted | RC1-HF01, TD-001 |
| DLG-006 | 04/08/2026 | Lo Scientific Data Engine è l'unico access layer condiviso per i componenti scientifici del portale | Evitare parsing e accessi paralleli ai dataset | Scientific Portal | Accepted | `scientific-data-engine.js` |
| DLG-007 | 04/08/2026 | I dataset JSON del portale sono proiezioni e non fonti primarie | Preservare data authority e ricostruibilità | Data Governance | Accepted | AP-002, AMP-002 |
| DLG-008 | 04/08/2026 | Il Governance Framework viene completato prima di RC1-HF01 | Stabilizzare contesto e processo prima della hotfix | Sequencing | Accepted | GP-001, RC1-HF01 |
| DLG-009 | 04/08/2026 | I documenti governance vengono creati incrementalmente con commit coerenti | Ridurre rischio e consentire review puntuale | Delivery | Accepted | `DEVELOPMENT_WORKFLOW.md` |
| DLG-010 | 04/08/2026 | `AI_BOOTSTRAP.md` è il punto di ingresso root per persone e assistenti AI | Rendere immediatamente visibile il percorso di lettura | Onboarding | Accepted | GP-001 |
| DLG-011 | 05/08/2026 | Il Chief Architect AI è autorizzato a utilizzare autonomamente il connettore GitHub fino al completamento del progetto, entro roadmap e boundary approvati | Eliminare approvazioni ripetitive e consentire esecuzione end-to-end delle milestone | Delivery Governance | Accepted | `DEVELOPMENT_WORKFLOW.md` v2.0 |
| DLG-012 | 05/08/2026 | Le milestone approvate vengono eseguite autonomamente fino alla chiusura tecnica e documentale | Ridurre handoff e mantenere responsabilità unitaria sulla delivery | Delivery Governance | Accepted | `DEVELOPMENT_WORKFLOW.md` v2.0 |
| DLG-013 | 05/08/2026 | Per file grandi o change set controllati si adottano le Git Database API (`blob -> tree -> commit -> ref`) | Evitare limiti e rischi delle sostituzioni complete tramite Contents API | Repository Operations | Accepted | commit `801c6246983af85fba571515f48fc038cccfcbcf` |

## 5. Delega operativa GitHub

La delega comprende, entro lo scope approvato:

- lettura e ricerca nel repository;
- creazione, aggiornamento e ritiro di file;
- creazione di blob, tree e commit;
- aggiornamento fast-forward dei branch;
- controllo GitHub Actions, job, log e artifact;
- verifica GitHub Pages;
- correzione autonoma di errori coerenti con la milestone;
- aggiornamento dei registri di governance.

Richiedono sempre approvazione esplicita:

- force push o aggiornamento non fast-forward;
- operazioni distruttive non previste;
- ampliamento dello scope o deviazione dalla roadmap;
- nuove integrazioni o dipendenze strutturali;
- cambi di boundary, authority, safety, security o contratti pubblici.

## 6. Template per nuove decisioni

```markdown
| DLG-NNN | YYYY-MM-DD | Decisione | Motivazione | Ambito | Proposed/Accepted/... | Riferimenti |
```

Per decisioni complesse aggiungere una sezione dettagliata:

```markdown
### DLG-NNN — Titolo

- Contesto:
- Decisione:
- Alternative considerate:
- Conseguenze positive:
- Conseguenze negative:
- Condizioni di revisione:
- Riferimenti:
```

## 7. Relazioni con altri registri

- un compromesso accettato con costo futuro va in `TECHNICAL_DEBT.md`;
- un'attività da eseguire va in `BACKLOG.md`;
- un difetto va nel sistema di issue/bug tracking;
- una decisione strutturale va in un ADR;
- una variazione di roadmap va prima in `AMP-002` e poi nelle proiezioni.

## 8. Review

Il Decision Log deve essere riesaminato durante:

- release e hotfix;
- Architecture Package;
- modifiche di governance;
- introduzione di nuovi componenti condivisi;
- supersession di una scelta operativa.
