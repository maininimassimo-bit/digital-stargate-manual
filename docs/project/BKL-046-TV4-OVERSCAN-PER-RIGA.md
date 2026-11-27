# BKL-046 — Colonne di overscan come riferimento per il rumore di riga

La [sottrazione stimata dai pixel attivi](BKL-046-TV4-RIGA-MASCHERA-DISGIUNTA.md) rimuove anche una componente di segnale diffuso costante lungo la riga. Qui ho stimato la correzione dalle colonne laterali 2–5 e 1018–1021 del medesimo fotogramma, con coordinate FITS a partire da zero. Ho adattato un coefficiente per quadrante usando esclusivamente i dark a otturatore chiuso. Le due metà dei dark sono state scambiate fra stima e verifica. I coefficienti per CLEAR1 sono stati ricavati da tutti i dark, senza usare i frame illuminati per l'adattamento. [Geometria MRI e overclock](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-C-MRI-3%2F4-9P-ENCOUNTER-V2.0)

Con stima per singola riga, la varianza mediana delle somme 16 × 16, divisa per pixel, scende da 11,35 a 5,45 DN² nei dark trattenuti e da 6,87 a 3,58 DN² in CLEAR1 a comando zero. Diminuisce in 48 verifiche su 48 dei dark e in 15 su 16 in CLEAR1. Le verifiche sono coppie per quadrante e condividono la stessa sessione di laboratorio. Il riscontro conserva anche le varianti che raggruppano 4 e 16 righe.

| Gruppo illuminato | Segnale medio centrale | Rapporto mediano varianza corretta su iniziale | Miglioramenti per coppia e quadrante |
| --- | ---: | ---: | ---: |
| CL | −10,1 DN | 0,576 | 15/16 |
| CM | −1,4 DN | 0,666 | 15/20 |
| CN | 29,5 DN | 0,617 | 8/8 |
| CO | 115,6 DN | 0,855 | 11/16 |
| CP | 368,3 DN | 0,975 | 10/20 |
| CQ | 1.231,2 DN | 0,889 | 18/20 |
| CR | 4.088,1 DN | 1,011 | 5/20 |

Il controllo sintetico conserva il profilo esteso iniettato nei soli pixel attivi, con la stessa stima sottratta anche al controllo senza iniezione. Questo verifica la separazione dei calcoli. Non misura la contaminazione ottica dell'overscan. Su tutta la rampa la differenza RMS della correzione media per riga rispetto a CL arriva a 0,160 DN. Il livello e il tempo variano insieme, quindi la causa della differenza resta aperta. [Cohorte a sette livelli](BKL-046-TV4-CLEAR1-SETTE-LIVELLI.md)

L'overscan offre un riferimento utile nelle pose a basso segnale provate. Il vantaggio si riduce e può invertirsi sui frame più luminosi. Prima di usare il metodo per fotometria diffusa restano da qualificare la contaminazione del riferimento, la regola di applicazione e il confronto nativo.

| Evidenza | SHA-256 |
| --- | --- |
| Confronto su dark trattenuti e CLEAR1 con replay | b637f87cd99c6c94f3bee82afffcaa9db74082fe3744866b4789061dda7f7b8f |
| Trasferimento a sette livelli con replay | b3675271524e6fb924aecb3373ce751a644f26a88b4fd69098e40b8a8ee6815e |
| Archivio riletto su H: | b5ea0058174fd793bd4fce9a1e8dc46233b61cf46241167df10a272288e04271 |

Zero chiusure scientifiche e zero esecuzioni native in questo incremento.
