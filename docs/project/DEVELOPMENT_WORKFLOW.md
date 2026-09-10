# Development Workflow

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-DEV-001 |
| Versione | 2.2 |
| Stato | Active |
| Data efficacia | 10/09/2026 |

## 1. Scopo

Definire il flusso obbligatorio per ogni modifica al Digital StarGate e stabilire il modello di esecuzione autonoma delle milestone concordate.

## 2. Principio operativo

Quando una milestone è presente nella roadmap approvata, le dipendenze sono soddisfatte e non richiede deviazioni architetturali, il Chief Architect procede autonomamente fino alla sua conclusione.

Il ciclo comprende, senza ulteriori richieste di approvazione intermedie:

1. verifica repository truth;
2. progettazione della modifica;
3. implementazione;
4. aggiornamento documentale e di governance;
5. commit e push;
6. controllo GitHub Actions sull'exact HEAD;
7. verifica GitHub Pages o artifact applicabile;
8. correzione degli errori coerenti con lo scope;
9. review/acceptance tecnica applicabile;
10. chiusura formale della milestone e post-merge verification.

L'utente riceve aggiornamenti di avanzamento e il rapporto conclusivo, ma non deve approvare ogni passaggio previsto.

## 3. Casi che richiedono approvazione esplicita

Il lavoro viene sospeso e sottoposto ad approvazione solo quando emerge almeno una delle seguenti condizioni:

- nuova integrazione non prevista dalla roadmap;
- modifica di principi architetturali, authority, boundary o invarianti;
- nuovo Architecture Package o ADR non già previsto;
- breaking change a contratti pubblici, API o dataset;
- variazione sostanziale di scope, priorità o sequencing;
- introduzione di una dipendenza tecnologica strutturale;
- impatto safety, security o accesso ad ambienti/dispositivi non autorizzati;
- rischio di perdita dati, rollback distruttivo o force update del branch;
- conflitto tra fonti autorevoli non risolvibile dal repository;
- costo operativo o debito tecnico significativamente superiore a quanto approvato.

Le correzioni tecniche necessarie a completare una milestone già approvata non richiedono nuova autorizzazione, purché restino entro i boundary concordati.

## 4. Workflow della milestone

### 4.1 Bootstrap e avvio

La sequenza normativa è posseduta da `AI_BOOTSTRAP.md`. Non duplicarla come authority autonoma in questo workflow.

Alla baseline 10/09/2026 l'avvio richiede, nell'ordine:

1. `AI_BOOTSTRAP.md`;
2. current handover indicato dal bootstrap;
3. current technical baseline indicata dal bootstrap;
4. Enterprise Architecture Context;
5. Repository Knowledge Map;
6. Backlog;
7. canonical roadmap source;
8. generated roadmap projection come projection, non authority;
9. Technical Debt;
10. Decision Log;
11. questo Development Workflow;
12. Coding Standards;
13. Release Playbook;
14. AMP-002;
15. Architecture Package, ADR, review, evidence e componenti direttamente coinvolti.

Dopo la lettura:

- verificare PR/branch, exact HEAD, diff e workflow reali;
- identificare authority e projection coinvolte;
- verificare dependency readiness;
- identificare acceptance criteria, rollback e validation matrix;
- marcare la milestone `In Progress` solo nella source governata applicabile e solo quando le entry condition sono soddisfatte.

I documenti handover/baseline precedenti restano snapshot storici e non devono prevalere sui successori correnti.

### 4.2 Design

- descrivere current state e target state;
- confermare responsabilità, source authority e projection boundary;
- individuare dipendenze, rischi, rollback e test;
- evitare duplicazioni e soluzioni temporanee non registrate;
- non introdurre threshold, authority o policy operative per inferenza.

### 4.3 Implementazione

- procedere in commit coerenti e incrementali;
- usare GitHub direttamente;
- per file grandi preferire Git Database API quando disponibile;
- aggiornare codice, configurazione e documentazione nello stesso package quando necessario;
- non distribuire una responsabilità in più moduli;
- preservare semantic type, lifecycle, source authority, Citation e Provenance nei consumer governati.

### 4.4 Validazione

Eseguire tutti i controlli applicabili:

```bash
dotnet restore DigitalStarGate.sln
dotnet build DigitalStarGate.sln --configuration Release --no-restore
dotnet test DigitalStarGate.sln --configuration Release --no-build
dotnet format DigitalStarGate.sln --verify-no-changes --no-restore
mkdocs build --strict
```

Verificare inoltre i workflow repository applicabili sull'exact HEAD. Un SUCCESS su un commit precedente non prova il commit corrente.

