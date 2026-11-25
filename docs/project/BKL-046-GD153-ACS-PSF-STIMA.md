# GD153 · Stima dei pixel mascherati nelle aperture ACS a 5 pixel

Si applica alle 18 esposizioni FLT lo stesso modello ePSF del [collaudo sui pixel tenuti fuori](BKL-046-GD153-ACS-PSF-HOLDOUT.md). Per posa si stimano soltanto i due pixel DQ non nulli nell'apertura a raggio 5 pixel. La scala e il piano di fuoco sono scelti sui pixel validi entro 10 pixel con lo stesso criterio del collaudo. Il flusso osservato e il contributo stimato sono registrati distintamente. Si conserva la stessa maschera DQ e nessun FITS viene modificato.

La stima ePSF rappresenta lo **0,268–0,833%** del flusso ricostruito. Lo stesso calcolo con la mediana radiale cambia il flusso totale per posa al massimo di 0,311% e il colore per visita al massimo di 2,38 mmag.

| Colore d'apertura | Escursione fra tre visite, soli pixel osservati | Escursione con stima ePSF |
| --- | ---: | ---: |
| F435W−F606W | 6,16 mmag | 7,94 mmag |
| F435W−F814W | 3,69 mmag | 0,86 mmag |
| F606W−F814W | 8,58 mmag | 8,79 mmag |

Come prova di sensibilità, nei rapporti di colore si perturbano i flussi con il massimo errore osservato su maschere artificiali per la rispettiva banda, in versi opposti. La larghezza risultante è 6,35–8,49 mmag a seconda della coppia di filtri e della visita. Si tratta di uno scenario deterministico, senza interpretazione come intervallo di confidenza. I pixel reali mascherati sono stime del modello e per essi non esiste una misura osservata in quella stessa visita. Restano aperti la correzione CTE, l'encircled energy, l'effetto della stessa risposta di calibrazione e il confronto multiposizione. Nessun avvio nativo e nessuna chiusura scientifica.

Il replay dagli archivi su H: ha riprodotto il JSON byte per byte. SHA-256 riscontro `bfa80e33c2905d71bec872d8e686493fc7c3ec485a91c013a2c59954cdee819b`. SHA-256 archivio `e2fa82a32089b6723e755e1562bbb25f9b9c3b6b7a1ad20fc14a275fcfcbcb4a`.
