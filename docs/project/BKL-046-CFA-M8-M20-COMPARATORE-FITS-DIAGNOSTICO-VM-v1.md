# BKL-046 · Comparatore FITS per il caso CFA M8–M20

Il comparatore legge le coppie FITS di intensità e pesi su 48 × 48 pixel. Usa il ritaglio di 29 × 29 fissato nel manifest e confronta il supporto RGB, i pesi per pixel e le intensità sul supporto valido. Riporta anche lo scostamento del flusso d'apertura rispetto all'oracolo offline per ciascun canale. La futura convenzione fornita al comparatore deve identificare il soggetto del controllo sintetico e legare le impronte della ricevuta R4 e del marker dell'archivio. La scala dei pesi è un dato in ingresso e il comparatore non la adatta ai risultati M8–M20.

I due autotest coincidono. Otto coppie FITS di prova a 32 bit sono state accettate. Sono stati respinti il rigetto omesso, i campioni azzerati con peso conservato, intensità alterate, perdita di supporto, pesi modificati e tre attestazioni sintetiche incompatibili. Le tolleranze numeriche sono candidate per la revisione e l'autotest usa la baseline offline come riferimento. La prova con PixInsight e la validazione scientifica restano aperte.
SHA-256 archivio H: c0de16eda425572c5ee68db16a0e5eb44c9686896880ffd380cf4a66ff080534.
