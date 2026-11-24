# BKL-046 · Correzione astrometrica delle pose brevi spostate GO16380

La [prova iniziale](BKL-046-GO16380-POSE-SPOSTATE.md) aveva trovato 118 sorgenti nel passaggio dal sensore 2 di A40 al sensore 1 delle pose spostate. Il presente controllo stima una correzione di semina per ciascuna posa spostata correlando i soli tasselli pari di A40. Richiede almeno quattro tasselli concordi con una maggioranza stretta. In entrambe le pose hanno concordato tutti e otto i tasselli utilizzabili, con uno spostamento di −1 e −3 pixel nel sistema A40. La correzione è usata per misurare i centroidi sui pixel originali. La conferma della coppia resta a 0,7 pixel nel sistema A40.

| Sensore di origine | Coppia originale, stima / verifica | Coppia spostata, stima / verifica | Unione per sorgente, stima / verifica | Tasselli nell'unione, stima / verifica |
| --- | ---: | ---: | ---: | ---: |
| 1 | 20 / 23 | 0 / 0 | 20 / 23 | 11 / 11 |
| 2 | 17 / 20 | 9 / 11 | 25 / 28 | 13 / 12 |

Fra le venti coppie valide nelle pose spostate, sedici corrispondono a sorgenti respinte per DQ in A40, otto nella stima e otto nella verifica. Il sensore 2 supera la soglia di copertura di 24 stelle e 8 tasselli per partizione considerando l'unione delle due coppie. Il sensore 1 è fuori dal campo delle pose spostate e resta sotto la soglia. La prova riguarda la disponibilità di riferimenti. Resta da verificare l'accuratezza assoluta dei centroidi e la copertura dei casi appaiati nelle pose profonde.

L'asse `SATURATION_BLEND/4` resta aperto. Nessuna modifica alle maschere o ai pixel scientifici, prova nativa o chiusura scientifica.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Protocollo | `7ec5956b0300544c3991fc758c4159c5853244bb93b7bbaf20d0308c772a7505` |
| Programma | `328b550b836823e71887eb97783f9fc46d8026348dbc3a4a480780a988b5c7dc` |
| Ricevuta per sorgente e tassello | `c2fdfdbe058ad67c934a11cba434bde0fdd3049248ee7b0356153f26eddd0e99` |
