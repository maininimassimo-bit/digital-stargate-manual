# BKL-046 · Copertura e potenza con misure raggruppate per campo

Il protocollo v4 richiede di studiare la numerosità e la copertura degli intervalli prima della calibrazione. Questo test di sviluppo usa differenze appaiate simulate fra due metodi. Ogni campo contiene 16 sorgenti e una componente comune. I campi sono indipendenti per costruzione. Due repliche con semi distinti forniscono 8.192 esperimenti per scenario e numerosità.

| Scenario con 61 campi | Copertura nominale 95%, intervallo sui campi | Copertura trattando le sorgenti come indipendenti | Potenza simulata sui campi per effetto 0,4 |
| --- | ---: | ---: | ---: |
| Gaussiano indipendente | 95,2% | 94,9% | 86,2% |
| Gaussiano, correlazione intra-campo 0,25 | 94,8% | 62,9% | 85,9% |
| Asimmetrico, correlazione 0,25 | 94,0% | 62,2% | 91,7% |
| Asimmetrico, correlazione 0,50 | 93,7% | 48,2% | 92,9% |

L'effetto 0,4 è espresso in deviazioni standard della media di campo e serve come scenario illustrativo. Con 101 campi, lo scenario più asimmetrico raggiunge il 99,5% di potenza simulata a quell'effetto e conserva una copertura del 93,9%. La copertura insufficiente rende la sola potenza inadeguata come criterio di scelta. La calibrazione effettiva dovrà vincolare la numerosità all'effetto pratico, alla dipendenza misurata e alla copertura. [Valori critici t del NIST](https://itl.nist.gov/div898/handbook/eda/section3/eda3672.htm)

Il test usa esclusivamente i semi di sviluppo e nessuna immagine o chiamata nativa. Non consuma semi di calibrazione o verifica e non fissa soglie scientifiche. Il JSON conserva i conteggi di entrambe le repliche. Per riprodurlo passare a `simula.py` il piano v4 congelato, la directory dei pacchetti con NumPy 2.3.5 e un nuovo percorso di uscita.
