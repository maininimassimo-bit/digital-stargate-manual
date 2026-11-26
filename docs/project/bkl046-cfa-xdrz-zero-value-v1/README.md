# Pixel azzerato e campione escluso in un XDRZ CFA

Il controllo riprende la maschera verde XDRZ con traslazione asimmetrica e aggiunge due ingressi. In ciascuno si azzera un solo pixel verde della seconda posa mantenendo lo XDRZ senza rigetto. Riferimento, matrice, fase RGGB, scala 1 e deposito 0,70 restano quelli del controllo originale. Le coordinate partono da zero.

| Pixel della seconda posa | Cella di riferimento | Incluso con il valore originale | Azzerato con peso conservato | Escluso |
| --- | --- | ---: | ---: | ---: |
| (14, 7) | (13, 8) | 0,50 / 2 | 0,125 / 2 | 0,25 / 1 |
| (15, 6) | (14, 7) | 0,49 / 2 | 0,09 / 2 | 0,18 / 1 |

I valori esprimono intensità verde lineare e peso grezzo nel modello. Se PixInsight tratta un valore numerico zero come campione senza supporto, il braccio azzerato può coincidere con l'esclusione. Per rilevarlo, confrontare intensità, peso e supporto RGB sull'intera mappa per le combinazioni senza maschera, maschera verde, maschera sul canale errato e due pose azzerate in prove separate. Conservare esiti ambigui o fuori modello.

La replica usa `genera.py` con tre argomenti in ordine: directory del controllo originale con manifest fissato, directory dei pacchetti Python con NumPy 2.3.5 e Astropy 7.2.0, nuova directory di uscita. Gli XDRZ puntano alla directory finale del kit su DSG-Shared. Le mappe sono predizioni del modello geometrico archiviate per una futura revisione. La semantica nativa resta da misurare.
