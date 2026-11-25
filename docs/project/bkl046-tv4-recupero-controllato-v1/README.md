# BKL-046 — Recupero sotto taglio controllato di pose TV4 reali

Ho selezionato i primi sei fotogrammi del gruppo DC a 10.003,5 ms, rimasti fuori dal fit. Nelle cinque regioni interne tutti i codici originali erano sotto il limite digitale. Ho simulato un taglio a 5.500 e 6.200 DN e usato i valori originali sopra soglia come riferimento. Il confronto riguarda i pixel effettivamente alterati dal taglio artificiale, quindi usa una maschera nota per costruzione. I modelli usano l'overscan parallelo e pose della stessa sequenza. Il modello a due livelli interpola i tempi di esposizione. Il modello con una sola posa di riferimento usa il livello più breve.

| Taglio | Pixel confrontati | Errore assoluto medio, limite inferiore | Modello a due livelli prima del riallineamento | Modello a due livelli dopo il riallineamento |
| --- | ---: | ---: | ---: | ---: |
| 5.500 DN | 1.857.076 | 366,17 DN | 96,86 DN | 12,52 DN |
| 6.200 DN | 134.408 | 113,56 DN | 16,65 DN | 12,79 DN |

A 5.500 DN, l'errore sul totale dei codici alterati passa da −6,24% con il solo limite inferiore a −1,35% usando il modello precedente al riallineamento e −0,087% con quello successivo. I due tagli condividono i fotogrammi. Il totale è una misura sui codici grezzi dei pixel alterati, con peso uguale per pixel. Le pose sono flat di laboratorio della stessa sessione. La validità del recupero con saturazione fisica, rumore reale oltre la soglia, sorgenti astronomiche e altri sensori resta aperta.

Il rapporto e il replay coincidono. Le pose di calibrazione e le impronte sono quelle del [confronto precedente](../bkl046-tv4-saturazione-predizione-v1/README.md). [Dataset NASA PDS](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-HRII%2FHRIV%2FMRI-2-GROUND-TV4-V1.0)