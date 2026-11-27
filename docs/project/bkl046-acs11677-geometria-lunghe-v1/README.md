# BKL-046 — Registrazione fra le pose ACS 11677 da 1.457 e 1.456 s

Ho selezionato i picchi dalla prima posa e rifiutato i nuclei con flag DQ. Il fit usa solo le stelle nelle tessere pari da 512 pixel. La verifica usa le tessere dispari. Il criterio congelato richiede almeno 24 stelle e otto tessere in ogni partizione e P90 radiale entro 0,1 pixel.

| Chip | Stelle per fit / verifica | P90 WCS primario | P90 traslazione | P90 affine |
| --- | ---: | ---: | ---: | ---: |
| 2 | 44 / 47 | 0,2076 px | 0,1194 px | 0,0863 px |
| 1 | 59 / 38 | 0,1420 px | 0,1367 px | 0,1068 px |

Solo il fit affine del chip 2 supera il criterio. Applicandolo al confronto diagnostico delle scie, la coincidenza al pixel più vicino cambia da 28.953 a 29.109 proiezioni con full well. Su queste ultime, 3.046 mostrano il bit 4096 in entrambe le pose e 2.360 in una sola. I numeri restano simili al confronto WCS. Sul chip 1 non ho trasferito il fit alle scie.

Il confronto geometrico riguarda stelle non sature della stessa coppia di pose lunghe. La ricorrenza dei flag non dimostra l'identità di eventi di raggi cosmici o l'accuratezza del flusso recuperato. Entrambi i replay coincidono byte per byte.