# BKL-046 · Recupero di campioni reali sottoposti a clipping artificiale

Il controllo oscura a 40.000 i valori originali di 38.832 campioni Bayer reali nelle 15 pose M8/M20. Per stimare ciascun campione usa la mediana dei valori sotto 62.000 nelle altre 14 pose. Il valore originale della posa esclusa serve come riferimento per il punteggio dopo la stima. L'analisi lavora sui codici grezzi e non usa interpolazione, normalizzazione fra pose o correzioni del fondo.

A un pixel e con almeno tre pose alternative concordi fra le due geometrie affini, si ottengono 38.529 stime. Solo 1.980 (5,14%) raggiungono un errore assoluto relativo entro il 5%. La disponibilità di campioni vicini lascia quindi un errore rilevante per questa regola di stima.

| Fascia del valore nascosto | Campioni di riferimento | Stime | Entro il 5% | Errore assoluto mediano | 90° percentile |
| --- | ---: | ---: | ---: | ---: | ---: |
| 40.000–49.999 | 21.906 | 21.842 | 1.599 | 27,48% | 48,31% |
| 50.000–61.999 | 16.926 | 16.687 | 381 | 34,12% | 53,39% |

La mediana dell'errore con segno è −27,43% e −34,12% nelle due fasce. Fra le stime, 9.025 battono l'errore assoluto del valore troncato a 40.000. Le stime alle coordinate fisse del sensore hanno errori mediani del 61,84% e 67,31% nei rispettivi sottoinsiemi stimabili. Il rapporto conserva anche le varianti a 1,5 pixel e con una sola posa alternativa.

Le pose condividono campo e condizioni di acquisizione. Le fasce e la soglia del 5% sono scelte del protocollo per questo confronto descrittivo. La selezione dei candidati esclude per definizione i valori sopra soglia. I risultati misurano l'errore sul codice originale di un fotosito sotto il limite digitale e non verificano una stima di flusso integrato o il recupero di acquisizioni già al limite. Chiusure scientifiche e avvii PixInsight in questo incremento pari a zero.

Per ripetere, passare a `misura.py` il protocollo, la directory estratta dal kit sui campioni alternativi, la directory estratta dal kit geometrico precedente, lo ZIP delle pose, la ricevuta delle pose, lo ZIP dei dark, la directory con NumPy 2.3.5 e Astropy 7.2.0 e un nuovo file di uscita. [Disponibilità di campioni alternativi](../bkl046-m8-m20-unclipped-alternative-support-v1/README.md)
