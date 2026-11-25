# BKL-046 · Confronto fra BIAS RED e intercetta dei flat TV4

La prova confronta il profilo spaziale dell’intercetta stimata sui [flat RED](BKL-046-TV4-FLAT-RISPOSTA-SPAZIALE.md) con la media di quattro pose BIAS/RED separate del 4 marzo. Le pose BIAS sono in modalità MRI 1 con esposizione comandata zero. La selezione e la deduplicazione delle quattro pose sono documentate nella [rilettura delle sessioni successive](BKL-046-TV4-TRASFERIMENTO-ACQUISIZIONI.md). I due insiemi sono disgiunti e usano gli stessi 1.280 blocchi.

Centrando le due mappe sulla propria media, l’RMSE fra BIAS e intercetta è **0,57 DN**. Le quattro mappe BIAS singole differiscono dalla loro media di 0,21–0,28 DN RMS. Per testare il trasferimento, la prova fissa l’offset alla media dei BIAS e stima la risposta dai sei flat di calibrazione. Una variante consente un solo spostamento comune della mappa BIAS, stimato sugli stessi sei flat, pari a **+29,03 DN**. Le sette pose riservate restano quelle della prova precedente.

| Modello | RMSE nei flat a tempi riservati, DN | RMSE nelle ripetizioni riservate, DN |
| --- | ---: | ---: |
| Offset e risposta spaziali stimati sui flat | 0,53–2,02 | 0,75–1,25 |
| Mappa BIAS misurata senza spostamento comune | 20,66–27,81 | 2,74–28,03 |
| Mappa BIAS con spostamento comune stimato | 0,58–2,13 | 0,76–1,25 |

La mappa BIAS e l’intercetta dei flat hanno forma spaziale simile sul campione, con un livello assoluto diverso. La correzione comune recupera gran parte della capacità predittiva sui flat. La causa fisica dello spostamento resta da isolare, così come il trasferimento a scene scientifiche e ad altre configurazioni. I 28 risultati precedenti coincidono con quelli ricalcolati. DIFFUSE_BACKGROUND/2 resta aperto.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | 8094f777fa72d4475adfd8cc7aa6a9e924d022cd4bf1a22f462ae5c0947befc9 |
| Programma | 639c4349be18afb2bfefc7209e8c8bf67922041a7f8022452049477277641e52 |
| Riconciliazione del confronto appaiato | 28b4534373ee527b3def857b05d84c5f682d5ef1a33a0b4ba6eef7937161f103 |
| Riscontro replicato da H: | 2b573af900a37c3c951b07801f38e9d5b591048e47d54e9704a19be30f2474d5 |
