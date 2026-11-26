# BKL-046 · Incertezza del rumore a raggio stellare confrontabile

| Deposito diretto confrontato | Nucleo | Bilineare con dispersione minore nella stima puntuale | Bilineare con direzione stabile |
| --- | --- | ---: | ---: |
| 1,00 px | 3 × 3 | 6/8 | 2/8 |
| 1,00 px | 5 × 5 | 8/8 | 0/8 |
| 0,70 px | 3 × 3 | 6/8 | 2/8 |
| 0,70 px | 5 × 5 | 6/8 | 0/8 |

I quattro casi stabili sono G1, entrambe le calibrazioni e i due depositi, con nucleo 3 × 3. La dispersione del bilineare in questi casi diminuisce del 16,1–18,0% nella stima puntuale. Nessun confronto ha una direzione stabile a favore del deposito. Nel nucleo 5 × 5 del deposito da 1,00 px, tutti e otto gli intervalli per regione comprendono lo zero, anche se tutte le stime puntuali favoriscono il bilineare.

La ripetizione osserva le finestre con supporto comune durante l'esecuzione del programma a monte e richiede una ricevuta identica byte per byte. Verifica inoltre le deviazioni standard delle somme compensate contro quelle della ricevuta. Mantiene le larghezze gaussiane già stimate e la stessa coppia di finestre per ogni metodo. Il protocollo fissa 10.000 ricampionamenti di stelle con reinserimento entro ciascuna delle quattro regioni di verifica. Ogni stella contribuisce con tutte le proprie finestre. La sensibilità spaziale usa le 256 combinazioni ordinate di quattro regioni campionate con reinserimento e le quattro esclusioni singole.

La direzione è stabile se gli intervalli descrittivi 2,5–97,5% di entrambi i ricampionamenti e tutte le esclusioni singole cadono dallo stesso lato dello zero. I confronti condividono campo, pose e metà temporali. Le calibrazioni A e B non costituiscono repliche indipendenti. Le due larghezze e le due aperture condividono i dati. Gli intervalli non hanno correzione per confronti multipli. L'analisi confronta un indicatore di raggio stellare. La risposta spaziale completa, il trasferimento ad altri campi e la prova nativa PixInsight restano da verificare.

Asse NOISE_FLUX, prove di dispersione d'apertura CFA dopo ricostruzione. Zero avvii nativi e zero chiusure scientifiche.
