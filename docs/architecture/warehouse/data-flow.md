# Flusso dei dati del Warehouse

## Scopo

Questa pagina descrive il flusso dei dati dalla produzione operativa
dell'osservatorio fino ai componenti che consumano i dataset consolidati.

Il principio fondamentale è la separazione tra:

- acquisizione dei dati grezzi;
- interpretazione e validazione Analytics;
- persistenza e consolidamento Warehouse;
- utilizzo da parte di Reporting, Dashboard e servizi futuri.

## Flusso end-to-end

```text
Osservatorio
│
├── N.I.N.A.
├── dispositivi e driver
├── sensori meteo
├── stato della cupola
└── configurazioni strumentali
        │
        v
Acquisition Layer
        │
        ├── log operativi
        ├── manifest di sessione
        ├── dati meteo
        └── dati tecnici
        │
        v
Analytics Engine
        │
        ├── parsing
        ├── normalizzazione
        ├── calcolo degli indicatori
        ├── validazione
        └── generazione dei metadata
        │
        v
Dataset Analytics validati
        │
        v
Warehouse Engine
        │
        ├── applicazione dello schema logico
        ├── controlli di consistenza
        ├── consolidamento
        ├── generazione dei dataset Parquet
        └── pubblicazione dei metadata Warehouse
        │
        +----------------------+----------------------+
        |                      |                      |
        v                      v                      v
Reporting Engine           Dashboard          Servizi futuri
                                                    |
                                                    v
                                      AI Observatory Assistant
```

## Responsabilità dei livelli

### Acquisition Layer

L'Acquisition Layer raccoglie i dati prodotti dall'osservatorio.

Non deve imporre logiche analitiche complesse. Il suo obiettivo è conservare
e rendere disponibili le evidenze operative necessarie alle elaborazioni
successive.

### Analytics Engine

L'Analytics Engine è responsabile dell'interpretazione dei dati grezzi.

Le sue responsabilità comprendono:

- parsing dei dati sorgente;
- normalizzazione dei valori;
- associazione tra sessioni, target e configurazioni;
- calcolo degli indicatori;
- applicazione dei quality gate;
- produzione di dataset CSV validati;
- produzione dei metadata di esecuzione.

### Warehouse Engine

Il Warehouse Engine consuma esclusivamente gli output validati degli Analytics.

Non deve:

- rileggere i log N.I.N.A.;
- analizzare immagini astronomiche;
- interpretare direttamente i manifest;
- duplicare algoritmi già presenti negli Analytics;
- introdurre una seconda interpretazione dei dati sorgente.

Il Warehouse applica uno schema persistente e produce dataset adatti a
interrogazioni, reporting e visualizzazione.

### Consumer

Reporting, Dashboard e servizi di intelligenza artificiale devono utilizzare
i dataset Warehouse oppure future interfacce formalmente approvate.

I consumer non devono dipendere dalla struttura interna dei log o dalle
convenzioni dei file grezzi.

## Contratti di passaggio

### Contratto Analytics → Warehouse

Gli Analytics devono fornire:

- dataset completi e leggibili;
- intestazioni conformi allo schema atteso;
- valori normalizzati;
- timestamp coerenti;
- identificatori stabili;
- metadata di generazione;
- esito positivo delle validazioni previste.

In presenza di errori bloccanti, il Warehouse non deve pubblicare un risultato
come valido.

### Contratto Warehouse → Consumer

Il Warehouse deve fornire:

- file Parquet leggibili;
- schema coerente;
- dataset identificabili in modo univoco;
- metadata aggiornati;
- numero di righe verificabile;
- tracciabilità della build;
- compatibilità con i consumer approvati.

## Gestione degli errori

Gli errori sono classificati in tre categorie.

| Categoria | Descrizione | Comportamento |
|---|---|---|
| Bloccante | Dataset mancante, schema non valido, file illeggibile | Build interrotta |
| Qualità | Valori anomali, incompletezza, duplicati | Build interrotta o dataset marcato non valido |
| Informativo | Dataset vuoto consentito, campo opzionale assente | Warning documentato |

La classificazione effettiva deve essere coerente con i validator presenti nel
codice e con le decisioni architetturali approvate.

## Idempotenza

A parità di input validati e di versione del codice, una build completa deve
produrre risultati logicamente equivalenti.

Questa proprietà consente:

- riproducibilità;
- confronto tra build;
- rollback;
- validazione in CI;
- diagnosi delle regressioni.

## Data lineage

Ogni dataset Warehouse deve poter essere ricondotto almeno a:

- dataset Analytics di origine;
- data e ora della build;
- versione del codice o commit;
- versione dello schema;
- esito delle validazioni;
- numero di righe prodotte.

Il lineage dettagliato sarà formalizzato nell'ADR dedicato alla Data Governance.

## Stato attuale

Operativo:

- consumo dei dataset Analytics validati;
- produzione dei dataset Warehouse in formato Parquet;
- validazione;
- metadata;
- test di integrazione;
- schema logico.

Evoluzione prevista:

- build incrementale;
- delta update;
- interrogazione tramite DuckDB;
- contratti SQL per il Dashboard;
- lineage più granulare.
