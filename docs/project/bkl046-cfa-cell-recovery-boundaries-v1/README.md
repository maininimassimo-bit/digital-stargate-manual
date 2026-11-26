# BKL-046 — Recupero CFA a cella intera e contorni della saturazione

Due scene RAW statiche della Canon EOS 1000D, con 11 e 6 tasselli registrati ammessi. Due pose brevi (0,125 e 0,25 s) stimano il segnale. La posa indipendente da 0,5 s è usata esclusivamente come riferimento di verifica. Le pose bersaglio durano 1 e 2 s. Le quattro fasi RGGB restano separate. La sostituzione a cella intera richiede che tutte le fasi superino i controlli sulle due pose brevi. Il controllo per fase del dossier precedente riproduce conteggi e percentili registrati.

| Scena / posa | Celle parzialmente sature | P90 R/G e B/G per fase | P90 R/G e B/G a cella intera | Coppie al contorno |
|---|---:|---:|---:|---:|
| 1 / 1 s | 1.504 | 3,61% / 11,19% | 2,91% / 3,91% | 116 |
| 1 / 2 s | 855 | 27,30% / 20,90% | 3,86% / 4,12% | 6 |
| 2 / 1 s | 21.964 | 9,60% / 3,23% | 3,51% / 2,61% | 311 |
| 2 / 2 s | 17.290 | 13,45% / 10,05% | 3,78% / 3,50% | 83 |

Il denominatore G è la media delle due fasi verdi. Soglia secca e rampa a cella intera coincidono sulle celle che hanno già raggiunto il plateau. Ai contorni la metrica è il P90 del residuo del gradino di log-rapporto, moltiplicato per 100. Nella scena 2 a 1 s vale 4,75 / 3,22 per fase, 6,13 / 4,20 a cella intera secca e 5,12 / 3,93 con rampa. Nella stessa scena a 2 s vale 4,85 / 5,82 per fase e 6,24 / 6,07 con rampa. Nella scena 1 a 2 s il confronto al contorno dispone di sole 6 coppie. Le celle sotto l'intervallo della rampa restano identiche ai valori registrati. Le statistiche includono le fasi sotto il plateau nelle celle parziali, che in alcuni casi peggiorano anche quando i rapporti migliorano.

La prova documenta il compromesso fra colore interno e discontinuità al bordo su due scene, con un riferimento che assume linearità nell'intervallo selezionato. Rimangono aperti la verifica su dati astronomici, il comportamento dopo demosaic e la prova nativa PixInsight. Zero chiusure scientifiche.

Le copie di replay su H: dei tre dossier sorgente forniscono registrazione, RAW e decoder. Il quarto dossier fornisce il precedente rapporto a posa esclusa. Eseguire verifica.py con gli argomenti in ordine: directory di questo protocollo, registrazione, RAW, directory decoder, directory DLL VC, dossier precedente, percorso del nuovo rapporto. I pin si trovano nei protocolli e nel codice.

[Dataset delle scene RAW](https://doi.org/10.17863/CAM.6881) · [Dossier precedente](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/ef741453da33f6a9212b1923162cb0cf673697d9/docs/project/bkl046-cfa-heldout-exposure-recovery-v1)
