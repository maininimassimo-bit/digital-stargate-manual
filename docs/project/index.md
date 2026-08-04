# Project Governance Center

Il Project Governance Center è il punto di accesso alle regole che governano sviluppo, pubblicazione, continuità e conoscenza del Digital StarGate Enterprise Portal.

## Bootstrap universale

Il punto di ingresso per nuove sessioni, collaboratori o assistenti AI è il file root:

```text
AI_BOOTSTRAP.md
```

Il bootstrap impone la verifica dello stato reale del repository e indirizza alla sequenza di lettura dei documenti canonici riportati di seguito.

## Documenti canonici

| Documento | Responsabilità |
|---|---|
| [Enterprise Architecture Context](ENTERPRISE_ARCHITECTURE_CONTEXT.md) | Baseline, visione, principi e stato di continuità |
| [Repository Knowledge Map](REPOSITORY_KNOWLEDGE_MAP.md) | Mappa dei domini, componenti e fonti presenti nel repository |
| [Development Workflow](DEVELOPMENT_WORKFLOW.md) | Processo milestone-by-milestone |
| [Coding Standards](CODING_STANDARDS.md) | Standard .NET, JavaScript, CSS, Markdown, contratti e dataset |
| [Release Playbook](RELEASE_PLAYBOOK.md) | Quality gate, release, deployment, acceptance e rollback |
| [Technical Debt Register](TECHNICAL_DEBT.md) | Debito tecnico noto, accettato e governato |
| [Decision Log](DECISION_LOG.md) | Decisioni operative e reversibili che non richiedono un ADR |
| [Project Backlog](BACKLOG.md) | Lavoro pianificato, priorità e dipendenze |

## Sequenza di lettura

1. Enterprise Architecture Context.
2. Repository Knowledge Map.
3. Project Backlog.
4. Technical Debt Register.
5. Decision Log.
6. Development Workflow.
7. Coding Standards.
8. Release Playbook.
9. `AMP-002 — Architecture Program Roadmap Realignment`.
10. Architecture Package, ADR, review, evidence e componenti direttamente coinvolti.

## Regola di prevalenza

Questi documenti non sostituiscono Architecture Package, ADR, assessment, evidence, roadmap o release note approvate.

In caso di divergenza prevalgono, nell'ordine:

1. Architecture Package, ADR, capability e standard approvati;
2. assessment ARB, validation record, evidence e gate;
3. roadmap autorevole `AMP-002`;
4. release note e commit effettivi;
5. contratti machine-readable;
6. dataset e dashboard come proiezioni;
7. Project Governance Center;
8. conversazioni.

## Regola di aggiornamento

Ogni milestone che modifica baseline, standard, release state, debito, decisioni o priorità deve aggiornare il documento proprietario nello stesso change set.

## Stato del Governance Package

| Elemento | Stato |
|---|---|
| Governance Foundation documentale | Completata |
| Bootstrap root | Creato |
| Integrazione navigazione MkDocs | In corso |
| Build `mkdocs build --strict` | Da verificare |
| Verifica GitHub Pages | Da verificare |
| Prossima milestone funzionale | RC1-HF01 Enterprise Theme Manager |
