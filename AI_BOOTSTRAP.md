# Digital StarGate AI Bootstrap

| Campo | Valore |
|---|---|
| Versione | 6.2 |
| Baseline | 15/09/2026 |
| Stato | Current root bootstrap — PR #206 merged/post-merge verified; PR #207 F3-A2-D4 protected DRAFT review candidate |

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
- BKL-031 F3-A2-D2 — first protected setup baseline is APPROVED; PR #202 merged as `bb11f25192200655427411a46a2e18560a5d9bec` and is post-merge verified;
- BKL-031 F3-A1-M1 — owner decisions and protected source authorization are complete;
- BKL-031 F3-A1-M2 — protected Site Authority DRAFT, schemas, validator and 51-case suite integrated/post-merge verified via PR #203;
- BKL-031 F3-A1-M3/M4 — exact-digest owner approval, protected receipt and unchanged APPROVED envelope integrated via PR #204, merge `e73b1aa631c41dff97b9e5ededb6d6be02a667d4`, with 10/10 post-merge workflows;
- BKL-031 F3-A1-M4 acceptance reconciliation — PR #205 merged as `d5f403bbe6a39731213c372cb22296324d10b03d` with 9/9 post-merge workflows;
- BKL-031 F3-A2-D3 — source, roles, separation and validity decisions are complete; protected decision evidence is the current integration package;
- BKL-031 F3-A2-D4 — bounded DRAFT materialization handoff is next; no assignment record, schema or runtime exists yet;
- Governance: `DSG-AEM-001` and `W-DSG-AEM-RULESET-001` are ACTIVE / POST-MERGE VERIFIED via PR #196 and merge `357a5edfbd39346b10a1a2d751018ff6d1dd208f`, with 9/9 workflows.

La closure BKL-046 non dichiara efficacia scientifica né produzione: `NOT_EVALUABLE_CURRENT_EVIDENCE`, `NOT_READY_FOR_PRODUCTION`, `aiModelImplemented=false`. Nessun modello/provider, automatic acceptance o PixInsight apply è autorizzato.

## 6. Sequenza governata

`... -> BKL-037 CLOSED -> BKL-041 CLOSED -> BKL-046 CLOSED -> BKL-031 [F1/F2 ACCEPTED / F3 SA ACCEPTED / F3-A1 CONTRACT ACCEPTED / F3-A2 BASELINE APPROVED / F3-A1 SITE APPROVED / ASSIGNMENT OWNER DECISIONS COMPLETE / DRAFT MATERIALIZATION NEXT] -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## 7. Authority e continuity

`BACKLOG.md` governa stato/priorità/dipendenze; `.github/roadmap/roadmap-source.json` governa la roadmap funzionale; `docs/data/roadmap.json` è generated projection. Closure, review, evidence e workflow sostengono le acceptance claim sui rispettivi exact SHA.

## 8. Safety boundary

Nessun portale, planner, comparison layer, quality score o AI è Safety Authority. Nessun device command, automatic remediation, go/no-go operativo o bypass degli interlock è autorizzato.

## 9. Punto di partenza operativo

PR #205 merged as `d5f403bbe6a39731213c372cb22296324d10b03d` and is the verified repository baseline, with 9/9 post-merge workflows. The protected Site Authority and setup baseline remain independently APPROVED; protected values stay outside public documentation and logs.

The owner has completed `BKL-031-F3-A2-D3`: the future `CurrentSetupAssignment` uses the protected GitHub registry outside `docs/`; the Repository Owner is assignment owner and human Approval Authority; the Architecture Office is non-approving custodian; validity starts with the approved setup baseline and is unbounded. This authorizes protected decision evidence only. `BKL-031-F3-A2-D4` is the next bounded DRAFT materialization handoff. No assignment is materialized or approved. S08 remains `UNAVAILABLE`; S09 remains `UNAVAILABLE_CURRENT`. Runtime, EAGLE and Safety Authority remain separate.

## F3-A2-D4 review-candidate update — 15/09/2026

PR #206 integrated the assignment owner decisions and passed post-merge verification. PR #207 materializes only a protected, resolver-ineligible DRAFT with closed schemas, canonical identity, exact protected bindings, 57 executable cases and a redacted workflow. The implementation head passed its dedicated gate. Assignment approval, receipt and runtime remain absent; S09 is `UNAVAILABLE_CURRENT`. After D4 merge and post-merge verification, the next step is the mandatory human exact-digest approval gate.
