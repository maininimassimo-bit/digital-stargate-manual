# BKL-046 · Propagazione della varianza nei 32 canali Roman H4RG

Il confronto usa gli stessi segmenti MAST della prova precedente. Per ciascun canale di lettura misura una finestra centrale da 64 × 64 pixel all’interno delle 64 righe acquisite. La maschera di ogni canale esclude i valori agli estremi della codifica a 16 bit rilevati in una qualsiasi delle 20 esposizioni e delle quattro letture. Uno dei blocchi 2 × 2 in uscita è escluso se il suo supporto 3 × 3 in ingresso interseca la maschera. La varianza in ingresso usa l’unione dei supporti conservati. [Dati Roman di laboratorio](https://archive.stsci.edu/missions-and-data/roman/wfi-triplet-test-data)

Sette canali contengono almeno un pixel al limite di codifica. Il supporto residuo è fra 941 e 961 blocchi per canale, oltre la soglia congelata di 769. Il canale con indice 15 conserva 957 blocchi su 961 e fornisce 30 confronti con la nuova maschera. I 60 confronti validi del rapporto precedente riproducono i risultati di varianza e di errore.

| Lettura | Confronti | Errore mediano con pesi completi | Errore mediano con stima diagonale | Canali con errore mediano minore usando i pesi completi |
| --- | ---: | ---: | ---: | ---: |
| 1 | 320 | 25,4% | 66,9% | 32/32 |
| 5 | 320 | 15,5% | 62,4% | 32/32 |
| 10 | 320 | 13,8% | 61,7% | 32/32 |

Ogni canale usa la stessa fascia di righe e le stesse coppie. Le letture di ciascuna esposizione condividono il riferimento iniziale. La copertura riguarda i 32 canali su quella fascia del rivelatore in configurazione di laboratorio. Restano da verificare la sensibilità alla posizione lungo le colonne di lettura, una dose misurata indipendentemente, la serie ASI2600MC a più dosi e gli operatori nativi.

Per riprodurre, passare a `misura.py` la directory estratta dell’[archivio della prova precedente](../bkl046-roman-gain-ramp-covariance-v1/README.md), la directory delle dipendenze NumPy e Astropy, un nuovo percorso di rapporto e `protocollo.json` di questa prova. L’archivio precedente ha SHA-256 `e9da7238075250b17b45119353680ad23f1811d601e93f75c8897b0b7df52eb1`.