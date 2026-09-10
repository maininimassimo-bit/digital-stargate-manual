# Digital StarGate Portal Experience Architecture

| Campo | Valore |
|---|---|
| Identificativo | DSGP-SOL-001 |
| Versione | 1.0 |
| Stato | Proposed |
| Data | 10/09/2026 |
| Ambito | GitHub Pages, MkDocs Material, presentation boundary |
| Governing vision | DSGP-VIS-001 |
| Design system | DSG-UI-001 v2.0 |
| Release | UI 7.0 |

## 1. Purpose

Definire una struttura UX moderna e coerente per il portale Digital StarGate senza sostituire MkDocs, cambiare i percorsi pubblici o interrompere le proiezioni generate automaticamente.

## 2. Scope

Inclusi:

- shell visuale, navigazione desktop e mobile;
- homepage e hub di dominio;
- gerarchia informativa e percorsi di accesso;
- presentation contract delle proiezioni roadmap, scientifiche e realtime;
- progressive enhancement, responsive design e accessibilità;
- classificazione e ritiro dalle superfici primarie di contenuti stale o legacy;
- aggiornamento automatico della homepage dopo ogni sessione importata.

Esclusi:

- comandi verso EAGLE o dispositivi;
- modifiche a Safety Authority e interlock;
- nuovi algoritmi analytics o BKL-041;
- sostituzione di GitHub Pages/MkDocs;
- migrazione dei contratti dati accettati.

## 3. Architectural drivers

1. Ridurre il tempo necessario per raggiungere stato osservatorio, sessioni, analytics, operations e fonti autorevoli.
2. Separare con chiarezza realtime, snapshot versionati e documentazione normativa.
3. Eliminare stato editoriale duplicato quando esiste una projection governata.
4. Aggiornare automaticamente le superfici session-driven dopo ogni import scientifico.
5. Preservare URL, deep link, ricerca e contenuti storici.
6. Garantire lettura e navigazione da tastiera, mobile e zoom testo al 200%.

## 4. Current state

L'audit del 10/09/2026 ha rilevato:

- 15 gruppi di navigazione top-level nel menu Material, con forte frammentazione del modello mentale;
- una seconda navigazione desktop custom con molte voci, menu densi e link ancorati ad AP-013;
- homepage con stato statico AP-013, 3 sessioni e 31,83 h, divergente dalle fonti correnti;
- refresh_homepage.py presente ma non incluso nel publish set dell'import automatico;
- hub moderni esistenti ma fuori dalla navigazione primaria;
- viste Repository Intelligence/Analytics e Scientific Intelligence con contatori o milestone statici;
- Design System e Publication Guidelines ancora Draft dal 26/07/2026.

## 5. Target state

### 5.1 Information architecture

Home costituisce l'ingresso comune e conduce a sei percorsi: Osservatorio, Scienza e Analytics, Operations, Architettura, Governance e documentazione, Manuale tecnico.

| Percorso | Domanda primaria | Fonte |
|---|---|---|
| Osservatorio | Cosa sta succedendo ora? | Telemetria con freshness |
| Scienza e Analytics | Cosa è stato osservato e cosa mostrano i dati? | Proiezioni versionate |
| Operations | Come si opera o si recupera? | Runbook e procedure |
| Architettura | Perché il sistema è costruito così? | ADR, AP, contratti, review |
| Governance e documentazione | Qual è lo stato del programma e dove trovo una fonte? | Roadmap, backlog, indici |
| Manuale tecnico | Come sono fatti impianto, strumenti e software? | Capitoli tecnici |

### 5.2 First viewport

La homepage espone immediatamente:

- identità dell'osservatorio;
- accesso a Mission Control e catalogo sessioni;
- dichiarazione read-only e authority;
- snapshot corrente generato da roadmap e storico scientifico.

Nessun hero editoriale nasconde la superficie operativa.

### 5.3 Presentation model

Il flusso è: import sessione, generatori governati, JSON e pagine versionate, Portal UI, vista read-only.

La UI:

- consuma proiezioni, non log grezzi;
- usa cache no-store per dati che possono cambiare;
- mostra loading, empty, error, degraded e stale state;
- non ricostruisce dati assenti;
- non modifica authority o contratti dei producer.

## 6. Automatic update contract

Dopo ogni sessione COMPLETE promossa:

