# BKL-046 · Aperture di GRW+70°5824 con il centro previsto dalle altre bande

Ho selezionato le otto visite rimanenti del gruppo `ibbsz` nel programma HST 11907 con un'esposizione pubblica individuale in ciascuna delle tre bande. La visita `ibbszj` del controllo precedente è esclusa dalla selezione. Ho acquisito 24 FLC distinti e verificato le identità degli header. Applicando la previsione assoluta Gaia del protocollo precedente, tutte le 24 pose superano il limite di quattro pixel e vengono respinte. [Controllo Gaia precedente](../bkl046-grw70-gaia-aperture-identity-v1/README.md)

Un controllo esplorativo distinto trova nelle altre due bande un picco finito, con DQ zero, sufficientemente prominente nel riquadro fissato attorno alla previsione Gaia. I due picchi sono trasformati nel sistema di pixel della posa lasciata fuori. Se concordano entro 1,5 pixel, il loro punto medio determina il centro iniziale per quella posa. Il metodo mantiene il limite di quattro pixel, i veto DQ e i controlli di supporto sulle due aperture. I picchi nelle due bande forniscono una previsione relativa nella stessa visita. Il test non costituisce una calibrazione astrometrica indipendente del campo.

| Esito del controllo esplorativo | Pose |
| --- | ---: |
| DQ nel nucleo | 12 |
| Supporto incompleto | 9 |
| Misurate a 5 e 10 pixel | 3 |

La sola visita `ibbsz1` fornisce tutte e tre le bande a entrambi i raggi. Passando da 5 a 10 pixel, il colore cambia di **+3,28 mmag** per F438W − F606W, **+9,65 mmag** per F438W − F814W e **+6,37 mmag** per F606W − F814W. Due altre visite, `ibbsz8` e `ibbszb`, forniscono i tre colori soltanto a 5 pixel.

Il confronto misura la dipendenza dall'apertura su una seconda stella con una regola di centro esplorativa. Una sola visita a entrambi i raggi non consente di stimare il trasferimento fra epoche né di convalidare la correzione di GD153. Le esclusioni del protocollo astrometrico assoluto restano registrate. Nessuna prova PixInsight o chiusura scientifica.

Per ripetere, usare `misura.py` con il kit estratto, il kit originale dei tre calibratori, NumPy 2.3.5/Astropy 7.2.0, un nuovo file di risultato e lo SHA-256 di acquisizione `9e6902c9f5ac8672f851bc64524272744205a1ef408286c8baee4a8c6bde8019`. `misura-centro.py` usa i medesimi kit con il risultato primario già verificato e un nuovo file di esito.