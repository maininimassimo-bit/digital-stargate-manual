# Digital StarGate AI Bootstrap

| Campo | Valore |
|---|---|
| Versione | 2.2 |
| Baseline | 09/09/2026 |
| Stato | Current root bootstrap — closure candidate |

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
- BKL-038 ha completato F1, F2-A, F3-A, F3-B e F4-A; PR #125 merge `d8249984d63455690b957156060f858eb3cc2713`.
- Post-merge BKL-038 F4-A sul merge SHA: BKL-038 F4 Governance #4, Developer Foundation #1110, Docs #729, Pages #720 e Word #1154 — SUCCESS.
- La closure formale BKL-038 è governata da `docs/project/BKL-038-CLOSURE-2026-09-09.md`; finché la closure PR non è merged/post-merge green, lo stato 09/09 è una continuity candidate.
- Il package successore dependency-ready è **BKL-039 — Equipment Performance Registry**.
- **BKL-037 non è corrente**: resta Planned finché BKL-045 non è accepted.
- BKL-038 resta bounded/read-only/descriptive-only: nessun threshold, severity policy, causal promotion, predictive maintenance, remediation o Safety Authority coupling è autorizzato.
- BKL-030 EAGLE history non è stata fabbricata/onboarded analiticamente: richiede futura evidence repository-resolvable governata.
- graph DB, vector DB, RAG, inference runtime/provider, automatic remediation e AI/Safety authority restano non autorizzati salvo governance successiva.
- runtime EAGLE e Safety Authority restano invariati.

### Sequenza governata corrente

`BKL-030 CLOSED -> BKL-015 CLOSED -> BKL-044 CLOSED -> BKL-035 CLOSED -> BKL-040 CLOSED -> BKL-038 CLOSURE -> BKL-039 CURRENT -> BKL-045 -> BKL-037 -> BKL-041 -> BKL-046 -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## 7. Quality-gate handover

La continuity authority candidate è `docs/project/HANDOVER_2026-09-09.md`; il delta tecnico candidate è `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-09.md`; la closure candidate BKL-038 è `docs/project/BKL-038-CLOSURE-2026-09-09.md`.

BKL-030, BKL-015, BKL-044, BKL-035, BKL-040 e gli incrementi BKL-038 accettati non possono essere riaperti implicitamente. Performance thresholds, health policy, anomaly severity policy, remediation, command path, Safety Authority coupling, graph infrastructure persistente o AI authority richiedono governance separata.

## 8. Divieti

Non inventare branch/file/commit/test/workflow/stati; non marcare approved senza evidence; non promuovere una projection a source primaria; non aggirare interlock/safe state; non introdurre inferenze AI come repository truth; non perdere semantic type/lifecycle/authority/Citation/Provenance nei consumer successivi.

## 9. Punto di partenza operativo

Completare prima la closure BKL-038: exact-head CI, ARB indipendente, Release Quality, merge expected-head e post-merge verification. Solo dopo la closure integrata iniziare BKL-039 da repository-proven equipment/session evidence, senza inventare rating, threshold, health policy o remediation semantics.