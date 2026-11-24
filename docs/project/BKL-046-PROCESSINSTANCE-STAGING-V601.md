# BKL-046 · Preparazione isolata dell’incremento ProcessInstance v601

La prova su DSG-Shared parte dalla copia attestata del registro di studio v600, dalla matrice e dal manifest v600 e dalla capsula candidata v46. Verifica le singole impronte prima di preparare i file. Il delta aggiunge l’attestazione a sette righe della matrice e conserva le altre 4.913 righe e tutti i 14.521 criteri. Le attestazioni mantengono l’ambito circoscritto dei sei contratti di metadati e l’esclusione motivata dell’API interna.

La proposta comprende il registro requisiti v46, la matrice v601, il delta, il manifest v601 e la proposta di registro di studio. Il manifest conserva i record ereditati e collega i tre nuovi artefatti mediante SHA-256. Il puntatore proposto fissa lo SHA-256 del manifest. La verifica ha riletto i nuovi file e respinto un padre diverso, una nuova esecuzione in una directory già esistente, un artefatto assente e uno modificato.

Il collaudo opera su una replica isolata. La rilettura attuale copre i tre nuovi artefatti e il collegamento fra manifest e puntatore simulato. Per la pubblicazione servono ancora la verifica dei file ereditati, la qualifica del blocco condiviso con il publisher e del recupero dopo interruzione, e la riconferma del padre vigente. Il registro autorevole continua a puntare a v600.

| Evidenza | SHA-256 |
| --- | --- |
| Riscontro replicato con il programma archiviato su H: | 4377458cc1508c81d64969650f5d0b70d5237808ae19f747dd0c0d90b2d02b5c |
| Archivio dei cinque file isolati riletto da H: | 5cf38fcb0aefe9188e2d382eaf0bcf2fa0a718094c3cbdd94f543720d85f2c9a |
