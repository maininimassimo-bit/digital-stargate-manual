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
| [BKL-041 Closure](BKL-041-CLOSURE-2026-09-11.md) | Closure della capability accettata più recente |
| [BKL-046 Program Assessment](../architecture/assessments/BKL-046-Architecture-Program-Assessment-and-F1-Handoff-2026-09-11.md) | Decisione di sequenziamento e handoff F1 |
| [BKL-046 F1 Semantic Contract](../architecture/scientific-assets/BKL-046-F1-AI-Post-Processing-Assistant-Source-Discovery-and-Advisory-Semantic-Contract.md) | Baseline semantica accepted dell'assistente advisory |
| [BKL-046 F1 Acceptance](BKL-046-F1-ACCEPTANCE-2026-09-11.md) | Acceptance, merge e verifica pubblicazione F1 |
| [BKL-046 F2 Acceptance](BKL-046-F2-ACCEPTANCE-2026-09-11.md) | Acceptance, merge e verifica pubblicazione F2 |
| [BKL-046 F3 Acceptance](BKL-046-F3-ACCEPTANCE-2026-09-11.md) | Acceptance, review AI-assistite owner-authorized, merge e verifica pubblicazione F3 |

## Registri e standard canonici

Backlog, Technical Debt, Decision Log, Development Workflow, Coding Standards e Release Playbook mantengono le rispettive authority.

## Stato corrente

- BKL-037 — Session Comparison & Benchmarking: CLOSED / ACCEPTED;
- BKL-041 — Scientific Data Quality Score: CLOSED / ACCEPTED / POST-MERGE VERIFIED;
- BKL-046 — AI Post-Processing Assistant: CURRENT / F4 Session/Provenance-Driven Read-Only Consumer; F1-F3 ACCEPTED.

## Sequenza governata

`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 [CURRENT] -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## Authority / projection

`.github/roadmap/roadmap-source.json` è source canonica; `docs/data/roadmap.json` è projection. Workflow/review/evidence valgono per l’exact SHA verificato.

## Safety boundary

Comparison, analytics, score e AI non sono Safety Authority e non autorizzano device command o remediation.
