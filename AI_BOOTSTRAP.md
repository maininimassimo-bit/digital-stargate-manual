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
- BKL-015 resta DONE / ACCEPTED; TD-008 resta RESOLVED.
- BKL-044 è CLOSED / ACCEPTED con F1-F4 completati.
- F4 Consumer / Read-Model Contract è stato integrato via PR #104, merge `b7c01ba7221818e1971403ab3befe38c8e40cc54`.
- Post-merge F4: Developer Foundation #1004, Docs #613, Word #1038 e Pages #697 — SUCCESS.
- Closure: `docs/project/BKL-044-CLOSURE-2026-09-07.md`.
- Il package governato corrente è **BKL-035 — Target Knowledge Base**.
- BKL-035 deve costruire una vista target-centrica collegando sessioni, SQM, setup, immagini e processing provenance sopra le foundation accettate BKL-015/BKL-044.
- repository authority e source authority devono restare preservate; la Target Knowledge Base è una projection/read model, non una nuova authority.
- graph DB, vector DB, RAG, inference runtime/provider e AI authority restano non autorizzati/indecisi salvo governance successiva.
- runtime EAGLE e Safety Authority restano invariati.

### Sequenza governata corrente

`BKL-030 CLOSED -> BKL-015 CLOSED -> BKL-044 CLOSED -> BKL-035 CURRENT -> BKL-040 -> BKL-037 -> BKL-038 -> BKL-039 -> BKL-041 -> BKL-045 -> BKL-046 -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

## 7. Quality-gate handover

La baseline di continuità è `docs/project/HANDOVER_2026-09-07.md`; il delta tecnico è `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-07.md`; la closure BKL-044 è `docs/project/BKL-044-CLOSURE-2026-09-07.md`.

BKL-030, BKL-015 e BKL-044 non possono essere riaperti implicitamente. Health policy, remediation, command path, Safety Authority coupling, graph infrastructure persistente o AI authority richiedono governance separata.

## 8. Divieti

Non inventare branch/file/commit/test/workflow/stati; non marcare approved senza evidence; non promuovere una projection a source primaria; non aggirare interlock/safe state; non introdurre inferenze AI come repository truth; non perdere semantic type/lifecycle/authority/Citation/Provenance nei consumer successivi.

## 9. Punto di partenza operativo

Aprire handover, current technical baseline, closure BKL-044 e le foundation BKL-015/BKL-044; verificare HEAD/workflow correnti. Il package governato corrente è **BKL-035 Target Knowledge Base**. Il primo incremento BKL-035 deve essere definito a partire dalle fonti target/session/SQM/setup/image/processing realmente governate nel repository, senza broad ingestion implicita.