# Scientific Data Platform Architecture

## Architettura logica

```text
Acquisition Systems
        |
        v
Ingestion & Validation
        |
        +--> Raw Archive
        |
        v
Metadata & Catalog
        |
        v
Processing Pipelines
        |
        +--> Intermediate Products
        +--> Final Scientific Products
        |
        v
Analytics / Reporting / Export
```

## Principi

- il dato raw non viene modificato;
- ogni trasformazione produce un nuovo artefatto;
- ogni prodotto mantiene il collegamento con gli input;
- i metadata accompagnano il dato per tutto il ciclo di vita;
- le pipeline devono essere ripetibili e osservabili;
- gli errori non devono cancellare o sovrascrivere gli originali.
