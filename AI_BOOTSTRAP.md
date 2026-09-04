# Digital StarGate AI Bootstrap

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro, collaboratore o assistente AI che intervenga sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale

Il repository GitHub è l'unica fonte autorevole. Non assumere che memoria della conversazione, prompt precedenti, roadmap visuali o dataset JSON rappresentino lo stato corrente. Verificare sempre branch, commit, file e workflow reali prima di proporre o applicare modifiche.

## 2. Sequenza obbligatoria di lettura

1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-09-04.md` — handover corrente
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-04.md` — baseline tecnica corrente
4. `docs/project/BACKLOG.md`
5. `.github/roadmap/roadmap-source.json`
6. `docs/data/roadmap.json` — projection generata, non authority
7. `docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md`
8. `docs/project/REPOSITORY_KNOWLEDGE_MAP.md`
9. `docs/project/TECHNICAL_DEBT.md`
10. `docs/project/DECISION_LOG.md`
11. `docs/project/DEVELOPMENT_WORKFLOW.md`
12. `docs/project/CODING_STANDARDS.md`
13. `docs/project/RELEASE_PLAYBOOK.md`
14. `docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md`
15. Architecture Package, ADR, review, evidence e componenti direttamente coinvolti nell'attività.

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
- AI spiegabile con evidence, confidence e distinzione observation/inference/recommendation;
- post-processing provenance machine-readable e local-first;
- AI PixInsight inizialmente `ADVISORY ONLY`;
- nessuna affermazione di build, test, commit, deploy o acceptance senza verifica reale.

## 6. Processo di sviluppo

Procedere una milestone alla volta: repository truth -> architettura -> implementazione -> test -> commit/push -> workflow -> Pages -> registri/governance -> handover/baseline. Non iniziare una milestone successiva se la baseline precedente presenta drift o quality gate rosso non spiegato e registrato.

Ogni modifica che cambia comportamento osservabile del portale, pipeline scientifica o stato di una capability deve includere un controllo esplicito di allineamento documentale e handover prima della closure.

## 7. Stato di continuità corrente — 04/09/2026

- `BKL-030 EAGLE Health & Reliability Telemetry` è **CLOSED / ACCEPTED** dopo G1-G8.
- G7 è stato integrato via PR #89, merge `a15d85b27ebfbe8a6488330920d10dda8db79a78`.
- G8 Safety Review è stato chiuso via PR #90, merge `eeba3372d8d788322f52553091f8d63cef5f9e68`.
- La pagina `Observatory Status` mostra correttamente la telemetria EAGLE hosted da Cloud Run; la projection resta read-only, fail-closed, `UNKNOWN / POLICY_NOT_ACTIVATED` a livello complessivo, senza remediation e senza Safety Authority.
- Il relay Cloud Run production usa la revisione `dsg-observatory-status-relay-00005-rof`; il trasporto N.I.N.A. e EAGLE Health è stato verificato end-to-end con `rejected=0` durante l'OAT.
- Su `EAGLE30154` è operativo il task `DigitalStarGate-EagleHealthTelemetry`, account `PrimaLuceLab`, logon S4U, cadenza 1 minuto, `MultipleInstances=IgnoreNew`, runtime `main`, secret DPAPI LocalMachine.
- Il runtime EAGLE autorevole resta `C:\DigitalStarGate\digital-stargate-manual-ap14-runtime` e deve rimanere sul branch `main` per preservare sia la telemetria sia l'importazione automatica delle sessioni.
- Prima di ogni session import verificare: branch `main`, working tree pulito, `git fetch origin`, `HEAD == origin/main`. Worktree feature/OAT non devono sostituire il runtime operativo.
- `DigitalStarGate.Reporting 1.0.8` resta la baseline runtime scientifica EAGLE per il producer sessione.
- AP-013C ha completato il proprio incremento DRY_RUN/NO_DELETE e resta separato da qualsiasi futura autorizzazione di cleanup produttivo.
- Nessuna severity numerica di EAGLE Health è approvata; capacità storage e salute fisica restano evidence separate.
- `Windows Time` può essere osservato come evidence ma nessuna remediation automatica è autorizzata.

### Sequenza governata corrente

`BKL-030 CLOSED -> BKL-015 Knowledge Graph machine-readable foundation -> BKL-044 Knowledge Graph / AI Evidence Contract -> BKL-035 -> BKL-040 -> BKL-037 -> BKL-038 -> BKL-039 -> BKL-041 -> BKL-045 -> BKL-046 -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

Lo stato deve essere nuovamente verificato nel repository a ogni utilizzo di questo file.

## 8. Quality-gate handover

La baseline corrente di continuità è `docs/project/HANDOVER_2026-09-04.md`; il delta tecnico corrente è `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-04.md`.

BKL-030 non può essere riaperto implicitamente da nuove feature. Qualunque health policy, health score, remediation, command path o Safety Authority coupling richiede un nuovo package/decisione governata.

Lo Scheduled Task EAGLE Health è un publisher read-only: non autorizza soglie, remediation o modifiche hardware.

## 9. Output richiesto a ogni intervento

Riportare file modificati, commit SHA, validazioni eseguite/non eseguite, rischi residui e prossimo passo in ordine di dipendenza. Se l'intervento cambia capability, pipeline o comportamento pubblicato, riportare anche l'esito del controllo di sincronizzazione handover/documentazione.

## 10. Divieti

Non inventare branch/file/commit/test/workflow/stati; non marcare approved senza evidence; non promuovere una projection a source primaria; non aggirare interlock/safe state/four-eyes/controller locale; non introdurre debito tecnico senza registrarlo; non inferire SQM, mains, safety o health da proxy non governati; non cancellare raw scientifici sulla base della sola export completion; non usare un worktree feature come runtime EAGLE operativo.

## 11. Punto di partenza operativo

Aprire `docs/project/HANDOVER_2026-09-04.md` e `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-04.md`, verificare HEAD/workflow correnti e riconfermare lo stato runtime EAGLE. Il prossimo package governato è **BKL-015 Knowledge Graph machine-readable foundation**. Prima di avviarlo devono risultare verdi i workflow del package handover corrente e il runtime EAGLE deve restare sul branch `main`.
