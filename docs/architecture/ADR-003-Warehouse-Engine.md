\# ADR-003 – Warehouse Engine



\## Status



Accepted



\## Context



Gli Analytics producono dataset CSV validati.



I componenti successivi (Dashboard, Homepage, Report, KPI) non devono

rileggere i log NINA.



È necessario introdurre un livello di Warehouse persistente.



\## Decision



Il Warehouse leggerà esclusivamente i dataset Analytics.



Output principale:



\- sessions.parquet

\- targets.parquet

\- equipment.parquet

\- weather.parquet



Il Warehouse non analizzerà direttamente:



\- log

\- immagini

\- manifest



Ogni dataset Warehouse deriverà solamente da dati già validati.



\## Consequences



Vantaggi



\- separazione dei livelli

\- build molto più veloce

\- dati consistenti

\- facile caching

\- facile estensione



Svantaggi



\- un passaggio aggiuntivo

\- dipendenza dagli Analytics



\## Future



\- Incremental build

\- Delta update

\- DuckDB

\- Dashboard SQL

