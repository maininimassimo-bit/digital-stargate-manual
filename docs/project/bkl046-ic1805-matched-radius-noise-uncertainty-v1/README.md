# BKL-046 · Verifica su IC 1805 della dispersione a raggio comparabile

Il confronto replica su un secondo campo il ricampionamento della dispersione delle somme compensate dopo l'allineamento del raggio stellare RMS. Il programma a monte riproduce la ricevuta originale byte per byte. Le deviazioni standard delle proiezioni coincidono con quelle archiviate, entro la precisione della ricevuta. Sono comprese 32 stelle in nove regioni di verifica, 256 finestre per parità e due calibrazioni. Per ogni contrasto si usano 10.000 ricampionamenti delle stelle entro regione, 10.000 ricampionamenti delle regioni e le nove esclusioni singole. Tutte le finestre di una stella restano insieme.

| Deposito diretto confrontato | Nucleo | Bilineare con dispersione minore nella stima puntuale | Bilineare con direzione stabile |
| --- | --- | ---: | ---: |
| 1,00 px | 3 × 3 | 2/8 | 2/8 |
| 1,00 px | 5 × 5 | 4/8 | 2/8 |
| 0,70 px | 3 × 3 | 3/8 | 2/8 |
| 0,70 px | 5 × 5 | 4/8 | 2/8 |

Gli otto casi stabili appartengono alla parità rossa, con riduzioni stimate del 2,6–6,6%. Nessun caso stabile favorisce il deposito. I quattro confronti G1 con nucleo 3 × 3 che favorivano stabilmente il bilineare in M8–M20 non si ripetono in IC 1805. In IC 1805 le quattro stime corrispondenti vanno da +0,16% a +1,91% e gli intervalli per stelle e per regioni includono tutti lo zero.

Le pose provengono da un campo e da un sensore diversi, quindi il confronto non isola la causa della differenza. IC 1805 conserva la calibrazione provvisoria senza dark-flat abbinati e la registrazione fuori soglia. Gli intervalli descrivono la sensibilità allo scambio di stelle e regioni dentro ciascun campo. Le calibrazioni condividono le pose e i confronti condividono finestre. Il raggio RMS è un solo indicatore della risposta spaziale.

Il risultato limita l'uso del vantaggio G1 come regola generale per la selezione del metodo nell'asse NOISE_FLUX. La verifica nativa e il confronto su dati con calibrazione e registrazione qualificate restano aperti. Zero avvii PixInsight e zero chiusure scientifiche.
