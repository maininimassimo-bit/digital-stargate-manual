# BKL‑046 · Registrazione della guida con stelle di riferimento

Il controllo stima la traslazione comune da finestre contenenti stelle di riferimento sintetiche non sature e separate dal bersaglio. Fissa 1, 4 o 16 riferimenti e riusa gli stessi pixel del bersaglio della prova precedente. La regola condizionale applica la correzione solo sopra una soglia di spostamento e dispersione dei riferimenti. Le soglie sono congelate e la cubica di Keys resta l’interpolatore per tutte le ricomposizioni. [Prova di registrazione dalla corona](BKL-046-SATURAZIONE-REGISTRAZIONE-GUIDA.md)

| Scarto della guida | P90 con 1 riferimento, correzione sempre applicata | P90 con 16 riferimenti, correzione sempre applicata | Correzioni applicate dalla regola con 16 riferimenti | Casi entro il 5% al bordo con regola, sostituzione netta / sfumata |
| --- | ---: | ---: | ---: | ---: |
| 0 | 0,478 px | 0,108 px | 0/148 | 132/148 / 96/148 |
| 0,25 px | 0,486 px | 0,109 px | 125/148 | 48/148 / 38/148 |
| 0,50 px | 0,477 px | 0,123 px | 148/148 | 47/148 / 34/148 |

A guida già allineata, la regola con 16 riferimenti conserva tutti i casi entro il criterio di bordo. A 0,25 pixel lascia senza correzione 23 casi e il P90 dell’errore effettivamente applicato risale a 0,25 pixel. A 0,50 pixel applica tutte le correzioni e mantiene il P90 a 0,123 pixel. Nessuno dei gruppi con spostamento non nullo rientra nel limite di 0,1 pixel.

I casi riusano 37 geometrie di bersaglio con quattro campioni di rumore. Le associazioni delle stelle guida sono note e si stima una traslazione comune. Tutte le coppie già risolte rimangono tali, senza picchi aggiuntivi non abbinati. La prova non trasferisce la regola a campi reali con distorsione, saturazione estesa o errori di associazione. L’asse `SATURATION_BLEND/4` resta aperto.

SHA‑256 della ricevuta `fbc152d40bdf7658728ba1bd54226256075f633b10bb232b0ae44516e3dbfb51`.
