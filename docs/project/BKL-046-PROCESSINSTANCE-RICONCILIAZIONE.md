# BKL-046 · Verifica del padre v600 per la riconciliazione ProcessInstance

Da DSG-Shared, il percorso J: e la condivisione corrispondente espongono lo stesso file del registro di studio. Identità del file, dimensione e SHA-256 concordano con la copia v600 attestata su H:. L’ultimo evento del registro fissa il manifest v600. Il manifest lega la matrice v600 e il registro requisiti v45 alle impronte ricalcolate.

La capsula candidata v46 modifica esattamente sette delle 4.920 righe e conserva tutti i 14.521 criteri. Sei righe registrano l’attestazione circoscritta dei metadati ProcessInstance. Una registra l’esclusione motivata di writeInstanceAddr dall’uso scientifico generale. Le altre 4.913 righe coincidono con il registro v45. Il riscontro è stato riprodotto usando la capsula archiviata su H:.

Le tre versioni verificate del publisher H-staging hanno il vincolo `DOCUMENTARY_OBJECT_DEFINITION_ATTESTATION_ONLY` e un percorso di registro fissato nel profilo del PC principale. La VM può leggere il padre dal suo percorso J:. La pubblicazione richiede un esecutore qualificato per il delta ProcessInstance, con verifica del padre vigente e commit coordinato di registro, matrice e manifest. Lo stato autorevole resta v600 con registro dei requisiti v45. La candidata v46 resta archiviata e le chiusure scientifiche restano zero.

| Evidenza | SHA-256 |
| --- | --- |
| Registro di studio v600 | e63e0bf660c8729ec2b968d17d1a88bfcc8ca23bd0ad86aff7c1a16ff24500b4 |
| Registro requisiti v45 | 3e1e1cb58d9dc705c6e7eb36cd5f1aabcc650995a640340474783663588597c0 |
| Capsula candidata | feac0ac90f56e7482fd71ff25a9e420e7ddc6eae379214a3ae6427310d6071d9 |
| Riscontro riprodotto | 24a9d541d4bfbbe2f6a67b8ca309702ca6e92ca825ba0136661c9715d7504e82 |
