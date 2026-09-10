# Digital StarGate AI Bootstrap

| Campo | Valore |
|---|---|
| Versione | 2.5 |
| Baseline | 10/09/2026 |
| Stato | Current root bootstrap — BKL-037 Session Comparison & Benchmarking |

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro, collaboratore o assistente AI che intervenga sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale

Il repository GitHub è l'unica fonte autorevole. Non assumere che memoria della conversazione, prompt precedenti, roadmap visuali o dataset JSON rappresentino lo stato corrente. Verificare sempre branch, commit, file e workflow reali prima di proporre o applicare modifiche.

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
15. Architecture Package, ADR, review, evidence e componenti direttamente coinvolti nell'attività.

Handover e baseline datati precedenti sono snapshot storici: conservarli per lineage e non usarli come stato corrente quando esiste un successore più recente.

## 3. Verifica iniziale obbligatoria

Prima di modificare repository o runtime: identificare branch e HEAD, verificare file/SHA interessati, distinguere authority e projection, controllare backlog/roadmap/debito/decisioni e verificare workflow reali. Per EAGLE verificare che `C:\DigitalStarGate\digital-stargate-manual-ap14-runtime` resti su `main`, pulito e allineato a `origin/main`, salvo worktree OAT isolato.

## 4. Principi non negoziabili

- repository as source of truth;
- dataset e read model sono projection, mai authority implicita;
- Safety Authority fisica/locale indipendente;
- nessun comando diretto dal portale o dall'AI agli apparati nella baseline corrente;
- AI spiegabile con evidence, confidence, Citation, Provenance e distinzione Observation/Evidence/Claim/Inference/Recommendation;
- processing provenance distingue sempre `OBSERVED`, `DECLARED` e `SUGGESTED`;
- nessuna affermazione di build/test/commit/deploy/acceptance senza verifica reale;
- missing/unavailable evidence non può essere inventata o promossa a fatto osservato.

## 5. Processo di sviluppo

Procedere una milestone alla volta: repository truth -> architettura -> implementazione -> test -> commit/push -> workflow -> Pages -> governance -> handover/baseline. Non iniziare una milestone successiva se la baseline precedente presenta drift o quality gate rosso non spiegato.

## 6. Stato di continuità corrente — 10/09/2026

- BKL-030, BKL-015, BKL-044, BKL-035, BKL-040, BKL-038 e BKL-039 sono CLOSED/DONE e ACCEPTED secondo i rispettivi record.
- BKL-045 — PixInsight Workflow Provenance Plugin è CLOSED / ACCEPTED; closure `docs/project/BKL-045-CLOSURE-2026-09-10.md`, PR #140 merge `a08aed981e5ffa4af6b68fea521ada25a4b2b338`.
- BKL-037 — Session Comparison & Benchmarking è il package governato CURRENT / In Progress nella canonical roadmap e nel backlog.
- BKL-041 — Scientific Data Quality Score è il successore pianificato e dipende da BKL-037.
- BKL-037 resta read-only/descriptive-only: nessun ranking, acceptance threshold, quality score, recommendation, remediation, command path o Safety Authority coupling.
- La provenance PixInsight mantiene la limitazione accettata `completeness=UNAVAILABLE` per la storia di processing non automaticamente osservabile.
- runtime EAGLE e Safety Authority restano invariati.

### Sequenza governata corrente

`... -> BKL-045 CLOSED -> BKL-037 [CURRENT] -> BKL-041 -> BKL-046 -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## 7. Authority e continuity

La canonical roadmap source è `.github/roadmap/roadmap-source.json`; `docs/data/roadmap.json` è una projection generata. Il live `BACKLOG.md` governa stato, priorità e dipendenze. Closure, review, evidence e workflow supportano le acceptance claim sui rispettivi exact SHA.

I package già accepted non possono essere riaperti implicitamente. Scoring scientifico autonomo appartiene a BKL-041 e non deve essere anticipato in BKL-037.

## 8. Divieti

Non inventare branch/file/commit/test/workflow/stati; non marcare approved senza evidence; non promuovere una projection a source primaria; non aggirare interlock/safe state; non introdurre inferenze AI come repository truth; non perdere semantic type/lifecycle/authority/Citation/Provenance nei consumer successivi.

## 9. Punto di partenza operativo

Continuare **BKL-037 — Session Comparison & Benchmarking** verificando prima lo stato live di `main`, backlog, canonical roadmap, package/closure BKL-037 e workflow. La capability deve confrontare esclusivamente dimensioni realmente comparabili e con unità/provenance compatibili; esclusioni e incompletezza restano visibili. Non iniziare BKL-041 finché BKL-037 non è formalmente chiuso/accettato e la transizione canonica non è integrata.