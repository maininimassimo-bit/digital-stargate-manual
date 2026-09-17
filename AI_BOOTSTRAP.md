# Digital StarGate AI Bootstrap

| Campo | Valore |
|---|---|
| Versione | 7.4 |
| Baseline | 18/09/2026 |
| Stato | Current root bootstrap — BKL-031 F9 implementation merged/post-merge verified; first governed refresh and formal acceptance reconciliation pending; S10 unavailable |

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale
Il repository GitHub è l'unica fonte autorevole. Memoria, conversazioni e projection non prevalgono sul repository corrente.

## 2. Sequenza obbligatoria di lettura
1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-09-17.md`
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-17.md`
4. `docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md`
5. `docs/project/REPOSITORY_KNOWLEDGE_MAP.md`
6. `docs/project/BACKLOG.md`
7. `.github/roadmap/roadmap-source.json`
8. `docs/data/roadmap.json` — generated projection, non authority
9. `docs/project/TECHNICAL_DEBT.md`
10. `docs/project/DECISION_LOG.md`
11. `docs/project/DEVELOPMENT_WORKFLOW.md`
12. `docs/project/DSG-AEM-001-CONTINUOUS-AUTONOMOUS-EXECUTION-MANDATE-2026-09-15.md`
13. `docs/project/CODING_STANDARDS.md`
14. `docs/project/RELEASE_PLAYBOOK.md`
15. `docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md`
16. package, ADR, review, evidence e componenti direttamente coinvolti.

Gli handover e le baseline precedenti restano snapshot storici.

## 3. Stato corrente
- BKL-031: **In Progress**.
- F3–F8: Accepted/Post-Merge Verified.
- F8 implementation: PR #279, reviewed head `3f05693482208df2b56b66dcb71162589880e72b`, merge `20669f7164460297d7318fc3b5874e4bc7f4bcde`, 9/9 exact-head e 10/10 post-merge SUCCESS.
- F8 acceptance reconciliation: PR #280, reviewed head `bca410dcde804483052beded16c29a9f58f43872`, merge `84d1b889a6c739c9e5d053e1f073fe1d87b8c5d4`, 17/17 exact-head e 19/19 post-merge SUCCESS; GitHub Pages build/integrity/deploy SUCCESS.
- F9 implementation: PR #282 merge `deeafa665353fa2e88b092a4e8ebaa3d5befa99f`, PR #283 public zero-cost reconciliation merge `f3d915540e942056c3ec9763fcf70a2c187768a0`, PR #284 planner exposure merge `3a803202b75cf88a575a26b5175a32fcb107369a`; applicable post-merge workflows SUCCESS.
- Next gate: **BKL-031 F9 governed refresh, portal verification and acceptance reconciliation**.
- S10 production runtime: `UNAVAILABLE`.

## 4. Boundary non negoziabili
- local physical interlocks = Safety Authority;
- BKL-032 = Session Readiness / Go-No-Go authority;
- BKL-031 = advisory/read-only, nessuna readiness/safety/action authority;
- nessun scheduler, automatic target selection o device command;
- coordinate sito protette mai in projection pubbliche;
- missing/stale/conflicted evidence fail-closed;
- provider/model/run lineage esplicita, nessun fallback/stitching silenzioso;
- recurring provider traffic non autorizzato senza separata authority/budget decision.

## 5. Provider budget corrente
- F4-C generalized validation: `2/2_EXHAUSTED`;
- F7 protected-site one-shot: `1/1_EXHAUSTED`;
- F8: zero provider requests;
- F9 non eredita automaticamente alcuna autorizzazione di traffico ricorrente.

## 6. Disciplina di delivery
Exact-head CI → ARB → Release Quality sullo stesso SHA → expected-head merge → post-merge verification → acceptance reconciliation. Nessuna acceptance o runtime claim può precedere l'evidence reale.

## 7. Punto di ripresa
Riprendere da **BKL-031 F9 governed refresh, portal verification and acceptance reconciliation** usando `docs/project/HANDOVER_2026-09-17.md` come handover compatto e `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-17.md` come baseline tecnica corrente.
