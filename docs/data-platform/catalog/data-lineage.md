# Data Lineage

Il lineage ricostruisce la provenienza di ogni prodotto.

## Relazione minima

```text
Raw Exposure
   -> Calibration Run
   -> Calibrated Frame
   -> Registration Run
   -> Registered Frame
   -> Integration Run
   -> Integrated Master
   -> Final Processing Run
   -> Final Product
```

Devono essere registrati identificativi, checksum, timestamp, software, versione, parametri, operatore o servizio e stato dell'esecuzione.
