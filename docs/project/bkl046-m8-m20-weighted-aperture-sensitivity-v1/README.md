# Effetto della pesatura sulle aperture Bayer di M8–M20

Il confronto cambia solo il centro previsto dall’affine ordinario e da quello pesato per segnale. Usa le 742 associazioni del protocollo fotometrico congelato, con la stessa maschera, apertura di raggio 6 pixel, anello 9–13 pixel e due calibrazioni disgiunte. Il programma riproduce prima, byte per byte, sia il rapporto di registrazione pesata sia il precedente rapporto fotometrico.

Lo spostamento dei centri è pari a 0,150 pixel nativi al P90. Una misura R è esclusa per contrasto insufficiente. Le altre 2.967 misure sono appaiate fra i due centri e le due calibrazioni.

| Parità | Misure appaiate | P90 della variazione simmetrica assoluta del flusso, A / B | Aperture con pixel diversi |
| --- | ---: | ---: | ---: |
| R | 741 | 0,475% / 0,499% | 249 |
| G1 | 742 | 0,371% / 0,368% | 250 |
| G2 | 742 | 0,442% / 0,438% | 244 |
| B | 742 | 0,506% / 0,504% | 256 |

Tutti i P90 restano entro la soglia diagnostica dell’1% per la sensibilità fotometrica. Il confronto misura quanto cambia il flusso nell’apertura al variare della geometria, senza un riferimento fotometrico assoluto. La convalida della ricostruzione a scala comune e la prova nativa restano aperte.

Per replicare eseguire `misura.py <protocollo.json> <studio-pesatura> <studio-fotometria> <radice-input> <pacchetti-Python> <nuovo-riscontro.json>`.
