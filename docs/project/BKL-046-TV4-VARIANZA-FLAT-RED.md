# BKL-046 · Varianza temporale nei flat TV4 RED a livelli riservati

La prova parte dalle pose del [confronto dei flat RED](BKL-046-TV4-FLAT-RISPOSTA-SPAZIALE.md) e da quattro BIAS RED separati. Usa due pose distinte per ciascuno dei cinque tempi dei flat e due coppie BIAS. Le differenze di coppia sono divise per la radice di due. Per ognuna delle cinque regioni fisse si sottrae la media di ogni blocco 16 × 16 e si misura la varianza residua. Le pose e i ruoli sono fissati prima di leggere i pixel.

I modelli usano i tre tempi di calibrazione per stimare il segnale atteso e la relazione fra segnale e varianza. I tempi di 33,5 e 303,5 ms sono riservati. La tabella riporta l’errore relativo assoluto mediano sulle cinque regioni.

| Modello della varianza | 33,5 ms | 303,5 ms |
| --- | ---: | ---: |
| Costante | 766,23% | 19,60% |
| Lineare con intercetta libera | 0,70% | 2,05% |
| Lineare con intercetta fissata dai BIAS | 15,57% | 3,50% |

Il modello libero stima intercette fra 1,90 e 2,48 DN². Le varianze misurate sui BIAS sono fra 0,54 e 1,23 DN². La varianza nelle pose riservate è 8,24–8,68 DN² a 33,5 ms e 59,92–64,22 DN² a 303,5 ms. La prova distingue l’andamento con il segnale e la sensibilità all’ancoraggio BIAS. La pendenza è una relazione empirica relativa a questa sequenza. La correlazione spaziale, l’incertezza di calibrazione, il trasferimento ad altre acquisizioni e la relazione con i processi nativi restano da verificare. Le cinque regioni condividono le pose. NOISE_FLUX/1 e NOISE_FLUX/2 restano aperti.

| Evidenza | SHA-256 |
| --- | --- |
| Protocollo | d69344551e4c1f5a7198e63711e703b7ff6eeec9883650e9c2faa82a937c37e6 |
| Programma | 95fd81e72111686a9cb23da59df55bfdb84698b1ced96059fd42eba5b388e5cd |
| Riscontro replicato da H: | 738a6e5149c950130f1003e9834fe049cdaad75d2875db918ae0803f95ffa472 |
