# BKL-046 · Ricostruzioni alla stessa scala in NGC 5986

Due pose ACS/WFC F606W di 350 s, `j9l915ooq` e `j9l915oqq`, sono proiettate su ritagli della griglia nativa della posa `j9l915oiq`, con lo stesso passo di un pixel. Due larghezze di impronta quadrata, 1,00 e 0,70 pixel, usano gli stessi centri previsti, la stessa media a pesi uguali e lo stesso supporto. Si applicano traslazioni locali. I conteggi della posa di riferimento non entrano nella ricostruzione, mentre la posa partecipa alla selezione e alla geometria delle sorgenti.

Il primo protocollo richiedeva riquadri interamente validi e non ha conservato alcuna coppia. Il secondo, esplorativo, esclude sette cambi di chip e usa per ogni stella soltanto i pixel validi nella posa di riferimento e coperti interamente da contributi DQ=0 e finiti in entrambe le pose, per entrambe le larghezze e per tutte le traslazioni provate. Il supporto deve conservare i 3 × 3 pixel centrali, almeno 17/25 pixel del nucleo e 12/24 della corona. Una coppia fallisce il requisito. Restano 109/117 coppie.

La metrica è la RMSE sul nucleo dopo sottrazione della mediana della corona comune e normalizzazione a somma unitaria sul nucleo, divisa per il picco del nucleo normalizzato nella posa di riferimento. Il caso perturbato usa il peggiore, per stella e larghezza, tra quattro spostamenti differenziali opposti di ±0,05 px per asse. I controlli analitici verificano la costanza con entrambe le larghezze e il recupero di un piano con larghezza unitaria.

| Chip | Coppie | P90 nominale, 1,00 → 0,70 | P90 perturbato, 1,00 → 0,70 | Coppie con errore nominale minore a 0,70 |
| --- | ---: | ---: | ---: | ---: |
| 1 | 49 | 8,86% → 8,97% | 8,98% → 9,38% | 33 |
| 2 | 60 | 8,47% → 8,26% | 8,83% → 8,49% | 46 |

La larghezza minore riduce l'errore nominale per 79 coppie, mentre il P90 peggiora sul chip 1 anche sotto perturbazione. Il confronto riguarda due pose, un riferimento osservativo con rumore proprio e quattro perturbazioni fissate. Restano aperti il confronto con distorsione e ricostruzione di campo intero, le misure di flusso e rumore e la verifica sulle sequenze CFA. Zero chiusure scientifiche e zero avvii nativi.

SHA-256 della ricevuta con maschera `a5d277ad3ae0ea9ef75a00186b5d08671b66fad05ae79135782dfd4a115084e8`.
