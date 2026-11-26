# BKL-046 · Controllo della previsione del centro fra bande su GD153

Ho applicato alle 48 pose archiviate di GD153 le regole di selezione dei due picchi utilizzate su GRW+70°5824. Per ogni banda donatrice, la posizione iniziale del riquadro è predetta dalle altre tre posizioni della stessa banda e visita. La posa che si vuole valutare resta fuori dalla stima. Ho confrontato il punto medio in coordinate del rivelatore con quello ottenuto proiettando i due picchi via WCS.

| Esito sulle 48 pose | Punto medio sul rivelatore | Punto medio via WCS |
| --- | ---: | ---: |
| Misura a entrambi i raggi | 20 | 20 |
| DQ nel nucleo | 4 | 4 |
| Supporto insufficiente | 24 | 24 |
| Scarto massimo fra previsione e centro di riferimento | 1,07 px | 1,08 px |

Lo scarto rispetto al riferimento è misurabile in 47 pose. I due metodi concordano sugli esiti di tutte le 48 pose. Nelle quattro terne integre già ammesse, entrambi restituiscono gli stessi colori a 5 e 10 pixel della misura di controllo che usa lo stesso stimatore e il centro di riferimento come punto iniziale. La ricentratura locale converge allo stesso centro per queste misure.

Il risultato verifica l'effetto del punto iniziale su dati GD153 già osservati e su una sola geometria di sensore. La coincidenza dei colori riguarda le aperture dopo ricentratura. Rimangono aperti il confronto con un riferimento astrometrico di campo e la ripetibilità fra le visite di GRW+70°5824. Nessun avvio PixInsight o chiusura scientifica. [Controllo esplorativo su GRW+70°5824](../bkl046-grw70-held-out-band-apertures-v1/README.md)

Per replicare, passare a `misura.py` questo kit, il kit delle pose GD153 11450, gli ZIP del controllo dither e delle aperture integre, i kit GRW+70°5824 11907 e dei tre calibratori, la directory con NumPy 2.3.5 e Astropy 7.2.0 e un nuovo risultato.