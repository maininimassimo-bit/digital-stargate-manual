# Digital StarGate AI Bootstrap

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro, collaboratore o assistente AI che intervenga sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale

Il repository GitHub è l'unica fonte autorevole. Non assumere che memoria della conversazione, prompt precedenti, roadmap visuali o dataset JSON rappresentino lo stato corrente. Verificare sempre branch, commit, file e workflow reali prima di proporre o applicare modifiche.

## 2. Sequenza obbligatoria di lettura

1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-08-30.md`
3. `docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md`
4. `docs/project/REPOSITORY_KNOWLEDGE_MAP.md`
5. `docs/project/BACKLOG.md`
6. `docs/project/FUNCTIONAL_ROADMAP_EXPANSION_2026-08-30.md`
7. `.github/roadmap/roadmap-source.json`
8. `docs/project/TECHNICAL_DEBT.md`
9. `docs/project/DECISION_LOG.md`
10. `docs/project/DEVELOPMENT_WORKFLOW.md`
11. `docs/project/CODING_STANDARDS.md`
12. `docs/project/RELEASE_PLAYBOOK.md`
13. `docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md`
14. Architecture Package, ADR, review, evidence e componenti direttamente coinvolti nell'attività.

## 3. Verifica iniziale

Prima di modificare il repository: identificare branch e HEAD; verificare file/SHA interessati; cercare documenti e identificativi sovrapposti; distinguere source primaria e projection; controllare backlog, technical debt e decisioni; verificare workflow e Pages; segnalare divergenze prima di scrivere.

## 4. Gerarchia delle fonti

1. Architecture Package, ADR, capability e standard approvati;
2. assessment ARB, validation record, execution evidence e gate;
3. roadmap autorevole e `.github/roadmap/roadmap-source.json` per la projection operativa;
4. backlog e documenti di planning approvati;
5. release note e commit pubblicati;
6. contratti machine-readable versionati;
7. dataset JSON/dashboard come proiezioni;
8. conversazioni e prompt.

## 5. Principi non negoziabili

- repository as source of truth;
- componenti modulari e responsabilità singola;
- Scientific Data Engine come access layer condiviso per i dati scientifici;
- dataset JSON come proiezioni, mai come fonte primaria;
- Safety Authority fisica/locale indipendente e autorevole;
- telemetria, Health Score e AI non sono Safety Authority;
- nessun comando diretto dal portale o dall'AI agli apparati nella baseline corrente;
- collector EAGLE leggeri; analytics/AI fuori dal computer operativo quando possibile;
- AI spiegabile con evidence, confidence e distinzione observation/inference/recommendation;
- post-processing provenance machine-readable e local-first;
- AI PixInsight inizialmente `ADVISORY ONLY`;
- nessuna affermazione di build, test, commit, deploy o acceptance senza verifica reale.

## 6. Processo di sviluppo

Procedere una milestone alla volta: repository truth -> architettura -> implementazione -> test -> commit/push -> workflow -> Pages -> registri/governance. Non iniziare una milestone successiva se la baseline precedente presenta drift o quality gate rosso non spiegato e registrato.

## 7. Stato di continuità corrente — 30/08/2026

- BKL-007, BKL-008, BKL-009 e BKL-010 sono `Done`; governance/Pages hardening corrente completato.
- AP-012 C04 è Closed/Approved; AP-013 e AP-014 sono accepted secondo le rispettive evidence.
- Observatory Status integra Network e Power da source verificate; Power osserva TS Shelter J6 con mask `0x00000001`; la Safety Authority resta separata.
- La nuova roadmap funzionale BKL-029–BKL-046 è approvata e registrata in backlog e planning.
- **BKL-029 SQM Sky Quality Telemetry & Scientific History è il prossimo sviluppo operativo.** SQM deve essere realtime e storicizzato nelle sessioni con provenance/statistiche.
- BKL-030 introduce EAGLE Health & Reliability: disco/trend, RAM, CPU, uptime, Event Log, crash, clock/NTP, task, heartbeat, producer freshness, USB/COM, update/reboot e configuration drift.
- BKL-015 Knowledge Graph viene dopo BKL-029/BKL-030 e deve essere progettato tenendo già conto di BKL-044 Knowledge/AI Evidence Contract.
- BKL-045 prevede una estensione PixInsight per workflow provenance riproducibile; la scelta modulo/plugin nativo vs package/script deve essere oggetto di architecture assessment.
- BKL-046 prevede AI Post-Processing Assistant dipendente da Knowledge Graph/Evidence Contract e BKL-045, inizialmente advisory e human-controlled.
- BKL-042 AI Observatory Assistant resta read-only/advisory nella prima release: troubleshooting, RCA, anomaly investigation, predictive maintenance, readiness, planning e knowledge navigation senza controllo diretto dei device.
- AP-015 Scientific Knowledge Platform resta successivo alle foundation intelligence/knowledge approvate.

### Sequenza governata di riferimento

`BKL-029 -> BKL-030 -> BKL-015 -> BKL-044 -> BKL-035 -> BKL-040 -> BKL-037 -> BKL-038 -> BKL-039 -> BKL-041 -> BKL-045 -> BKL-046 -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

Lo stato deve essere nuovamente verificato nel repository a ogni utilizzo di questo file.

## 8. Quality-gate handover

Il run Developer Foundation #791 ha fallito esclusivamente su `Verify generated roadmap` perché la projection versionata era precedente all'espansione; build/test/format e i test eseguiti prima del gate erano PASS. Pages della stessa baseline ha generato e pubblicato correttamente la nuova projection. La projection è stata quindi riallineata nel repository. **Una nuova chat deve verificare i workflow generati dagli ultimi commit e non assumere PASS finché Developer Foundation, documentazione/Pages e gli altri workflow applicabili non risultano completati con successo.**

## 9. Output richiesto a ogni intervento

Riportare file modificati, commit SHA, validazioni eseguite/non eseguite, rischi residui e prossimo passo in ordine di dipendenza.

## 10. Divieti

Non inventare branch/file/commit/test/workflow/stati; non marcare approved senza evidence; non promuovere una projection a source primaria; non aggirare interlock/safe state/four-eyes/controller locale; non introdurre debito tecnico senza registrarlo; non inferire SQM, mains, safety o health da proxy non governati.

## 11. Punto di partenza operativo

Aprire `docs/project/HANDOVER_2026-08-30.md`, verificare HEAD e workflow correnti, poi eseguire la prima voce `Ready` compatibile con le dipendenze. Se la baseline è verde, partire da **BKL-029 SQM source discovery e architecture**.
