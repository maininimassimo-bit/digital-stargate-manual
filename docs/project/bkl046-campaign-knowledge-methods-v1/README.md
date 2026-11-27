# BKL-046 · Criteri d'uso per PSF e rumore

Queste schede completano la descrizione tecnica del piano v4 con otto riscontri verificabili. Si applicano agli scenari indicati e conservano aperti gli assi scientifici.

| Decisione | Criterio ricavato dalle prove | Ambito e verifica residua |
| --- | --- | --- |
| Generare la risposta di un pixel | Per Moffat strette usare l'integrale di area. Controllare la convergenza per pixel e sulla somma del campo. La somma può restare invariata mentre la quadratura ridistribuisce segnale tra pixel. | La quadratura per segmenti rientra nelle tolleranze dei 72 casi analitici. Restano da misurare PSF strumentali e comportamento dell'operatore nativo. |
| Riportare la posizione di una sorgente | Esporre l'incertezza lungo entrambi gli assi. Per una PSF molto sottocampionata, un bordo può fornire informazione in una sola direzione. La precisione fotometrica non implica precisione astrometrica. | I limiti Fisher e il test Poisson assumono forma, risposta e rumore ideali. Il test di discriminazione confronta due posizioni prefissate. Restano da provare la stima libera e le immagini reali. |
| Costruire intervalli e scegliere la numerosità | Se le sorgenti condividono un effetto di campo, usare il campo come unità. Valutare la copertura insieme alla potenza. Il bootstrap studentizzato migliora la copertura in alcuni scenari, che può comunque rimanere sotto il livello nominale. | Vengono usati solo semi di sviluppo. La calibrazione deve fissare effetto pratico, dipendenza, stimatore e numerosità prima della partizione di verifica. |
| Propagare il rumore dopo interpolazione | Conservare la covarianza introdotta dalla condivisione dei pixel di ingresso. Valutare separatamente se aggiungere la covarianza misurata sul rivelatore. Il trasferimento della matrice deve dimostrare utilità sul gruppo di destinazione. | I test ASI2600MC mostrano esiti diversi tra flat e serie senza illuminazione. Un peso osservato su una serie non è stato promosso a parametro generale. Restano aperti il trasferimento tra dosi ottiche e la prova nativa. |

`fonti.json` conserva il percorso GitHub, l'impronta e il commit di rilettura di ciascun rapporto. `riscontro.json` lega i criteri elencati alla stessa baseline v1.171 e alla contabilità dei requisiti ancora aperti.
