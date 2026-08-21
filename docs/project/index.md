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
| Integrazione navigazione MkDocs | Presente nella baseline corrente |
| Build/quality gate documentale | PASS — Developer Foundation #725 |
| Generazione manuale Word | PASS — run #606 |
| Verifica GitHub Pages | Baseline BKL-025 PASS; deployment operativo |
| AP-014 Operational Acceptance | **Accepted** — v1.4 |
| AP14-W07 EAGLE M27 OAT | **Accepted** — v2.1 |
| Remediation AP-014 | BKL-019–BKL-026 `Done` |
| Observatory Status realtime | Vertical slice read-only integrata; Power/Network restano `UNKNOWN` finché prive di sorgenti verificate |
| Prossima milestone governata | Riprendere la sequenza backlog/roadmap successiva ad AP-014; AP-015 resta pianificato dopo le dipendenze previste |

### Governance reconciliation — 21/08/2026

La chiusura AP-014 è evidence-based:

- la sessione M27 10/11 agosto conserva `PARTIAL` dove l'evidence originaria non attesta i metadata;
- i workflow promotion/analytics introdotti dopo la pubblicazione storica sono `N/A historical baseline`, non evidence retroattive;
- il promotion fail-safe contract è PASS in Developer Foundation #714;
- la real-session semantic idempotency è PASS in Developer Foundation #723;
- la riconciliazione finale dell'acceptance è validata sull'exact head `a52c678ba6f3b498bc711ec7b8d5fad7359c7709` da Developer Foundation #725 e Genera manuale Word #606;
- AP-014 Operational Acceptance v1.4 e AP14-W07 EAGLE M27 OAT Result v2.1 sono `Accepted`;
- BKL-013, BKL-018 e BKL-026 sono `Done`.

La separazione fra telemetria realtime e proiezioni scientifiche storiche resta intenzionale. `UNKNOWN` rimane il valore fail-safe per sorgenti realtime non verificate.