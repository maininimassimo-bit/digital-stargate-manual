# Digital StarGate AI Bootstrap

| Campo | Valore |
|---|---|
| Versione | 2.3 |
| Baseline | 09/09/2026 |
| Stato | Current root bootstrap — BKL-039 closure candidate |

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro, collaboratore o assistente AI che intervenga sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale

Il repository GitHub è l'unica fonte autorevole. Non assumere che memoria della conversazione, prompt precedenti, roadmap visuali o dataset JSON rappresentino lo stato corrente. Verificare sempre branch, commit, file e workflow reali prima di proporre o applicare modifiche.

## 2. Sequenza obbligatoria di lettura

1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-09-09.md`
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-09.md`
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

I documenti handover/baseline con data precedente sono snapshot storici: conservarli per lineage, ma non usarli come stato corrente quando esiste un successore datato più recente.

## 3. Verifica iniziale obbligatoria

Prima di modificare repository o runtime: identificare branch e HEAD, verificare file/SHA interessati, distinguere authority e projection, controllare backlog/roadmap/debito/decisioni e verificare workflow reali. Per EAGLE verificare che `C:\DigitalStarGate\digital-stargate-manual-ap14-runtime` resti su `main`, pulito e allineato a `origin/main`, salvo worktree OAT isolato.

## 4. Principi non negoziabili

- repository as source of truth;
- dataset e read model sono projection, mai authority implicita;
- Safety Authority fisica/locale indipendente;
- nessun comando diretto dal portale o dall'AI agli apparati nella baseline corrente;
- AI spiegabile con evidence, confidence, Citation, Provenance e distinzione Observation/Evidence/Claim/Inference/Recommendation;
- Knowledge Graph repository-centric come projection;
- nessuna affermazione di build/test/commit/deploy/acceptance senza verifica reale.

## 5. Processo di sviluppo

Procedere una milestone alla volta: repository truth -> architettura -> implementazione -> test -> commit/push -> workflow -> Pages -> governance -> handover/baseline. Non iniziare una milestone successiva se la baseline precedente presenta drift o quality gate rosso non spiegato.

## 6. Stato di continuità corrente — 09/09/2026

- BKL-030 CLOSED / ACCEPTED.
- BKL-015 DONE / ACCEPTED; TD-008 RESOLVED.
- BKL-044 CLOSED / ACCEPTED.
- BKL-035 CLOSED / ACCEPTED.
- BKL-040 CLOSED / ACCEPTED.
- BKL-038 CLOSED / ACCEPTED; final implementation PR #125 merge `d8249984d63455690b957156060f858eb3cc2713`, closure governata da `docs/project/BKL-038-CLOSURE-2026-09-09.md`.
- BKL-039 ha completato F4-A/F4-B/F5-A/F5-B/F5-C/F5-D; PR #132 merge `651fc340fbb5e58ca36409d574bdd09c3ae55790`.
- Post-merge BKL-039 sul merge SHA: BKL-039 F5 Governance #32, BKL-039 F4 Governance #29, Developer Foundation #1194, Docs #813, Word #1238 e Pages #727 — SUCCESS.
- La closure formale BKL-039 è governata da `docs/project/BKL-039-CLOSURE-2026-09-09.md`; finché la closure PR non è merged/post-merge green, lo stato è una continuity candidate.
- Il package successore dependency-ready è **BKL-045 — PixInsight Workflow Provenance Plugin**.
- **BKL-037 non è ancora corrente**: resta Planned finché BKL-045 non è accepted.
- BKL-039 resta historical/read-only/descriptive-only: nessun rating, threshold, health policy, recommendation, remediation o Safety Authority coupling è autorizzato.
- graph DB, vector DB, RAG, inference runtime/provider, automatic remediation e AI/Safety authority restano non autorizzati salvo governance successiva.
- runtime EAGLE e Safety Authority restano invariati.

### Sequenza governata corrente

`BKL-030 CLOSED -> BKL-015 CLOSED -> BKL-044 CLOSED -> BKL-035 CLOSED -> BKL-040 CLOSED -> BKL-038 CLOSED -> BKL-039 CLOSURE -> BKL-045 NEXT -> BKL-037 -> BKL-041 -> BKL-046 -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## 7. Quality-gate handover

La continuity authority candidate è `docs/project/HANDOVER_2026-09-09.md`; il delta tecnico candidate è `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-09.md`; la closure BKL-039 candidate è `docs/project/BKL-039-CLOSURE-2026-09-09.md`.

I package già accepted non possono essere riaperti implicitamente. Performance thresholds, health policy, anomaly severity policy, remediation, command path, Safety Authority coupling, graph infrastructure persistente o AI authority richiedono governance separata.

## 8. Divieti

Non inventare branch/file/commit/test/workflow/stati; non marcare approved senza evidence; non promuovere una projection a source primaria; non aggirare interlock/safe state; non introdurre inferenze AI come repository truth; non perdere semantic type/lifecycle/authority/Citation/Provenance nei consumer successivi.

## 9. Punto di partenza operativo

Completare la closure documentale BKL-039 con exact-head CI, merge expected-head e post-merge verification. Solo dopo la closure integrata promuovere BKL-045 come package governato corrente e avviare source discovery/contract del PixInsight Workflow Provenance Plugin. Non iniziare BKL-037 prima dell'acceptance di BKL-045.