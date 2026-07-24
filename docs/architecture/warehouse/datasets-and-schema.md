# Dataset e schema del Warehouse

## Scopo

Questa pagina descrive i dataset approvati del Warehouse e le regole generali
che ne governano lo schema.

Il dettaglio puntuale delle colonne deve essere mantenuto allineato al codice
e agli schema file presenti nel repository. Questa pagina definisce il
contratto funzionale e non sostituisce gli schema eseguibili.

## Dataset approvati

Il Warehouse comprende cinque dataset principali:

```text
sessions.parquet
targets.parquet
equipment.parquet
quality.parquet
weather.parquet
```

## `sessions.parquet`

### Finalità

Rappresenta le sessioni osservative consolidate.

### Contenuti logici

Può comprendere:

- identificativo della sessione;
- data e ora di inizio;
- data e ora di fine;
- durata;
- stato della sessione;
- numero di target;
- numero di acquisizioni;
- tempo totale di integrazione;
- esito complessivo;
- indicatori sintetici di qualità;
- riferimenti ai metadata.

### Chiave logica

La chiave deve identificare una sessione in modo stabile e non ambiguo.

L'identificatore non deve dipendere esclusivamente dal nome visualizzato nel
portale.

## `targets.parquet`

### Finalità

Rappresenta i target acquisiti nelle sessioni osservative.

### Contenuti logici

Può comprendere:

- identificativo della sessione;
- identificativo o nome normalizzato del target;
- coordinate;
- filtro;
- numero di frame;
- durata delle esposizioni;
- tempo totale di integrazione;
- gain e offset, quando disponibili;
- configurazione strumentale;
- indicatori aggregati;
- esito dell'acquisizione.

### Granularità

La granularità deve essere dichiarata nello schema.

Esempi possibili:

- una riga per target e sessione;
- una riga per target, sessione e filtro;
- una riga per target, sessione e configurazione.

I consumer non devono dedurre la granularità implicitamente.

## `equipment.parquet`

### Finalità

Descrive l'utilizzo delle configurazioni strumentali.

### Contenuti logici

Può comprendere:

- telescopio;
- montatura;
- camera;
- sistema di guida;
- filtro;
- focheggiatore;
- configurazione ottica;
- focale;
- rapporto focale;
- binning;
- numero di sessioni;
- tempo di utilizzo;
- indicatori prestazionali aggregati.

### Regola di normalizzazione

I nomi dell'attrezzatura devono essere normalizzati per evitare che varianti
testuali dello stesso dispositivo producano entità differenti.

## `quality.parquet`

### Finalità

Raccoglie gli indicatori di qualità derivati dalle sessioni e dalle
acquisizioni.

### Contenuti logici

Può comprendere:

- identificativo della sessione;
- target;
- filtro;
- HFR o FWHM, se disponibili;
- eccentricità;
- numero di stelle;
- scarto di guida;
- frame accettati;
- frame scartati;
- percentuale di scarto;
- indicatori sintetici;
- motivazioni di esclusione.

### Interpretazione

Gli indicatori devono mantenere unità di misura e significato univoci.

Quando un valore non è disponibile, deve essere rappresentato come valore
mancante e non sostituito automaticamente con zero.

## `weather.parquet`

### Finalità

Rappresenta le condizioni meteorologiche associate alle sessioni e allo stato
operativo dell'osservatorio.

### Contenuti logici

Può comprendere:

- timestamp;
- temperatura;
- umidità;
- pressione;
- velocità e direzione del vento;
- copertura nuvolosa;
- punto di rugiada;
- rischio di condensa;
- stato `safe` o `unsafe`;
- sorgente della misura;
- qualità o completezza della rilevazione.

### Requisiti temporali

I timestamp devono:

- essere espressi in un formato standard;
- includere o dichiarare la timezone;
- risultare ordinabili;
- poter essere associati a una sessione.

## Regole comuni dello schema

### Nomi delle colonne

I nomi delle colonne devono essere:

- stabili;
- descrittivi;
- senza ambiguità;
- coerenti tra i dataset;
- preferibilmente in `snake_case`;
- in inglese quando rappresentano identificatori tecnici.

### Tipi di dato

Devono essere usati tipi coerenti:

| Tipo logico | Utilizzo |
|---|---|
| String | Identificatori, nomi, categorie |
| Integer | Conteggi |
| Float | Misure e indicatori |
| Boolean | Stati binari |
| Timestamp | Date e orari |
| Duration | Durate, oppure numero con unità documentata |

Le misure non devono essere conservate come testo salvo casi eccezionali.

### Valori mancanti

La mancanza di un valore deve essere distinta da:

- valore zero;
- stringa vuota;
- stato negativo;
- errore di acquisizione.

### Unità di misura

Le unità devono essere documentate nello schema o nel nome della colonna.

Esempi:

```text
exposure_seconds
integration_minutes
temperature_celsius
wind_speed_kmh
fwhm_arcsec
```

### Identificatori

Gli identificatori devono essere:

- stabili;
- riproducibili;
- non dipendenti dall'ordine delle righe;
- adatti alle join;
- documentati.

## Versionamento dello schema

Ogni modifica incompatibile deve comportare:

1. aggiornamento della versione dello schema;
2. aggiornamento dei validator;
3. aggiornamento dei test;
4. aggiornamento della documentazione;
5. verifica dei consumer;
6. eventuale strategia di migrazione.

L'aggiunta di una colonna opzionale può essere compatibile, ma deve comunque
essere documentata.

## Relazioni logiche

```text
sessions
   |
   +----< targets
   |
   +----< quality
   |
   +----< weather
   |
   +---- equipment
```

La relazione reale deve essere implementata tramite identificatori coerenti e
non tramite confronti fragili su descrizioni libere.

## Metadata di dataset

Per ciascun dataset è raccomandato registrare:

- nome;
- versione dello schema;
- data della build;
- numero di righe;
- elenco delle colonne;
- tipi;
- input di origine;
- hash o identificativo della build;
- esito della validazione;
- eventuali warning.

## Compatibilità

I consumer devono dipendere dal contratto dello schema, non dalla posizione
fisica delle colonne o da dettagli accidentali della generazione.

Una modifica allo schema deve essere considerata completata solo dopo la
verifica di Reporting, Dashboard e degli altri consumer.
