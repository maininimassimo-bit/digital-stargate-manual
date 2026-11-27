# Trasferimento della pesatura stellare sul campo IC 1805

La pesatura provata su M51 è stata applicata alle pose RAW Canon EOS 40D di IC 1805. Il confronto conserva 38 pose, una posa di riferimento condivisa e 1.123 associazioni di verifica con 42 stelle Gaia. I centroidi sono la media dei due verdi del mosaico. I due fit di ciascun modello usano le stesse stelle di stima e sono valutati sulle stesse stelle escluse.

Il peso deriva dal rapporto tra picco e rumore di fondo, preso al minimo fra le due pose e le due parità verdi. Come nello studio di M51, il rapporto rispetto alla mediana delle stelle di stima viene elevato al quadrato e limitato con pesi fra 0,25 e 4. Gli osservatori raccolgono coordinate e segnale dal programma congelato senza cambiare le stelle accettate. Il rapporto Gaia originale deve essere riprodotto byte per byte.

| Modello | P90 unitario | P90 pesato | Pose con P90 migliorato | Pose con P90 ≤ 0,30, unitario → pesato |
| --- | ---: | ---: | ---: | ---: |
| Similarità | 0,439 | 0,428 | 23/38 | 1 → 4 |
| Affine | 0,378 | 0,366 | 26/38 | 7 → 14 |

I residui sono in pixel nativi. Il P90 complessivo cala del 2,4% per la similarità e del 3,0% per l’affine. La riduzione è più contenuta di quella misurata con la preview sulle due coppie di M51. Cambiano campo, camera e metodo dei centroidi. Il riuso delle stesse stelle e della posa di riferimento lega fra loro i risultati per posa. La soglia complessiva resta aperta.

Per replicare eseguire `misura.py <protocollo.json> <studio-Gaia-IC1805> <radice-input> <directory-DLL-VC> <pacchetti-Python> <nuovo-riscontro.json>`.
