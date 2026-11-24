# BKL-046 · Sensibilità della fotometria PSF alle lacune DQ di P330E

La prova usa i 24 campi DQ delle [visite P330E successive](BKL-046-WFC3-P330E-SUPPORTO-DQ.md) e le PSF empiriche WFC3/UVIS della libreria STScI. Il modello di fit è il profilo standard nella posizione fiduciale più vicina del sensore. I profili iniettati provengono dalle alternative della libreria a fuoco variabile. Il protocollo usa quattro fasi subpixel, posizione nota, apertura di raggio 10 pixel e nessun rumore. Normalizza ogni profilo all'integrale nella stessa apertura e stima ampiezza e fondo. Il confronto usa tutti i campioni oppure esclude quelli con DQ diverso da zero. Nessun pixel osservato viene sostituito. [Libreria PSF WFC3](https://www.stsci.edu/hst/instrumentation/wfc3/data-analysis/psf)

| Banda | Casi | P90 errore di flusso, supporto completo | P90 con maschere DQ | P90 dell'errore aggiunto dalle maschere | Massimo errore aggiunto dalle maschere |
| --- | ---: | ---: | ---: | ---: | ---: |
| F438W | 320 | 14,77% | 15,24% | 0,86% | 10,14% |
| F606W | 288 | 21,00% | 21,04% | 0,76% | 10,56% |
| F814W | 320 | 18,86% | 18,78% | 0,48% | 7,61% |

Con profilo iniettato uguale al modello, i controlli appaiati recuperano il flusso entro la tolleranza numerica fissata. L'errore nei casi a fuoco variabile è già presente con supporto completo. Le maschere aggiungono errori importanti in singoli casi. I 928 casi riutilizzano maschere e profili e non sono acquisizioni indipendenti. La visita con un'identità del picco incerta contribuisce soltanto come maschera al test sintetico.

Il protocollo non identifica il fuoco effettivo di P330E e non misura il flusso delle visite archiviate. `FILTER_COLOR/2` e `FILTER_COLOR/3` restano aperti. Nessuna prova nativa o chiusura scientifica.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Protocollo e impronte delle sei librerie | `40604f833187cc8335169e34f64b0ce685f139c2f7e2ced6775e3fdc00f150ee` |
| Programma | `142b33150928ae436f360825db11b26d8f483fe24abc03a9c90acaf7ff5b646c` |
| Ricevuta dei 928 casi | `164bcdfba45b918277fb1e2883affaee407b39374f03b6d3e2db2e0f23c6d0ed` |
