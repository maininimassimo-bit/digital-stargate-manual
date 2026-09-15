# Digital StarGate AI Bootstrap

| Campo | Valore |
|---|---|
| Versione | 4.8 |
| Baseline | 15/09/2026 |
| Stato | Current root bootstrap — BKL-031 F3-A1 Site Authority Contract review candidate; not implemented |

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro, collaboratore o assistente AI che intervenga sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale

Il repository GitHub è l'unica fonte autorevole. Memoria, conversazioni, roadmap visuali e dataset JSON non prevalgono sul repository corrente.

## 2. Sequenza obbligatoria di lettura

1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-09-15.md`
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-15.md`
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
- BKL-031 F3 handoff and Solution Architecture: ACCEPTED WITH CONDITIONS / POST-MERGE VERIFIED; PR #192 acceptance closure merged as `21524c687a1fa6a9d840a3951c7ef4fe298f9c3c` with 9/9 workflows;
- BKL-031 F3-A1 — Site Authority Contract: owner-authorized documentation-only review candidate; `ARB-191-MI02` has a normative resolution proposal pending ARB, while `ARB-191-MI01` remains an enforcement gate. No record, schema, adapter or runtime exists.

La closure BKL-046 non dichiara efficacia scientifica né produzione: `NOT_EVALUABLE_CURRENT_EVIDENCE`, `NOT_READY_FOR_PRODUCTION`, `aiModelImplemented=false`. Nessun modello/provider, automatic acceptance o PixInsight apply è autorizzato.

## 6. Sequenza governata

`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 CLOSED -> BKL-031 [F1/F2 ACCEPTED / F3 SA ACCEPTED / F3-A1 CONTRACT REVIEW CANDIDATE] -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## 7. Authority e continuity

`BACKLOG.md` governa stato/priorità/dipendenze; `.github/roadmap/roadmap-source.json` governa la roadmap funzionale; `docs/data/roadmap.json` è generated projection. Closure, review, evidence e workflow sostengono le acceptance claim sui rispettivi exact SHA.

## 8. Safety boundary

Nessun portale, planner, comparison layer, quality score o AI è Safety Authority. Nessun device command, automatic remediation, go/no-go operativo o bypass degli interlock è autorizzato.

## 9. Punto di partenza operativo

PR #192 ha integrato l'Acceptance Record F3 in `main@21524c687a1fa6a9d840a3951c7ef4fe298f9c3c` con 9/9 workflow post-merge. F3-A1 è ora il package documentale corrente: definisce il Site Authority Contract e propone la risoluzione normativa di `ARB-191-MI02`, ma non è accettato né implementato.

Il prossimo gate è la verifica CI dell'exact head della draft PR F3-A1, seguita solo su nuova autorizzazione da ARB/Release Quality. Coordinate reali, schema/fixture/validator/adapter, storage, provider/ADR, F3-A2/A3/B/C, forecast, ranking, readiness, runtime, device command, PC/EAGLE e Safety Authority restano non autorizzati.
