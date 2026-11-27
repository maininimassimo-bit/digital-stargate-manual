# BKL-046 · Covarianza parziale per la varianza dei flat ASI2600MC

Il controllo riproduce tutti i 2.520 esiti del protocollo precedente. Per ciascuna delle sette coppie escluse, la forma della covarianza di ingresso proviene dalle altre sei. Si confrontano cinque pesi fissati prima del calcolo. Il peso zero corrisponde a ingresso indipendente, ma conserva la covarianza generata dal ricampionamento. Il peso uno usa tutta la matrice di covarianza stimata.

| Mezzo pixel su entrambi gli assi | Peso | Errore mediano | P95 dell'errore |
| --- | ---: | ---: | ---: |
| Flat grezzi | 0 | 6,21% | 39,10% |
| Flat grezzi | 0,75 | 10,86% | 35,59% |
| Dopo sottrazione del piano | 0 | 5,36% | 17,80% |
| Dopo sottrazione del piano | 0,25 | 5,30% | 16,80% |
| Dopo sottrazione del piano | 1 | 5,91% | 19,54% |

Dopo la sottrazione del piano, a peso 0,25 migliorano quattro delle sette mediane per coppia. Sui dati grezzi l'effetto sulla coda e quello sulla mediana vanno in direzioni opposte. Il rapporto conserva le scelte a priori, tutte le fasi e le mediane per coppia. I risultati riusano le stesse acquisizioni tra le stime. Nessun peso è stato scelto sui dati esclusi e resta da verificarne il trasferimento a sessioni e dosi diverse.

Per riprodurre il rapporto, fornire a `misura.py` il protocollo, le directory dei due studi precedenti, l'archivio originale dei flat, NumPy 2.3.5 e Astropy 7.2.0 e un percorso nuovo per il risultato. La prova è offline e riguarda NOISE_FLUX/3.
