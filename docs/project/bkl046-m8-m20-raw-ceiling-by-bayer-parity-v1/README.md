# BKL-046 · Limite digitale per parità Bayer nelle pose M8/M20

La misura usa 15 FITS originali Colmic da 180 secondi, prima di calibrazione, debayer, registrazione e normalizzazione. Verifica la codifica unsigned a 16 bit e conta i campioni al codice massimo 65.535. Il rapporto conserva anche la fascia al 99% e la soglia 62.000 già utilizzata per le maschere. [Serie M8/M20](https://siril.org/tutorials/tuto-scripts/index.html)

| Parità RGGB | Campioni al massimo per posa, minimo–massimo | Occorrenze nelle 15 pose | Posizioni grezze sempre al massimo |
| --- | ---: | ---: | ---: |
| R | 867–930 | 13.414 | 17 |
| G1 | 1.081–1.155 | 16.683 | 51 |
| G2 | 1.074–1.146 | 16.657 | 46 |
| B | 830–901 | 12.946 | 48 |

Dei 28.989 blocchi con almeno un campione al massimo, **24.186** ne hanno da uno a tre e **4.803** li hanno tutti e quattro. I conteggi sono per blocco e per posa. I quattro fotositi del blocco misurano posizioni leggermente diverse, e le pose riusano lo stesso campo. Le posizioni sempre al massimo sono riportate in coordinate del rivelatore per conteggio. La persistenza non identifica la causa.

Il riscontro si applica a `SATURATION_BLEND/1` e `SATURATION_BLEND/3`. Il limite misurato è quello della codifica. Restano aperti il limite fisico del rivelatore, il comportamento a esposizioni più brevi e il recupero fotometrico. Zero avvii PixInsight e zero chiusure scientifiche.

Replica con Python 3.12, NumPy 2.3.5 e Astropy 7.2.0. `misura.py` riceve il protocollo, lo ZIP delle pose, la ricevuta delle pose, la directory delle dipendenze e il nuovo percorso del rapporto.
