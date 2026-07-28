# Scientific Data Model

## Entità principali

| Entità | Descrizione |
|---|---|
| ObservationSession | sessione osservativa completa |
| Exposure | singola posa acquisita |
| CalibrationFrame | bias, dark, flat o dark-flat |
| InstrumentConfiguration | configurazione ottica e strumentale |
| Target | oggetto o campo osservato |
| ProcessingRun | esecuzione di una pipeline |
| DataProduct | prodotto raw, calibrato, integrato o finale |
| QualityAssessment | metriche e valutazioni qualitative |
| StorageLocation | posizione logica e fisica del dato |
| LineageRelation | relazione tra input, processo e output |

## Identificativi

Gli identificativi devono essere stabili, univoci e non dipendere dal percorso del file. È raccomandato l'uso di UUID o identificativi composti governati dalla piattaforma.
