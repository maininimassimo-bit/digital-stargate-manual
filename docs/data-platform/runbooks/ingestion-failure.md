# Runbook — Ingestion Failure

1. identificare file e sessione;
2. verificare che la scrittura sia conclusa;
3. controllare spazio disco e permessi;
4. validare il FITS e il checksum;
5. spostare il file in quarantena se corrotto;
6. ripetere l'ingestion senza sovrascrivere il raw;
7. registrare causa, azione ed esito;
8. aprire incidente se l'errore è ricorrente.
