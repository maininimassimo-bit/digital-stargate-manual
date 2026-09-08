# Digital StarGate AI Bootstrap

| Campo | Valore |
|---|---|
| Versione | 2.1 |
| Baseline | 08/09/2026 |
| Stato | Current root bootstrap |

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro, collaboratore o assistente AI che intervenga sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale

Il repository GitHub è l'unica fonte autorevole. Non assumere che memoria della conversazione, prompt precedenti, roadmap visuali o dataset JSON rappresentino lo stato corrente. Verificare sempre branch, commit, file e workflow reali prima di proporre o applicare modifiche.

## 2. Sequenza obbligatoria di lettura

1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-09-08.md`
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-08.md`
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

## 6. Stato di continuità corrente — 08/09/2026

- BKL-030 CLOSED / ACCEPTED.
- BKL-015 DONE / ACCEPTED; TD-008 RESOLVED.
- BKL-044 CLOSED / ACCEPTED con F1-F4 completati.
- BKL-035 CLOSED / ACCEPTED con F1-F4 completati.
- BKL-040 CLOSED / ACCEPTED con F1-F4 completati; PR #117 merge `80d22a255540ac582733c60dfe9bbf7807bcdf9b`.
- Post-merge BKL-040 F4: Developer Foundation #1053, Docs #671, Word #1096 e Pages #712 — SUCCESS.
- PR #118 governa la closure finale, continuity reconciliation e document alignment di BKL-040.
- Il package dependency-ready corrente è **BKL-038 — Anomaly & Trend Center**.
- **BKL-037 non è corrente**: resta Planned finché la dipendenza dichiarata BKL-045 non è accepted.
- BKL-038 deve costruire anomaly/trend semantics sopra BKL-030 e BKL-040 accettati, preservando source authority, explainability e Safety boundaries.
- repository authority e source authority devono restare preservate; anomaly/trend view e AI/read model sono projection, non nuove authority.
- graph DB, vector DB, RAG, inference runtime/provider, automatic remediation e AI/Safety authority restano non autorizzati salvo governance successiva.
- runtime EAGLE e Safety Authority restano invariati.

### Sequenza governata corrente

`BKL-030 CLOSED -> BKL-015 CLOSED -> BKL-044 CLOSED -> BKL-035 CLOSED -> BKL-040 CLOSED -> BKL-038 CURRENT -> BKL-039 -> BKL-045 -> BKL-037 -> BKL-041 -> BKL-046 -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## 7. Quality-gate handover

La continuity authority corrente è `docs/project/HANDOVER_2026-09-08.md`; il delta tecnico è `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-08.md`; la closure BKL-040 è `docs/project/BKL-040-CLOSURE-2026-09-08.md`.

BKL-030, BKL-015, BKL-044, BKL-035 e BKL-040 non possono essere riaperti implicitamente. Health policy, anomaly severity policy, remediation, command path, Safety Authority coupling, graph infrastructure persistente o AI authority richiedono governance separata.

## 8. Divieti

Non inventare branch/file/commit/test/workflow/stati; non marcare approved senza evidence; non promuovere una projection a source primaria; non aggirare interlock/safe state; non introdurre inferenze AI come repository truth; non perdere semantic type/lifecycle/authority/Citation/Provenance nei consumer successivi.

## 9. Punto di partenza operativo

Aprire handover e current technical baseline 08/09, Context, Knowledge Map, closure BKL-040 e le foundation BKL-030/BKL-040; verificare HEAD/workflow correnti. Dopo la merge/acceptance finale di PR #118, il package governato corrente è **BKL-038 Anomaly & Trend Center**. Il primo incremento deve partire esclusivamente da fonti storiche e health evidence realmente governate nel repository, senza threshold, ingestion o remediation impliciti.