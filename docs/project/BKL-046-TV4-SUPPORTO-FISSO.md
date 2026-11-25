# BKL-046 — Supporto fisso nei flat TV4 CLEAR1 e RED

Ho verificato i 1.280 blocchi da 16 × 16 pixel nelle cinque regioni già fissate. Il controllo esclude ogni blocco con almeno un pixel negativo o pari o superiore a 15.000 DN e richiede supporto completo per ogni posa del confronto. Il campione è costituito dalle dieci pose CLEAR1 già acquisite e dalle tredici pose FLBB24/RED della prova precedente. [Archivio NASA PDS TV4](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-HRII%2FHRIV%2FMRI-2-GROUND-TV4-V1.0)

| Integrazione CLEAR1 | Prima serie, valide / disponibili | Seconda serie, valide / disponibili |
| ---: | ---: | ---: |
| 3,5 ms | 2/2 | 1/1 |
| 53,5 ms | 1/2 | 0/2 |
| 503,5 ms | 1/1 | 1/1 |
| 1.003,5 ms | 0/1 | 0/0 |

Le quattro pose CLEAR1 con supporto incompleto perdono 192, 192, 1.085 e 1.280 blocchi. La perdita di tutti i blocchi riguarda la posa disponibile a 1.003,5 ms. Tutte e tredici le pose RED conservano il supporto. La sequenza RED ha però una sola campagna e un ordine di tempi crescente. La copertura geometrica, da sola, non scioglie la confusione fra esposizione e deriva.

Ho individuato come sorgente alternativa le calibrazioni MRI EPOXI, che documentano quattro sessioni con stim lamp e dark. La tabella riassuntiva dei singoli prodotti non era raggiungibile dagli endpoint SBN provati dalla VM. Restano da verificare le esposizioni effettive, i modi, l'eventuale compressione, le mappe qualità dei FITS e la stabilità dell'illuminazione. L'archivio consente di cercare questi controlli, ma la sua descrizione non qualifica la sequenza per la separazione di fondo e risposta. [Archivio NASA PDS EPOXI](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-MRI-2-EPOXI-CALIBRATIONS-V2.0)

DIFFUSE_BACKGROUND/2 resta aperto. L'audit conserva soglia e regioni originali. Zero prove native e zero chiusure scientifiche.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | `bd8c1764127e8dcd10ae669b6fc5629d1b742d9b2845e21219fb21de24b76907` |
| Programma | `28abea8e1481fe6f27b7b64cbdf5960386ec28c479e671a4bd7b0c24b7812e40` |
| Riscontro | `6acf42878ca9751bee410f2707bc325a9dc0863341713d3e6c2a571850e38229` |

Il pacchetto BKL046-TV4-verifica-supporto-v1.zip, SHA-256 `ac9bac53aab33a3782cf523d6547cff0c57572cdd961fa9410daad87739aa6c4`, è stato riletto da H: sullo stesso handle dopo flush. Il programma estratto da quella copia ha rigenerato il riscontro con gli stessi byte a partire dalle immagini già conservate.
