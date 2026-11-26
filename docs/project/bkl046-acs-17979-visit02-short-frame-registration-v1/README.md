# BKL-046 · Abbinamento diretto delle due pose ACS da 40 s

I due FLT F606W hanno lo stesso bersaglio, durata, gain e apertura dichiarati. Ho cercato la traslazione di riquadri da 256 px entro ±110 px, su 12 posizioni per chip. Ho inoltre calcolato la correlazione di fase sul chip entro ±1.000 px. La preparazione esclude DQ diversi da 0/64, limita i valori estremi e sottrae una media locale. Il verso dello spostamento è dalla posizione in jfln02qzq alla posizione in jfln02qtq. Il programma 17979 è il monitor CTE esterno ACS. [Piano di calibrazione STScI](https://www.stsci.edu/hst/instrumentation/acs/calibration/calibration-plans)

Nessuno dei 24 riquadri raggiunge la correlazione minima di 0,20. Il massimo delle correlazioni per riquadro è circa 0,084 sul chip 1 e 0,079 sul chip 2. La correlazione di fase ha un massimo a offset nullo, di ampiezza rispettivamente 0,017 e 0,019. Quel picco da solo non stabilisce una corrispondenza stellare. I controlli applicano una traslazione nota (21, −17) e una scala d'intensità 0,6 alla stessa immagine. Il metodo recupera l'offset su entrambi i chip. Quel controllo verifica il calcolo in condizioni ideali.

La prova non trova una traslazione comune utilizzabile per queste immagini, entro lo spazio di ricerca dichiarato. Resta aperta la causa della discordanza. Il risultato non identifica un guasto strumentale e non qualifica jfln02qtq come secondo riferimento fotometrico. [Dossier con i riscontri Gaia](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/fa81eab025d9df14b1e3c965a5004bc8a29a7b5c/docs/project/bkl046-acs-17979-gaia-astrometry-v1)

Per ripetere, eseguire `verifica.py` con i runtime Astropy e SciPy, la directory dei FITS, il protocollo e un nuovo file di uscita. Le impronte dei due FITS sono nel protocollo.
