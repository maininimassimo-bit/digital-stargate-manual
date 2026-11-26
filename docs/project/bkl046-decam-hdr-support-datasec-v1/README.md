# BKL-046 · Supporto delle pose brevi DECam M8/M20

Nel ritaglio M8 da 100 s, 163.944 campioni della sezione scientifica raggiungono o superano il livello nominale del proprio amplificatore. Nella posa da 30 s, **158.183 (96,49%)** delle loro posizioni proiettate hanno i quattro campioni circostanti non nulli e sotto il minore dei due livelli nominali. Anche chiedendo 16 campioni sotto l'80% di quel livello si ottengono 155.514 posizioni (94,86%). La posa da 45 s della stessa notte non fornisce alcun supporto a quattro campioni per queste posizioni.

| Posa di origine M8 | Posa di confronto | Campioni di origine al livello nominale o sopra | Quattro campioni utili | Sedici campioni sotto l'80% |
| ---: | ---: | ---: | ---: | ---: |
| 100 s | 45 s | 163.944 | 0 | 0 |
| 100 s | 30 s | 163.944 | 158.183 | 155.514 |
| 45 s | 30 s | 164.565 | 158.748 | 156.026 |

Tre ritagli estesi di NOIRLab contengono l'intero CCD, con 4.146 righe e 2.160 colonne. Tutti i campioni dei ritagli piccoli coincidono esattamente con le rispettive sottoarray. Questa verifica stabilisce l'origine sul CCD e permette di applicare DATASEC, DATASECA e DATASECB. Il centro di catalogo M8 cade nella sezione scientifica della posa da 30 s e fuori da quella dei ritagli da 45 e 100 s. Nella posa da 100 s, 34.776 dei 35.397 codici zero sono fuori da DATASEC. Restano 621 zeri nella sezione scientifica, esclusi dai campioni utilizzabili.

Il rapporto sulle impronte geometriche conserva anche le proiezioni prima del filtro DATASEC. Per M20, tutti i 395 e 394 campioni più luminosi dei due ritagli da 180 s hanno supporto a 16 campioni nella posa da 30 s secondo il WCS. L'incremento M8 con DATASEC non estende questo controllo alle sezioni dei CCD di M20.

La posa M8 da 30 s usa un altro CCD e un'altra data. Le proiezioni usano le coordinate TPV degli header e conservano separatamente copertura e soglie. La convalida sul cielo richiede stelle misurate sul supporto comune, compatibilità delle PSF, calibrazione e confronto fotometrico. Il supporto trovato riguarda le posizioni della parte di campo effettivamente ripresa nei ritagli. Zero avvii PixInsight e zero chiusure scientifiche.

Per ripetere, usare il kit di verifica DECam precedente con i ritagli piccoli e questo kit con i ritagli completi. `misura.py` riceve protocollo, directory del kit precedente, directory delle dipendenze e un nuovo percorso di uscita. `verifica-sezioni.py` riceve la directory di questo kit, la directory precedente, NumPy 2.3.5/Astropy 7.2.0 e un nuovo percorso di uscita. I ritagli estesi usano gli URL del rapporto precedente con SIZE pari a 0,5 gradi per asse. [Riferimenti DECam e provenienza](../bkl046-m8-m20-decam-hdr-reference-screen-v1/README.md) · [NOIRLab Astro Data Archive](https://astroarchive.noirlab.edu/)
