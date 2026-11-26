# BKL-046 · Previsione della varianza assoluta nella rampa Roman

Le previsioni usano solo le nove coppie di stima in ciascun canale, fascia e lettura. La coppia riservata resta esclusa a tutte le letture e fornisce esclusivamente la misura di confronto. Ho verificato 1.920 riscontri contro il precedente confronto condizionato alla varianza. Il protocollo conserva lo spostamento bilineare di mezzo pixel su entrambi gli assi e le stesse maschere.

| Fascia | Lettura | Ingresso indipendente | Covarianza allo stesso livello | Varianza empirica allo stesso livello | Retta empirica dagli altri livelli | Retta RAW e covarianza dagli altri livelli |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Inferiore | 1 | 21,63% | 6,18% | 6,35% | 10,92% | 8,45% |
| Inferiore | 5 | 13,54% | 4,40% | 3,92% | 4,36% | 5,33% |
| Inferiore | 10 | 11,92% | 4,29% | 3,90% | 4,22% | 8,96% |
| Superiore | 1 | 28,13% | 9,09% | 9,54% | 12,72% | 15,70% |
| Superiore | 5 | 14,43% | 4,30% | 4,43% | 4,42% | 8,79% |
| Superiore | 10 | 12,60% | 4,47% | 3,87% | 4,39% | 12,03% |

La tabella riporta l'errore relativo assoluto mediano sulla varianza della somma ricampionata. I modelli con calibrazione allo stesso livello migliorano il riferimento indipendente in tutte e sei le combinazioni. La mediana empirica è competitiva con il modello esplicito di covarianza quando è disponibile una misura allo stesso livello e con lo stesso operatore. La retta empirica appresa dalle altre letture ha errore mediano di 4,22–4,42% sulle letture 5 e 10 e 10,92–12,72% sulla lettura 1. La lettura 10 è un'estrapolazione. Il modello che trasferisce insieme varianza RAW e forma della covarianza ha errori maggiori sulla lettura 10. Tutte le previsioni risultano positive.

La retta usa livelli medi del rivelatore ricavati dalle nove coppie di stima, compreso il livello di segnale da prevedere. La sequenza è una sola, i livelli condividono la lettura iniziale e i canali riusano le esposizioni. La dose ottica indipendente e la validazione su altre sessioni e sul processo nativo restano aperte.

Per riprodurre usare Python 3.12 con il protocollo, i fascicoli di trasferimento tra livelli, covarianza a coppie escluse, fasce, canali, le dipendenze con NumPy 2.3.5 e una nuova directory di uscita. Il dettaglio dei 1.920 confronti è nell'archivio locale.
