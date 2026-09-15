# Digital StarGate AI Bootstrap

| Campo | Valore |
|---|---|
| Versione | 5.3 |
| Baseline | 15/09/2026 |
| Stato | Current root bootstrap — PR #195 F3-A2 handoff accepted/post-merge verified; DSG-AEM-001 active; detailed F3-A2 contract next |

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
12. `docs/project/DSG-AEM-001-CONTINUOUS-AUTONOMOUS-EXECUTION-MANDATE-2026-09-15.md`
13. `docs/project/CODING_STANDARDS.md`
14. `docs/project/RELEASE_PLAYBOOK.md`
15. `docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md`
16. Package, ADR, review, evidence e componenti direttamente coinvolti.

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
- BKL-031 F3-A1 — Site Authority Contract: ACCEPTED WITH CONDITIONS / POST-MERGE VERIFIED via PR #193; acceptance reconciliation PR #194 merged as `1fd771632239cdca38d7527c55b974d805ffd1b9` with 9/9 workflows;
- BKL-031 F3-A2 — Setup Authority Contract: handoff ACCEPTED WITH CONDITIONS / POST-MERGE VERIFIED via PR #195 and merge `8520f4272d31f5578769e8d12ac34101e1c044e8`, with 9/9 workflows; detailed contract is next. `ARB-195-MI01` is due before its approval; no assignment, schema, adapter or runtime exists;
- Governance: `DSG-AEM-001` and `W-DSG-AEM-RULESET-001` are active until completion or owner revocation.

La closure BKL-046 non dichiara efficacia scientifica né produzione: `NOT_EVALUABLE_CURRENT_EVIDENCE`, `NOT_READY_FOR_PRODUCTION`, `aiModelImplemented=false`. Nessun modello/provider, automatic acceptance o PixInsight apply è autorizzato.

## 6. Sequenza governata

`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 CLOSED -> BKL-031 [F1/F2 ACCEPTED / F3 SA ACCEPTED / F3-A1 ACCEPTED / F3-A2 HANDOFF ACCEPTED / DETAILED CONTRACT NEXT] -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## 7. Authority e continuity

`BACKLOG.md` governa stato/priorità/dipendenze; `.github/roadmap/roadmap-source.json` governa la roadmap funzionale; `docs/data/roadmap.json` è generated projection. Closure, review, evidence e workflow sostengono le acceptance claim sui rispettivi exact SHA.

## 8. Safety boundary

Nessun portale, planner, comparison layer, quality score o AI è Safety Authority. Nessun device command, automatic remediation, go/no-go operativo o bypass degli interlock è autorizzato.

## 9. Punto di partenza operativo

PR #195 ha integrato l'handoff F3-A2 in `main@8520f4272d31f5578769e8d12ac34101e1c044e8` con 9/9 workflow post-merge, inclusi Pages e Governed Projection Sync. `DSG-AEM-001` e `W-DSG-AEM-RULESET-001` sono attivi.

Il prossimo package è il detailed F3-A2 Setup Authority Contract affidato al Solution Architect. Deve risolvere `ARB-195-MI01` senza attestare una baseline concreta inesistente. Real setup assignment, schema/fixture/validator/adapter, storage, provider/ADR, F3-A3/B/C, forecast, ranking, readiness, runtime, device command, PC/EAGLE e Safety Authority restano non autorizzati.
