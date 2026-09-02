# Digital StarGate AI Bootstrap

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro, collaboratore o assistente AI che intervenga sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale

Il repository GitHub è l'unica fonte autorevole. Non assumere che memoria della conversazione, prompt precedenti, roadmap visuali o dataset JSON rappresentino lo stato corrente. Verificare sempre branch, commit, file e workflow reali prima di proporre o applicare modifiche.

## 2. Sequenza obbligatoria di lettura

1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-09-02.md` — handover corrente
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-02.md` — delta tecnico corrente
4. `docs/project/HANDOVER_2026-09-01.md` — record storico immediatamente precedente
5. `docs/project/HANDOVER_2026-08-30.md` — record storico
6. `docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md`
7. `docs/project/REPOSITORY_KNOWLEDGE_MAP.md`
8. `docs/project/BACKLOG.md`
9. `docs/project/FUNCTIONAL_ROADMAP_EXPANSION_2026-08-30.md`
10. `.github/roadmap/roadmap-source.json`
11. `docs/project/TECHNICAL_DEBT.md`
12. `docs/project/DECISION_LOG.md`
13. `docs/project/DEVELOPMENT_WORKFLOW.md`
14. `docs/project/CODING_STANDARDS.md`
15. `docs/project/RELEASE_PLAYBOOK.md`
16. `docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md`
17. Architecture Package, ADR, review, evidence e componenti direttamente coinvolti nell'attività.

I documenti di contesto datati possono contenere fotografie storiche. Per lo stato operativo corrente applicare sempre repository truth, evidence, handover e technical baseline più recenti; non reinterpretare una vecchia sezione `planned/next` come stato corrente.

## 3. Verifica iniziale

Prima di modificare il repository: identificare branch e HEAD; verificare file/SHA interessati; cercare documenti e identificativi sovrapposti; distinguere source primaria e projection; controllare backlog, technical debt e decisioni; verificare workflow e Pages; segnalare divergenze prima di scrivere.

## 4. Gerarchia delle fonti

1. Architecture Package, ADR, capability e standard approvati;
2. assessment ARB, validation record, execution evidence e gate;
3. roadmap autorevole e `.github/roadmap/roadmap-source.json` per la projection operativa;
4. backlog e documenti di planning approvati;
5. handover corrente e current technical baseline per la continuità operativa;
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
- collector EAGLE leggeri; analytics/AI fuori dal computer operativo quando possibile;
- AI spiegabile con evidence, confidence e distinzione observation/inference/recommendation;
- post-processing provenance machine-readable e local-first;
- AI PixInsight inizialmente `ADVISORY ONLY`;
- nessuna affermazione di build, test, commit, deploy o acceptance senza verifica reale.

## 6. Processo di sviluppo

Procedere una milestone alla volta: repository truth -> architettura -> implementazione -> test -> commit/push -> workflow -> Pages -> registri/governance. Non iniziare una milestone successiva se la baseline precedente presenta drift o quality gate rosso non spiegato e registrato.

Ogni modifica che cambia comportamento osservabile del portale, pipeline scientifica o stato di una capability deve includere un controllo esplicito di allineamento documentale e handover prima della closure.

## 7. Stato di continuità corrente — 02/09/2026

