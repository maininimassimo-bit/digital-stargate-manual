# BKL-046 — Confronto ePSF su una nuova posa GO-11880

Il protocollo è stato congelato prima di leggere i pixel della posa indipendente da 40 s `jbb502igq`. Il modello ePSF standard STScI F606W SM4 è interpolato sulla griglia del rivelatore. La verifica confronta ePSF e momenti positivi sulla stessa intersezione di stelle, usando le tessere pari per la stima e le dispari per il controllo. [Modelli ePSF ACS di STScI](https://www.stsci.edu/hst/instrumentation/acs/data-analysis/psf)

| Coppia di chip | Stelle di verifica | P90 con momenti positivi | P90 con ePSF |
| --- | ---: | ---: | ---: |
| 1 → 2 | 49 | 0,1294 px | 0,0618 px |
| 2 → 1 | 56 | 0,1224 px | 0,0603 px |

Il modello ePSF con correzione affine rispetta il limite di 0,1000 px in entrambe le coppie. Le altre coppie hanno supporto insufficiente. Nella coorte da 340 centri, 276 rientrano nelle due coppie qualificate. Il filtro diagnostico trova 183 casi con altri flag DQ, 77 con supporto o ricentraggio insufficiente e 16 con il flag di pieno pozzo. I rimanenti 64 centri sono esclusi dalla copertura univoca o dalla qualifica geometrica della coppia di chip.

La prova qualifica la registrazione sulle stelle di verifica di questa posa. Il controllo di qualità e saturazione non ammette alcun riferimento per le scie esaminate. Nessuna misura indipendente del flusso e nessuna chiusura scientifica.
