# BKL-046 · Trasferimento della correzione d'apertura fra UVIS2 e UVIS1

Ho usato le sette visite GRW+70°5824 ammesse a entrambi i raggi con il centro previsto dalle altre due bande. Le due visite UVIS2 del primo lotto definiscono la correzione. Applico lo stesso termine alle tre visite riservate UVIS2 e alle due riservate UVIS1. La stima non usa nessuna visita riservata. [Censimento e antecedente confronto su UVIS2](../bkl046-grw70-11907-held-out-color-transfer-v1/README.md)

| Colore | Errore assoluto mediano su UVIS2, senza → con correzione | Errore assoluto mediano su UVIS1, senza → con correzione |
| --- | ---: | ---: |
| F438W − F606W | 10,00 → 2,59 mmag | 3,21 → 11,20 mmag |
| F438W − F814W | 27,01 → 7,92 mmag | 4,77 → 22,05 mmag |
| F606W − F814W | 12,83 → 6,33 mmag | 4,35 → 10,85 mmag |

La stessa correzione migliora i nove confronti riservati sul chip di stima e peggiora tutti e sei quelli sull'altro chip. Nessuno dei sei valori UVIS1 cade nell'intervallo fra i due valori usati per la stima su UVIS2. Lo scarto massimo dopo il trasferimento è 26,83 mmag. Nel controllo inverso, stimando su UVIS1 e verificando sulle tre visite riservate UVIS2, migliora F438W − F606W nelle tre visite, mentre gli altri due colori peggiorano in tutte e tre.

Il confronto misura il trasferimento fra chip nei dati osservati. Le visite dei due chip hanno epoche e posizioni sul sensore diverse. Il test non misura un effetto causale del chip e gli estremi di due visite non rappresentano un intervallo di confidenza. Rimangono aperti la propagazione dell'incertezza, il trasferimento ad altri bersagli e la prova nativa. Zero chiusure scientifiche e zero esecuzioni PixInsight.

Per ripetere, passare a `misura.py` il protocollo, lo ZIP del censimento e un nuovo percorso per il risultato. Il programma verifica l'archivio e il suo rapporto, ricalcola i termini dalle misure a 5 e 10 pixel e controlla che il confronto su UVIS2 riproduca l'esito pubblicato.