# Project Governance Center

Il Project Governance Center raccoglie le regole che governano sviluppo, pubblicazione, continuità e conoscenza del Digital StarGate.

## Bootstrap universale

Il punto di ingresso unico è `AI_BOOTSTRAP.md`. Il bootstrap determina la mandatory reading sequence corrente e questo indice non costituisce una seconda source of truth.

## Continuity authority corrente

| Documento | Ruolo |
|---|---|
| `AI_BOOTSTRAP.md` | Root bootstrap universale |
| [Handover 10/09/2026](HANDOVER_2026-09-10.md) | Continuity handover corrente |
| [Current Technical Baseline 10/09/2026](CURRENT_TECHNICAL_BASELINE_2026-09-10.md) | Baseline tecnica corrente |
| [Enterprise Architecture Context](ENTERPRISE_ARCHITECTURE_CONTEXT.md) | Contesto architetturale enterprise |
| [Repository Knowledge Map](REPOSITORY_KNOWLEDGE_MAP.md) | Mappa domini, authority, projection e knowledge foundation |

Handover e baseline precedenti restano snapshot storici per lineage.

## Registri e standard canonici

| Documento | Responsabilità |
|---|---|
| [Project Backlog](BACKLOG.md) | Stato, priorità e dipendenze del lavoro governato |
| [Technical Debt Register](TECHNICAL_DEBT.md) | Debito tecnico noto e disposition |
| [Decision Log](DECISION_LOG.md) | Decisioni operative/reversibili |
| [Development Workflow](DEVELOPMENT_WORKFLOW.md) | Processo milestone-by-milestone |
| [Coding Standards](CODING_STANDARDS.md) | Standard repository |
| [Release Playbook](RELEASE_PLAYBOOK.md) | Quality gate, release, acceptance e rollback |

## Authority / projection rule

- GitHub repository: source of truth;
- `.github/roadmap/roadmap-source.json`: canonical roadmap source;
- `docs/data/roadmap.json`: generated projection;
- `BACKLOG.md`: stato/priorità/dipendenze live;
- AMP-002: planning authority dell'architecture program, non live status register;
- portal dataset/read model: projection;
- workflow/review/evidence: validi per exact HEAD/merge SHA verificato.

## Stato corrente — 10/09/2026

- BKL-030, BKL-015, BKL-044, BKL-035, BKL-040, BKL-038 e BKL-039: CLOSED/DONE / ACCEPTED;
- BKL-045 — PixInsight Workflow Provenance Plugin: CLOSED / ACCEPTED, closure 10/09 e PR #140 integrata;
- BKL-037 — Session Comparison & Benchmarking: CURRENT / In Progress;
- BKL-041 — Scientific Data Quality Score: NEXT / Planned;
- Analytics Center/Executive Dashboard sono riallineati fino alla PR #151, restando read-only/non-Safety Authority.

## Sequenza governata corrente

```text
Completed baseline through BKL-045
  -> BKL-037 Session Comparison & Benchmarking [CURRENT]
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

La sequenza deve essere verificata nel live `BACKLOG.md` e nella canonical roadmap source prima di iniziare il package successivo.

## Safety boundary

Portale, telemetry, comparison/benchmarking, analytics e AI non sono Safety Authority e non autorizzano device command o automatic remediation. Gli interlock fisici e la Safety Authority locale restano indipendenti e autorevoli.
