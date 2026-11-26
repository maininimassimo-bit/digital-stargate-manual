# BKL-046 — Recupero CFA dopo il demosaic bilineare

Confronto su due scene statiche RAW Canon EOS 1000D. Due pose brevi (0,125 e 0,25 s) stimano il recupero delle pose da 1 e 2 s. Una posa indipendente da 0,5 s fornisce il riferimento. Lo stesso demosaic bilineare ricostruisce tutte le stime e il riferimento. I pixel sono ammessi quando tutti i fotositi della finestra 3×3 superano i controlli sulle pose brevi e sul riferimento. La verifica riproduce anche tutte le misure del dossier precedente prima del demosaic.

| Scena / posa | Pixel in celle parzialmente sature | P90 R/G e B/G per fase | P90 R/G e B/G a cella intera |
|---|---:|---:|---:|
| 1 / 1 s | 1.106 | 2,61% / 10,82% | 10,61% / 12,80% |
| 1 / 2 s | 342 | 13,83% / 20,34% | 18,14% / 24,60% |
| 2 / 1 s | 38.657 | 9,70% / 3,00% | 8,38% / 7,88% |
| 2 / 2 s | 14.680 | 14,25% / 9,98% | 17,07% / 15,22% |

Nella scena 2 a 2 s, quando ogni cella toccata dalla finestra 3×3 soddisfa il controllo sulle quattro fasi brevi, il P90 scende da 15,63% / 9,67% a 3,15% / 2,70% (1.975 pixel). Quando almeno una cella vicina non soddisfa quel controllo, il P90 sale da 13,98% / 10,01% a 18,68% / 16,18% (12.705 pixel). La stratificazione diagnostica una dipendenza dalla copertura locale delle pose brevi e usa lo stesso supporto per confrontare i metodi.

Nella scena 2 a 1 s, su 238 coppie contigue attraverso i contorni, il P90 del residuo del gradino di log-rapporto moltiplicato per 100 passa da 2,80 / 2,08 per fase a 3,35 / 2,86 a cella intera secca e a 3,14 / 2,52 con la rampa. Nella scena 1 a 2 s soltanto due coppie superano il criterio sul vicinato. Per questa combinazione il risultato al contorno resta poco informativo. Il test controlla sia la ricostruzione esatta di piani affini sia la risposta spaziale a un impulso rosso.

Il risultato riguarda il demosaic bilineare e due scene statiche. Il riferimento ha lo stesso interpolatore e assume linearità nell'intervallo selezionato. Zero chiusure scientifiche. Restano aperti i riferimenti astronomici indipendenti e la qualifica nativa.

Eseguire verifica.py passando, nell'ordine, directory del protocollo, directory di registrazione, directory RAW, directory decoder, directory DLL VC, dossier a posa esclusa, dossier a cella con contorni e output JSON. Le impronte sono nel protocollo e nei protocolli sorgente. L'archivio contiene codice, protocollo, rapporto e questa descrizione.

[Dataset RAW](https://doi.org/10.17863/CAM.6881) · [Studio precedente](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/35f745126bc2e6c741028df44fd6e3b7bd1fec8a/docs/project/bkl046-cfa-cell-recovery-boundaries-v1) · [Descrizione del demosaic bilineare](https://www.ipol.im/pub/art/2011/g_mhcd/article.pdf)
