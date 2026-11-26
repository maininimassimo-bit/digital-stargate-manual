# BKL-046 · Scarto Gaia–ACS al variare dell'apertura

Il protocollo confronta le misure F658N/F660N di GD71 e GD153 con la previsione Gaia fissata. Per ciascun raggio conserva tutti gli abbinamenti delle pose ammesse, il rapporto delle medie e la crescita rispetto a tre pixel sulle stesse pose. La forchetta degli abbinamenti è una misura di sensibilità alla scelta delle pose.

| Sorgente e raggio | Abbinamenti | Crescita rispetto alle stesse pose a 3 px | Aumento ancora necessario anche per l'abbinamento più vicino a Gaia |
| --- | ---: | ---: | ---: |
| GD71, 5 px | 4 | 0,66% | 2,95% |
| GD71, 10 px | 2 | 0,98% | 2,77% |
| GD153, 5 px | 4 | 1,07% | 2,36% |
| GD153, 10 px | 4 | 1,26% | 2,23% |

A 10 px GD71 ha una sola posa F660N ammessa, quindi il confronto con 3 px usa lo stesso sottoinsieme. A 15 e 20 px non esistono rapporti con entrambe le bande ammesse. Tra i rapporti ammessi, omettere i pixel con DQ 64 modifica il rapporto di meno dello 0,07%. La tabella nominale WFC a 0,5 secondi d'arco assegna a F658N e F660N la stessa energia racchiusa. Il riporto illustrativo con questi valori lascia invariato il rapporto e non qualifica una correzione per le pose storiche. [Manuale ACS, tabella 5.1](https://hst-docs.stsci.edu/acsdhb/chapter-5-acs-data-analysis/5-1-photometry)

La crescita misurata spiega una parte dello scarto. Restano da misurare la crescita oltre l'apertura disponibile e gli effetti CTE e di calibrazione. Le forchette non sono intervalli di confidenza e il riscontro non chiude criteri scientifici.

Per ripetere con Python 3.12 passare il protocollo, i riscontri delle curve GD71 e GD153, il confronto Gaia–ACS, la covarianza Gaia e un nuovo percorso di uscita.
