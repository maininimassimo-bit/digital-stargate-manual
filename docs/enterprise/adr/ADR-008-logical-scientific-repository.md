# ADR-008 - Logical Scientific Repository

| Campo | Valore |
|---|---|
| Stato | Proposed |
| Data | 2026-07-28 |
| Decisione | Repository logico indipendente dallo storage fisico |

## Contesto

I dataset astronomici possono raggiungere dimensioni non compatibili con GitHub e possono essere distribuiti tra dischi, NAS e storage futuri.

## Decisione

Digital StarGate gestisce un catalogo logico con metadati, checksum, ubicazioni e lifecycle. I file pesanti risiedono in storage scientifico dedicato.

## Conseguenze

- GitHub resta dedicato a codice, documentazione, configurazioni e metadati selezionati;
- lo storage può evolvere senza cambiare il modello di dominio;
- servono controlli di integrità e sincronizzazione.
