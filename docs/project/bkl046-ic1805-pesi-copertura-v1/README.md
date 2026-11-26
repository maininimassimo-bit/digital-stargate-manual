# BKL-046 · Copertura effettiva con pesi geometrici IC 1805

Il controllo riproduce tutti i conteggi geometrici dei 72 riferimenti IC 1805 e delle due metà di pose. Ogni peso è l'area di sovrapposizione del deposito quadrato con la cella unitaria di uscita. Su ciascun contributo la somma sulle quattro celle deve restituire l'area del deposito. Il numero effettivo di contributi è il quadrato della somma dei pesi diviso per la somma dei loro quadrati.

| Larghezza del deposito, posizione nominale | Almeno due contributi positivi in ogni cella e metà | Numero effettivo almeno due | Mediana del numero effettivo nella cella peggiore |
| --- | ---: | ---: | ---: |
| 1,00 px | 72/72 | 71/72 | 6,10 |
| 0,70 px | 71/72 | 66/72 | 3,89 |

Con il deposito da 0,70 pixel esiste almeno una combinazione in cui una singola posa fornisce tutto il peso. I limiti conservativi sulle aree con perturbazioni di 0,30 o 0,462645 pixel non garantiscono due contributi effettivi per alcuna stella. Il limite è pessimista perché combina estremi separati dei pesi. Questo esito non misura il numero effettivo che si otterrebbe sotto una specifica perturbazione.

I pesi sono geometrici e ignorano difetti, bordi reali, qualità e rumore delle pose. Il confronto riguarda CFA_DITHER_DRIZZLE/3. Restano da verificare i pesi effettivi e l'operatore nativo. Eseguire `misura.py` con il protocollo, il protocollo e il rapporto congelati del conteggio geometrico, la directory con NumPy 2.3.5 e un percorso nuovo per l'esito.
