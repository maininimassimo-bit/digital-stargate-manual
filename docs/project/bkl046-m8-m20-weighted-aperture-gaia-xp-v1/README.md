# Effetto delle aperture pesate sul colore B−R rispetto a Gaia XP

Il confronto BKL-046 riguarda le aperture originali Bayer di M8–M20. Conserva 39 identità Gaia XP, 20 per stimare lo zero cromatico e 19 per la verifica. Le 545 associazioni appaiate coprono 13–14 pose per stella. Il colore di ogni stella è la mediana del B−R ricavato dai flussi di ciascuna posa. Per ogni modello di risposta, lo zero cromatico si stima soltanto sui centri a pesi unitari della calibrazione A e si riusa in tutte le misure di verifica.

| Risposta sintetica | Calibrazione | P90 residuo a pesi unitari (mag) | P90 residuo con pesi per segnale (mag) |
| --- | --- | ---: | ---: |
| Sony QE, UV/IR e L-Pro | A | 0,162 | 0,155 |
| Sony QE, UV/IR e L-Pro | B | 0,177 | 0,148 |
| Siril IMX571 e L-Pro | A | 0,147 | 0,147 |
| Siril IMX571 e L-Pro | B | 0,160 | 0,135 |

Il P90 della differenza assoluta fra i colori delle due aperture sulle 19 stelle vale 0,0062 mag in A e 0,0051 mag in B. La pesatura abbassa il P90 del residuo in tre combinazioni su quattro. Nella combinazione Siril A la differenza è +0,00032 mag. Le due risposte strumentali sono approssimazioni e le calibrazioni condividono pose e stelle. Il confronto quantifica l’errore cromatico residuo rispetto ai modelli XP con uno zero comune stimato. Restano aperte la calibrazione fotometrica assoluta e la ricostruzione nativa a scala comune.

Per replicare eseguire `misura.py <protocollo.json> <studio-aperture> <studio-fase-XP> <studio-pesi> <studio-fotometria> <radice-input> <pacchetti-Python> <nuovo-riscontro.json>`. Il programma riproduce byte per byte il rapporto delle aperture prima di confrontare i colori.
