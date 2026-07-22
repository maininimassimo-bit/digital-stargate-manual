\# ADR-001 – Session Layer



\## Status



Accepted



\---



\## Context



Digital StarGate Analytics utilizza numerosi moduli che operano sui dati delle sessioni osservative.



Fino alla release 5.1 ogni componente individuava la sessione esclusivamente dal nome della cartella.



Questo approccio non permette di validare:



\- finestra temporale della sessione;

\- timezone;

\- durata;

\- file appartenenti alla sessione;

\- stato della sessione.



Il problema è emerso durante l'analisi di target-exposures.csv.



Sono state trovate immagini appartenenti alla notte precedente.



\---



\## Decision



Introduzione del package



dsg-analytics/session



contenente:



\- SessionMetadata

\- parser.py



che rappresenta l'unica sorgente autorevole dei metadati di una sessione.



Tutti i moduli dovranno ottenere i dati esclusivamente tramite:



load\_session\_metadata()



\---



\## Consequences



Vantaggi



\- eliminazione di duplicazione codice

\- filtro temporale centralizzato

\- migliore testabilità

\- riuso in Warehouse

\- riuso in Dashboard

\- riuso in Reporter

\- riuso in Homepage



Svantaggi



\- un piccolo layer aggiuntivo

\- dipendenza dal manifest.json



\---



\## First Consumers



\- extract\_target\_metrics.py

\- Warehouse Builder

\- Weather Loader



\---



\## Future Extensions



Il package Session potrà successivamente includere:



\- statistics()

\- log discovery

\- health check

\- session validation

\- timeline generation

