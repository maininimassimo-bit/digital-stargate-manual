# BKL-046 · Replica della finestra di correlazione Gaia XP nella coorte ACS

La finestra storica fissata prima della replica copre 632–646 nm, con otto campioni. Ha un autovalore sotto −1e−8 in tutte e tre le sorgenti archiviate, distinte dalla sorgente v571. Il minimo della finestra varia da −0,0461 a −0,0252. Le finestre contigue più brevi che falliscono contengono cinque o sei campioni e terminano tutte a 646 nm. Nessun minore di ordine tre scende sotto la soglia sul determinante. Nelle tre covarianze formali condizionate il controllo della stessa finestra passa.

Il confronto riproduce prima i tre esiti della coorte congelata. Le sorgenti condividono catalogo e modello e il risultato non stima la frequenza del difetto nella popolazione. La covarianza formale omette le sistematiche. Nessuna nuova esecuzione PixInsight, correzione della matrice o chiusura scientifica.

Per riprodurre con Python e NumPy 2.3.5 impostare OPENBLAS_NUM_THREADS=1 e passare protocollo, estrattore della coorte, verificatore v571, directory della coorte e nuovo percorso del riscontro. Le impronte degli ingressi sono fissate nel protocollo.
