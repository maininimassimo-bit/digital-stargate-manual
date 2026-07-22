# Release Notes — Milestone 5.1, Sprint 1

## Nuove funzionalità

- package `warehouse`;
- schema logico versionato;
- cinque dataset ufficiali:
  - sessions;
  - targets;
  - equipment;
  - weather;
  - quality;
- repository centrale dei percorsi;
- validazione dello schema;
- scrittura atomica di schema e metadata;
- nuovo step dependency-aware nella pipeline.

## Stato della migrazione

Dashboard e homepage continuano a leggere i file correnti.

Lo Sprint 2 introdurrà:

- lettura delle sorgenti esistenti;
- normalizzazione;
- scrittura dei dataset;
- rilevazione del motore Parquet disponibile;
- conteggi e sorgenti nel metadata;
- controlli di consistenza tra CSV e Warehouse.
