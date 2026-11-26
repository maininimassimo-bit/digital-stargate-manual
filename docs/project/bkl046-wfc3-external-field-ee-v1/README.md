# BKL-046 · Curve WFC3 su due campi fuori dal campione di stelle standard

Ho selezionato dal catalogo MAST le sei esposizioni WFC3/UVIS di 35 secondi del programma 11452 su 47 Tucanae e Omega Centauri. Per ciascun campo le esposizioni F438W, F606W e F814W rientrano in 0,03 giorni. Ho individuato i candidati in F606W, proiettato le posizioni sugli altri FLC e conservato solo corrispondenze con aperture integre a 5 e 10 pixel e con i criteri d'isolamento soddisfatti in tutte le bande. [Prodotti HST su MAST](https://archive.stsci.edu/missions-and-data/hst/) · [Curve WFC3 STScI](https://www.stsci.edu/hst/instrumentation/wfc3/data-analysis/photometric-calibration/uvis-encircled-energy)

| Campo | Sorgenti ammesse UVIS1 | Sorgenti ammesse UVIS2 |
| --- | ---: | ---: |
| 47 Tucanae | 11 | 12 |
| Omega Centauri | 0 | 0 |

Nel campo di Omega Centauri il veto più frequente è la presenza di un altro picco entro il raggio d'isolamento. Il rapporto conserva i conteggi per filtro e i risultati individuali delle 23 sorgenti ammesse. La tabella confronta l'errore assoluto mediano, in millimagnitudini, sul cambiamento di colore da 5 a 10 pixel.

| 47 Tucanae, chip e metodo | F438W − F606W | F438W − F814W | F606W − F814W |
| --- | ---: | ---: | ---: |
| UVIS1, zero | 7,56 | 12,86 | 6,77 |
| UVIS1, tabella del chip | 8,34 | 12,02 | 4,74 |
| UVIS1, tabella UVIS2 per il campo intero | 10,24 | 31,83 | 28,83 |
| UVIS2, zero | 18,06 | 18,02 | 4,93 |
| UVIS2, tabella UVIS2 | 17,14 | 21,13 | 27,43 |

Il campione aggiunge sorgenti osservate esterne alla lista di stelle standard usate per le curve. Le sorgenti ammesse condividono una sola visita e tre esposizioni. Restano aperte la ripetibilità fra campi, la misura del contributo di vicini sotto soglia e l'incertezza dovuta a corrispondenze e calibrazione. Il controllo non estende il risultato di un singolo campo all'intera camera. Zero avvii PixInsight e zero chiusure scientifiche. [Controllo precedente sulle stelle standard](../bkl046-wfc3-official-ee-aperture-transfer-v1/README.md)

Per riprodurre dalla copia H/K, passare a `misura.py` la directory del kit estratto, quella con Astropy 7.2.0 e NumPy 2.3.5, un nuovo file di risultato e l'impronta dell'acquisizione `3d6bf1d72f4966fbcdf8620b44294cca7815c9ce764158719cd82c9bbf2dbea7`. Il kit conserva i sei FITS, le tabelle EE, le mappe PAM e il catalogo fissato.