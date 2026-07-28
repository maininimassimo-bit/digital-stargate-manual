# Runbook — Pipeline Recovery

1. identificare lo stadio fallito;
2. preservare log, parametri e output parziali;
3. verificare disponibilità e checksum degli input;
4. correggere configurazione o dipendenza;
5. riavviare dal primo checkpoint sicuro;
6. generare un nuovo processing run;
7. non sovrascrivere prodotti precedentemente pubblicati;
8. aggiornare lineage ed esito.
