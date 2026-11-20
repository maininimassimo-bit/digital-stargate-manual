# PixInsight nella VM di elaborazione — 20 novembre 2026

Il setup Windows ha completato l’installazione di PixInsight. I campi ProductVersion e FileVersion dell’eseguibile installato riportano entrambi 1.9.6. La distribuzione commerciale identifica il pacchetto come build 1719. La verifica ha utilizzato i metadati del file. Il primo avvio, l’attivazione e le prove di elaborazione restano da verificare.

## Evidenze disponibili per la ripresa

- **BKL-046.** L’osservazione 448 del test NATIVE_STREAM_HASH_WITNESS_001 registra una lettura stabile e la corrispondenza dell’hash. Il verdetto conserva aperte le attestazioni di origine nativa, custodia, memoria e uscita del processo originale. L’osservazione non autorizza un nuovo tentativo o il rilascio del gate comune.
- **BKL-051.** Il rapporto di allineamento del 18 novembre registra il rilascio della sola prenotazione fallita della R3. Per il piano operativo R4 il rilievo ARB-APIOP-R4-001 riguarda l’ordine tra la registrazione dei listener error/close e la validazione del processo figlio. Alla data di quel rapporto servivano modifiche e la revisione RQ non era iniziata.

Questa verifica documenta l’ambiente di elaborazione. Le due milestone restano aperte e l’autorizzazione a una prova nativa deve essere verificata sul registro canonico prima dell’esecuzione.
