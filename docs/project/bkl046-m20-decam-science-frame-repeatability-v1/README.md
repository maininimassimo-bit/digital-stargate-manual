# BKL-046 · M20, verifica del sensore e confronto fotometrico in banda r

Il ritaglio da 30 s proviene da **FN1, CCD 73**, un sensore di messa a fuoco. I due ritagli da 180 s provengono da **S16, CCD 15**, un sensore scientifico. Il confronto dei ritagli con le rispettive immagini complete ha verificato tutti i campioni e le sezioni DATASEC. Il caso FN1 resta un controllo geometrico. È escluso dalla stima fotometrica. [Guida DECam, figura 2.2](https://noirlab.edu/science/sites/default/files/media/archives/documents/scidoc0436.pdf)

La ricerca iniziale di una controparte entro ±8 pixel dalla posizione WCS ha trovato soltanto due corrispondenze utilizzabili su 26 candidati, una nel gruppo di stima e una nella verifica. Le altre 24 misure sono state rifiutate. Il rapporto conserva questo esito e il programma non calcola un rapporto fotometrico quando mancano i controlli.

La ricerca esplorativa allargata a ±16 pixel ha consentito di stimare lo spostamento su 14 sorgenti e verificarlo su altre sei. Lo spostamento rispetto all'header è circa +11,21 pixel in x e −9,08 in y. Il residuo mediano sulle sei sorgenti di verifica è 0,117 pixel dopo la correzione.

| Raggio dell'apertura | Rapporto di scala stimato | Errore assoluto mediano sulle sei sorgenti | 90° percentile |
| ---: | ---: | ---: | ---: |
| 3 pixel | 2,505 | 3,43% | 4,34% |
| 5 pixel | 2,533 | 0,17% | 1,41% |
| 7 pixel | 2,552 | 0,91% | 1,29% |

Entrambe le esposizioni durano 180 s. Il rapporto di scala è misurato sui flussi grezzi sopra il fondo locale e varia fra aperture. I risultati del secondo passaggio sono esplorativi, perché l'allargamento della ricerca segue l'esito iniziale sullo stesso campo. I dati provengono da una sola coppia di pose. Restano aperti calibrazione strumentale, trasferimento fra tempi diversi e confronto con una posa breve acquisita su un CCD scientifico. Zero avvii PixInsight e zero chiusure scientifiche.

Per riprodurre, verificare il kit dei ritagli originali e l'archivio delle immagini complete, poi eseguire `misura.py` con la directory contenente il protocollo e i tre FITS completi, la directory dei ritagli, le dipendenze NumPy 2.3.5/Astropy 7.2.0 e un nuovo percorso di uscita. Per la sensibilità, usare una copia del kit con `protocollo-sensibilita-16px.json` come `protocollo.json`. I dati provengono dall'Astro Data Archive di NSF NOIRLab, gestito da AURA tramite accordo di cooperazione con la National Science Foundation. [Archivio NOIRLab](https://astroarchive.noirlab.edu/)
