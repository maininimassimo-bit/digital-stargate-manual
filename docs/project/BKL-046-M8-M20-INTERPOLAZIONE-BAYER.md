# BKL-046 · Interpolazione bilineare e deposizione diretta CFA

Confronto su 54 ritagli stellari, 14 pose Bayer, quattro parità e due calibrazioni. Ai depositi diretti di 1,00 e 0,70 pixel si aggiunge una ricostruzione di riferimento. Questa interpola ciascuna parità sulla griglia del rivelatore e poi allinea in bilineare sulla stessa griglia di uscita dei depositi. Le due parità verdi rimangono separate. Il confronto riguarda quindi l'interpolazione per parità e lascia fuori gli algoritmi RGB adattivi. Il controllo numerico riproduce un piano inclinato e verifica il rifiuto del contributo di pixel anomali.

Le aperture usano l'intersezione dei pixel validi per tutte le ricostruzioni, con copertura minima effettiva del 99,13% sullo stack completo e del 98,58% sull'annulus delle due metà. Tutte le stelle sono misurabili. Il raggio è la radice del secondo momento radiale nell'apertura di 6 px, con pesi positivi dopo sottrazione del fondo. La dispersione è la MAD scalata della differenza tra le due metà della sequenza nell'annulus comune.

| Parità | Raggio mediano cal. A, 1,00 → bilineare | MAD mediana cal. A, 1,00 → bilineare | P90 variazione di flusso del bilineare rispetto a 1,00, cal. A / B |
| --- | ---: | ---: | ---: |
| R | 2,044 → 2,246 px | 31,81 → 15,70 ADU | 0,92% / 0,85% |
| G1 | 2,135 → 2,335 px | 33,16 → 16,69 ADU | 0,44% / 0,43% |
| G2 | 2,131 → 2,337 px | 32,78 → 16,28 ADU | 0,45% / 0,49% |
| B | 2,123 → 2,329 px | 26,07 → 13,50 ADU | 0,65% / 0,64% |

Il bilineare riduce quasi della metà la dispersione tra le due metà e allarga il profilo stellare di circa il 10%. La dispersione include registrazione, PSF, fondo e correlazione introdotta dal ricampionamento. Un valore per pixel minore non quantifica il rumore integrato in apertura né la precisione fotometrica. Il bilineare conserva una variazione di flusso al P90 fra le calibrazioni da 1,08% a 1,58% secondo la parità. Il confronto riguarda un campo, due gruppi di calibratori e una registrazione ancora fuori soglia. Rimangono aperti il confronto con un demosaicer RGB nativo e la replica su un secondo campo. Zero chiusure scientifiche.

SHA-256 della ricevuta `ba65d831ffd5906e9945455689632dbf0994a06a0fcbba26e2d9ec7aa735a979`.
