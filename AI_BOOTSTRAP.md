# Digital StarGate AI Bootstrap

| Campo | Valore |
|---|---|
| Versione | 3.0 |
| Baseline | 11/09/2026 |
| Stato | Current root bootstrap — BKL-041 Scientific Data Quality Score |

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro, collaboratore o assistente AI che intervenga sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale

Il repository GitHub è l'unica fonte autorevole. Memoria, conversazioni, roadmap visuali e dataset JSON non prevalgono sul repository corrente.

## 2. Sequenza obbligatoria di lettura

1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-09-10.md`
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-10.md`
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
- BKL-041 — Scientific Data Quality Score: CURRENT / In Progress;
- BKL-046 — AI Post-Processing Assistant: NEXT / Planned.

BKL-037 resta read-only/descriptive-only e non autorizza ranking, score, threshold, recommendation, remediation, command path o Safety Authority.

BKL-041 F1–F3 sono Accepted. F4 è Accepted tramite PR #162, merge `ed9ffcc92e1a5252b0d8c37634bc652397f3cde1`, con projection full-catalog, consumer e refresh automatico freshness-verified. F5 è l'incremento corrente per validation sulla cohort reale completa e closure. L'evidence corrente non autorizza un profilo produttivo: capability sperimentale read-only accettabile con limitation, production readiness `NOT_READY_FOR_PRODUCTION`. Conteggi e coverage sono evidence descrittiva, non threshold di accettazione.

## 6. Sequenza governata

`... -> BKL-037 CLOSED -> BKL-041 [CURRENT] -> BKL-046 -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## 7. Authority e continuity

`BACKLOG.md` governa stato/priorità/dipendenze; `.github/roadmap/roadmap-source.json` governa la roadmap funzionale; `docs/data/roadmap.json` è generated projection. Closure, review, evidence e workflow sostengono le acceptance claim sui rispettivi exact SHA.

## 8. Safety boundary

Nessun portale, comparison layer, quality score o AI è Safety Authority. Nessun device command, automatic remediation o bypass degli interlock è autorizzato.

## 9. Punto di partenza operativo

Completare **BKL-041 F5 — Real-Evidence Validation and Capability Closure**. Validare la cohort senza outcome filtering, rendere machine-readable readiness, bias e limitation, mantenere automatic refresh/freshness, completare ARB/RQ e chiudere il package soltanto su evidence verificata. Non promuovere il profilo sintetico né autorizzare production use, ranking, automatic acceptance o Safety Authority.
