# BKL-046 · Ricostruzione Bayer a scala comune in M8 e M20

Le 14 pose Bayer di verifica sono depositate come impronte quadrate nelle quattro parità separate, su una griglia di passo pari a un pixel nativo. Si usano 54 ritagli stellari e due larghezze di impronta, 1,00 e 0,70 px, con le due calibrazioni disgiunte A/A e B/B. Per ciascun ritaglio si usa la traslazione data dal fit affine con Huber valutato al centro della stella. La geometria, l'apertura e la maschera unione dei pixel anomali sono comuni. Una prova a segnale costante verifica il valore ricostruito nei pixel coperti e rileva le lacune lasciate da un pixel mascherato.

Per il flusso si sommano i pixel netti ricostruiti nell'apertura sullo stack completo, con fondo stimato nell'annulus sullo stesso supporto. Per la dispersione si alternano le pose in due gruppi da sette e si misura la MAD scalata della loro differenza nell'annulus comune. Tutte le 54 stelle per parità passano il criterio di copertura. Nei ritagli misurati, tutti i pixel dell'apertura dello stack completo e dell'annulus delle due metà hanno almeno un contributo per entrambe le larghezze.

| Parità | P90 variazione flusso tra calibrazioni, 1,00 / 0,70 | P90 variazione flusso tra larghezze, cal. A / B | MAD mediana fra metà, cal. A 1,00 → 0,70 |
| --- | ---: | ---: | ---: |
| R | 1,58% / 1,56% | 0,47% / 0,40% | 31,81 → 36,02 ADU |
| G1 | 1,11% / 1,14% | 0,20% / 0,18% | 33,16 → 38,99 ADU |
| G2 | 1,14% / 1,07% | 0,18% / 0,21% | 32,78 → 38,96 ADU |
| B | 1,04% / 1,05% | 0,36% / 0,33% | 26,07 → 30,43 ADU |

L'effetto dei calibratori rimane sopra l'1% al P90 in tutte le parità. L'impronta più stretta cambia meno il flusso e aumenta la dispersione tra metà con entrambe le calibrazioni. La dispersione comprende fondo, differenze di PSF, registrazione e copertura effettiva. Il risultato riguarda ritagli locali e un solo campo, con accuratezza stellare della registrazione ancora fuori soglia. Restano da verificare il confronto con demosaicizzazione e ricampionamento, la robustezza su altri campi e il processo nativo. Zero esecuzioni PixInsight e zero chiusure scientifiche.

SHA-256 della ricevuta `bd9719bbe544a4edeaaa64e881bf6f5871034f839887c614a1b1845521e8e458`.
