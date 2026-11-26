# BKL-046 · Fondo M8/M20 con scala stellare e bordi esclusi

Il test applica alle 27 coppie di pose già registrate le 72 scale stellari archiviate per coppia. Per ogni scala, il piano e l'offset vengono stimati sulle celle che restano dopo aver escluso la fascia da verificare. Il piano passa quando riduce di almeno il 10% la mediana assoluta rispetto all'offset e non aumenta il P90. L'esito congiunto richiede le due partizioni a scacchiera e tutte e quattro le fasce ai bordi per la stessa scala.

| Criterio | Coppie favorevoli con scala unitaria | Prove favorevoli su 1944 | Coppie favorevoli con almeno una scala su 27 | Coppie favorevoli con tutte le scale su 27 |
| --- | ---: | ---: | ---: | ---: |
| Scacchiera | 6 | 886 | 21 | 6 |
| Tutti i bordi | 1 | 190 | 7 | 1 |
| Entrambi | 0 | 148 | 5 | 1 |

Il programma riproduce esattamente le metriche precedenti per le partizioni a scacchiera a ciascuna scala e quelle dei quattro bordi a scala unitaria. Le quattro coppie con esito congiunto variabile lasciano aperta la scelta della correzione al variare della scala. L'unica coppia sempre favorevole delimita un risultato diagnostico sul campo analizzato. Pose, stelle e stime vengono riusate. Il campione finito lascia aperti l'incertezza della scala, il fondo assoluto, la conservazione del segnale diffuso e la qualifica nativa.

Per replicare, passare nell'ordine il protocollo, la directory dell'archivio di riferimento estratto con le sottodirectory capture e stellar, il rapporto completo delle scale empiriche, il protocollo dei bordi, il rapporto dei bordi M8M20, la directory con NumPy 2.3.5 e Astropy 7.2.0 e una directory di uscita nuova. Il kit H/K conserva tutti gli esiti per coppia, scala e bordo. [Scale empiriche](../bkl046-m8-m20-empirical-scale-background-v1/README.md) · [Bordi a scala unitaria](../bkl046-diffuse-held-out-edges-v1/README.md)