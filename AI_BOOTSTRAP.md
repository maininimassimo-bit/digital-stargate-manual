# Digital StarGate AI Bootstrap

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro, collaboratore o assistente AI che intervenga sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale

Il repository GitHub è l'unica fonte autorevole. Non assumere che memoria della conversazione, prompt precedenti, roadmap visuali o dataset JSON rappresentino lo stato corrente. Verificare sempre branch, commit, file e workflow reali prima di proporre o applicare modifiche.

## 2. Sequenza obbligatoria di lettura

1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-09-07.md` — handover corrente
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-07.md` — baseline tecnica corrente
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
14. `docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md` e `docs/project/REPOSITORY_KNOWLEDGE_MAP.md` solo come mappe storico/strutturali quando utili, verificandone sempre data e baseline.

I documenti datati precedenti restano record storici. Per lo stato operativo corrente applicare repository truth, evidence, handover e technical baseline più recenti.

## 3. Verifica iniziale obbligatoria

Prima di modificare il repository o il runtime:

- identificare branch e HEAD;
- verificare file/SHA interessati;
- cercare documenti e identificativi sovrapposti;
- distinguere source primaria e projection;
- controllare backlog, roadmap, technical debt e decisioni;
- verificare workflow e Pages;
- segnalare divergenze prima di scrivere;
- per interventi sull'EAGLE verificare sempre che `C:\DigitalStarGate\digital-stargate-manual-ap14-runtime` sia sul branch `main`, working tree pulito e `HEAD == origin/main`, salvo worktree OAT esplicitamente isolato.

## 4. Gerarchia delle fonti

1. Architecture Package, ADR, capability e standard approvati;
2. assessment ARB, validation record, execution evidence e gate;
3. `.github/roadmap/roadmap-source.json` come roadmap authority;
4. backlog e planning approvati;
5. handover corrente e current technical baseline;
6. release note e commit pubblicati;
7. contratti machine-readable versionati;
8. dataset JSON/dashboard come proiezioni;
9. documenti di contesto storici;
10. conversazioni e prompt.

## 5. Principi non negoziabili

- repository as source of truth;
- componenti modulari e responsabilità singola;
- Scientific Data Engine come access layer condiviso per i dati scientifici;
- dataset JSON come proiezioni, mai come fonte primaria;
- Safety Authority fisica/locale indipendente e autorevole;
- telemetria, SQM scientifico, Health Score e AI non sono Safety Authority;
- nessun comando diretto dal portale o dall'AI agli apparati nella baseline corrente;
- collector EAGLE leggeri e read-only; analytics/AI fuori dal computer operativo quando possibile;
- AI spiegabile con evidence, confidence e distinzione observation/evidence/claim/inference/recommendation;
- post-processing provenance machine-readable e local-first;
- AI PixInsight inizialmente `ADVISORY ONLY`;
- Knowledge Graph repository-centric come projection, non authority;
- nessuna affermazione di build, test, commit, deploy o acceptance senza verifica reale.

## 6. Processo di sviluppo

Procedere una milestone alla volta: repository truth -> architettura -> implementazione -> test -> commit/push -> workflow -> Pages -> registri/governance -> handover/baseline. Non iniziare una milestone successiva se la baseline precedente presenta drift o quality gate rosso non spiegato e registrato.

Ogni modifica che cambia comportamento osservabile del portale, pipeline scientifica o stato di una capability deve includere un controllo esplicito di allineamento documentale e handover prima della closure.

## 7. Stato di continuità corrente — 07/09/2026

- `BKL-030 EAGLE Health & Reliability Telemetry` resta **CLOSED / ACCEPTED**.
- `BKL-015 Knowledge Graph machine-readable` resta **DONE / ACCEPTED** dopo F1-F3.
- `TD-008 Knowledge Traceability` resta **RESOLVED** per AP/ADR/component/evidence machine-readable traceability.
- `BKL-044 Knowledge Graph / AI Evidence Contract` è **IN PROGRESS**.
- BKL-044 F1 è stato integrato via PR #98, merge `6b9db9b342144645da62381d6833ff1ebff3c22c`.
- F1 stabilisce le semantiche Observation, Evidence, Claim, Inference, Recommendation, Confidence, Citation, Provenance, Conflict e Unknown.
- Le review F1 sono `Approved with Conditions` (ARB) e `Conditionally Ready — F1 only` (Release Quality).
- Il prossimo incremento governato è **BKL-044 F2 — machine-readable schema and fail-closed validation**.
- Il Knowledge Graph repository BKL-015 resta una projection repository-centric; il suo schema reale è `schemas/knowledge-graph-foundation.schema.json`.
- BKL-044 non autorizza automaticamente graph DB, vector DB, RAG, inference runtime o AI authority.
- Il runtime EAGLE resta invariato e deve rimanere sul branch `main` per preservare telemetria e importazione automatica delle sessioni.
- `DigitalStarGate.Reporting 1.0.8` resta la baseline runtime scientifica EAGLE nota.
- AP-013C resta chiuso per DRY_RUN/NO_DELETE; nessun cleanup produttivo C8/source è autorizzato.

### Sequenza governata corrente

`BKL-030 CLOSED -> BKL-015 CLOSED -> BKL-044 IN PROGRESS (F1 MERGED; F2 NEXT) -> BKL-035 -> BKL-040 -> BKL-037 -> BKL-038 -> BKL-039 -> BKL-041 -> BKL-045 -> BKL-046 -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

Lo stato deve essere nuovamente verificato nel repository a ogni utilizzo di questo file.

## 8. Quality-gate handover

La baseline corrente di continuità è `docs/project/HANDOVER_2026-09-07.md`; il delta tecnico corrente è `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-07.md`.

BKL-030 e BKL-015 non possono essere riaperti implicitamente da nuove feature. Qualunque health policy, remediation, command path, Safety Authority coupling, graph infrastructure persistente o AI authority richiede un package/decisione governata separata.

## 9. Output richiesto a ogni intervento

Riportare file modificati, commit SHA, validazioni eseguite/non eseguite, rischi residui e prossimo passo in ordine di dipendenza. Se l'intervento cambia capability, pipeline o comportamento pubblicato, riportare anche l'esito del controllo di sincronizzazione handover/documentazione.

## 10. Divieti

Non inventare branch/file/commit/test/workflow/stati; non marcare approved senza evidence; non promuovere una projection a source primaria; non aggirare interlock/safe state/four-eyes/controller locale; non introdurre debito tecnico senza registrarlo; non inferire SQM, mains, safety o health da proxy non governati; non cancellare raw scientifici sulla base della sola export completion; non usare un worktree feature come runtime EAGLE operativo; non introdurre inferenze AI nel Knowledge Graph come repository truth senza provenance e contratto approvato.

## 11. Punto di partenza operativo

Aprire `docs/project/HANDOVER_2026-09-07.md` e `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-07.md`, verificare HEAD/workflow correnti e riconfermare lo stato runtime EAGLE solo se il lavoro richiede il runtime. Il package governato corrente è **BKL-044**, con **F2** come prossimo incremento.