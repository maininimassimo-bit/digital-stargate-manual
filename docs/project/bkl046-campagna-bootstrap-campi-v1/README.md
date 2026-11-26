# BKL-046 · Confronto di intervalli bootstrap per campo

Il test di sviluppo confronta l'intervallo t sui campi, l'intervallo percentile e il bootstrap studentizzato. Ogni ricampionamento usa campi interi e mantiene l'unità statistica del piano. Le medie di campo simulate hanno la stessa distribuzione latente dello studio precedente. I dati e i ricampionamenti hanno semi distinti. Vi sono 4.096 esperimenti per riga e 511 ricampionamenti per esperimento. [Metodo bootstrap e intervalli studentizzati](https://doi.org/10.1214/aos/1176350933)

| Scenario | Campi | t sui campi | Percentile | Studentizzato |
| --- | ---: | ---: | ---: | ---: |
| Gaussiano correlato | 61 | 95,1% | 94,0% | 94,7% |
| Asimmetrico con correlazione 0,50 | 16 | 91,7% | 89,0% | 93,4% |
| Asimmetrico con correlazione 0,50 | 31 | 93,0% | 91,8% | 94,3% |
| Asimmetrico con correlazione 0,50 | 61 | 93,7% | 93,2% | 94,6% |
| Asimmetrico con correlazione 0,50 | 101 | 93,6% | 93,2% | 94,0% |

La tabella riporta la copertura empirica per intervalli nominali al 95%. Negli scenari asimmetrici il bootstrap studentizzato aumenta la copertura di 0,5–1,8 punti percentuali rispetto al t, nei limiti dell'errore Monte Carlo. Le stime rimangono sotto il livello nominale. Il controllo gaussiano non mostra lo stesso vantaggio. Il rapporto conserva per ciascuna replica la copertura, gli errori nelle due code, la larghezza, i rifiuti e la discordanza sugli stessi campioni.

La calibrazione della campagna resta aperta. Il confronto usa solo semi di sviluppo e non fissa l'estimatore finale o il numero di campi. Per riprodurlo passare a `simula-bootstrap.py` il rapporto precedente congelato, la directory con NumPy 2.3.5 e un nuovo percorso per il risultato. [Studio precedente](../bkl046-campagna-intervalli-per-campo-v1/README.md)
