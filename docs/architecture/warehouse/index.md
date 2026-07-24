# Architettura del Warehouse

## Scopo

Il **Warehouse Engine** costituisce il livello dati persistente e validato della
piattaforma Digital StarGate.

Il suo compito è trasformare i dataset prodotti dagli Analytics in strutture
stabili, tipizzate e adatte all'utilizzo da parte di Reporting, Dashboard e
futuri servizi di intelligenza artificiale.

## Confine architetturale

Il Warehouse legge esclusivamente dataset già elaborati e validati dagli
Analytics.

Non deve analizzare direttamente:

- log N.I.N.A.;
- immagini astronomiche;
- manifest di sessione;
- file operativi grezzi dell'osservatorio.

Questa separazione evita duplicazioni della logica di parsing e garantisce che
tutti i componenti successivi utilizzino la stessa interpretazione dei dati.

## Flusso logico

```text
Osservatorio e N.I.N.A.
          |
          v
Analytics Engine
          |
          v
Dataset CSV validati
          |
          v
Warehouse Engine
          |
          +-- schema logico
          +-- metadata e lineage
          +-- validazioni Warehouse
          +-- dataset Parquet
          |
          +-------------------+
          |                   |
          v                   v
Reporting Engine          Dashboard
          \                   /
           \                 /
            v               v
          AI Observatory Assistant
```

## Dataset approvati

Il Warehouse produce attualmente i seguenti dataset:

| Dataset | Finalità |
|---|---|
| `sessions.parquet` | Dati aggregati delle sessioni osservative |
| `targets.parquet` | Dati di acquisizione per target e configurazione |
| `equipment.parquet` | Utilizzo e prestazioni delle configurazioni strumentali |
| `quality.parquet` | Indicatori aggregati di qualità delle immagini |
| `weather.parquet` | Dati meteorologici e condizioni di sicurezza |

## Controlli principali

Il processo di costruzione applica controlli su:

- presenza dei file sorgente;
- colonne obbligatorie;
- tipi numerici;
- timestamp ISO 8601 e timezone;
- valori booleani;
- intervalli ammessi;
- chiavi primarie duplicate;
- coerenza dello schema;
- leggibilità dei file Parquet;
- corrispondenza tra metadata e numero di righe.

## Contratto con i componenti consumer

Reporting, Dashboard e AI Observatory Assistant devono consumare:

- i dataset Warehouse;
- oppure una futura interfaccia di interrogazione formalmente approvata.

Non devono rileggere i log N.I.N.A. né ricostruire autonomamente le trasformazioni
già eseguite dagli Analytics o dal Warehouse.

## Documenti di riferimento

- **ADR-003 - Warehouse Engine**: decisione architetturale.
- **EA-002 - Integrated Repository and Warehouse Assessment**: verifica dello
  stato effettivo dell'implementazione.
- **ADR-004 - Platform Architecture**: futuro documento di riferimento per
  l'intera piattaforma.

## Lingua e convenzioni

La documentazione della piattaforma è redatta principalmente in **italiano**.

Restano in inglese:

- nomi dei componenti software;
- nomi di file, dataset, classi e funzioni;
- comandi e frammenti di codice;
- stati standard degli ADR;
- termini tecnici consolidati quando la traduzione ridurrebbe la precisione.

## Evoluzione prevista

La sezione Warehouse sarà progressivamente articolata nelle seguenti pagine:

```text
architecture/warehouse/
├── index.md
├── data-flow.md
├── datasets-and-schema.md
├── validation-and-quality-gates.md
└── build-and-operations.md
```

Le pagine aggiuntive saranno inserite nella navigazione MkDocs solo dopo la loro
creazione e verifica.
