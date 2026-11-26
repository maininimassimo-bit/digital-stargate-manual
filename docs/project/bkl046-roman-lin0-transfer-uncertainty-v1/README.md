# BKL-046 · Incertezza del trasferimento di varianza Roman GAIN → LIN0

La rianalisi usa i 960 confronti eseguibili a segnale comparabile nella prima lettura. I 1.920 confronti fuori intervallo restano esclusi dall'inferenza. Il programma verifica le mediane e i P95 di tutti i modelli contro la ricevuta congelata. Mantiene fisse le previsioni e confronta gli errori assoluti relativi sugli stessi casi.

Le differenze sono in punti percentuali, modello da GAIN meno riferimento empirico LIN0. Il programma esegue 10.000 ricampionamenti accoppiati delle 15 coppie di esposizioni, con e senza ricampionamento incrociato dei blocchi contigui di canali. Le due fasce e tutti i modelli condividono le estrazioni. Il rapporto include anche ogni esclusione singola di una coppia.

| Previsione empirica GAIN | Fascia | Differenza puntuale | Coppie e blocchi da 4 canali | Coppie e blocchi da 8 canali |
| --- | --- | ---: | ---: | ---: |
| Mediana | Inferiore | −0,05 | Vedi rapporto | [−0,82, +0,50] |
| Mediana | Superiore | −0,19 | Vedi rapporto | [−0,64, +0,32] |
| P95 | Inferiore | +0,24 | Vedi rapporto | [−1,75, +1,42] |
| P95 | Superiore | +0,33 | [−1,68, +21,20] | [−1,63, +18,37] |

L'intervallo per il P95 superiore ricampionando solo le coppie è [−0,84, +2,72]. La sensibilità aumenta quando si ricampionano anche i canali. Nessun vantaggio dei modelli trasferiti con covarianza o varianza empirica ha direzione stabile rispetto al riferimento LIN0 nei rispettivi otto confronti. Il modello che assume ingresso indipendente ha errore stabilmente più alto del riferimento in tutti e quattro i propri confronti.

Gli intervalli sono descrittivi e condizionati alle previsioni fisse e alle due sessioni. Il ricampionamento non ristima i modelli e non tratta i canali come sessioni indipendenti. Il rapporto documenta la sensibilità del trasferimento, soprattutto nella coda della distribuzione. Una prova di equivalenza e la validazione nativa restano aperte.

Per riprodurre usare Python 3.12 con il protocollo, la directory della prova GAIN → LIN0 con dettaglio congelato, le dipendenze NumPy 2.3.5 e un nuovo percorso di uscita.
