# BKL-046 — Controllo di overscan del contrasto TV4 CLEAR1

Ho riprodotto il [contrasto fra esposizioni](BKL-046-TV4-CLEAR1-CONTRASTO-ESTREMI.md) sulle stesse cinque pose FLAT24/CLEAR1, con le stesse regioni e gli stessi 1.280 blocchi. Per ogni posa ho calcolato separatamente quattro mediane di overscan seriale e quattro di overscan parallelo, usando le strisce conservative già fissate per [TV4 RED](BKL-046-TV4-OVERSCAN-RED.md). Ogni mediana è assegnata ai blocchi del quadrante corrispondente. Ho misurato il contrasto fra esposizioni prima e dopo la sottrazione di ciascun riferimento. Le righe parallele possono risentire del trasferimento di carica. [Calibrazione dello strumento Deep Impact](https://archive.stsci.edu/files/live/sites/mast/files/home/missions-and-data/epoch-1/_documents/calibration_paper_draft.pdf)

| Riferimento sottratto | Contrasto medio residuo, DN | Riduzione del valore medio assoluto |
| --- | ---: | ---: |
| Nessuno | −3.890,74 | — |
| Overscan seriale | −3.886,87 | 0,10% |
| Overscan parallelo | −3.824,49 | 1,70% |

Le due sottrazioni lasciano pressoché intera la variazione tra serie che cresce con l'esposizione. Questo restringe il ruolo dei due riferimenti per quadrante sul campione esaminato. Restano da stimare eventuali componenti elettroniche che queste strisce non catturano, corrente oscura, stabilità della dose ottica e risposta del sensore. Il controllo non replica la calibrazione di missione. DIFFUSE_BACKGROUND/2 rimane aperto, con zero prove native e zero chiusure scientifiche.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | `9fca8f414d0bd708c7232f8b1deacd2aea13e630c5788cecb29dc8b93ca595b6` |
| Programma | `df6a132701a749b849adc0e4276f315ede5cd9d579a86b2c6ba1980c12ca6ac1` |
| Riscontro | `929bcca067729fb2106dc0d1092ab9a79f07e5c372d4b344b05c9a592afc3dde` |
| Archivio riprodotto da H: | `3bd6c64ed4280f0e23124cc12ecbf2ca1bc7e1b860a6b588bf5c3cc01bcf8dac` |
