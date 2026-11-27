# BKL-046 · Diagnostica di centro e forma della PSF WFC3/P330E

Il confronto incrocia centro stimato o esatto con forma interpolata o esatta, sulle stesse 1.536 immagini sintetiche della [prova di interpolazione](BKL-046-WFC3-P330E-INTERPOLAZIONE.md). Il fit con sola forma esatta usa la coppia di piani che ha generato il profilo e trasla il modello sulla stessa griglia di centratura degli altri fit. Il fit con solo centro esatto stima il fuoco con l’interpolazione precedente. I due controlli ricevono informazioni disponibili esclusivamente nella simulazione.

| Banda | Segnale in elettroni | P90 con entrambi stimati | Solo centro esatto | Solo forma esatta | Entrambi esatti |
| --- | ---: | ---: | ---: | ---: | ---: |
| F438W | 20.000 | 2,77% | 1,82% | 2,44% | 1,74% |
| F438W | 200.000 | 2,91% | 0,85% | 2,43% | 0,49% |
| F606W | 20.000 | 3,47% | 2,70% | 2,70% | 1,71% |
| F606W | 200.000 | 3,43% | 1,76% | 2,05% | 0,51% |
| F814W | 20.000 | 3,64% | 1,69% | 2,63% | 1,71% |
| F814W | 200.000 | 3,70% | 0,95% | 2,26% | 0,51% |

Tutte le percentuali usano le maschere reali. La sola correzione della forma lascia tutte le bande sopra l’1%. Ad alto segnale il centro esatto porta F438W e F814W sotto il riferimento, mentre F606W resta a 1,76%. I P90 sono statistiche dei singoli fit e le differenze non costituiscono una scomposizione additiva. L’evidenza indica di verificare la centratura su fasi nuove prima della fotometria reale e di conservare una verifica specifica del modello di fuoco in F606W.

Verifica appaiata dei 9.216 esiti precedenti senza differenze nei record e 15.360 esiti totali. Rilettura da H: riprodotta byte per byte. Gli assi FILTER_COLOR/2 e FILTER_COLOR/3 restano aperti. Il test non misura il flusso reale di P330E.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | 3f77aa01101e7e5f62223e295b416889691ab104cc0481b70524ab68a98d31fd |
| Programma | e592302030acf18920f89ab20ed835a4d8effb8219e1aae7670f7c1f185e9366 |
| Verifica | bd23b0e997452e2d1978d49cfa7ad48552aa7a083a453c01231d77ac7edde487 |
| Ricevuta | aa0b9bf2a69ac6079a456182d733b6fba99fd3bec4f87260dbfd705787b69385 |
