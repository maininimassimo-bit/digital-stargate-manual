# BKL‑046 · Flag DQ e supporto comune nei quadrupoli ACS/WFC

Il controllo rilegge le stesse 234 immagini stellari delle due esposizioni ACS/WFC di NGC 5986. Il valore DQ di ogni pixel viene scomposto nei bit documentati da STScI. I conteggi per bit possono sovrapporsi. Nessuno dei bit osservati cade nei 3 × 3 offset centrali. [Definizioni DQ di STScI](https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps) · [Controllo con riquadro interamente pulito](BKL-046-NGC5986-QUADRUPOLI-ACS.md)

| Bit DQ | Riquadri interessati | Pixel con il bit |
| --- | ---: | ---: |
| 16 | 74 | 93 |
| 32 | 33 | 36 |
| 64 | 139 | 203 |
| 128 | 9 | 81 |
| 4096 | 22 | 49 |

La maschera comune conserva solo gli offset validi in entrambe le esposizioni e le orbite complete per rotazioni di 90° attorno al pixel centrale arrotondato. Ogni pixel con DQ diverso da zero resta escluso. La maschera richiede tutti i 3 × 3 offset centrali, almeno 49/81 offset totali e almeno il 75% del peso gaussiano in entrambe le pose. Otto coppie non raggiungono il numero minimo di offset.

| Chip | Coppie | Momenti misurabili con la maschera | Angolo proiettato disponibile in entrambe le pose | Differenza entro 5° |
| --- | ---: | ---: | ---: | ---: |
| 1 | 49 | 45 | 37 | 30 |
| 2 | 68 | 64 | 47 | 34 |
| Totale | 117 | 109 | 84 | 64 |

Su nove coppie interamente pulite con angolo proiettato disponibile, il controllo incrocia 89 maschere distinte. Restano disponibili 797 confronti su 801. Il P90 della variazione nella differenza angolare fra le due pose è 2,023°, oltre il limite congelato di 2°. La maschera porta la copertura da 10 a 109 coppie rispetto al riquadro interamente pulito, ma rimane fuori criterio. Le combinazioni riusano nove stelle e non rappresentano repliche indipendenti. La simmetria del supporto riguarda il pixel arrotondato. L’asse `PSF_PIXEL/2` resta aperto.

SHA‑256 della ricevuta `cb5692b0b9eac56a6285a08d5a7891dda03e0daead894e4e9b39a3fa5cd3a425`.
