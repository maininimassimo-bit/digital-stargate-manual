# BKL-046 · Fase e scelta dell'impronta in NGC 5986

Confronto esplorativo sulle 109 coppie con supporto comune già misurate a scala nativa. Il predittore è la minima distanza di fase tra i due assi, calcolata dalle posizioni previste. L'effetto da prevedere è la differenza appaiata di RMSE normalizzata fra impronte di 0,70 e 1,00 px. Per limitare le differenze spaziali, l'associazione è calcolata dopo centratura entro tessere da 128 px sul rivelatore della posa di riferimento, con permutazioni dei risultati all'interno della stessa tessera e dello stesso chip.

| Caso | Correlazione entro tessera | p bilaterale di permutazione | Stelle / tessere informative |
| --- | ---: | ---: | ---: |
| Nominale | −0,165 | 0,4341 | 27 / 12 |
| Peggiore fra quattro registrazioni perturbate | 0,010 | 0,9654 | 27 / 12 |

Per ciascuna tessera esclusa dall'addestramento, il confronto usa le altre tessere dello stesso chip per scegliere la larghezza con l'errore medio minore. Una regola sceglie per chip, l'altra separa anche le 24 coppie che superano la soglia nominale di 0,25 px su entrambi gli assi dalle altre 85. Le regole selezionano sempre 0,70 px per entrambe le condizioni, anche senza ricorrere alla scelta di riserva prevista per gruppi piccoli. Il P90 complessivo con registrazione perturbata passa comunque da 8,90% con 1,00 px a 9,10% con 0,70 px. La scelta sull'errore medio lascia un compromesso nella coda.

La fase nominale non ha aggiunto capacità di scelta in questa coorte. Le permutazioni presuppongono scambiabilità locale e il campione informativo è piccolo. La validazione esclude tessere, mentre riusa lo stesso campo, le stesse pose e lo stesso riferimento osservativo. Il risultato non stima le prestazioni su altri campi o su sequenze CFA. L'asse `CFA_DITHER_DRIZZLE/2` rimane aperto.

SHA-256 della ricevuta `10c7f2add8e3bda980502b3f4f712bf5c7c295b0cba3edb3bf1bd50b9e6e8a5d`.
