# BKL-046 · Rumore CFA e registrazione nella conoscenza v1.171

Questo addendum collega sei ricevute di cinque studi alla conoscenza intermedia v1.171. Il verificatore confronta i byte del rapporto locale, del membro ZIP e della copia GitHub al commit indicato. Controlla le impronte degli archivi sui due volumi e lega ogni studio agli assi aperti del rendiconto v65.

| Asse | Decisione documentata | Evidenza ancora richiesta |
| --- | --- | --- |
| NOISE_FLUX/1 | I flat brevi di M8–M20 sostengono una stima locale della varianza con il segnale. La serie ha una sola durata. | Calibrazione assoluta con più livelli, tempi e repliche nei regimi di rumore di lettura, misto e dominato dal segnale. |
| NOISE_FLUX/3 | La dispersione delle aperture sulla griglia RAW per parità e quella sulle ricostruzioni hanno supporti diversi. Nel confronto a raggio simile, il vantaggio più stabile cambia fra M8–M20 e IC 1805. | Misure native su pose indipendenti con risposta spaziale e aperture comparabili, conservando anche i casi sfavorevoli. |
| CFA_DITHER_DRIZZLE/2 | Su M51 la coppia migliore ha P90 di 0,363 pixel nativi contro la soglia di 0,30. Le tre pose restano fuori dalla replica del rumore a pari raggio. | Registrazione e calibrazione qualificate, con un riscontro indipendente. |
| CFA_DITHER_DRIZZLE/4 | I quattro vantaggi G1 di M8–M20 non si ripetono su IC 1805. Quest’ultimo confronto ha registrazione fuori soglia e calibrazione provvisoria. | Replica su un campo indipendente qualificato e verifica della risposta spaziale oltre il raggio RMS. |

Il file strutturato mantiene a zero le chiusure scientifiche. La consegna finale e la ricostruzione integrale da GitHub restano aperte. Il verificatore usa PowerShell 7, GitHub CLI e le copie già archiviate. Passare la radice del volume VM ospitato da K:, la cartella degli archivi di progetto su H: e il percorso di una nuova ricevuta. Confrontare quest’ultima con `conoscenza.json`.
