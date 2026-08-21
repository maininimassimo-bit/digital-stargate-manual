# Digital StarGate AI Bootstrap

Questo file è il punto di ingresso obbligatorio per ogni nuova sessione di lavoro, collaboratore o assistente AI che intervenga sul repository `maininimassimo-bit/digital-stargate-manual`.

## 1. Regola fondamentale

Il repository GitHub è l'unica fonte autorevole.

Non assumere che memoria della conversazione, prompt precedenti, roadmap visuali o dataset JSON rappresentino lo stato corrente. Verificare sempre branch, commit, file e workflow reali prima di proporre o applicare modifiche.

## 2. Sequenza obbligatoria di lettura

1. `docs/project/ENTERPRISE_ARCHITECTURE_CONTEXT.md`
2. `docs/project/REPOSITORY_KNOWLEDGE_MAP.md`
3. `docs/project/BACKLOG.md`
4. `docs/project/TECHNICAL_DEBT.md`
5. `docs/project/DECISION_LOG.md`
6. `docs/project/DEVELOPMENT_WORKFLOW.md`
7. `docs/project/CODING_STANDARDS.md`
8. `docs/project/RELEASE_PLAYBOOK.md`
9. `docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md`
10. Architecture Package, ADR, review, evidence e componenti direttamente coinvolti nell'attività.

## 3. Verifica iniziale

Prima di modificare il repository:

- identificare il branch di destinazione;
- leggere il commit HEAD corrente;
- verificare file e SHA interessati;
- cercare documenti, componenti e identificativi sovrapposti;
- distinguere fonte primaria e proiezione;
- controllare backlog, debito tecnico e decisioni correlate;
- verificare lo stato reale dei workflow e del portale pubblicato quando rilevante;
- segnalare divergenze prima di scrivere.

## 4. Gerarchia delle fonti

Ordine di prevalenza:

1. Architecture Package, ADR, capability e standard approvati;
2. assessment ARB, validation record, execution evidence e gate;
3. roadmap autorevole `AMP-002`;
4. release note e commit effettivamente pubblicati;
5. contratti machine-readable versionati;
6. dataset JSON e dashboard come proiezioni;
7. Project Governance Center;
8. conversazioni e prompt.

## 5. Principi non negoziabili

- repository as source of truth;
- design enterprise e UI/UX coerente;
- componenti modulari;
- responsabilità singola;
- nessuna duplicazione di logica, dati o stili;
- JavaScript e CSS separati per componente;
- Scientific Data Engine come access layer condiviso per i dati scientifici;
- dataset JSON come proiezioni, mai come fonte primaria;
- Domain indipendente da framework e Infrastructure;
- safety e security prevalgono sulla continuità;
- nessun comando diretto dal portale agli apparati;
- Instant Navigation e inizializzazione idempotente;
- nessuna affermazione di build, test, commit, deploy o acceptance senza verifica reale.

## 6. Processo di sviluppo

Procedere una milestone alla volta:

1. repository truth;
2. architettura della modifica;
3. mockup, quando necessario;
4. implementazione;
5. test e validazione;
6. commit;
7. push;
8. verifica workflow;
9. verifica GitHub Pages;
10. aggiornamento context, backlog, decision log e technical debt.

## 7. Distinzione dei registri

- nuova decisione strutturale: ADR;
- decisione operativa reversibile: `DECISION_LOG.md`;
- compromesso con costo futuro: `TECHNICAL_DEBT.md`;
- lavoro pianificato: `BACKLOG.md`;
- variazione della roadmap architetturale: prima `AMP-002`, poi le proiezioni;
- difetto operativo o software: issue/bug tracking.

## 8. Stato di continuità corrente — 21/08/2026

- Governance Foundation documentale completata e integrata nella navigazione MkDocs;
- `AI_BOOTSTRAP.md` è il bootstrap canonico;
- Enterprise Theme Framework completato e accettato; `dsg-theme-manager.js` è l'authority del tema e supporta `light`, `dark` e `system`;
- AP-012 conserva evidence residue reali su `ARB-012-C04`: provisioning isolato, account non-production e PRV/ENV/W07 restano da completare;
- AP-013 è formalmente `Accepted`; AP-013B OneDrive-mediated COPY_ONLY è `Passed — Limited Production` con scheduler/runtime evidence e vincoli no-delete/no-overwrite;
- AP-014 è formalmente `Accepted` e integrato in `main`;
- Observatory Status realtime è operativo per le source integrate; Power e Network restano `UNKNOWN` finché BKL-027 non identifica sorgenti read-only verificabili e BKL-028 non le integra;
- AP-015 / Knowledge Graph resta pianificato dopo le dipendenze P1 correnti.

Lo stato deve essere nuovamente verificato nel repository a ogni utilizzo di questo file.

## 9. Output richiesto a ogni intervento

Al termine riportare sempre:

- file creati, aggiornati o ritirati;
- commit SHA effettivi;
- validazioni eseguite;
- validazioni non eseguite;
- rischi e incongruenze residue;
- prossimo passo in ordine di dipendenza.

## 10. Divieti

Non:

- inventare branch, file, commit, test, workflow o stati;
- marcare come approvato ciò che non dispone di approvazione/evidence;
- promuovere una proiezione a fonte primaria;
- distribuire la stessa responsabilità in più moduli;
- aggirare interlock, safe state, four-eyes o controller locale;
- modificare documenti autorevoli solo per allinearli a una dashboard incoerente;
- introdurre debito tecnico senza registrarlo.

## 11. Punto di partenza operativo

Dopo aver completato le verifiche sopra, aprire:

`docs/project/index.md`

ed eseguire la prima voce `Ready` del backlog compatibile con la richiesta dell'utente e con le dipendenze correnti.