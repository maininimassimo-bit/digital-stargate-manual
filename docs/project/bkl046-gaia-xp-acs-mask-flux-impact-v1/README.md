# BKL-046 · Effetto della maschera Gaia XP sui flussi ACS

Il protocollo elimina il contributo degli otto campioni 632–646 nm dai pesi fotonici delle catene nominali ACS WFC1. L'integrazione è verificata a quattro e otto nodi. Il confronto usa la sorgente storica v571 e tre sorgenti della stessa coorte Gaia. Non sono applicate interpolazione dei valori mancanti o rinormalizzazione dei pesi.

| Quantità | Cambiamento osservato nei quattro casi |
| --- | --- |
| Flusso F606W | Omissione dal 7,17% all'8,55% |
| Flusso F658N | Omissione dallo 0,0367% allo 0,0394% |
| Flusso F660N | Omissione dallo 0,00139% allo 0,00151% |
| Rapporto F658N/F660N | Diminuzione dallo 0,0353% allo 0,0379% |
| Rapporto F606W/F658N | Diminuzione dal 7,13% all'8,52% |

Con la covarianza formale condizionata, la deviazione standard relativa del rapporto stretto cresce dello 0,043–0,048% rispetto a quella senza maschera. Nel rapporto F606W/F658N cresce dello 0,79–1,47%. Il riscontro conserva separatamente la propagazione con la correlazione storica dopo la maschera.

La rimozione del modo negativo cambia la risposta dell'integrazione. Nel workflow preservare la distinzione tra stima mascherata e flusso definito dalla passband originale, soprattutto per F606W. Restano aperte la fotometria indipendente e le sistematiche di calibrazione. Nessuna esecuzione PixInsight o chiusura scientifica.

Per riprodurre, eseguire verifica.py con Python e NumPy 2.3.5, con OPENBLAS_NUM_THREADS=1. Passare nell'ordine il protocollo, la directory di esclusione, la directory del supporto della coorte, l'estrattore, il verificatore del supporto v571, la directory delle sorgenti della coorte, la capsula restaurata, la directory del protocollo ACS e un nuovo percorso per il risultato.
