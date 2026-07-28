# DATA-000 — Scientific Data Platform Registry

## Scopo

Il registro identifica i principali building block della piattaforma dati.

| ID | Componente | Responsabilità | Stato |
|---|---|---|---|
| DATA-001 | Acquisition Ingestion | acquisizione e presa in carico dei file | Defined |
| DATA-002 | Metadata Extractor | estrazione header e metadata tecnici | Defined |
| DATA-003 | Validation Service | controlli integrità e qualità minima | Defined |
| DATA-004 | Scientific Archive | conservazione dei dati e dei prodotti | Defined |
| DATA-005 | Processing Pipeline | calibrazione, registrazione e integrazione | Defined |
| DATA-006 | Catalog Service | indicizzazione e ricerca | Defined |
| DATA-007 | Lineage Registry | tracciamento delle trasformazioni | Defined |
| DATA-008 | Analytics Layer | metriche, dashboard e reporting | Defined |
| DATA-009 | Retention Manager | politiche di conservazione e cancellazione | Defined |
| DATA-010 | Export Service | pubblicazione e condivisione controllata | Planned |

## Regole

Ogni nuovo componente dati deve dichiarare owner, input, output, dipendenze, classificazione dei dati, requisiti di retention e criteri di monitoraggio.
