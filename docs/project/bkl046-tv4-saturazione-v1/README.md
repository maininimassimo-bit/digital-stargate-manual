# BKL-046 — TV4 CLEAR1, pixel al valore massimo e saturazione estesa

Per `SATURATION_BLEND/1` ho selezionato i primi sei fotogrammi cronologici di ciascuno dei gruppi CT, CW, CU e DA del 2 marzo 2003. La selezione ha preceduto il download e usa i metadati per fotogramma. Nel gruppo CW la durata effettiva di 22.503,5 ms coincide con l'indice e le righe delle acquisizioni. Una nota riepilogativa nel log indica 2.500 ms. Ho verificato 24 FITS e 24 etichette con i checksum PDS e ho misurato le aree direttamente sui codici grezzi, prima di correzioni o normalizzazioni.

| Gruppo e integrazione | Riscontro su sei fotogrammi |
| --- | --- |
| CT, 15.003,5 ms | Un solo pixel al codice massimo in ciascun frame. Tutti coincidono alla posizione X=1023, Y=1015 in coordinate FITS-array da zero. Le cinque regioni interne non raggiungono il codice massimo. |
| DA, 15.003,5 ms, dopo il riallineamento | Due dei sei frame presentano lo stesso singolo pixel al massimo. Le cinque regioni interne non raggiungono il codice massimo. |
| CW, 22.503,5 ms | Nessun pixel arriva a 16.383 DN. Le cinque regioni fisse restano sotto 15.000 DN. |
| CU, 30.003,5 ms | Tutti i frame mostrano saturazione estesa. Il 28,25–28,61% dell'array e il 45,34–45,90% della regione centrale raggiungono il codice massimo. Nelle quattro regioni fuori centro la frazione varia da meno dell'1% a oltre il 67%. |

Il campo `MAXIMUM` delle etichette coincide con quello di catalogo. In 17 dei 24 frame il valore differisce dal massimo letto nell'intero array, quindi la valutazione conserva entrambi. Il singolo pixel al bordo e la saturazione estesa portano a diagnosi diverse. La misura usa il limite digitale a 14 bit. Capacità fisica del pixel, causa del valore al bordo, recupero fotometrico e trasferibilità ad altri sensori restano aperti. Il replay coincide byte per byte. Nessuna prova nativa.

[Dataset NASA PDS](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-HRII%2FHRIV%2FMRI-2-GROUND-TV4-V1.0)