# Development Workflow

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-DEV-001 |
| Versione | 2.0 |
| Stato | Active |
| Data efficacia | 05/08/2026 |

## 1. Scopo

Definire il flusso obbligatorio per ogni modifica al Digital StarGate Enterprise Portal e stabilire il modello di esecuzione autonoma delle milestone concordate.

## 2. Principio operativo

Quando una milestone è presente nella roadmap approvata e non richiede deviazioni architetturali, il Chief Architect procede autonomamente fino alla sua conclusione.

Il ciclo comprende, senza ulteriori richieste di approvazione intermedie:

1. verifica repository truth;
2. progettazione della modifica;
3. implementazione;
4. aggiornamento documentale e di governance;
5. commit e push;
6. controllo GitHub Actions;
7. verifica GitHub Pages o artifact applicabile;
8. correzione degli errori coerenti con lo scope;
9. acceptance tecnica;
10. chiusura formale della milestone.

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

### 4.1 Avvio

- leggere `AI_BOOTSTRAP.md`;
- verificare branch, HEAD e workflow;
- leggere Context, Knowledge Map, Backlog, Technical Debt e Decision Log;
- identificare fonti autorevoli, file, componenti e acceptance criteria;
- marcare la milestone `In Progress` nei registri applicabili.

### 4.2 Design

- descrivere current state e target state;
- confermare responsabilità e boundary;
- individuare dipendenze, rischi, rollback e test;
- evitare duplicazioni e soluzioni temporanee non registrate.

### 4.3 Implementazione

- procedere in commit coerenti e incrementali;
- usare GitHub direttamente;
- per file grandi preferire Git Database API: blob, tree, commit e ref;
- aggiornare codice, configurazione e documentazione nello stesso package quando necessario;
- non distribuire una responsabilità in più moduli.

### 4.4 Validazione

Eseguire tutti i controlli applicabili:

```bash
dotnet restore DigitalStarGate.sln
dotnet build DigitalStarGate.sln --configuration Release --no-restore
dotnet test DigitalStarGate.sln --configuration Release --no-build
dotnet format DigitalStarGate.sln --verify-no-changes --no-restore
mkdocs build --strict
```

Per modifiche al portale verificare inoltre:

- rendering Home e pagine interne;
- light/dark e persistenza;
- refresh diretto;
- Instant Navigation;
- desktop e tablet;
- tastiera e focus;
- console e caricamento asset;
- artifact GitHub Pages.

### 4.5 Correzione autonoma

Se CI, Pages o acceptance rilevano errori entro lo scope approvato:

- diagnosticare il primo errore reale;
- applicare il fix minimo coerente;
- ripetere build, deploy e verifica;
- documentare regressioni, rollback e debito tecnico;
- continuare fino a esito positivo o fino all'emersione di una condizione che richiede approvazione.

### 4.6 Chiusura

Una milestone è chiusa solo quando:

- acceptance criteria soddisfatti;
- CI applicabile verde;
- deployment verificato;
- test manuale richiesto completato;
- Context, Backlog, Technical Debt, Decision Log e baseline aggiornati;
- commit finali e stato residuo comunicati.

## 5. Comunicazione

Durante l'esecuzione vengono comunicati soltanto:

- avanzamenti significativi;
- errori o regressioni rilevanti;
- blocchi che richiedono decisione;
- conclusione della milestone.

Non vengono richieste approvazioni per attività già previste dalla roadmap.

## 6. Gestione GitHub

Il repository è gestito direttamente tramite il connettore GitHub.

Per modifiche semplici si usano le Contents API. Per file grandi o change set controllati si usano:

```text
create_blob -> create_tree -> create_commit -> update_ref
```

`update_ref` deve essere fast-forward. `force=true` richiede sempre approvazione esplicita.

## 7. Definition of Done

La milestone è completata quando implementazione, validazione, pubblicazione, governance e comunicazione finale sono tutte concluse. Un singolo commit o una build positiva non costituiscono da soli la chiusura.