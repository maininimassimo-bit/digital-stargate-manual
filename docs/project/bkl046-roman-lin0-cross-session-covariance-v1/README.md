# BKL-046 · Trasferimento della covarianza Roman da GAIN a LIN0

Ho acquisito 30 esposizioni LIN0 a 1400 nm, della stessa unità 21816 usata nella serie GAIN. Le due serie provengono da acquisizioni distinte. Ho usato due fasce e 32 canali, con la stessa maschera in entrambe le serie. Per ogni confronto ho usato la varianza scalare della coppia LIN0 valutata. La forma della covarianza viene stimata sulle dieci coppie GAIN oppure sulle altre 14 coppie LIN0. Nessuna coppia contribuisce alla propria stima. [Dati Roman di laboratorio](https://archive.stsci.edu/missions-and-data/roman/wfi-triplet-test-data)

| Fascia, lettura | Errore mediano, ingresso indipendente | Forma da GAIN | Forma da altre coppie LIN0 |
| --- | ---: | ---: | ---: |
| Inferiore, 1 | 13,6% | 11,6% | 4,3% |
| Inferiore, 5 | 10,0% | 4,9% | 3,1% |
| Inferiore, 10 | 10,7% | 3,4% | 3,1% |
| Superiore, 1 | 13,8% | 20,5% | 3,8% |
| Superiore, 5 | 10,2% | 4,9% | 3,0% |
| Superiore, 10 | 10,8% | 3,7% | 3,4% |

Sono stati misurati tutti i 2.880 confronti. La forma stimata in GAIN migliora cinque delle sei mediane aggregate rispetto al modello con ingresso indipendente. Peggiora la mediana nella fascia superiore alla prima lettura. Stimare la forma sulle altre coppie LIN0 dà l’errore mediano più basso in ciascuna combinazione.

Il confronto allinea gli indici delle letture. I valori di `TGROUP` sono 2,88–2,93 s in LIN0 e 3,08–3,17 s in GAIN. Le letture hanno segnali diversi, quindi il test non isola l’effetto della sessione da quello della dose. Restano aperti il confronto a dose calibrata, la validazione in volo e l’operatore nativo. [Stima su coppie GAIN separate](../bkl046-roman-gain-held-pair-covariance-v1/README.md)

Per riprodurre offline, passare a `misura.py` la directory del kit, i kit estratti GAIN delle fasce, della rampa e dei canali, la directory delle dipendenze NumPy 2.3.5 e Astropy, una nuova directory di uscita e lo SHA-256 della cattura `edfce4e4134528b790f3fd2e972527495b75bd59e8b0d9876d2d7f1b2bc1bc2e`. Il kit contiene gli header e gli intervalli SCI acquisiti. Usare Python 3.12.