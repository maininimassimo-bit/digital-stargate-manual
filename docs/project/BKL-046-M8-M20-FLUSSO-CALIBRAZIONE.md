# BKL-046 · Effetto dei calibratori sul flusso stellare Bayer

I due gruppi disgiunti da sette dark, flat e dark-flat producono due stime di calibrazione. Ogni misura riusa la stessa posa originale, la stessa parità CFA e la stessa apertura di 6 pixel nativi, con annulus di 9–13 pixel. Il centro è fissato dalla registrazione affine con Huber. Si applicano tutte le combinazioni dark A/B e flat A/B. Si escludono gli stessi pixel saturi o caldi in tutte le combinazioni. Il flusso è la somma dei pixel dell'apertura al netto della mediana dell'annulus. La dispersione dell'annulus è la MAD moltiplicata per 1,4826.

Sono disponibili 3.023 misure appaiate su 54 stelle e 14 pose. Una misura rossa non raggiunge il contrasto minimo. Le percentuali riportano il P90 della differenza relativa simmetrica assoluta rispetto alla combinazione A/A.

| Parità | Misure | Flusso, solo flat | Flusso, solo dark | Flusso, entrambi | MAD dell'annulus, entrambi |
| --- | ---: | ---: | ---: | ---: | ---: |
| R | 755 | 1,95% | 0,43% | 1,92% | 13,12% |
| G1 | 756 | 1,25% | 0,36% | 1,28% | 10,31% |
| G2 | 756 | 1,25% | 0,36% | 1,30% | 10,07% |
| B | 756 | 1,25% | 0,55% | 1,24% | 10,85% |

Il cambio dei flat produce la maggiore variazione del flusso in tutte le parità. Cambiando entrambi i calibratori, ogni parità supera la soglia diagnostica dell'1% al P90. Le 3.023 misure condividono stelle, pose e calibratori. La MAD dell'annulus include la struttura del fondo e non isola il rumore elettronico. La prova quantifica la sensibilità ai due gruppi da sette sulla stessa esposizione. Non misura l'errore assoluto della calibrazione completa o il risultato dopo demosaicizzazione e ricostruzione. Zero chiusure scientifiche e zero avvii nativi.

SHA-256 della ricevuta `82198e82179b377b50d5a6af55bdeb76423583e9d3f8cbf5abd2423b3ade9420`.
