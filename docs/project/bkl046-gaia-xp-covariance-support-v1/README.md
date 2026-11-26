# BKL-046 · Supporto del difetto di semidefinitezza nella correlazione Gaia XP v571

Sul fascicolo storico di una sola sorgente, il protocollo fissa le rappresentazioni da confrontare e le tolleranze prima dell'esecuzione. Il verificatore ricostruisce la correlazione dal triangolo inferiore storico e confronta la correlazione formale condizionata e il caso diagonale. Per ogni matrice enumera tutte le coppie e tutti i minori principali di ordine tre. Per la matrice storica usa l'interlacciamento degli autovalori per trovare la banda contigua più corta che scende sotto la soglia di −1e−8.

- Nessuna delle 58.653 coppie presenta un autovalore negativo. Nessuno dei 6.666.891 minori di ordine tre scende sotto la soglia sul determinante.
- La finestra contigua più corta che fallisce contiene otto campioni. Il suo autovalore minimo è circa −0,0166. Tutte le finestre da sette campioni superano il controllo. Il minimo della matrice completa è circa −0,0942.
- La correlazione formale condizionata passa alla soglia fissata. La diagonale è un controllo numerico. Il difetto storico è rilevabile dentro una banda contigua breve anche quando coppie e triple superano i controlli.

Il risultato non identifica la configurazione minima di campioni non contigui e non qualifica una correzione della matrice. La covarianza condizionata omette le sistematiche. La prova interessa la rappresentazione numerica della sorgente storica e non include nuove sorgenti indipendenti, chiamate native o ammissione scientifica.

Per ripetere usare Python e NumPy 2.3.5, con OPENBLAS_NUM_THREADS=1. Passare il protocollo, lo ZIP ricostruito v571 e un nuovo percorso di uscita. Il verificatore controlla i digest del protocollo, dello ZIP e della matrice.
