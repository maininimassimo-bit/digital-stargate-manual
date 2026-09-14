# Digital StarGate AI Bootstrap

| Campo | Valore |
|---|---|
| Versione | 4.5 |
| Baseline | 14/09/2026 |
| Stato | Current root bootstrap — BKL-031 F1/F2 accepted; F3 Solution Architecture review candidate |

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro, collaboratore o assistente AI che intervenga sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale

Il repository GitHub è l'unica fonte autorevole. Memoria, conversazioni, roadmap visuali e dataset JSON non prevalgono sul repository corrente.

## 2. Sequenza obbligatoria di lettura

1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-09-14.md`
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-14.md`
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

- BKL-037 — Session Comparison & Benchmarking: CLOSED / ACCEPTED;
- BKL-041 — Scientific Data Quality Score: CLOSED / ACCEPTED / POST-MERGE VERIFIED;
- BKL-046 — AI Post-Processing Assistant: CLOSED / ACCEPTED / POST-MERGE VERIFIED come capability deterministica advisory read-only con limitation;
- BKL-031 F1 — Source Discovery and Semantic Boundary: ACCEPTED / POST-MERGE VERIFIED;
- BKL-031 F2 — Machine-Readable Context/Source Contract and Bounded Fixtures: ACCEPTED / POST-MERGE VERIFIED via PR #188 and merge `7f861f7399079858c9744e69b6c773664b6b5b54`;
- BKL-031 F3 handoff: integrated/post-merge verified via PR #190 and merge `2ffc77917bcd3fc25a3c5657e8f12e62c9284303`; Solution Architecture and validation plan are current review candidates only.

La closure BKL-046 non dichiara efficacia scientifica né produzione: `NOT_EVALUABLE_CURRENT_EVIDENCE`, `NOT_READY_FOR_PRODUCTION`, `aiModelImplemented=false`. Nessun modello/provider, automatic acceptance o PixInsight apply è autorizzato.

## 6. Sequenza governata

`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 CLOSED -> BKL-031 [F1/F2 ACCEPTED / F3 SA REVIEW CANDIDATE] -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## 7. Authority e continuity

`BACKLOG.md` governa stato/priorità/dipendenze; `.github/roadmap/roadmap-source.json` governa la roadmap funzionale; `docs/data/roadmap.json` è generated projection. Closure, review, evidence e workflow sostengono le acceptance claim sui rispettivi exact SHA.

## 8. Safety boundary

Nessun portale, planner, comparison layer, quality score o AI è Safety Authority. Nessun device command, automatic remediation, go/no-go operativo o bypass degli interlock è autorizzato.

## 9. Punto di partenza operativo

BKL-031 F2 è ACCEPTED / POST-MERGE VERIFIED e l'handoff F3 è integrato/post-merge verified tramite PR #190. Il Solution Architecture Package F3 e il validation plan sono review candidate: non sono accettati né implementati. Restano non autorizzati ARB/Release Quality, merge del package, ADR/provider selection, record reali sito/setup, schema/fixture/validator/adapter, forecast, ranking, readiness, runtime, device command, workload EAGLE e Safety Authority.