- BKL-007–BKL-013 e BKL-018–BKL-029 risultano `Done` secondo backlog/evidence correnti; AP-014 resta accepted sulla propria evidence storica.
- BKL-029 SQM Sky Quality Telemetry & Scientific History è `Done`; SQM è scientific telemetry/history, mai Safety Authority.
- La sessione reale `2026-09-01_2026-09-02` / M 27 è stata promossa e rianalizzata con evidence SQM governata: min `8.91`, mean `17.738`, max `20.92`, median `18.755`, valid samples `1306`, temporal coverage `0.9886`, quality `AVAILABLE`.
- `DigitalStarGate.Reporting 1.0.7` è la baseline runtime EAGLE corrente. Merge repository Reporting: `c5f1bd617eb7b256372f0257a3cf22b60d503d3b`.
- La 1.0.7 materializza automaticamente `raw/sqm/sqm-history.ndjson` e `raw/sqm/sqm-summary.json` prima del manifest, leggendo per default `%LOCALAPPDATA%\DigitalStarGate\telemetry\sqm-history.ndjson`.
- La 1.0.7 stabilizza `Publish-DSGSession`: sul runtime EAGLE il test ha restituito un solo `System.Management.Automation.PSCustomObject`, `COUNT=1`, con `Committed=False` e `Pushed=False` nel test non distruttivo.
- Il runtime clone EAGLE è stato verificato su `main`, clean e `HEAD...origin/main = 0 0` dopo la validazione.
- L'evidence OAT AP-014 con Reporting 1.0.6 resta storicamente valida e non va riscritta; per operazioni correnti usare la baseline 1.0.7.
- Restano due hardening item separati: restore-to-main garantito del launcher in caso di eccezione e ripristino/estensione della copertura storica della Reporting quality gate.
- **BKL-030 EAGLE Health & Reliability è la prossima capability `Ready`.** Primo passo: D1/D2 source discovery read-only su `EAGLE30154` con `scripts/telemetry/Inspect-EagleHealthSources.ps1`; nessun health signal è Safety Authority e nessuna soglia va inventata.
- BKL-015 Knowledge Graph segue BKL-030 e deve tenere conto di BKL-044 Knowledge/AI Evidence Contract.
- BKL-045 PixInsight Workflow Provenance e BKL-046 AI Post-Processing Assistant restano successivi alle foundation knowledge/evidence; AI inizialmente advisory/human-controlled.

### Sequenza governata di riferimento

`BKL-029 Done -> Reporting 1.0.7 runtime remediation validated -> BKL-030 Ready -> BKL-015 -> BKL-044 -> BKL-035 -> BKL-040 -> BKL-037 -> BKL-038 -> BKL-039 -> BKL-041 -> BKL-045 -> BKL-046 -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

Lo stato deve essere nuovamente verificato nel repository a ogni utilizzo di questo file.

## 8. Quality-gate handover

La baseline corrente di continuità è `docs/project/HANDOVER_2026-09-02.md`; il delta tecnico corrente è `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-02.md`.

Per la remediation Reporting 1.0.7, i gate del repository `DigitalStarGate.Reporting` sul PR head `a76faf8ca173204427ee638a6fde6a5edf05c3f3` sono risultati `SUCCESS`: Reporting Quality Gate #22, Runtime Hardening Regression #6 e NO_SESSION Regression #8; la PR #4 è stata mergiata come `c5f1bd617eb7b256372f0257a3cf22b60d503d3b`.

La validazione runtime EAGLE successiva ha verificato modulo 1.0.7, exporter SQM reale e contratto `Publish-DSGSession` singolo-oggetto. Queste verifiche non sostituiscono repository truth: una nuova sessione deve verificare commit e workflow successivi.

## 9. Output richiesto a ogni intervento

Riportare file modificati, commit SHA, validazioni eseguite/non eseguite, rischi residui e prossimo passo in ordine di dipendenza. Se l'intervento cambia capability, pipeline o comportamento pubblicato, riportare anche l'esito del controllo di sincronizzazione handover/documentazione.

## 10. Divieti

Non inventare branch/file/commit/test/workflow/stati; non marcare approved senza evidence; non promuovere una projection a source primaria; non aggirare interlock/safe state/four-eyes/controller locale; non introdurre debito tecnico senza registrarlo; non inferire SQM, mains, safety o health da proxy non governati.

## 11. Punto di partenza operativo

Aprire `docs/project/HANDOVER_2026-09-02.md` e `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-02.md`, verificare HEAD e workflow correnti, quindi controllare che il runtime EAGLE resti su `main`, clean e sincronizzato prima di qualunque session producer operation. In assenza di drift/gate rossi, il prossimo lavoro di capability è **BKL-030 D1/D2 EAGLE Health source discovery**, mantenendo il collector discovery-only/read-only fino alla classificazione delle source e alla conferma del boundary.
