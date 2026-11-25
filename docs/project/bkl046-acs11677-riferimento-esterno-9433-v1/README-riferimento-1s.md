# BKL-046 — Esposizione indipendente ACS/WFC F606W da un secondo

Il FITS `j6mfa8v8q_flc.fits` del programma 9433 è stato acquisito dalla sorgente pubblica MAST. Dimensione, versione dell'oggetto, ETag e CRC64NVME concordano con quelli del provider. Il WCS del FITS e del suo headerlet dichiara FK5 J2000. Il FITS sorgente di GO-11677 dichiara ICRS. La proiezione effettua esplicitamente la conversione di sistema e conferma la copertura interna univoca di 264 dei 340 centri congelati.

Il filtro diagnostico trova 33 centri con picco e qualità compatibili con un riferimento non saturo, 131 con flag DQ e 100 con supporto o ricentraggio insufficiente. Le quattro coppie di chip hanno rispettivamente 6, 2, 0 e 2 stelle geometriche abbinate. Nessuna coppia raggiunge le 24 stelle e le 8 tessere richieste per ciascuna metà della stima e del controllo indipendente. Nessuna delle 33 sorgenti diagnostiche può quindi essere ammessa a una misura di flusso con questo protocollo.

L'esposizione è anteriore di 2.593,8 giorni rispetto al riferimento. Questo esito, dominato dal numero insufficiente di corrispondenze, lascia da valutare separatamente l'esposizione da 30 secondi di GO-11887, acquisita circa 177 giorni prima del riferimento. Rimangono aperte la misura del flusso stellare e la chiusura scientifica.
