# Pesatura per segnale nella registrazione di M8–M20

La terza acquisizione usa il mosaico RGGB della ZWO ASI2600MC Pro. Le 49 tracce stellari di stima e le 54 tracce di verifica sono quelle del fit affine congelato. Per ognuna delle 14 pose si misura il minimo del rapporto fra picco e rumore di fondo fra i due verdi e fra la posa e il riferimento. Il peso relativo al valore mediano delle stelle di stima viene elevato al quadrato e limitato a 0,25–4. Il confronto applica anche Huber ai residui, con la soglia di 0,30 pixel e le 12 iterazioni del fit precedente.

| Fit affine | P90 complessivo (pixel nativi) | Pose con P90 ≤ 0,30 | Pose migliorate rispetto al confronto |
| --- | ---: | ---: | --- |
| Pesi unitari | 0,414 | 1/14 | Riferimento |
| Huber | 0,394 | 3/14 | 10/14 rispetto ai pesi unitari |
| Pesi per segnale | 0,390 | 1/14 | 7/14 rispetto ai pesi unitari |
| Pesi per segnale e Huber | 0,386 | 1/14 | 4/14 rispetto a Huber |

Sulle 756 associazioni la pesatura per segnale riduce il P90 complessivo del 5,9% rispetto ai pesi unitari, con miglioramenti in metà delle pose. Aggiungere la pesatura a Huber riduce il P90 aggregato del 2,0%, ma porta da tre a una le pose entro soglia. I dati indicano che l’effetto varia con la posa e con il criterio di valutazione. Le stelle e la posa di riferimento condivise rendono dipendenti le misure. Le associazioni di M8–M20 sono tracce del rivelatore. Il criterio di registrazione e la verifica scientifica nativa restano aperti.

Il programma verifica byte per byte la riproduzione del rapporto precedente. Per replicare eseguire `misura.py <protocollo.json> <studio-fit-stellare> <acquisizione> <affine-regionale> <riscontro-stelle.json> <pacchetti-Python> <nuovo-riscontro.json>`.
