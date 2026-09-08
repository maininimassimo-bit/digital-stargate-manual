# Project Governance Center

Il Project Governance Center raccoglie le regole che governano sviluppo, pubblicazione, continuità e conoscenza del Digital StarGate.

## Bootstrap universale

Il punto di ingresso unico per nuove sessioni, collaboratori o assistenti AI è:

```text
AI_BOOTSTRAP.md
```

`AI_BOOTSTRAP.md` determina la mandatory reading sequence corrente. Questo indice non la sostituisce e non deve diventare una seconda source of truth.

## Continuity authority corrente

| Documento | Ruolo |
|---|---|
| `AI_BOOTSTRAP.md` | Root bootstrap universale |
| [Handover 08/09/2026](HANDOVER_2026-09-08.md) | Continuity handover corrente |
| [Current Technical Baseline 08/09/2026](CURRENT_TECHNICAL_BASELINE_2026-09-08.md) | Baseline tecnica corrente |
| [Enterprise Architecture Context](ENTERPRISE_ARCHITECTURE_CONTEXT.md) | Contesto architetturale enterprise corrente |
| [Repository Knowledge Map](REPOSITORY_KNOWLEDGE_MAP.md) | Mappa domini, authority, projection e knowledge foundation |

Handover e baseline con data precedente restano snapshot storici e non devono essere interpretati come stato corrente quando esiste un successore più recente.

## Registri e standard canonici

| Documento | Responsabilità |
|---|---|
| [Project Backlog](BACKLOG.md) | Stato, priorità e dipendenze del lavoro governato |
| [Technical Debt Register](TECHNICAL_DEBT.md) | Debito tecnico noto e disposition |
| [Decision Log](DECISION_LOG.md) | Decisioni operative/reversibili che non richiedono ADR |
| [Development Workflow](DEVELOPMENT_WORKFLOW.md) | Processo milestone-by-milestone |
| [Coding Standards](CODING_STANDARDS.md) | Standard .NET, JavaScript, CSS, Markdown, contratti e dataset |
| [Release Playbook](RELEASE_PLAYBOOK.md) | Quality gate, release, acceptance e rollback |

## Mandatory reading sequence

Per la sequenza normativa fare sempre riferimento a `AI_BOOTSTRAP.md`. Alla baseline 08/09/2026 comprende:

1. root bootstrap;
2. current handover;
3. current technical baseline;
4. Enterprise Architecture Context;
5. Repository Knowledge Map;
6. Backlog;
7. canonical roadmap source;
8. generated roadmap projection;
9. Technical Debt;
10. Decision Log;
11. Development Workflow;
12. Coding Standards;
13. Release Playbook;
14. AMP-002;
15. package, ADR, review ed evidence direttamente coinvolti.

## Authority / projection rule

Il repository GitHub è la source of truth. Le authority specifiche restano nei rispettivi documenti/registri governati.

- `.github/roadmap/roadmap-source.json` è la canonical roadmap source corrente;
- `docs/data/roadmap.json` è una generated projection;
- AMP-002 resta la planning authority dell'architecture program e non va reinterpretato come live status register;
- portal dataset, knowledge read model e replay read model sono projection;
- workflow, review ed evidence provano solo l'exact HEAD/merge SHA effettivamente verificato.

## Stato corrente — 08/09/2026

- BKL-030 — CLOSED / ACCEPTED;
- BKL-015 — DONE / ACCEPTED;
- BKL-044 — CLOSED / ACCEPTED;
- BKL-035 — CLOSED / ACCEPTED;
- BKL-040 — F1-F4 CLOSED / ACCEPTED; closure finale in PR #118;
- BKL-038 — Anomaly & Trend Center è il package dependency-ready corrente, ma l'implementazione deve attendere merge e post-merge verification di PR #118;
- BKL-037 resta Planned finché BKL-045 non è accepted.

BKL-040 è una bounded historical/read-only foundation: la materializzazione eseguibile F3/F4 copre N.I.N.A., PHD2 e CloudWatcher più session projection dove definita. Non dichiara implicitamente Power/Network/Safety come historical replay channels implementati.

`TD-012` registra il compatibility debt F1/F2 e deve essere preservato senza retrofit silenzioso della baseline accettata.

## Safety boundary

Portale, telemetry, Knowledge Graph, replay, anomaly/trend analysis e AI non sono Safety Authority e non autorizzano device command o automatic remediation.

Gli interlock fisici e la Safety Authority locale restano indipendenti e autorevoli.

## Sequenza governata corrente

```text
Completed baseline through BKL-030, BKL-015, BKL-044, BKL-035 and BKL-040
  -> BKL-038 Anomaly & Trend Center [CURRENT]
  -> BKL-039 Equipment Performance Registry
  -> BKL-045 PixInsight Workflow Provenance Plugin
  -> BKL-037 Session Comparison & Benchmarking
  -> BKL-041 Scientific Data Quality Score
  -> BKL-046 AI Post-Processing Assistant
  -> BKL-031 Observation Planner
  -> BKL-032 Session Readiness
  -> BKL-036 Observatory Health Score
  -> BKL-033 Digital Twin
  -> BKL-034 Scientific Image Gallery
  -> BKL-042 AI Observatory Assistant
  -> BKL-043 Reliability Engineering
  -> BKL-014 / AP-015 Scientific Knowledge Platform
```

La sequenza deve essere sempre verificata nel live `BACKLOG.md` e nella canonical roadmap source prima di iniziare il package successivo.
