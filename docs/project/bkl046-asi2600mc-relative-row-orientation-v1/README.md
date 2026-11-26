# Orientamento relativo delle coordinate ASI2600MC

I primi sette dark a 180 s fissano 77 siti con residui persistenti rispetto ai vicini della stessa parità Bayer. La lista è congelata prima della verifica sugli altri otto dark, sui 15 flat e sulle 15 pose M8–M20. Si confrontano identità, riflessione orizzontale, riflessione verticale e rotazione di 180° nel reticolo memorizzato. La soglia diagnostica per sito è il maggiore tra 100 ADU e il 25% del residuo mediano di addestramento.

| Serie di verifica | Mediana dei siti riconosciuti alle coordinate originali | File in cui le coordinate originali superano tutte le trasformazioni |
| --- | ---: | ---: |
| Dark 180 s | 64,5 / 77 | 8/8 |
| Pose M8–M20 | 62 / 77 | 15/15 |
| Flat 3 s | 33 / 77 | 6/15 |

Nei dark di verifica le tre trasformazioni riconoscono zero siti. In ogni posa M8–M20 le coordinate originali conservano almeno 52 siti in più della migliore alternativa. Nei flat la separazione è debole. Il punteggio misura la persistenza di una firma di coordinate a questa soglia e i siti non sono trattati come acquisizioni indipendenti.

La firma supporta l’allineamento relativo tra dark e pose M8–M20 nei file archiviati. Il FITS non riporta ROWORDER e il controllo non stabilisce quale bordo corrisponda alla prima riga fisica del rivelatore. Restano aperti la conferma con un riferimento fisico e il comportamento del lettore nativo.

Per riprodurre eseguire `misura.py protocollo.json <directory-calibratori> <directory-pose> <pacchetti-Python> <nuovo-rapporto.json>`. Lo script verifica gli archivi, i 45 FITS e il rapporto di acquisizione. Il rapporto conserva i conteggi per trasformazione e per file.
