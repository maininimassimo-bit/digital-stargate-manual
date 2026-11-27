# BKL-046 — Confronto TV4 CLEAR1 a esposizione ripetuta

L'indice TV4 identificato dallo SHA-256 `20b904e7845615791b4c660399ea6a4870a951ac7ac1c32bd7ed8b16396c4799` contiene 279 record MRI FLAT24/CLEAR1 in modalità 1 per la directory esaminata del 27 febbraio 2003. Raggruppando i record consecutivi per integrazione emergono 32 serie. Il disegno congela la prima e l'ultima posa di due serie per ciascuno dei tempi comuni 3,5, 53,5, 503,5 e 1.003,5 ms. Include altre due pose del ritorno a 1.003,5 ms. Le temperature CCD indicizzate delle serie selezionate sono 255,785–256,009 K nella prima e 241,109–241,405 K nella seconda, quindi il contrasto fra serie non isola la temperatura. [Archivio NASA PDS TV4](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-HRII%2FHRIV%2FMRI-2-GROUND-TV4-V1.0)

La cattura ha prodotto 10 coppie FITS/etichetta verificabili su 18. Le richieste restanti hanno avuto timeout di connessione o negoziazione TLS. Il solo tempo con entrambe le coppie complete è 53,5 ms. Nelle cinque regioni predefinite, tre pose su quattro contengono pixel a partire dalla soglia di esclusione di 15.000 DN. I massimi raggiungono 16.133 DN nella prima serie e 16.131 DN nella seconda. Il confronto ha quindi applicato la regola di astensione prevista. Queste soglie identificano il supporto escluso dal protocollo. Da sole non stimano il livello di saturazione del sensore.

Il disegno conserva gli input mancanti e il controllo di ritorno. Questa selezione non qualifica la stima separata dei termini additivo e moltiplicativo. Per una prova successiva serve una sequenza con livelli ripetuti, supporto valido in tutte le pose e misure indipendenti dell'illuminazione. DIFFUSE_BACKGROUND/2 resta aperto. Zero prove native e zero chiusure scientifiche.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo congelato | `6072e98a59cebeeaaf8b3ab330d970f729c9943af45cda207d49b5f8231159aa` |
| Inventario dopo il recupero | `ab2d5e8da01e71b8f7b4833c9932834718586e5b4220242fced9eabd2410f552` |
| Rilettura delle dieci coppie | `5517d9b6b1988529b7b8ddb34893b58c5b558e714ce0159603ba1ca0bb8060c4` |
| Riscontro a 53,5 ms | `2fd8e8414778bca177a2aec7e2c40043928fde40b809a638964a8cf2b35838ce` |

Il pacchetto BKL046-TV4-CLEAR1-ripetizioni-53ms-replay.zip contiene le dieci coppie verificate, il disegno, i programmi e i riscontri. Lo SHA-256 `f513adeaf4b4680103345fa253c821bd8480938c86874b888db017d4c20e1d3d` coincide tra la copia su O: e la rilettura su H: eseguita attraverso lo stesso handle dopo flush. La riesecuzione dalla copia su O: ha riprodotto le due ricevute byte per byte.
