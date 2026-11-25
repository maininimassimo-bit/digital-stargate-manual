# BKL-046 · Identità della finestra associata al processo originale

Il candidato enumera le finestre principali con barra del titolo e senza proprietario nella stessa sessione Windows. Verifica che esista una sola finestra idonea, che l'handle della finestra appartenga al PID e al thread rilevati e che l'handle del processo originale conservi PID e istante di creazione. La funzione destinata al supervisore richiede anche che la finestra sia visibile e rilegge l'identità prima di qualsiasi uso successivo.

Il collaudo ha usato finestre testimone reali ma invisibili. Due processi con lo stesso titolo sono stati distinti correttamente. Due finestre idonee dello stesso processo hanno prodotto un rifiuto. Il percorso riservato alle finestre visibili ha escluso il testimone invisibile. Dopo la chiusura ordinaria del testimone, il vecchio handle è stato rifiutato e la finestra dell'altro processo è rimasta aperta. Le due esecuzioni coincidono.

La prova attesta l'associazione e l'invalidazione sul testimone. La compatibilità del filtro con la finestra PixInsight, la cattura e la chiusura nella sessione ammessa restano da verificare dopo revisione. Nessun avvio PixInsight.

Ricevuta SHA-256 `18c928ee8c5b7b7d2408010f506c8b81248d1ab4374621655b0d064bd21b82a5`.
