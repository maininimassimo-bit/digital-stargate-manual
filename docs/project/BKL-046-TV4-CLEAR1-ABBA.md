# BKL-046 — Sequenza TV4 CLEAR1 con ritorno di esposizione

Dall'indice immutabile TV4 ho selezionato quattro serie FLCL24/CLEAR1 del 2 marzo 2003 nell'ordine A–B–B–A. A vale 7.503,5 ms e B 15.003,5 ms. Il protocollo fissa la prima e l'ultima posa di ciascuna serie, otto in tutto, prima di qualsiasi lettura dei pixel. L'indice riporta un massimo fra 5.422 e 10.454 DN nelle otto pose, sotto la soglia di controllo di 15.000 DN. Il valore d'indice serve alla preselezione. La verifica sulle cinque regioni dei FITS rimane necessaria. [Archivio NASA PDS TV4](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-HRII%2FHRIV%2FMRI-2-GROUND-TV4-V1.0)

Ho calcolato il contrasto sulle quattro serie usando il tempo medio di ciascuna coppia. Le due pose nella stessa serie non sono state contate come repliche indipendenti. La tabella riporta la frazione della norma del contrasto fra esposizioni che resta dopo la proiezione fuori dallo spazio della deriva temporale.

| Deriva ammessa | Contrasto residuo | Gradi di libertà residui |
| --- | ---: | ---: |
| Lineare | 99,92% | 1 |
| Quadratica | 25,06% | 0 |

Con deriva lineare, l'ordine A–B–B–A consente un contrasto quasi ortogonale alla variazione nel tempo. Un termine quadratico assorbe gran parte del contrasto e il fit quadratico esaurisce i gradi di libertà a livello di serie. Con due livelli, il disegno stima al più un contrasto di risposta nelle ipotesi dichiarate. Il catalogo non mostra candidati CLEAR1 del tipo BIAS, SHUTBLK, DRKCOLD o AMB all'interno di questa finestra. Le 24 pose DRKCOLD e le 32 AMB della stessa directory precedono le quattro serie. Restano da acquisire riferimenti indipendenti per illuminazione e fondo.

Il ritiro di FITS ed etichette dagli URL PDS selezionati ha ottenuto zero coppie complete. Il risultato disponibile riguarda il disegno e la sua identificabilità, con zero prove native e zero chiusure scientifiche. DIFFUSE_BACKGROUND/2 resta aperto.

| Evidenza | SHA-256 |
| --- | --- |
| Disegno da indice | `3d2357f89cb63b2428e7943c1ab9980539b314badfe9adfbca1cc4007b2c8856` |
| Riscontro del contrasto | `212629bbeea3636538c48cb695bac2c8e85b270ed62dfe8b94904441c6ff738a` |
| BKL046-TV4-CLEAR1-abba-v1.zip | `1a87cd6d9e95a77f28e8e640338f0d759daca40a51091f83a6fbe11605729dd3` |

Lo ZIP è stato riletto da H: dopo il flush sullo stesso handle. I programmi estratti hanno riprodotto disegno e contrasto a partire dall'indice già conservato.
