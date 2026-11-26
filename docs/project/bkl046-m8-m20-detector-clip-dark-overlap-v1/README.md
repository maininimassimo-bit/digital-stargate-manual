# BKL-046 · Ricorrenza del clipping alle coordinate del sensore in M8/M20

Un fotosito rosso raggiunge 65.535 in tutti i 15 dark e in tutte le 15 pose M8/M20. La sua posizione coincide alla coordinata intera del sensore. Le 15 occorrenze associate costituiscono lo 0,0251% delle 59.700 occorrenze al limite nelle pose. Il confronto identifica un sito persistente anche al buio, utile come controllo positivo.

| Parità CFA | Siti al limite in almeno una posa | Siti al limite in tutte le pose | Occorrenze al limite nelle pose | Occorrenze nella coda dei dark | Occorrenze su siti al limite nei dark |
| --- | ---: | ---: | ---: | ---: | ---: |
| R | 3.600 | 17 | 13.414 | 17 | 15 |
| G1 | 3.759 | 51 | 16.683 | 4 | 0 |
| G2 | 3.717 | 46 | 16.657 | 15 | 0 |
| B | 3.042 | 48 | 12.946 | 14 | 0 |
| Totale | 14.118 | 162 | 59.700 | 50 | 15 |

La coda è definita separatamente per parità sul massimo di ogni fotosito nei 15 dark. Include lo 0,1% superiore per rango e tutte le parità di valore alla soglia. Comprende da 6.543 a 6.613 siti per parità e 12 dei siti al limite in almeno una posa. Fra i dark solo il sito rosso arriva anche alla soglia 62.000. Il rapporto conserva gli istogrammi di ricorrenza completi, distinguendo i siti dalle occorrenze per posa.

Il confronto è eseguito sui FITS CFA senza registrazione o interpolazione. Le due serie sono da 180 secondi e guadagno 100. I dark del 9–10 luglio 2020 precedono le pose del 18 agosto 2020. La mancata coincidenza con questi dark lascia aperta la causa delle altre saturazioni persistenti. Restano da verificare la risposta fisica, il recupero fotometrico e il comportamento nativo. Nessun avvio PixInsight e nessuna chiusura scientifica.

Per replicare, passare a `misura.py` il protocollo, lo ZIP delle pose, la ricevuta delle pose, lo ZIP dei dark, la ricevuta dei calibratori, il rapporto precedente sulle parità, la directory di NumPy 2.3.5/Astropy 7.2.0 e un percorso nuovo per il risultato. Gli ingressi sono fissati per SHA-256 e gli originali sono conservati negli archivi di progetto.
