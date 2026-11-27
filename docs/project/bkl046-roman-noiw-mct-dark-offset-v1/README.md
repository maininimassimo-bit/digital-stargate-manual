# BKL-046 · Riferimento MCT al buio nella serie Roman NOIW

Ho riletto header e tabelle `LABHK` di tutti i 39 FITS Roman NOIW. I 195 intervalli HTTP sono vincolati all’ETag e alla lunghezza del rispettivo file. Le 287 righe di telemetria contengono 212 istanti distinti. Le righe ripetute allo stesso istante coincidono in tutti i campi. [Archivio NOIW](https://archive.stsci.edu/dcl/triplet-tests/fr03/20210907230637_noiw/) · [Descrizione del test senza illuminazione](https://archive.stsci.edu/missions-and-data/roman/wfi-triplet-test-data)

Il monitor MCT della serie al buio va da 6,943 a 10,900 mV, con mediana di 8,268 mV. Nella serie GAIN il monitor va da 800,2 a 808,7 mV. La prima esposizione NOIW è a 5,998 giorni dalla prima GAIN. Le letture NOIW forniscono un riferimento osservato in un’altra sessione di laboratorio.

Ho sottratto in via ipotetica il minimo, la mediana e il massimo NOIW dal segnale MCT GAIN, mantenendo le stesse coppie e finestre temporali. Alla lettura 10 con l’inizio nominale, il coefficiente di variazione del segnale normalizzato è 0,4495% senza sottrazione e fra 0,4499% e 0,4501% con le tre ipotesi. Le tre ipotesi conservano il risultato descrittivo della prova GAIN. [Telemetria GAIN](../bkl046-roman-gain-lab-photodiode-v1/README.md)

Resta da verificare quale offset valga durante le esposizioni GAIN, la conversione in fotoni al sensore e la temporizzazione per pixel. Nessuna chiusura scientifica o esecuzione nativa.

Per riprodurre offline, passare a `verifica.py` la directory del kit, la directory delle dipendenze Astropy, `replay`, la directory estratta del kit GAIN, un nuovo rapporto e lo SHA-256 della cattura `6f853e724ca56695ba1f4011c84367a06c0c49c6ce4e4cb28007a931240aed5f`.