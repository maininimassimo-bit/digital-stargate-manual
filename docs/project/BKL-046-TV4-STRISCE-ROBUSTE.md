# BKL-046 · Correzione robusta delle strisce TV4

Il confronto usa gli stessi riferimenti disgiunti e i due contrasti riservati delle [prove di segnale diffuso](BKL-046-TV4-SEGNALE-DIFFUSO.md). Confronta i dati grezzi, la media, la media dopo troncamento del 20% su ciascuna coda e la mediana. Nessun operatore usa le posizioni del segnale iniettato. Per ogni metodo, la covarianza del rumore è stimata sui due contrasti di calibrazione e verificata sui due contrasti riservati, con tre aperture e tre kernel.

| Operatore | Filamenti entro il 5% per flusso centrale e forma | Filamenti paralleli agli assi entro il 5% | Errore massimo di flusso centrale | Varianza osservata mediana rispetto al grezzo |
| --- | ---: | ---: | ---: | ---: |
| Grezzo | 180 / 180 | 60 / 60 | < 0,01% | 1,000 |
| Media | 60 / 180 | 0 / 60 | 53,05% | 0,522 |
| Media troncata | 60 / 180 | 0 / 60 | 53,38% | 0,525 |
| Mediana | 60 / 180 | 0 / 60 | 53,91% | 0,650 |

La perdita nei filamenti paralleli agli assi si ripete a tutti e tre i picchi iniettati, 0,5, 2 e 8 DN. Il flusso totale nella regione resta conservato entro la tolleranza numerica prevista, mentre il flusso e la forma nell'apertura locale possono cambiare. Per nessun operatore, incluso il grezzo, una combinazione apertura/kernel raggiunge l'errore mediano di previsione della varianza del 15%.

I risultati conservano l'intero banco di 800 risposte alle iniezioni, inclusi i controlli compatti e costanti, e 360 misure di varianza in aperture. Provengono da una sola acquisizione di laboratorio. Le iniezioni sono digitali e non simulano rumore fotonico aggiuntivo. `DIFFUSE_BACKGROUND/1` e `NOISE_FLUX/3` restano aperti. Nessuna prova nativa o chiusura scientifica.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Protocollo | `f7ba8aa2b3bbc29f91e160d62802c1bf6df399a6c07cf621c76f0e56d14d02fe` |
| Programma | `856942c3842c212ed6821c08ca23a03ecd3325f4b6ae417eb286e9d816f9099f` |
| Ricevuta completa delle aperture e delle iniezioni | `78a577edaacc37828049c2f57578ff04b57386e267beca87d6b10113b81ad3c1` |
