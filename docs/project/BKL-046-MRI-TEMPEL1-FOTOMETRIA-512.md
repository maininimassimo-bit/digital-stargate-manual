# BKL-046 — Fondo e giunzione nei sottoquadri MRI da 512 pixel

Ho acquisito tutte le 60 pose in modalità 2 della [tabella fotometrica NASA](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-C-MRI-5-TEMPEL1-PHOTOMETRY-V1.0), verificando i checksum di 60 FITS RADREV v3 e 60 etichette. Il confronto usa il centro della tabella, i flag PDS e le stesse aperture fra 5 e 30 px di diametro. Su 53 pose è disponibile l'intera curva per tutte e tre le varianti. Le altre sette hanno almeno un'apertura sotto il 98% di supporto e i risultati parziali restano in archivio.

La prima variante usa un unico fondo per riga. La seconda stima le due metà separatamente da fasce distinte. La terza applica anche ai RADREV v3 l'aggiustamento geometrico descritto per la fotometria pubblicata sulle immagini v2. Il confronto riguarda i rapporti normalizzati al diametro 30 px. [Metodo della tabella PDS](https://pds-smallbodies.astro.umd.edu/holdings/dif-c-mri-5-tempel1-photometry-v1.0/document/photometry_report.asc)

| Posizione della posa | Curva completa | Scarto con un fondo per riga | Con due fondi | Con due fondi e aggiustamento geometrico |
| --- | ---: | ---: | ---: | ---: |
| Il diametro 30 px interseca la giunzione orizzontale | 49 | 1,30% | 1,27% | 2,23% |
| Il diametro 30 px interseca solo il confine fra metà laterali | 4 | 3,47% | 3,87% | 3,87% |

Ogni cella di scarto è la mediana degli scarti medi assoluti per posa, calcolati sui sei diametri minori. I due fondi migliorano 26 dei 49 casi alla giunzione orizzontale. Con la variante geometrica aggiuntiva nessuno di questi 49 scarti medi diminuisce rispetto ai due fondi. Nella posa 9000286, la prima verificata lontano dalla giunzione orizzontale, stimare i due fondi porta lo scarto medio da 4,97% a 5,72%. Il solo trattamento del confine non spiega quindi la discrepanza. [Primo confronto PDS](BKL-046-MRI-TEMPEL1-FOTOMETRIA-PDS.md)

Restano da separare le differenze di versione RADREV, la stima del fondo e l'implementazione della correzione usata per produrre la tabella. Il confronto copre la curva normalizzata per queste 60 pose e non qualifica il flusso assoluto o le aperture estese del test a pieno formato.

| Evidenza | SHA-256 |
| --- | --- |
| Cattura dei 60 prodotti | 4c343c2087082eafdd60f1b4156c1ff390abe3a77108cad1b699647c2ed3221c |
| Riscontro e replay identico | 454bf32f64e8070e389a540949063f49aee224afee2ad0f10c1f645c56a3b3ff |
| Archivio riletto su H: | 8b085687c6479c1914d682d5c8147f5365349e799d7f35948198687b14ea2835 |

Zero chiusure scientifiche e zero esecuzioni native in questo incremento.
