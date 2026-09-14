# Project Governance Center

Il Project Governance Center raccoglie le regole che governano sviluppo, pubblicazione, continuità e conoscenza del Digital StarGate.

## Bootstrap universale

Il punto di ingresso unico è `AI_BOOTSTRAP.md`.

## Continuity authority corrente

| Documento | Ruolo |
|---|---|
| `AI_BOOTSTRAP.md` | Root bootstrap |
| [Handover 14/09/2026](HANDOVER_2026-09-14.md) | Handover corrente |
| [Current Technical Baseline 14/09/2026](CURRENT_TECHNICAL_BASELINE_2026-09-14.md) | Baseline tecnica corrente |
| [Enterprise Architecture Context](ENTERPRISE_ARCHITECTURE_CONTEXT.md) | Contesto enterprise |
| [Repository Knowledge Map](REPOSITORY_KNOWLEDGE_MAP.md) | Mappa authority/projection |
| [BKL-037 Closure](BKL-037-CLOSURE-2026-09-10.md) | Closure del predecessore accettato |
| [BKL-041 Closure](BKL-041-CLOSURE-2026-09-11.md) | Closure della capability accettata più recente |
| [BKL-046 Program Assessment](../architecture/assessments/BKL-046-Architecture-Program-Assessment-and-F1-Handoff-2026-09-11.md) | Decisione di sequenziamento e handoff F1 |
| [BKL-046 F1 Semantic Contract](../architecture/scientific-assets/BKL-046-F1-AI-Post-Processing-Assistant-Source-Discovery-and-Advisory-Semantic-Contract.md) | Baseline semantica accepted dell'assistente advisory |
| [BKL-046 F1 Acceptance](BKL-046-F1-ACCEPTANCE-2026-09-11.md) | Acceptance, merge e verifica pubblicazione F1 |
| [BKL-046 F2 Acceptance](BKL-046-F2-ACCEPTANCE-2026-09-11.md) | Acceptance, merge e verifica pubblicazione F2 |
| [BKL-046 F3 Acceptance](BKL-046-F3-ACCEPTANCE-2026-09-11.md) | Acceptance, review AI-assistite owner-authorized, merge e verifica pubblicazione F3 |
| [BKL-046 F4 Architecture](../architecture/scientific-assets/BKL-046-F4-Session-Provenance-Driven-Read-Only-Consumer.md) | F4 accettata e verificata post-merge |
| [BKL-046 F4 Acceptance](BKL-046-F4-ACCEPTANCE-2026-09-12.md) | Acceptance, review AI-assistite, deroga consumata, merge e verifica live |
| [BKL-046 F5 Program Handoff](../architecture/assessments/BKL-046-F5-Architecture-Program-Handoff-2026-09-12.md) | Baseline, maturity, gap e sequenza F5 |
| [BKL-046 F5 Architecture](../architecture/scientific-assets/BKL-046-F5-Real-Evidence-Evaluation-and-Capability-Closure.md) | F5 accepted e verificata post-merge |
| [BKL-046 F5 Validation Plan](../architecture/validation/BKL-046-F5-Real-Evidence-Evaluation-Plan.md) | Validation e closure gate completati |
| [BKL-046 Closure](BKL-046-CLOSURE-2026-09-13.md) | Closure deterministica read-only accettata |
| [BKL-031 Program Assessment](../architecture/assessments/BKL-031-Architecture-Program-Assessment-and-F1-Handoff-2026-09-13.md) | Current package e handoff F1 |
| [BKL-031 F1 Source and Semantic Boundary](../architecture/scientific-assets/BKL-031-F1-Observation-Planner-Source-Discovery-and-Semantic-Boundary.md) | Package architetturale F1 accepted/post-merge verified |
| [BKL-031 F1 Validation Plan](../architecture/validation/BKL-031-F1-Source-and-Semantic-Validation-Plan.md) | Gate e casi negativi per la review F1 |
| [BKL-031 F1 AI-Assisted ARB](../architecture/reviews/ARB-BKL-031-F1-AI-Assisted-Architecture-Review-2026-09-14.md) | Approved with Conditions; non equivalente a review umana indipendente |
| [BKL-031 F1 AI-Assisted Release Quality](../architecture/reviews/RQ-BKL-031-F1-AI-Assisted-Release-Quality-Review-2026-09-14.md) | Conditionally Ready for Merge; non equivalente ad approvazione umana indipendente |
| [BKL-031 F1 Acceptance](BKL-031-F1-ACCEPTANCE-2026-09-14.md) | F1 accepted/post-merge verified; condizioni trasferite |
| [BKL-031 F2 Handoff](../architecture/assessments/BKL-031-F2-Machine-Readable-Context-Contract-Handoff-2026-09-14.md) | Fulfilled handoff; F2 accepted/post-merge verified |
| [BKL-031 F2 Acceptance](BKL-031-F2-ACCEPTANCE-2026-09-14.md) | F2 acceptance, merge-control decision and post-merge evidence |
| [BKL-031 F3 Handoff](../architecture/assessments/BKL-031-F3-Governed-Site-Setup-Ephemeris-Lunar-Handoff-2026-09-14.md) | Current handoff only; design and implementation not authorized |
| [PR #185 BKL-031 F1 Acceptance/F2 Handoff AI-Assisted ARB](../architecture/reviews/ARB-PR185-BKL-031-F1-Acceptance-F2-Handoff-AI-Assisted-Architecture-Review-2026-09-14.md) | Approved with Conditions — 99/100; non equivalente ad approvazione umana indipendente |
| [PR #185 BKL-031 F1 Acceptance/F2 Handoff AI-Assisted Release Quality](../architecture/reviews/RQ-PR185-BKL-031-F1-Acceptance-F2-Handoff-AI-Assisted-Release-Quality-Review-2026-09-14.md) | Conditionally Ready for Merge; non equivalente ad approvazione umana indipendente |
| [PR #184 PHD2 RMS AI-Assisted ARB](../architecture/reviews/ARB-PR184-PHD2-RMS-AI-Assisted-Architecture-Review-2026-09-14.md) | Approved with Conditions; hotfix RMS profile-aware; non equivalente a review umana indipendente |
| [PR #184 PHD2 RMS AI-Assisted Release Quality](../architecture/reviews/RQ-PR184-PHD2-RMS-AI-Assisted-Release-Quality-Review-2026-09-14.md) | Conditionally Ready for Merge; rielaborazione post-merge richiesta |

## Registri e standard canonici

Backlog, Technical Debt, Decision Log, Development Workflow, Coding Standards e Release Playbook mantengono le rispettive authority.

## Stato corrente

- BKL-037 — Session Comparison & Benchmarking: CLOSED / ACCEPTED;
- BKL-041 — Scientific Data Quality Score: CLOSED / ACCEPTED / POST-MERGE VERIFIED;
- BKL-046 — AI Post-Processing Assistant: CLOSED / ACCEPTED / POST-MERGE VERIFIED come capability deterministica read-only con limitation;
- BKL-031 F1: ACCEPTED / POST-MERGE VERIFIED;
- BKL-031 F2: ACCEPTED / POST-MERGE VERIFIED;
- BKL-031 F3: CURRENT HANDOFF ONLY; design/implementation not authorized.

## Sequenza governata

`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 CLOSED -> BKL-031 [F1/F2 ACCEPTED / F3 CURRENT HANDOFF] -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## Authority / projection

`.github/roadmap/roadmap-source.json` è source canonica; `docs/data/roadmap.json` è projection. Workflow/review/evidence valgono per l’exact SHA verificato.

## Safety boundary

Comparison, analytics, score e AI non sono Safety Authority e non autorizzano device command o remediation.
