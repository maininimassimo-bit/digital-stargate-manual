# Decision Log

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-DEC-001 |
| Versione | 1.0 |
| Stato | Active |
| Data baseline | 04/08/2026 |

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
| DLG-005 | 04/08/2026 | Il Navigation Manager resta in `page-enhancements.js`; la gestione tema avrà un componente dedicato | Applicare responsabilità singola ed eliminare coupling fragile | Portal JS | Accepted | RC1-HF01, TD-001 |
| DLG-006 | 04/08/2026 | Lo Scientific Data Engine è l'unico access layer condiviso per i componenti scientifici del portale | Evitare parsing e accessi paralleli ai dataset | Scientific Portal | Accepted | `scientific-data-engine.js` |
| DLG-007 | 04/08/2026 | I dataset JSON del portale sono proiezioni e non fonti primarie | Preservare data authority e ricostruibilità | Data Governance | Accepted | AP-002, AMP-002 |
| DLG-008 | 04/08/2026 | Il Governance Framework viene completato prima di RC1-HF01 | Stabilizzare contesto e processo prima della hotfix | Sequencing | Accepted | GP-001, RC1-HF01 |
| DLG-009 | 04/08/2026 | I documenti governance vengono creati incrementalmente con commit coerenti | Ridurre rischio e consentire review puntuale | Delivery | Accepted | `DEVELOPMENT_WORKFLOW.md` |
| DLG-010 | 04/08/2026 | `AI_BOOTSTRAP.md` sarà il punto di ingresso root per persone e assistenti AI | Rendere immediatamente visibile il percorso di lettura | Onboarding | Accepted | GP-001 |

## 5. Template per nuove decisioni

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

## 6. Relazioni con altri registri

- un compromesso accettato con costo futuro va in `TECHNICAL_DEBT.md`;
- un'attività da eseguire va in `BACKLOG.md`;
- un difetto va nel sistema di issue/bug tracking;
- una decisione strutturale va in un ADR;
- una variazione di roadmap va prima in `AMP-002` e poi nelle proiezioni.

## 7. Review

Il Decision Log deve essere riesaminato durante:

- release e hotfix;
- Architecture Package;
- modifiche di governance;
- introduzione di nuovi componenti condivisi;
- supersession di una scelta operativa.
