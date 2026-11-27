# BKL-046 · Trasferimento della covarianza tra livelli di segnale Roman

Il test rilegge 1.920 confronti su due fasce del sensore di laboratorio Roman 21816. Riproduce gli errori precedenti per l'ingresso indipendente e per la covarianza appresa allo stesso livello. La stima usa la forma della covarianza nello stesso canale e fascia alla lettura 1, 5 o 10. Per ogni confronto esclude entrambe le esposizioni della coppia a tutte le letture. La varianza scalare della coppia, il supporto e lo spostamento bilineare di mezzo pixel sui due assi restano identici.

| Fascia | Lettura da prevedere | Errore mediano indipendente | Covarianza dello stesso livello | Da lettura 1 | Da lettura 5 | Da lettura 10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Inferiore | 1 | 21,92% | 5,63% | — | 9,46% | 11,34% |
| Inferiore | 5 | 13,42% | 4,05% | 12,19% | — | 3,94% |
| Inferiore | 10 | 11,98% | 3,66% | 13,63% | 3,68% | — |
| Superiore | 1 | 27,85% | 7,49% | — | 16,31% | 16,55% |
| Superiore | 5 | 14,26% | 4,08% | 19,02% | — | 4,03% |
| Superiore | 10 | 12,65% | 3,61% | 21,45% | 4,13% | — |

Gli errori sono relativi alla varianza empirica della somma ricampionata. Le mediane dei quattro trasferimenti tra lettura 5 e lettura 10 differiscono di al massimo 0,52 punti percentuali dal modello dello stesso livello, con arrotondamento a due decimali. Il trasferimento dalla lettura 1 alla lettura 10 peggiora la mediana rispetto all'ingresso indipendente in entrambe le fasce. Il rapporto contiene anche il P95, i conteggi per coppia e il modello che media le matrici degli altri due livelli.

La comparazione riguarda letture della stessa serie, con acquisizioni e lettura iniziale condivise. I segnali caratterizzano il rivelatore. La dose ottica indipendente, il trasferimento tra sessioni o sensori e l'equivalenza del processo nativo restano da verificare. Zero chiusure scientifiche.

Per riprodurre usare Python 3.12 con il protocollo, la directory del test precedente a coppie escluse, i kit delle fasce e dei canali, NumPy 2.3.5 e una nuova directory di uscita. L'archivio locale contiene anche il dettaglio dei 1.920 confronti.
