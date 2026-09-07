# Digital StarGate AI Bootstrap

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro, collaboratore o assistente AI che intervenga sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale

Il repository GitHub è l'unica fonte autorevole. Non assumere che memoria della conversazione, prompt precedenti, roadmap visuali o dataset JSON rappresentino lo stato corrente. Verificare sempre branch, commit, file e workflow reali prima di proporre o applicare modifiche.

## 2. Sequenza obbligatoria di lettura

1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-09-07.md`
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-07.md`
4. `docs/project/BACKLOG.md`
5. `.github/roadmap/roadmap-source.json`
6. `docs/data/roadmap.json` — projection generata, non authority
7. `docs/project/TECHNICAL_DEBT.md`
8. `docs/project/DECISION_LOG.md`
9. `docs/project/DEVELOPMENT_WORKFLOW.md`
10. `docs/project/CODING_STANDARDS.md`
11. `docs/project/RELEASE_PLAYBOOK.md`
12. `docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md`
13. Architecture Package, ADR, review, evidence e componenti direttamente coinvolti nell'attività.

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

## 6. Stato di continuità corrente — 07/09/2026

- BKL-030 resta CLOSED / ACCEPTED.
- BKL-015 resta DONE / ACCEPTED.
- TD-008 resta RESOLVED.
- BKL-044 resta IN PROGRESS.
- F1 è CLOSED / ACCEPTED via PR #98.
- F2 è CLOSED / ACCEPTED via PR #100.
- F3 è CLOSED / ACCEPTED via PR #102, merge `8d9f47922de1536b424cdd29ca00fc61c5c9fa49`.
- ARB F3 re-review: APPROVED 99/100.
- Release Quality F3: READY.
- Post-merge F3: Developer Foundation #992, docs #601, Word #1026 e Pages #695 — SUCCESS.
- Il prossimo incremento governato è **BKL-044 F4 — Consumer / Read-Model Contract**.
- F4 deve preservare semantic type, lifecycle, source authority, Citation, Provenance e Confidence nei consumer senza semantic flattening o authority escalation.
- graph DB, vector DB, RAG, inference runtime/provider e AI authority restano non autorizzati/indecisi.
- runtime EAGLE e Safety Authority restano invariati.

### Sequenza governata corrente

`BKL-030 CLOSED -> BKL-015 CLOSED -> BKL-044 IN PROGRESS (F1/F2/F3 ACCEPTED; F4 CURRENT) -> BKL-035 -> BKL-040 -> BKL-037 -> BKL-038 -> BKL-039 -> BKL-041 -> BKL-045 -> BKL-046 -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## 7. Quality-gate handover

La baseline di continuità è `docs/project/HANDOVER_2026-09-07.md`; il delta tecnico è `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-07.md`; la closure F3 è `docs/project/BKL-044-F3-CLOSURE-2026-09-07.md`.

BKL-030 e BKL-015 non possono essere riaperti implicitamente. Health policy, remediation, command path, Safety Authority coupling, graph infrastructure persistente o AI authority richiedono governance separata.

## 8. Divieti

Non inventare branch/file/commit/test/workflow/stati; non marcare approved senza evidence; non promuovere una projection a source primaria; non aggirare interlock/safe state; non introdurre inferenze AI come repository truth; non appiattire semantic type/lifecycle/authority/Citation/Provenance nei consumer F4.

## 9. Punto di partenza operativo

Aprire handover, current technical baseline, closure F3 e contratto BKL-044 v0.6; verificare HEAD/workflow correnti. Il package governato corrente è **BKL-044**, con **F4 Consumer / Read-Model Contract** come incremento corrente.