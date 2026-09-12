# Digital StarGate AI Bootstrap

| Campo | Valore |
|---|---|
| Versione | 3.6 |
| Baseline | 12/09/2026 |
| Stato | Current root bootstrap — BKL-046 AI Post-Processing Assistant |

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro, collaboratore o assistente AI che intervenga sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale

Il repository GitHub è l'unica fonte autorevole. Memoria, conversazioni, roadmap visuali e dataset JSON non prevalgono sul repository corrente.

## 2. Sequenza obbligatoria di lettura

1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-09-12.md`
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-12.md`
4. `docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md`
5. `docs/project/REPOSITORY_KNOWLEDGE_MAP.md`
6. `docs/project/BACKLOG.md`
7. `.github/roadmap/roadmap-source.json`
8. `docs/data/roadmap.json` — projection generata, non authority
9. `docs/project/TECHNICAL_DEBT.md`
10. `docs/project/DECISION_LOG.md`
11. `docs/project/DEVELOPMENT_WORKFLOW.md`
12. `docs/project/CODING_STANDARDS.md`
13. `docs/project/RELEASE_PLAYBOOK.md`
14. `docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md`
15. Package, ADR, review, evidence e componenti direttamente coinvolti.

Handover e baseline precedenti restano snapshot storici.

## 3. Verifica iniziale obbligatoria

Verificare branch, HEAD, PR, workflow, backlog, canonical roadmap, generated projection, closure/review/evidence e dependency readiness prima di modificare repository o runtime.

## 4. Principi non negoziabili

- repository as source of truth;
- projection mai authority implicita;
- Safety Authority fisica/locale indipendente;
- missing/unavailable evidence mai inventata;
- provenance `OBSERVED`, `DECLARED`, `SUGGESTED` sempre distinta;
- Citation, Provenance, semantic type, lifecycle e confidence preservati;
- nessuna claim di test, build, deployment o acceptance senza evidence reale.

## 5. Stato corrente

- foundation completata e accettata attraverso BKL-045;
- BKL-037 — Session Comparison & Benchmarking: CLOSED / ACCEPTED;
- BKL-041 — Scientific Data Quality Score: CLOSED / ACCEPTED / POST-MERGE VERIFIED;
- BKL-046 — AI Post-Processing Assistant: CURRENT / F5 Real-Evidence Evaluation and Capability Closure design; F1-F4 ACCEPTED / POST-MERGE VERIFIED.

BKL-037 resta read-only/descriptive-only e non autorizza ranking, score, threshold, recommendation, remediation, command path o Safety Authority.

BKL-041 F1–F5 sono CLOSED / ACCEPTED tramite PR #163, merge `e4ccd216b0a0ca4033277ece513f051b052d2b83`, ARB R1 98/100, Release Quality `READY FOR MERGE` e Pages `34602219671` verde. L'outcome accetta esclusivamente la capability sperimentale read-only con limitation: production readiness resta `NOT_READY_FOR_PRODUCTION`; conteggi e coverage sono evidence descrittiva, non threshold di accettazione.

## 6. Sequenza governata

`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 [CURRENT] -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## 7. Authority e continuity

`BACKLOG.md` governa stato/priorità/dipendenze; `.github/roadmap/roadmap-source.json` governa la roadmap funzionale; `docs/data/roadmap.json` è generated projection. Closure, review, evidence e workflow sostengono le acceptance claim sui rispettivi exact SHA.

## 8. Safety boundary

Nessun portale, comparison layer, quality score o AI è Safety Authority. Nessun device command, automatic remediation o bypass degli interlock è autorizzato.

## 9. Punto di partenza operativo

Avviare **BKL-046 F5 — Real-Evidence Evaluation and Capability Closure** come incremento di architettura/design sulla baseline F4 accettata tramite PR #175, merge `af48cc2441cf956d88c13c81845fc2a2f7c599f2`. F5 deve definire cohort, sufficienza delle evidenze, criteri di valutazione e limitation trattenute per decidere una possibile closure della capability read-only. Non sono autorizzati model/provider, confidence scientifica, automatic acceptance, PixInsight apply, remediation, device command o Safety Authority.
