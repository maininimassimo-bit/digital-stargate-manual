# BKL-046 · Centroidi sui campioni verdi originali di IC 1805

La misura stima il nucleo ellittico comune ai due verdi del mosaico Bayer sui loro pixel originali. Il fondo e l'ampiezza sono ammessi distinti per parità. Il controllo con una sorgente gaussiana di posizione nota e ampiezze diverse nelle due parità recupera il centro entro 0,03 pixel nell'esempio sintetico.

Le 38 pose si confrontano sulle stesse associazioni stellari accettate dal fit sui campioni originali, da 40 a 71 per posa. L'analisi conserva le regioni di stima e verifica separate. Per la geometria ricalcolata, le stelle di stima sono inizializzate dal campo affine precedente e rifittate sui RAW. Le stelle di verifica partono dalle corrispondenze già archiviate e restano escluse dalla stima. Le sorgenti con segnale o supporto insufficiente, saturazione o profilo fuori dai limiti dichiarati vengono escluse.

| Centroidi e geometria | P90 complessivo (px nativi) | Pose con P90 ≤ 0,30 px |
| --- | ---: | ---: |
| Centroidi a metà scala, geometria precedente | 0,712 | 0/38 |
| Verdi originali, geometria precedente | 0,470 | 0/38 |
| Verdi originali, geometria ristimata | 0,463 | 0/38 |

Il valore da confrontare è 0,712 px sul sottoinsieme comune. Il precedente 0,814 px si riferiva a tutte le associazioni allora misurabili. Gran parte della riduzione è già visibile mantenendo la geometria precedente. I residui combinano sensibilità del centroide, accuratezza della geometria, rumore e qualità dell'associazione. Le posizioni sui RAW non costituiscono un riferimento astrometrico indipendente e il campo rimane fuori soglia. La replica scientifica e il confronto radiometrico restano aperti. Zero avvii PixInsight e zero chiusure scientifiche.

SHA-256 della ricevuta `a7d0c4d58cb59d6898aa597e3faf94cbbc40b94871dcb41f8f54028586d812a9`.
