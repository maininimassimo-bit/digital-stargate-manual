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
| Governance Foundation documentale | **Completata** — BKL-002–BKL-006 Done |
| Bootstrap root | **Done** — BKL-003 |
| Enterprise Theme Framework | **Completed / Accepted** — BKL-001; WP-03 |
| Integrazione navigazione MkDocs | **Done** — Project Governance presente in `mkdocs.yml` |
| Build/quality gate documentale | PASS — Developer Foundation #730 |
| Generazione manuale Word | PASS — run #611 |
| Verifica GitHub Pages | PASS — BKL-025 baseline |
| AP-012 residual evidence | **In Progress** — BKL-011; ARB-012-C04 W06/W07 |
| AP-013 / AP-013B COPY_ONLY | **Accepted / Limited Production** — BKL-012 Done |
| AP-014 Operational Acceptance | **Accepted** — v1.4 |
| AP14-W07 EAGLE M27 OAT | **Accepted** — v2.1 |
| Observatory Status realtime | Vertical slice read-only integrata; **Power/Network ancora da completare** |
| Observatory Status Power/Network discovery | **Ready — BKL-027** |
| Observatory Status Power/Network integration | Planned — BKL-028 |
| AP-015 / Knowledge Graph | Planned dopo le dipendenze P1 |

### Repository Governance Reconciliation post AP-014 — 21/08/2026

La repository truth ha consentito di chiudere senza ripetizioni operative BKL-001, BKL-002, BKL-003, BKL-004, BKL-005, BKL-006 e BKL-012.

Evidence principali:

- WP-03 Enterprise Theme Framework Completion Report: `Accepted`, Theme Service centralizzato e CI verde;
- `mkdocs.yml`: sezione `Project Governance` presente;
- `AI_BOOTSTRAP.md`: bootstrap canonico presente in root;
- `docs/project/index.md`: Knowledge Map e registri canonici esposti;
- Developer Foundation #730 e BKL-025: build/Pages governance già verificate;
- AP-013B OneDrive Transport Operational Acceptance: `Passed — Limited Production`, scheduler Export/Import attive, `LastTaskResult = 0`, batch e retry idempotente;
- AP-013 Formal Operational Acceptance: `Accepted` e formal closure authorized.

Non sono stati chiusi per inferenza:

- **BKL-011**, perché ARB-012-C04 documenta ancora provisioning/account/PRV/ENV reali non completati;
- **BKL-007–BKL-010**, perché restano attività di hardening effettive.

Power e Network di Observatory Status sono ora esplicitamente governati da BKL-027/BKL-028. Fino alla verifica delle sorgenti runtime, `UNKNOWN` resta il valore fail-safe corretto.

## Prossima sequenza governata

```text
BKL-011 AP-012 residual evidence [IN PROGRESS]
  -> BKL-027 Observatory Status Power/Network source discovery [READY]
  -> BKL-028 Observatory Status Power/Network integration
  -> BKL-007/008/009/010 governance hardening
  -> AP-015 / Knowledge Graph
```