# BKL-046 — Trasferimento del profilo PSF WFC3 fra pose P330E

Ho riusato le 22 predizioni con pixel osservati del [controllo sulle lacune fra pose](BKL-046-WFC3-P330E-LACUNE-FRA-POSE.md). Appartengono a 11 coppie di esposizioni in quattro visite. Per ogni direzione ho scelto il piano discreto di fuoco sui pixel validi della posa gemella. Nella posa bersaglio ho trasferito solo l'indice del piano di fuoco, usando la cella della libreria corrispondente al suo sensore e alla sua posizione. Centro, ampiezza e fondo sono stimati usando esclusivamente i pixel di addestramento della posa bersaglio. L'errore è valutato sui pixel di nucleo osservati che corrispondono a lacune DQ nella posa gemella. [Libreria PSF WFC3/UVIS](https://www.stsci.edu/hst/instrumentation/wfc3/data-analysis/psf)

| Banda | Predizioni direzionali | P90 RMS con fuoco locale | P90 RMS trasferendo il fuoco | P90 RMS con profilo standard |
| --- | ---: | ---: | ---: | ---: |
| F438W | 8 | 18,29% | 18,29% | 14,47% |
| F606W | 6 | 13,48% | 13,66% | 11,19% |
| F814W | 8 | 8,06% | 8,17% | 8,07% |

Il denominatore è il picco osservato del nucleo. Il controllo ha riprodotto i 22 RMS del fit discreto locale precedente. Trasferire il piano cambia la scelta in 11 predizioni. Rispetto al fit locale l'errore diminuisce in quattro, aumenta in sette e resta identico negli altri undici casi. In questo campione il trasferimento non migliora il P90 in nessuna delle tre bande.

Le direzioni condividono le stesse coppie e visite. Il confronto riguarda la predizione di pixel effettivamente osservati. Non riempie quelli assenti e non stima colori, integrali fotometrici o il vero fuoco dello strumento. Per generalizzare servono altre acquisizioni e controlli indipendenti di riferimento e incertezza. FILTER_COLOR/3 e PSF_PIXEL/3 rimangono aperti. Zero prove native e zero chiusure scientifiche.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | `74facd735fafa8d247fc7d80601858aefbfa47b87864edb50790a0750df26d97` |
| Programma | `5c0f2efaac3bca481cc216283cc9d02e5388ce7783912da63d937bd1b9783082` |
| Riscontro | `8ba69887e224b1ce02e82bad6e4c441d24b0d175cb73fb19caa312d01229cee6` |
| Archivio riprodotto da H: | `043d01776ed01204cc72a8f5ca5ad4502d8fba62069dbb345e36c4a20cffa88c` |
