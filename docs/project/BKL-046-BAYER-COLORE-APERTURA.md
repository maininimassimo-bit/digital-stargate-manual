# BKL-046 · Colore Bayer e dimensione dell'apertura

Nelle ricostruzioni M8/M20 e IC 1805 si misura la differenza del colore strumentale blu meno rosso passando da un'apertura di raggio 3 a una di raggio 6 pixel nativi. Il fondo viene sottratto nello stesso annulus. Le misure usano l'intersezione del supporto per tutte le parità, i metodi e le calibrazioni. Si conserva anche il controllo fra le due parità verdi. La misura è relativa alla variazione di apertura dello stesso oggetto e non richiede uno zero fotometrico.

Le correzioni sono mediane stimate sulla calibrazione A in righe separate del rivelatore. In verifica si confrontano nessuna correzione, correzione dallo stesso campo e correzione dall'altro campo. M8/M20 fornisce 25 stelle di stima e 29 di verifica. IC 1805 ne fornisce 40 e 32. La tabella riporta il P90 assoluto in magnitudini per blu meno rosso, deposizione da 1 pixel e calibrazione A.

| Campo | Senza correzione | Correzione nello stesso campo | Correzione dall'altro campo |
| --- | ---: | ---: | ---: |
| M8/M20 | 0,141 | 0,186 | 0,217 |
| IC 1805 | 0,105 | 0,049 | 0,062 |

La correzione migliora il P90 in IC 1805 e lo peggiora in M8/M20. La calibrazione B conserva lo stesso esito qualitativo. Nessuna configurazione blu meno rosso raggiunge 0,01 mag al P90. L'uso dell'altro campo è un controllo di trasferibilità tra due sensori con bande diverse e non rappresenta una calibrazione cromatica. Il raggio da 6 pixel è un riferimento interno finito. Le differenze comprendono PSF, fondo, campionamento e registrazione e non isolano un effetto cromatico della sola ottica. Restano aperti il riferimento fotometrico indipendente, i dark-flat abbinati e la prova nativa. Zero chiusure scientifiche.

SHA-256 della ricevuta `34881bf55161e630b2b1e1cc9aa230fdf615decdf14f7cd9d044bf417256edbc`.
