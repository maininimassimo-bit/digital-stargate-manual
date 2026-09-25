# Digital StarGate AI Bootstrap

| Campo | Valore |
|---|---|
| Versione | 7.6 |
| Baseline | 25/09/2026 |
| Stato | Current root bootstrap — BKL-043 F3/F4 exact pilot authorization preparation; S10 unavailable |

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale
Il repository GitHub è l'unica fonte autorevole. Memoria, conversazioni e projection non prevalgono sul repository corrente.

## 2. Sequenza obbligatoria di lettura
1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-09-25-BKL043-F4.md`
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-25.md`
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
- BKL-031: **Closed / Accepted / Post-Merge Verified** via PR #301 merge `4a509d574a004fe7fb72bc6c678c9e7f71fe821f`.
- F3–F8: Accepted/Post-Merge Verified.
- F8 implementation: PR #279, reviewed head `3f05693482208df2b56b66dcb71162589880e72b`, merge `20669f7164460297d7318fc3b5874e4bc7f4bcde`, 9/9 exact-head e 10/10 post-merge SUCCESS.
- F8 acceptance reconciliation: PR #280, reviewed head `bca410dcde804483052beded16c29a9f58f43872`, merge `84d1b889a6c739c9e5d053e1f073fe1d87b8c5d4`, 17/17 exact-head e 19/19 post-merge SUCCESS; GitHub Pages build/integrity/deploy SUCCESS.
- F8 evidence: notte bounded 17–18/09/2026, forecast reale F7 site-specific, astronomia night-specific, suitability OTA/camera/filter esplicita, ranking/finestre advisory read-only.
- BKL-032 Session Readiness / Go-No-Go Decision Support è Closed / Accepted / Post-Merge Verified via PR #304; il suo evaluator resta read-only e il runtime source/transport è separatamente gated.
- BKL-036 è Closed come capability repository-only bounded; F3 Health Score resta `UNAVAILABLE`.
- AP-007 è **Accepted with conditions** come architecture baseline; non è un servizio operativo verificato.
- AP-008 è chiuso nel perimetro bounded read-only; non abilita command path, remediation o Safety Authority.
- BKL-042 è **Closed / Accepted** nel perimetro bounded read-only con limiti OAT espliciti.
- BKL-043 è il package corrente: F1/F2 sono completati, F3 è repository-only con test offline passati e F4 è una decision draft. Scope e target `EAGLE30154` sono selezionati, ma nessun runtime o pilot è autorizzato.
- S10 production runtime: `UNAVAILABLE`.

## 4. Boundary non negoziabili
- local physical interlocks = Safety Authority;
- BKL-032 = Session Readiness / Go-No-Go decision-support authority;
- BKL-031 = advisory/read-only, nessuna readiness/safety/action authority;
- nessun scheduler, automatic target selection o device command;
- coordinate sito protette mai in projection pubbliche;
- missing/stale/conflicted evidence fail-closed;
- provider/model/run lineage esplicita, nessun fallback/stitching silenzioso;
- il traffico MeteoHub F9 resta entro il modello ADR-012 governato: nessun limite giornaliero imposto dal workflow, budget EUR 0, fail-closed e GRIB effimeri.

## 5. Provider budget corrente
- F4-C generalized validation: `2/2_EXHAUSTED`;
- F7 protected-site one-shot: `1/1_EXHAUSTED`;
- F8: zero provider requests;
- F9 closure: refresh MeteoHub governato verificato; nessuna estensione di traffico oltre il limite ADR-012.

## 6. Disciplina di delivery
Exact-head CI → ARB → Release Quality sullo stesso SHA → expected-head merge → post-merge verification → acceptance reconciliation. Nessuna acceptance o runtime claim può precedere l'evidence reale.

## 7. Punto di ripresa
Riprendere da **BKL-043 F3/F4 exact pilot authorization preparation** usando `docs/project/HANDOVER_2026-09-25-BKL043-F4.md` come handover compatto e `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-25.md` come baseline tecnica corrente. Il prossimo gate è chiudere F3, completare tutti i campi F4 e ottenere review indipendenti; un eventuale pilot richiede poi una decisione owner separata.
