# BKL-046 — Controlli ACS/WFC F555W pre-SM4 su standard CALSPEC

La ricerca MAST per G191B2B, GD153, GD71 e GRW+70D5824 restituisce 35 voci pre-SM4. Le voci includono sia aggregati sia prodotti associati. Le 19 associazioni originali riportano due immagini FLT ciascuna nel catalogo dei prodotti. Tutti i 38 file selezionati hanno dimensione concorde con MAST e SHA-256 nel manifest.

Il primo tentativo centra i riquadri usando la posizione SIMBAD propagata con il moto proprio e una ricerca di otto pixel nella WCS dell'immagine. Solo tre riquadri superano i filtri geometrici e DQ. Uno dei tre contiene un massimo locale di circa 11 elettroni e la stella luminosa cade fuori dalla finestra. Il primo rapporto resta nel dossier per rendere riproducibile questo errore di selezione.

La seconda verifica usa i due FLT di ciascuna associazione. Cerca, entro 100 pixel per asse dalla previsione WCS, la coppia di picchi non flaggati che massimizza il minore dei due valori. Ogni picco deve avere almeno 5.000 elettroni e le posizioni devono concordare entro due pixel. Il controllo richiede inoltre SNR di apertura nominale almeno 100, supporto nelle ali in tutti gli otto settori e zero flag full well e ADC entro tre pixel.

| Standard | Associazioni con entrambi i riquadri conformi | Fotogrammi conformi |
|---|---:|---:|
| G191B2B | 2 | 4 |
| GD153 | 3 | 6 |
| GD71 | 4 | 8 |
| GRW+70D5824 | 10 | 20 |

Le due immagini di un'associazione condividono puntamento e sorgente. Le 38 immagini rappresentano quattro stelle, quindi i conteggi per immagine non costituiscono 38 controlli stellari indipendenti. Il campione qualifica centri e geometrie per un fit successivo. L'uso dei bersagli come standard fotometrici non fornisce limiti individuali di esclusione di compagne, e i campi differiscono per affollamento e fondo da Orione. Non sono state assegnate etichette negative, né eseguiti fit, avvii nativi o chiusure scientifiche.

I report conservano posizioni nel subarray e nel chip ottenute sottraendo LTV con LTM unitario, offset dalle previsioni, indicatori DQ, SNR e impronte dei riquadri. I dati FLT e le risposte dei cataloghi sono nell'archivio privato H:. [Standard fotometrici ACS](https://doi.org/10.3847/0004-6256/152/3/60) · [Struttura ACS e keyword del subarray](https://hst-docs.stsci.edu/acsdhb/chapter-2-acs-data-structure/2-4-headers-and-keywords)
