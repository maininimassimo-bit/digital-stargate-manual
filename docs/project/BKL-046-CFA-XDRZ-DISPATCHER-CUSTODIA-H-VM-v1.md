# BKL-046 · Custodia dei file su H: durante il rilascio R4

Il dispatcher rilegge i 17 oggetti e il marker attraverso handle Windows aperti con condivisione di sola lettura. Mantiene gli handle aperti durante l'ultima verifica della prenotazione e fino alla risposta di R4. L'ausiliario verifica lunghezze e impronte attraverso gli stessi handle che escludono scritture e sostituzioni. Il dispatcher verifica inoltre l'insieme dei nomi prima e dopo la chiamata di rilascio.

In due collaudi su DSG-Shared, Windows ha respinto l'apertura in scrittura della schermata durante la chiamata di rilascio e l'ha consentita alla fine. Il caso valido ha prodotto la ricevuta R4 sul registro di prova. Finestra non reattiva, FITS alterato e collisione nell'archivio hanno conservato le rispettive prenotazioni. Le impronte dei 30 file del registro canonico sono rimaste identiche.

La custodia temporanea copre gli oggetti esistenti durante il rilascio. L'archivio torna scrivibile alla fine. Per la conservazione di lungo periodo servono una protezione persistente o impronte pubblicate in un registro indipendente. Restano l'entrypoint revisionato e l'ammissione reale. PixInsight è rimasto chiuso.
SHA-256 archivio H: 174f3a2e2835df876073c6c2293c074bab5ac246a607142feb16cfa5fd062c16.
