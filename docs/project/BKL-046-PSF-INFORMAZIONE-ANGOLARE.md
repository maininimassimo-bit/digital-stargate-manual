# BKL‑046 · Informazione locale sull’orientazione e campionamento subpixel

Il protocollo usa le 48 geometrie ellittiche distinte della prova Moffat con rumore, alla scala maggiore di 0,65 pixel. Confronta un raster singolo, quattro ripetizioni alla stessa fase e quattro raster con offset relativi esatti di mezzo pixel sui due assi. La somma in quadratura degli SNR nominali è la stessa nei tre casi. Nei fit congiunti la forma e la correzione del centro sono comuni, mentre ampiezza e fondo sono liberi per ogni raster. [Prova con rumore](BKL-046-PSF-RUMORE-ORIENTAZIONE.md)

La derivata dei pixel rispetto all’angolo viene proiettata ortogonalmente alle derivate dei parametri liberi. Il reciproco della norma pesata dal rumore dà il limite inferiore locale per la deviazione standard di una stima regolare non distorta. Il metodo è affine all’uso della matrice di Fisher per stimare congiuntamente parametri di sorgenti campionate a pixel. Il lavoro citato tratta astrometria e fotometria in un proprio modello osservativo. [Méndez et al.](https://arxiv.org/abs/1407.3753)

| SNR nominale complessivo | Rapporto assiale | Mediana del limite con un raster, centro libero | Mediana con quattro fasi, centro libero | Geometrie con limite ≤ 5° con quattro fasi |
| --- | ---: | ---: | ---: | ---: |
| 25 | 0,60 | 45,89° | 13,67° | 0/24 |
| 25 | 0,85 | 83,68° | 32,80° | 0/24 |
| 100 | 0,60 | 11,47° | 3,42° | 24/24 |
| 100 | 0,85 | 20,92° | 8,20° | 0/24 |

Le quattro ripetizioni senza offset riproducono il limite del raster singolo. Le quattro fasi migliorano il limite in tutte le geometrie. A SNR 100, un solo raster con centro noto scende a 5° o meno in 18/24 geometrie a rapporto 0,60 e in 0/24 a rapporto 0,85. Il controllo a due passi di differenziazione mostra una divergenza relativa massima di 2,17 × 10⁻⁹.

Il limite riguarda il modello locale con scala, famiglia e registrazione relative note. Il traguardo di pianificazione a 5° riguarda una deviazione standard teorica. La prova precedente richiedeva invece una frazione di angoli effettivamente entro 5°. La misura empirica su fasi multiple, con incertezza degli offset e profili fuori famiglia, rimane aperta. L’asse `PSF_PIXEL/2` resta aperto.

SHA‑256 della ricevuta `1a7719133f96e02e80e1a6a7a1cb61569c8b0251e34a99bb063554b818260be5`.
