# BKL-046 · Trasferimento del controllo TV4 ad altre acquisizioni MRI

Il [riferimento di calibrazione](BKL-046-TV4-RIFERIMENTO-CALIBRAZIONE.md) e le sue soglie derivano ancora dalla sequenza del 2 marzo. Sono stati applicati senza nuova calibrazione a due pose SHUTBLK/CLEAR1 del 3 marzo e quattro pose BIAS/RED del 4 marzo. Tutte hanno MRI in modalità 1, matrice 1024 × 1024, esposizione comandata zero e minimo di 3,5 ms. Quattro record BIAS ricompaiono in due directory PDS. Sono stati contati una sola volta dopo aver verificato i campi di acquisizione e l’identità delle matrici dei pixel. I file originali e le etichette portano impronte distinte e sono conservati. [NASA Planetary Data System](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-HRII%2FHRIV%2FMRI-2-GROUND-TV4-V1.0)

Il test confronta l’accordo fra strisce da solo con l’accordo più il riferimento di calibrazione. I numeri sono i casi accettati che superano il riferimento diagnostico del 5% con entrambe le strisce contaminate su 64 pixel.

| Sessione e operatore | Solo accordo | Con riferimento | Controlli senza iniezione accettati con riferimento |
| --- | ---: | ---: | ---: |
| 3 marzo SHUTBLK, media | 32/40 | 6/40 | 3/5 |
| 3 marzo SHUTBLK, media troncata | 30/40 | 14/40 | 4/5 |
| 4 marzo BIAS, media | 32/80 | 6/80 | 3/10 |
| 4 marzo BIAS, media troncata | 30/80 | 14/80 | 4/10 |

Le sei pose danno tre differenze disgiunte. I 960 esiti includono ripetizioni su regioni, direzioni e iniezioni negli stessi tre contrasti. Il risultato mostra trasferimento parziale del controllo sullo stesso sensore in condizioni diverse, con esiti residui oltre il riferimento e astensioni anche in assenza di iniezione. Il confronto conserva la natura digitale della contaminazione. DIFFUSE_BACKGROUND/3 resta aperto.

| Evidenza | SHA-256 |
| --- | --- |
| Inventario della cattura PDS | 8dff6a428a15692f317a38a8c9331d6ce3b885f45aad37d63f4aab0d8cc714a3 |
| Indice PDS | 20b904e7845615791b4c660399ea6a4870a951ac7ac1c32bd7ed8b16396c4799 |
| Protocollo | 6f5df67d3ab71845042b0d9917d1b2f3d036a75a7b97b37b7f59c4be302de49f |
| Programma | 657526266a924f4af624f330f792fe99985d626864157ee85c02d21869fdeeb5 |
| Riscontro replicato da H: | b8434df013e50957c814e5117a0f42397168f7da86eb25e787850e63c4d259c4 |
