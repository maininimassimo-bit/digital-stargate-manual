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

## 7. Stato di continuità corrente — 01/09/2026

- BKL-007–BKL-013 e BKL-018–BKL-029 risultano `Done` secondo backlog/evidence correnti; governance e AP-014 acceptance restano consolidate.
- AP-012 C04 è Closed/Approved; AP-013 e AP-014 sono accepted secondo le rispettive evidence.
- Observatory Status integra Network e Power da source verificate; Power osserva TS Shelter J6 con mask `0x00000001`; la Safety Authority resta separata.
- La roadmap funzionale BKL-029–BKL-046 è approvata e registrata in backlog e planning.
- **BKL-029 SQM Sky Quality Telemetry & Scientific History è chiuso `Done`.** PR #68 è stata mergiata in `main` con merge commit `0ebf04ec0ba1c4a1236f2a52e8a7e44abe0c6441`; realtime, historical provenance, E2E, CI/ARB e runtime OAT sono accettati.
- **BKL-030 EAGLE Health & Reliability è la prossima capability `Ready`.** Il primo passo è D1/D2 source discovery read-only su EAGLE30154 usando `scripts/telemetry/Inspect-EagleHealthSources.ps1`; nessun health signal è Safety Authority e nessuna soglia va inventata.
- BKL-015 Knowledge Graph viene dopo BKL-030 e deve essere progettato tenendo già conto di BKL-044 Knowledge/AI Evidence Contract.
- BKL-045 prevede una estensione PixInsight per workflow provenance riproducibile; la scelta modulo/plugin nativo vs package/script deve essere oggetto di architecture assessment.
- BKL-046 prevede AI Post-Processing Assistant dipendente da Knowledge Graph/Evidence Contract e BKL-045, inizialmente advisory e human-controlled.
- BKL-042 AI Observatory Assistant resta read-only/advisory nella prima release: troubleshooting, RCA, anomaly investigation, predictive maintenance, readiness, planning e knowledge navigation senza controllo diretto dei device.
- AP-015 Scientific Knowledge Platform resta successivo alle foundation intelligence/knowledge approvate.

### Sequenza governata di riferimento

`BKL-029 Done -> BKL-030 Ready -> BKL-015 -> BKL-044 -> BKL-035 -> BKL-040 -> BKL-037 -> BKL-038 -> BKL-039 -> BKL-041 -> BKL-045 -> BKL-046 -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

Lo stato deve essere nuovamente verificato nel repository a ogni utilizzo di questo file.

## 8. Quality-gate handover

La baseline BKL-029 accettata corrisponde alla PR #68, con HEAD pre-merge `6c255b7beee299e361b9b5da5d35fbfa6f3f4756`. Su quella baseline risultano completed/success Developer Foundation #868, Validate Digital StarGate History #25, Validate documentation #460 e Genera manuale Word #874. La PR è stata quindi mergiata come `0ebf04ec0ba1c4a1236f2a52e8a7e44abe0c6441`.

Sul merge SHA è stata verificata l'attivazione dei workflow post-merge; Validate documentation #461 è risultata `SUCCESS` e l'ispezione dei workflow sul merge SHA non ha rilevato failure al momento della closure review.

Questa baseline non è una deroga alla repository truth: una nuova chat deve sempre verificare HEAD e workflow successivi. Se esistono commit posteriori, il loro stato prevale sulla fotografia riportata qui.

## 9. Output richiesto a ogni intervento

Riportare file modificati, commit SHA, validazioni eseguite/non eseguite, rischi residui e prossimo passo in ordine di dipendenza.

## 10. Divieti

Non inventare branch/file/commit/test/workflow/stati; non marcare approved senza evidence; non promuovere una projection a source primaria; non aggirare interlock/safe state/four-eyes/controller locale; non introdurre debito tecnico senza registrarlo; non inferire SQM, mains, safety o health da proxy non governati.

## 11. Punto di partenza operativo

Aprire `docs/project/HANDOVER_2026-08-30.md`, verificare HEAD e workflow correnti, poi eseguire la prima voce `Ready` compatibile con le dipendenze. Con BKL-029 chiuso, il punto di partenza è **BKL-030 D1/D2 EAGLE Health source discovery**, mantenendo il collector discovery-only/read-only fino alla classificazione delle source e alla conferma del boundary.