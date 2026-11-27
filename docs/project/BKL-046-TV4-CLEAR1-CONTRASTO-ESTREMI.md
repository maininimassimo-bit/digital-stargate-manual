# BKL-046 — Contrasto fra due esposizioni TV4 CLEAR1

Ho verificato cinque pose FLAT24/CLEAR1 del 27 febbraio 2003 già conservate. A 3,5 ms sono disponibili due pose della prima serie e una della seconda. A 503,5 ms è disponibile una posa per serie. Tutte rispettano il controllo originale nelle cinque regioni, per 1.280 blocchi da 16 × 16 pixel per immagine. La scelta mantiene i due tempi con supporto completo in entrambe le serie nell'insieme acquisito. Il tempo di 53,5 ms resta escluso dal confronto per il controllo fallito in tre pose. [Archivio NASA PDS TV4](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-HRII%2FHRIV%2FMRI-2-GROUND-TV4-V1.0)

| Seconda serie meno prima | Differenza media, DN | RMS sui blocchi, DN |
| --- | ---: | ---: |
| A 3,5 ms | −66,20 | 66,21 |
| A 503,5 ms | −3.956,95 | 3.957,24 |
| Differenza fra i due contrasti | −3.890,74 | 3.891,04 |
| Fra le due pose della prima serie a 3,5 ms | −0,25 | 0,76 |

Sostituendo la media delle prime due pose a 3,5 ms con ciascuna singolarmente, la differenza fra i contrasti varia da −3.890,87 a −3.890,62 DN. Una sola mappa additiva per il cambio di serie, invariabile con il tempo d'integrazione, produrrebbe differenza nulla per gli stessi blocchi. In questo campione quella descrizione è insufficiente.

L'equivalente pendenza fra i due tempi cambia in media di −7,78 DN/ms. Con due soli livelli il valore è un contrasto empirico. L'illuminazione, la temperatura del banco e del CCD, la corrente oscura dipendente dal tempo e la risposta del sensore possono contribuire al risultato. I blocchi condividono le stesse cinque pose e a 503,5 ms è disponibile una sola posa per serie. Il risultato è descrittivo e lascia aperti il controllo temporale A–B–B–A, il riferimento indipendente di dose ottica e la prova nativa. DIFFUSE_BACKGROUND/2 resta aperto.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | `dfdec83a2c1c392511e1d31c59b7ae847e4caa23b9f912da09e664ca87747c84` |
| Programma | `97d4e5331ea1b4e22eadd82602287e889263a880c289417e2786654a4e3424d5` |
| Riscontro | `0ffeba29cd42ff2ea9e63c74ecf42bbcd496137215de38460ecb7c9d76d03bef` |
| Archivio riprodotto da H: | `0b3729acb6a5287f7d8c40cb3443ef6bd0a109367f312f2274b697f87695275c` |
