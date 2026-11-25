# BKL-046 — TV4 CLEAR1 con segnale comparabile in una sessione distinta

Il controllo `DIFFUSE_BACKGROUND/2` usa le acquisizioni MRI `FLAT24` del 27 febbraio 2003, gruppi BB e FS, con integrazioni effettive di 503,5 e 1.003,5 ms. I livelli di catalogo e i massimi globali hanno guidato la scelta dei due gruppi. Il protocollo ha fissato i primi sei frame cronologici per gruppo prima di scaricare i FITS. L'esposizione e le condizioni termiche differiscono dalla sessione di riferimento del 2 marzo. I due gruppi del 27 febbraio non costituiscono due sessioni indipendenti.

Sono stati verificati 24 oggetti PDS. Tutti i 12 FITS rispettano il limite di 15.000 DN nella regione centrale fissata. Per aperture 16 × 16, il rapporto mediano tra varianza osservata e previsione a pixel indipendenti vale 2,00 (coppie adiacenti) e 1,33 (separate) per BB. In FS entrambi i rapporti mediani sono circa 257. Le due modalità riutilizzano gli stessi fotogrammi. Le permutazioni sono descrittive.

La diagnosi di sensibilità mostra che in FS le medie per quadrante spiegano oltre il 99% della varianza di ogni differenza appaiata dopo la correzione con overscan. I rapporti scendono a 1,02–1,49 rimuovendo quelle medie e a 1,03–1,51 calcolandoli sui pixel senza la correzione con overscan. In BB la correzione è rilevante alle aperture grandi anche con una quota di varianza attribuita ai quadranti molto più bassa. Le due analisi non stabiliscono l'origine fisica del contributo dei quadranti. Documentano la sensibilità alla stima dell'offset e impediscono di trasferire un fattore unico al fondo diffuso.

Risultato e diagnosi sono stati riprodotti byte per byte. Il criterio scientifico resta aperto. Nessuna esecuzione nativa.

[Dataset NASA PDS](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-HRII%2FHRIV%2FMRI-2-GROUND-TV4-V1.0)