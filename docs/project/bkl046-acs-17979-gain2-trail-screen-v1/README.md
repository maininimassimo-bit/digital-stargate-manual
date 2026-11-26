# BKL-046 · Preselezione delle scie ACS/WFC a gain 2 nella visita 17979/02

I FITS del puntamento centrale confermano gain 2 e F606W. I 300 s del catalogo si riferiscono all'associazione. Il prodotto individuale analizzato dura 150 s; i due riferimenti della visita durano 40 s ciascuno. I due FLT brevi sono stati acquisiti con risposte HTTP parziali verificate per intervallo e lunghezza. [Archivio MAST](https://mast.stsci.edu/api/v0/)

Le due componenti connesse con estensione verticale di almeno cinque pixel contengono 6 e 7 pixel, rispettivamente. Tutti i pixel delle due componenti hanno DQ 12544, che combina full well (256) e le due classi di rifiuto per raggi cosmici (4096 e 8192). Il protocollo esclude queste componenti, perciò nessuna passa al confronto fotometrico con le pose brevi. Questa esclusione riguarda le scie di questo FLT e lascia aperta la verifica a gain 2. [Definizioni dei flag CALACS](https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps)

Per ripetere, eseguire `verifica.py` con il runtime Astropy, il runtime SciPy, la directory dei FITS e delle mappe PAM, il protocollo e un nuovo percorso di uscita. L'archivio su H: conserva tutti gli input vincolati dal protocollo. Nessuna chiusura scientifica.
