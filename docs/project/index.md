# Project Governance Center

Il Project Governance Center raccoglie le regole che governano sviluppo, pubblicazione, continuità e conoscenza del Digital StarGate.

## Bootstrap universale

Il punto di ingresso unico è `AI_BOOTSTRAP.md`.

## Continuity authority corrente

| Documento | Ruolo |
|---|---|
| `AI_BOOTSTRAP.md` | Root bootstrap |
| [Handover 10/09/2026](HANDOVER_2026-09-10.md) | Handover corrente |
| [Current Technical Baseline 10/09/2026](CURRENT_TECHNICAL_BASELINE_2026-09-10.md) | Baseline tecnica corrente |
| [Enterprise Architecture Context](ENTERPRISE_ARCHITECTURE_CONTEXT.md) | Contesto enterprise |
| [Repository Knowledge Map](REPOSITORY_KNOWLEDGE_MAP.md) | Mappa authority/projection |
| [BKL-037 Closure](BKL-037-CLOSURE-2026-09-10.md) | Closure del predecessore accettato |

## Registri e standard canonici

Backlog, Technical Debt, Decision Log, Development Workflow, Coding Standards e Release Playbook mantengono le rispettive authority.

## Stato corrente

- BKL-037 — Session Comparison & Benchmarking: CLOSED / ACCEPTED;
- BKL-041 — Scientific Data Quality Score: CURRENT / In Progress;
- BKL-046 — AI Post-Processing Assistant: NEXT / Planned.

## Sequenza governata

`... -> BKL-037 CLOSED -> BKL-041 [CURRENT] -> BKL-046 -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## Authority / projection

`.github/roadmap/roadmap-source.json` è source canonica; `docs/data/roadmap.json` è projection. Workflow/review/evidence valgono per l’exact SHA verificato.

## Safety boundary

Comparison, analytics, score e AI non sono Safety Authority e non autorizzano device command o remediation.
