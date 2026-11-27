# BKL-046 · Scomposizione dei veti DQ nella misura guidata da Gaia

La verifica riproduce i 548 tentativi A40 della [misura a partire da Gaia](BKL-046-GO16380-MISURE-DA-GAIA.md) e la ragione di esclusione del centroide congelato. Controlla separatamente il DQ nel nucleo di raggio tre pixel, il numero di pixel validi nell'anello di fondo e la presenza di valori non finiti. Per le sorgenti scartate in A40, il nucleo B40 viene esaminato nella posizione prevista. I conteggi B40 descrivono le maschere in quella posizione. [Definizioni DQ ACS](https://www.stsci.edu/hst/instrumentation/acs/data-analysis/dq-flag-definitions)

| Motivo o flag | Sensore 1, A40 / presente anche in B40 | Sensore 2, A40 / presente anche in B40 |
| --- | ---: | ---: |
| Veto di qualità per DQ non nullo nel nucleo | 230 / — | 224 / — |
| Pixel tiepidi, 64 | 143 / 143 | 152 / 152 |
| Pixel caldi, 16 | 134 / 134 | 116 / 115 |
| Sink pixel o pixel affetti, 1024 | 54 / 54 | 57 / 53 |
| Full well, 256 | 34 / 34 | 39 / 38 |
| Raggi cosmici segnalati da AstroDrizzle, 4096 | 9 / 8 | 10 / 10 |

I flag possono coesistere su una sorgente. Nessuno dei rifiuti è attribuibile alla mancanza di pixel di fondo o a valori scientifici non finiti. La ricorrenza dei flag nelle posizioni previste di B40 indica che una seconda esposizione nello stesso assetto offre poca copertura complementare. Il controllo successivo deve selezionare osservazioni in cui le stesse sorgenti cadono su una zona diversa del rivelatore, prima di verificare la copertura con gli stessi veti.

L'asse `SATURATION_BLEND/4` resta aperto. La verifica ha letto le maschere originali. Nessuna sostituzione di pixel, esecuzione nativa o chiusura scientifica.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Protocollo | `ab806bb2b311b3ec25d33053c46529dd5b149b763431062f3c4bc86bce53c65e` |
| Programma | `87c6ad63572e1faeeba2acfb7d29ba8bcb3d6648cb386661f7c0850d1d36ee24` |
| Ricevuta con bit e parole DQ per sorgente | `33a626a1e152de4cb04ea38e2202436f0b82207f7d00200c0b6c8559203ffe94` |
