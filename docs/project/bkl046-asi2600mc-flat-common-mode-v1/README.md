# BKL-046 · Contributi a larga scala nella covarianza dei flat ASI2600MC

Il test riproduce le 252 misure sui blocchi completi del rapporto precedente. Confronta tre trattamenti sugli stessi blocchi di verifica: differenza grezza, correzione per un rapporto d'illuminazione stimato nei riquadri esclusi dalla verifica, e rimozione di un piano stimato su blocchi complementari dello stesso riquadro. Le due metà dei blocchi si scambiano i ruoli. [Rapporto sorgente](../bkl046-asi2600mc-calibrator-covariance-v1/README.md)

| Parità Bayer | P95 grezzo | P95 dopo correzione d'illuminazione | P95 dopo rimozione del piano |
| --- | ---: | ---: | ---: |
| B | 1,332 | 1,329 | 1,156 |
| G1 | 1,318 | 1,317 | 1,155 |
| G2 | 1,364 | 1,372 | 1,160 |
| R | 1,128 | 1,127 | 1,118 |

I rapporti confrontano la varianza della somma del blocco con quella stimata usando le sole varianze dei pixel. Il rapporto d'illuminazione stimato varia fino al 3,2% rispetto all'unità. La correzione scalare lascia invariato il numero di casi oltre 1,2. Con la rimozione del piano questi casi scendono da 69 a 8 su 504. Il risultato evidenzia un contributo a larga scala nelle differenze su queste pose. L'origine del contributo e il trasferimento a più dosi o ad altri strumenti restano da verificare. Le misure condividono pose e riquadri. Zero avvii PixInsight e zero chiusure scientifiche.

Replica con Python 3.12, NumPy 2.3.5 e Astropy 7.2.0. Gli argomenti sono il protocollo, il kit precedente estratto, lo ZIP originale dei flat, le dipendenze e la directory di uscita vuota.