Per modifiche al portale verificare inoltre rendering, light/dark, refresh diretto, Instant Navigation, desktop/tablet, tastiera/focus, console e caricamento asset.

Per generated projection verificare sempre la source canonica e il generator/check applicabile; non correggere manualmente una projection quando deve essere rigenerata.

#### 4.4.1 Roadmap Projection Sync

La roadmap applica il seguente authority boundary:

- `.github/roadmap/roadmap-source.json` è la canonical source governata;
- `docs/data/roadmap.json` è una generated projection e non è authority autonoma;
- `.github/scripts/generate-roadmap.mjs` è l'unico generatore governato della projection;
- `.github/workflows/roadmap-projection-sync.yml` sincronizza automaticamente la projection quando cambia la canonical source.

Il workflow di sync deve:

1. attivarsi sulle modifiche della canonical roadmap source e poter essere eseguito manualmente per recovery;
2. eseguire il generator in modalità `--write`;
3. eseguire il controllo `--check` e la consistency governance prima del commit;
4. committare esclusivamente `docs/data/roadmap.json` quando il contenuto derivato cambia;
5. non modificare backlog, closure, ADR, architecture package o altre authority;
6. evitare loop: il commit della sola projection non modifica la canonical source e non riattiva il sync;
7. preservare i gate indipendenti Developer Foundation, Scientific Platform Governance e Pages;
8. in una PR, rilanciare i check PR che GitHub marca `action_required` dopo un commit generato dal bot, senza trasformare tale rilancio in acceptance automatica.

La sincronizzazione automatica non promuove package, non decide priorità e non modifica authority: materializza soltanto la projection deterministica della source già modificata e governata.

### 4.5 Correzione autonoma

Se CI, Pages o acceptance rilevano errori entro lo scope approvato:

- diagnosticare il primo errore reale;
- applicare il fix minimo coerente;
- ripetere build/deploy/verifica sull'exact HEAD aggiornato;
- documentare regressioni, rollback e debito tecnico;
- continuare fino a esito positivo o fino all'emersione di una condizione che richiede approvazione.

### 4.6 Governance review

Quando richiesta dal package:

1. completare remediation e quality gate exact-head;
2. eseguire Architecture Review Board indipendente senza correggere silenziosamente il package durante la review;
3. se ARB non approva, tornare alla remediation;
4. solo dopo ARB APPROVED eseguire Release Quality;
5. dichiarare READY FOR MERGE solo con evidence reale sull'exact HEAD.

### 4.7 Merge e post-merge

- usare expected-head protection quando possibile;
- registrare il merge SHA reale;
- verificare i workflow applicabili sul merge SHA in `main`;
- non dichiarare repository-integrated finché i post-merge gate richiesti non sono verificati;
- aggiornare continuity authority quando il package cambia lo stato corrente.

### 4.8 Chiusura

Una milestone è chiusa solo quando:

- acceptance criteria soddisfatti;
- CI applicabile verde sull'exact HEAD/merge SHA richiesto;
- deployment verificato quando applicabile;
- review indipendenti richieste completate;
- Context, Knowledge Map, Backlog, Technical Debt, Decision Log e baseline verificati/aggiornati secondo ownership;
- commit/merge finali e stato residuo comunicati.

## 5. Safety boundary

Per l'osservatorio, safety prevale sulla continuità. Portale, telemetry, replay, analytics e AI non sono Safety Authority salvo governance esplicita futura.

Nessun workflow di sviluppo autorizza implicitamente command path, bypass di interlock, automatic remediation o modifica della Safety Authority locale.

## 6. Comunicazione

Durante l'esecuzione vengono comunicati soltanto:

- avanzamenti significativi;
- exact HEAD e commit/merge SHA reali;
- workflow/run number e SUCCESS/FAILURE reali;
- errori o regressioni rilevanti;
- blocchi che richiedono decisione;
- necessità o non necessità di comandi PC/EAGLE;
- conclusione della milestone.

Non vengono richieste approvazioni per attività già previste dalla roadmap e comprese nei boundary approvati.

## 7. Gestione GitHub

Il repository è gestito direttamente tramite il connettore GitHub.

Le modifiche devono essere applicate al branch previsto dopo verifica dell'HEAD e del blob SHA del file. `force=true`, force push o update non fast-forward richiedono sempre approvazione esplicita.

## 8. Definition of Done

La milestone è completata quando implementazione, validazione, review applicabili, merge/post-merge, pubblicazione, governance e comunicazione finale sono tutte concluse. Un singolo commit o una build positiva non costituiscono da soli la chiusura.
