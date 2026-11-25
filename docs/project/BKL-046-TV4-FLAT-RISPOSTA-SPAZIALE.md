# BKL-046 · Offset additivo e risposta spaziale nei flat TV4 RED

La prova usa 13 pose MRI FLBB24/RED del 4 marzo 2003, tutte in modalità 1 e con matrice 1024 × 1024. La selezione segue l’ordine di acquisizione nell’indice PDS, su un solo percorso per pose che possono comparire in più directory. Sei pose con integrazioni di 13,5, 103,5 e 1003,5 ms sono usate per stimare i modelli. Sette pose sono riservate, incluse quattro a 33,5 e 303,5 ms, tempi esclusi dalla stima. [Archivio TV4 NASA PDS](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-HRII%2FHRIV%2FMRI-2-GROUND-TV4-V1.0)

Il confronto usa medie di blocchi 16 × 16 su cinque regioni fisse, per 1.280 blocchi per posa. Ogni modello predice i DN come intercetta più risposta per millisecondo moltiplicata per l’integrazione. Intercetta e risposta possono essere comuni o variare per blocco.

| Modello | RMSE sui due tempi riservati, DN | RMSE sulle ripetizioni riservate, DN |
| --- | ---: | ---: |
| Intercetta e risposta comuni | 22,88–37,52 | 22,05–88,81 |
| Intercetta spaziale, risposta comune | 6,20–25,64 | 20,56–47,78 |
| Intercetta comune, risposta spaziale | 13,17–20,84 | 2,49–21,20 |
| Intercetta e risposta spaziali | 0,53–2,02 | 0,75–1,25 |

Nel modello congiunto, il 5°–95° percentile delle intercette è 385,95–439,07 DN e quello delle risposte è 5,31–5,53 DN/ms. L’intercetta è stimata per estrapolazione e la risposta comprende l’illuminazione del banco e il sistema ottico. La prova verifica la capacità predittiva sulla sequenza di flat, lasciando aperte la calibrazione indipendente dei termini fisici, la separazione su dati scientifici e la prova nativa di DIFFUSE_BACKGROUND/2.

| Evidenza | SHA-256 |
| --- | --- |
| Inventario delle pose e delle etichette | c29dbda2102048f9e3f4f190c5e6872fcc5ed797aac93f718ca430bd3d72d6fa |
| Protocollo | 81748911840a7a64b9937a7ff8e57bb7b1a87081c48dfd3f3ad786428d339bb2 |
| Programma | 16b622b549bea0d5745e7601fd33b6592169eb8d873436585865f0e53635458d |
| Riscontro replicato da H: | 0f4bce3f967101ab1dbd6ea1cc8e179932640ae3d30ebd2028bf8d0f39a0f3b2 |
