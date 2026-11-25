# BKL-046 · Effetto della registrazione sugli stack Bayer M8–M20

La prova ricostruisce separatamente le quattro parità Bayer per 53 stelle con predizioni appaiate in tutte le 14 pose. Tiene fissi il reticolo di uscita a passo nativo, le due calibrazioni, la maschera dei pixel e le due larghezze del deposito quadrato. Per ciascuna stella il centro di uscita è comune. Le posizioni previste dai due fit determinano le traslazioni locali verso quel centro. Il confronto comprende quindi anche il ricentraggio di riferimento. I flussi e le statistiche del fondo usano pixel comuni a entrambe le geometrie e a entrambe le larghezze. La copertura comune è completa per tutte le aperture, gli anelli di fondo e gli anelli delle due metà.

| Parità | P90 variazione assoluta del flusso con deposito 1,00 px, calibrazione A / B | Deposito 0,70 px, calibrazione A / B |
| --- | ---: | ---: |
| R | 1,999% / 2,064% | 2,080% / 1,934% |
| G1 | 1,012% / 1,074% | 1,089% / 1,252% |
| G2 | 0,561% / 0,672% | 0,701% / 0,687% |
| B | 0,993% / 0,914% | 0,760% / 1,026% |

Nove dei sedici confronti sono sopra l'1%. Il rosso resta il più sensibile con entrambe le calibrazioni e le larghezze. Cambiando registrazione, la variazione mediana della MAD del fondo nelle differenze tra i due semistack va da −1,82% a +2,10%, a seconda della parità, della larghezza e della calibrazione. La statistica può includere struttura residua. La prova controlla la sensibilità del flusso e del fondo su questo campo e con questo algoritmo offline. Restano aperte la verifica con un riferimento fotometrico e quella nella ricostruzione nativa PixInsight.

Due esecuzioni hanno prodotto ricevute identiche con SHA-256 `daaf63de21c7af58d1eea5676f9fde80f4e4d5aefb84bc7ae745b68a16010817`. Zero esecuzioni native.