1. analyze-session-automatic.yml aggiorna storico, report e projection scientifiche già incluse nei governed_paths;
2. il commit generato pubblica catalogo, latest observation, report, Analytics e projection dipendenti;
3. deploy-pages.yml pubblica la nuova baseline;
4. la homepage legge roadmap, catalogo e latest observation direttamente a runtime con cache no-store;
5. loading e failure state non espongono valori storici plausibili.

Questa soluzione non richiede nuovi permessi, push o deploy nei workflow privilegiati esistenti. Il file homepage resta strutturale; sono le projection versionate già governate a cambiare dopo l'import.

| Superficie | Artefatto | Trigger sessione |
|---|---|---|
| Homepage | roadmap.json + catalogo + latest observation | hydration runtime dopo il deploy delle projection |
| Ultima osservazione | docs/data/realtime/latest-observation.json | rigenerazione e commit |
| Catalogo | docs/data/scientific-session-catalog.json | rigenerazione e commit |
| Session Comparison | docs/data/session-comparison-projection.json | rigenerazione e commit |
| Equipment Performance | projection BKL-039 | rigenerazione e commit |
| Report sessioni | docs/session-reports e indice | rigenerazione e commit |
| Analytics Center | dashboard e summary | rigenerazione e commit |

## 7. Component boundaries

- theme-tokens.css: colori, superfici, spaziatura, raggi, ombre e focus.
- portal-shell.css: tipografia, contenuto, tabelle, side navigation e pattern condivisi.
- enterprise-navigation.css: navigazione desktop e drawer.
- enterprise-home.css: sola homepage.
- page-enhancements.js: shell, ricerca, navigation state, breadcrumb e prev/next.
- homepage-effects.js: hydration dello snapshot homepage da projection governate.
- component JavaScript di dominio: rendering delle rispettive projection.

Non viene introdotta una nuova dipendenza frontend.

## 8. Accessibility and interaction rules

- un solo H1 per pagina;
- controlli con nome accessibile e focus visibile;
- drawer con aria-hidden, inert, Escape e ripristino del focus;
- testo principale almeno equivalente a 16 px nel contesto Material;
- stato mai affidato al solo colore;
- layout senza scroll orizzontale non intenzionale;
- rispetto di prefers-reduced-motion;
- contenuto statico utile anche se JavaScript non è disponibile.

## 9. Security, safety and operations

Il portale resta un presentation boundary read-only. Nessun codice UI accede direttamente a device, relay, driver o credenziali. UNKNOWN, STALE e dati mancanti rimangono espliciti. Gli interlock fisici locali restano indipendenti.

Il rollback consiste nel revert del package UI 7.0; dataset, import scientifico e dispositivi non vengono modificati.

## 10. Migration strategy

1. introdurre token e shell compatibili;
2. sostituire homepage e navigazione senza cambiare URL;
3. rendere dinamici o ritirare i duplicati statici;
4. collegare la homepage alla pipeline session-driven;
5. aggiornare Design System, publication rules, release note e nav;
6. validare su exact head e pubblicare tramite GitHub Pages.

## 11. Risks and trade-offs

| Rischio | Trattamento |
|---|---|
| Override CSS su pagine eterogenee | shell non invasiva e CSS proprietario per componente |
| JavaScript non disponibile | progressive enhancement e fallback testuale |
| Projection non disponibile | fail-closed con stato esplicito |
| Duplicazione dati in homepage | placeholder fail-closed e hydration dalle projection |
| Regressione Instant Navigation | inizializzazione idempotente con document$ |
| URL storici | nessun rename o delete dei percorsi pubblici |

## 12. Traceability

| Driver | Artefatto |
|---|---|
| Portal vision | docs/architecture/digital-stargate-portal-vision.md |
| Design rules | docs/ui/design-system.md |
| Freshness audit | docs/ui/content-freshness-audit-2026-09-10.md |
| Session pipeline | .github/workflows/analyze-session-automatic.yml |
| Homepage consumer | docs/javascripts/homepage-effects.js |
| Release | docs/releases/ui-7.0.md |
| Navigation | mkdocs.yml |

## 13. Acceptance criteria

- sei percorsi principali coerenti su desktop e mobile;
- homepage priva di package o KPI sessione hard-coded;
- homepage aggiornata dalle projection pubblicate dopo ogni sessione importata;
- nessun hub primario espone contatori legacy;
- JavaScript syntax check e regression test superati;
- mkdocs build --strict superato;
- ARB e Release Quality favorevoli su exact head;
- GitHub Pages post-merge SUCCESS.

## 14. Open issues

Nessuna evoluzione di stack, BFF, identity o command surface è autorizzata da questo incremento.
