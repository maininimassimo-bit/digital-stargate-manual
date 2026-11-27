# BKL-046 · Previsione della varianza da Roman GAIN a LIN0

Le due serie sono acquisizioni distinte della stessa unità di laboratorio 21816. Il test ricostruisce la prova precedente byte per byte sul medesimo supporto. Per ogni coppia LIN0, la mediana del segnale delle altre 14 coppie, nello stesso canale, fascia e lettura, determina la posizione sulla curva GAIN. Le previsioni di varianza usano esclusivamente le dieci coppie GAIN per ciascuno dei tre livelli. La coppia LIN0 esclusa fornisce soltanto il valore osservato. Il confronto interno usa la mediana delle altre 14 varianze LIN0.

| Fascia, lettura LIN0 1 | GAIN, varianza empirica interpolata | GAIN, varianza RAW e covarianza interpolate | GAIN, ingresso indipendente | LIN0, riferimento interno |
| --- | ---: | ---: | ---: | ---: |
| Inferiore | 4,50% | 4,61% | 12,71% | 4,55% |
| Superiore | 4,02% | 4,42% | 13,18% | 4,22% |

Gli errori sono mediane relative assolute rispetto alla varianza della somma ricampionata. La previsione empirica da GAIN ha P95 del 13,35% e 13,13%, contro 13,10% e 12,80% del riferimento interno LIN0. Le mediane sono vicine nel campione osservato. I test condividono gruppi di esposizioni e canali e non stimano un margine di equivalenza.

Restano registrati tutti i 2.880 confronti. Il segnale consentiva l'interpolazione in 960 confronti alla lettura 1. I 1.920 confronti delle letture 5 e 10 sono fuori intervallo. Il segnale LIN0 usato come ascissa proviene da acquisizioni della sessione bersaglio. La dose fisica, l'estrapolazione a segnali più alti, altri sensori e l'operatore nativo restano da verificare.

Per riprodurre usare Python 3.12, il protocollo, la directory del confronto LIN0 a segnale comparabile, una nuova directory di uscita e i kit del confronto LIN0 per indice, delle fasce GAIN, della rampa GAIN, dei canali e delle dipendenze. Il kit LIN0 per indice deve includere il dettaglio congelato alla radice e gli intervalli FITS nella sottocartella di cattura. L'archivio locale include il dettaglio dei 2.880 confronti.
