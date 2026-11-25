# BKL-046 — Copertura delle decisioni di distribuzione v1.171

Il manifesto lega la capsula originale a 2.953 unità di revisione. Sono 2.712 occorrenze di record, riferibili a 2.526 impronte sorgente, e 241 sezioni esterne all'elenco dei record. Ogni unità è identificata con posizione, numero di byte e SHA-256. Le segnalazioni preesistenti riguardano 178 occorrenze e 18 sezioni. La decisione sull'intero documento rimane necessaria anche per le unità prive di segnalazioni.

Il controllo richiede una decisione proveniente dal canale autorizzato e legata alla capsula, al manifesto completo, all'identificativo immutabile della destinazione privata e all'impronta dei destinatari. Un'approvazione di unità include l'impronta della relativa motivazione. Il controllo verifica copertura e riferimenti ai byte. L'esame delle motivazioni e l'autorità di approvazione spettano ai revisori.

Il collaudo usa decisioni sintetiche e 16 casi. Una decisione assente, trattenuta o negativa lascia la copertura incompleta. Il programma respinge un manifesto ridotto anche se coerente con il pin di prova, i byte sostituiti, i duplicati, lo scambio di destinazione e la mancanza di motivazione. Il pacchetto riletto da H: ha rigenerato manifesto e riscontro byte per byte.

| Evidenza | SHA-256 |
| --- | --- |
| Manifesto delle 2.953 unità | `bf8c953f16e73edeba21e72b3c8ce076cf126a92d18f40b5e5854a86751a73c1` |
| Riscontro delle prove | `d0eb025c540c4c1584dc7079483a1234a33ec56bc39ea3df3fb8da1fd7be395b` |
| Archivio `BKL046-v1171-copertura-decisioni-v1.zip` | `f807be9a4651d9ebf54d56ff6f724f36c7921d5f6305ba7ac588fb3d0715ac11` |

La copertura operativa è ancora 0/2.953. Restano la decisione autentica sul perimetro e sulla destinazione, la pubblicazione autorizzata e la rilettura GitHub dell'asset e delle dipendenze. Il risultato mantiene v1.171 come baseline intermedia.
