# Validazione e quality gate del Warehouse

## Scopo

La validazione impedisce che dataset incompleti, incoerenti o non leggibili
vengano pubblicati come fonte affidabile per Reporting e Dashboard.

Il controllo deve essere applicato sia agli input provenienti dagli Analytics
sia agli output prodotti dal Warehouse.

## Principi

1. Nessun dataset è considerato valido solo perché il file esiste.
2. Gli errori di schema sono bloccanti.
3. I tipi di dato devono essere verificati.
4. Gli identificatori devono essere coerenti.
5. I metadata devono descrivere il contenuto effettivamente prodotto.
6. I test automatici devono coprire i flussi principali e gli errori attesi.
7. La validazione deve essere riproducibile in locale e in CI.

## Quality gate sugli input

Prima della costruzione del Warehouse devono essere verificati:

- presenza dei dataset Analytics richiesti;
- leggibilità dei file;
- intestazioni;
- colonne obbligatorie;
- compatibilità della versione;
- tipi di dato;
- timestamp;
- identificatori;
- valori ammessi;
- duplicati;
- completezza minima;
- metadata Analytics.

Un input non valido non deve essere corretto silenziosamente dal Warehouse.

Le correzioni semantiche appartengono generalmente agli Analytics.

## Quality gate sugli output

Dopo la generazione devono essere verificati:

- esistenza dei file Parquet attesi;
- leggibilità tramite libreria Parquet;
- schema risultante;
- numero di righe;
- tipi fisici e logici;
- chiavi duplicate;
- valori null non ammessi;
- intervalli;
- coerenza tra dataset;
- metadata;
- stato complessivo della build.

## Controlli strutturali

### File richiesti

Devono essere presenti tutti i dataset previsti dalla build:

```text
sessions.parquet
targets.parquet
equipment.parquet
quality.parquet
weather.parquet
```

Un dataset opzionalmente vuoto deve comunque rispettare il contratto stabilito:
file valido con schema corretto oppure assenza formalmente ammessa.

### Colonne obbligatorie

Ogni dataset deve dichiarare un insieme minimo di colonne.

La perdita o rinomina di una colonna obbligatoria è un errore bloccante.

### Tipi di dato

Devono essere rilevati almeno:

- numeri memorizzati come testo;
- timestamp non interpretabili;
- booleani espressi con valori non previsti;
- conteggi negativi;
- durate non numeriche;
- unità miste nella stessa colonna.

## Controlli semantici

### Identificatori e relazioni

Devono essere verificate:

- unicità delle chiavi previste;
- esistenza delle sessioni referenziate;
- coerenza tra target e sessioni;
- coerenza tra quality e acquisizioni;
- associazione temporale dei dati meteo;
- normalizzazione delle configurazioni strumentali.

### Intervalli

Esempi di controlli:

| Campo | Controllo indicativo |
|---|---|
| Percentuale | Da 0 a 100 |
| Conteggio frame | Maggiore o uguale a 0 |
| Durata | Maggiore o uguale a 0 |
| Umidità | Da 0 a 100 |
| Esposizione | Maggiore di 0 quando presente |
| Timestamp fine | Non precedente al timestamp iniziale |

Gli intervalli effettivi devono essere definiti nel codice e nei relativi test.

### Timestamp e timezone

I timestamp devono:

- essere validi;
- usare un formato coerente;
- dichiarare la timezone o essere normalizzati;
- evitare commistioni non documentate tra ora locale e UTC;
- mantenere un ordinamento cronologico corretto.

## Metadata validation

I metadata devono corrispondere ai file prodotti.

Devono essere verificati:

- nome del dataset;
- numero di righe;
- versione dello schema;
- timestamp di generazione;
- stato;
- elenco delle colonne, se registrato;
- origine dei dati;
- identificativo della build.

Un metadata che indica `populated` con un file mancante o illeggibile deve
essere considerato non valido.

## Classificazione degli esiti

### `valid`

Tutti i controlli bloccanti sono superati.

### `valid_with_warnings`

I dataset sono utilizzabili, ma sono presenti anomalie non bloccanti
formalmente ammesse.

### `invalid`

Uno o più controlli bloccanti non sono superati.

### `not_built`

La build non è stata completata oppure non è stata eseguita.

## Test automatici

La suite dovrebbe comprendere:

- unit test dei validator;
- test dello schema;
- test dei metadata;
- test con input minimo valido;
- test con colonne mancanti;
- test con tipi errati;
- test con duplicati;
- test con timestamp non validi;
- test di integrazione end-to-end;
- test di leggibilità dei Parquet;
- test di regressione sui dataset campione.

## Esecuzione locale

La forma esatta dipende dalla struttura del repository. La procedura deve
comunque includere:

```powershell
python -m pytest
```

oppure il comando specifico definito dal progetto.

Prima di documentare un comando come ufficiale, deve essere verificato contro
i file reali del repository, per esempio `pyproject.toml`, `requirements.txt`,
script di build o workflow GitHub Actions.

## CI/CD

In GitHub Actions la pipeline dovrebbe:

1. installare le dipendenze;
2. eseguire i test;
3. validare gli input campione;
4. costruire il Warehouse;
5. validare i Parquet;
6. verificare i metadata;
7. eseguire `mkdocs build --strict`;
8. pubblicare solo in caso di esito positivo.

## Gestione dei warning

I warning devono essere:

- espliciti;
- tracciabili;
- associati al dataset;
- riportati nei metadata o nei log;
- non utilizzati per nascondere errori di schema.

L'aumento progressivo dei warning deve essere monitorato come possibile
degrado della qualità.

## Criteri di accettazione

Una build Warehouse è accettabile quando:

- tutti i dataset previsti sono prodotti;
- i file sono leggibili;
- lo schema è valido;
- le relazioni principali sono coerenti;
- i metadata corrispondono agli output;
- i test automatici sono superati;
- non risultano errori bloccanti;
- la documentazione MkDocs viene costruita in modalità strict.
