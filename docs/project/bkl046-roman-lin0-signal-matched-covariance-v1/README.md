# BKL-046 · Covarianza GAIN → LIN0 a segnale registrato comparabile

Ho riprodotto i 2.880 confronti precedenti, con le due fasce, la stessa maschera e le stesse 15 coppie LIN0. Per ogni fascia e canale ho interpolato la forma della covarianza fra i due livelli GAIN che racchiudono il segnale misurato nella coppia LIN0. Tutte le previsioni usano la stessa varianza scalare della coppia valutata. I confronti fuori dall’intervallo GAIN rimangono registrati senza estrapolazione. [Confronto per indice di lettura](../bkl046-roman-lin0-cross-session-covariance-v1/README.md)

| Fascia, lettura LIN0 1 | Coppie × canali | Mediana, GAIN allo stesso indice | Mediana, GAIN interpolato per ADU | Mediana, stima dalle altre coppie LIN0 |
| --- | ---: | ---: | ---: | ---: |
| Inferiore | 480 | 11,6% | 4,2% | 4,3% |
| Superiore | 480 | 20,5% | 4,1% | 3,8% |

L’interpolazione migliora 857 dei 960 confronti ammessi rispetto allo stesso indice. Le 1.920 misure LIN0 alle letture 5 e 10 restano fuori dalla gamma GAIN. I livelli GAIN sono definiti dalla mediana delle coppie di origine su ciascun canale e fascia. Il segnale è in ADU e resta distinto dalla dose calibrata. L’operatore nativo resta da verificare.

Per riprodurre offline passare a `misura.py` la directory estratta del kit LIN0 precedente, le tre directory estratte GAIN delle fasce, della rampa e dei canali, le dipendenze, una nuova directory di uscita, il pin della cattura LIN0 `edfce4e4134528b790f3fd2e972527495b75bd59e8b0d9876d2d7f1b2bc1bc2e` e `protocollo.json` di questa prova.