# BKL-046 · Verifica di pubblicabilità della conoscenza v1.146

Il verificatore legge tutti i 1.153.824.341 byte del JSON storico dalla capsula v571. Controlla l'impronta dell'intero JSON e dell'indice dei 708 contenuti incorporati. Conta i marcatori nelle 141 sezioni del file e nei contenuti incorporati, associandoli all'inventario storico tramite gli intervalli di byte congelati.

| Famiglia di marcatori | Rapporti incorporati con almeno un riscontro | Occorrenze fuori dalla sezione dei rapporti |
| --- | ---: | ---: |
| Percorsi locali | 200 | 98.100 |
| Gaia e GaiaXPy | 11 | 10 |
| Altri archivi astronomici | 3 | 1 |
| Riferimenti PixInsight o a sorgenti PJSR | 27 | 258 |
| Espressioni convenzionali per allegati codificati | 0 | 0 |

In totale 215 rapporti contengono almeno un marcatore. Di questi, 209 non hanno una corrispondenza esatta nel precedente inventario dei diritti. I conteggi includono occorrenze ripetute. Il programma produce conteggi e impronte, senza esporre percorsi, URL trovati o contenuto dei rapporti. Un indice difforme viene respinto. Cinque esempi sintetici distinti verificano le espressioni di ricerca.

I marcatori individuano materiale da esaminare e possono includere citazioni o riferimenti innocui. L'assenza di un marcatore non dimostra l'assenza di contenuti di terzi o privati. Il controllo documenta perché un esame limitato ai 708 rapporti lascerebbe fuori informazioni rilevanti. Il perimetro dell'intero file e la consegna finale restano aperti.

Per riprodurre con Python 3.12 passare il protocollo, la capsula storica, l'indice dei rapporti incorporati e un nuovo file di uscita. La directory di uscita ospita anche un temporaneo di circa 1,16 GB, chiuso e rimosso al termine.
