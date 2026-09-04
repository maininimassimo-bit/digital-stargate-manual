# Digital StarGate AI Bootstrap

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro, collaboratore o assistente AI che intervenga sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale

Il repository GitHub è l'unica fonte autorevole. Non assumere che memoria della conversazione, prompt precedenti, roadmap visuali o dataset JSON rappresentino lo stato corrente. Verificare sempre branch, commit, file e workflow reali prima di proporre o applicare modifiche.

## 2. Sequenza obbligatoria di lettura

1. `AI_BOOTSTRAP.md`
2. `docs/project/HANDOVER_2026-09-04.md` — handover corrente
3. `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-04.md` — delta tecnico corrente
4. `docs/project/HANDOVER_2026-09-03.md` — record storico immediatamente precedente
5. `docs/project/HANDOVER_2026-09-02.md` — record storico
6. `docs/project/HANDOVER_2026-09-01.md` — record storico
7. `docs/project/HANDOVER_2026-08-30.md` — record storico
8. `docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md`
9. `docs/project/REPOSITORY_KNOWLEDGE_MAP.md`
10. `docs/project/BACKLOG.md`
11. `docs/project/FUNCTIONAL_ROADMAP_EXPANSION_2026-08-30.md`
12. `.github/roadmap/roadmap-source.json`
13. `docs/project/TECHNICAL_DEBT.md`
14. `docs/project/DECISION_LOG.md`
15. `docs/project/DEVELOPMENT_WORKFLOW.md`
16. `docs/project/CODING_STANDARDS.md`
17. `docs/project/RELEASE_PLAYBOOK.md`
18. `docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md`
19. Architecture Package, ADR, review, evidence e componenti direttamente coinvolti nell'attività.

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

## 7. Stato di continuità corrente — 04/09/2026

- `DigitalStarGate.Reporting 1.0.8` resta la baseline runtime EAGLE corrente; exact NINA/PHD2 evidence selection, SQM packaging e fix PowerShell 5.1 restano invariati.
- La sessione `2026-09-03_2026-09-04` è stata promossa; il `main` verificato prima del package documentale è `ffc2e2cc719336ea6e4134884017a94f811ce08f` (`chore(analytics): refresh 2026-09-03_2026-09-04 projections`).
- BKL-030 EAGLE Health & Reliability è `In Progress`; G1–G5 sono completati e il prossimo gate della capability è G6 history/persistence.
- Il G5 Runtime OAT ha verificato collector read-only FAST/MEDIUM/SLOW_ON_CHANGE. Event Log empty-window è stato corretto; configuration drift resta `BASELINE_NOT_APPROVED`.
- C: è stato osservato durante G5 con 672,124,928 byte liberi / 0.301%. È evidence di capacity risk, non una severity derivata: nessun threshold numerico è approvato.
- AP-013B raw transport resta la baseline `COPY_ONLY` e il rollback comportamentale corrente.
- Il 04/09 un incidente OneDrive ha prodotto divergenza EAGLE 445/445 vs PC 426/426. Il gap di 19 coppie M 27 `0123–0141` è stato recuperato dopo troubleshooting/reset controllato OneDrive; PC transport ha raggiunto 445/445 e tutti i 19 XISF sono stati verificati in `F:\Astrofotografia`.
- L'importer finale ha osservato 445 READY, tutti già importati, con zero failure e zero cancellazioni.
- È approvata la **progettazione** di AP-013C Verified Transport Cleanup / convergence monitoring. Non è ancora autorizzata cancellazione produttiva.
- AP-013C deve essere fail-closed: evidence incompleta/UNKNOWN => no-delete. La sola presenza nel transport EAGLE non dimostra convergenza end-to-end.
- Files On-Demand non sostituisce il lifecycle governato Digital StarGate e non va usato con `Always keep on this device` indiscriminato sul transport EAGLE.
- Il restore-to-main garantito del launcher e la riconciliazione della Reporting quality gate storica restano debiti separati già registrati.

### Sequenza governata di riferimento

`BKL-030 G1-G5 complete -> AP-013C architecture/design + dry-run/OAT -> BKL-030 G6 history -> BKL-015 -> BKL-044 -> BKL-035 -> BKL-040 -> BKL-037 -> BKL-038 -> BKL-039 -> BKL-041 -> BKL-045 -> BKL-046 -> BKL-031 -> BKL-032 -> BKL-036 -> BKL-033 -> BKL-034 -> BKL-042 -> BKL-043 -> BKL-014/AP-015`.

Lo stato deve essere nuovamente verificato nel repository a ogni utilizzo di questo file.

## 8. Quality-gate handover

La baseline corrente di continuità è `docs/project/HANDOVER_2026-09-04.md`; il delta tecnico corrente è `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-04.md`.

Le evidence Reporting 1.0.8 e BKL-030 G5 già registrate restano valide per ciò che hanno effettivamente testato. L'incidente/recovery OneDrive è registrato separatamente in `docs/architecture/evidence/AP-013B-OneDrive-Transport-Incident-Recovery-2026-09-04.md` e non modifica retroattivamente AP-013B.

Nessun test AP-013C o cleanup produttivo può essere dichiarato finché il relativo Architecture Package, implementazione e OAT non esistono realmente.

## 9. Output richiesto a ogni intervento

Riportare file modificati, commit SHA, validazioni eseguite/non eseguite, rischi residui e prossimo passo in ordine di dipendenza. Se l'intervento cambia capability, pipeline o comportamento pubblicato, riportare anche l'esito del controllo di sincronizzazione handover/documentazione.

## 10. Divieti

Non inventare branch/file/commit/test/workflow/stati; non marcare approved senza evidence; non promuovere una projection a source primaria; non aggirare interlock/safe state/four-eyes/controller locale; non introdurre debito tecnico senza registrarlo; non inferire SQM, mains, safety o health da proxy non governati; non cancellare raw scientifici sulla base della sola export completion.

## 11. Punto di partenza operativo

Aprire `docs/project/HANDOVER_2026-09-04.md` e `docs/project/CURRENT_TECHNICAL_BASELINE_2026-09-04.md`, verificare HEAD e workflow correnti e riconfermare lo stato runtime EAGLE/PC prima di operazioni sul transport. Il prossimo package governato è AP-013C Verified Transport Cleanup / convergence monitoring; BKL-030 G6 resta il successivo gate Health & Reliability dopo la chiusura del delta transport, salvo diversa priorità approvata.
