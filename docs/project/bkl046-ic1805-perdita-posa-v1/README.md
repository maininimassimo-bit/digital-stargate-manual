# IC 1805 e perdita di una posa CFA

Il collaudo BKL-046 riusa gli spostamenti nominali congelati delle 72 stelle di verifica. Per ogni stella si rimuove a turno un contributo locale da una delle due metà intercalate. Per ciascuna combinazione di parità CFA in ingresso e in uscita si calcola il peso come area di sovrapposizione e il numero effettivo di contributi come (Σw)²/Σw². Il risultato per stella è il minimo tra celle, metà e rimozioni.

| Larghezza deposito (px) | Stelle con almeno 2 contributi effettivi nominali | Stelle che li conservano dopo ogni singola rimozione | Stelle con una cella vuota dopo almeno una rimozione | Mediana del minimo dopo rimozione |
| --- | ---: | ---: | ---: | ---: |
| 1,00 | 71/72 | 69/72 | 0/72 | 5,096 |
| 0,70 | 66/72 | 59/72 | 1/72 | 2,987 |

L’ordinale di posa vale per la singola stella e metà. Il test non associa gli ordinali tra stelle e non misura la perdita di uno specifico file sull’intero campo. Usa la geometria nominale, senza propagare l’incertezza sugli spostamenti, le maschere di qualità, i pesi fotometrici o le covarianze. Il valore 2 è una soglia diagnostica. La prova non richiede PixInsight e non chiude un criterio scientifico.

Il riepilogo riporta l’impronta del JSON analitico. L’archivio locale contiene il JSON analitico e i due riscontri in ingresso. La replica richiede Python con NumPy 2.3.5 e accetta, nell’ordine, il protocollo, il riscontro geometrico, quello pesato, la directory dei pacchetti e il percorso per un nuovo JSON di uscita.
