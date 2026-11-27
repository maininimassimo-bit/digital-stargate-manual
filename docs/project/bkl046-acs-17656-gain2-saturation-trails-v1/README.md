# BKL-046 · Confronto di scie ACS/WFC a gain 2 nel programma 17656

Due pose da 400 s della visita 01 e due da 150 s della visita 02 sono state confrontate con jfdp02vwq e jfdp02w3q, entrambe da 40 s. La guida FINE LOCK/GYRO coincide con quella richiesta, senza mancata acquisizione e con TakeData attivo in tutti i campioni dei quattro log. I log di associazione sono selezionati per nome di esposizione e verificati con gli orari dei singoli FITS. Tutte le pose usano F606W e gain 2. [Log HST](https://hst-docs.stsci.edu/hstdhb/5-observation-logs/5-2-using-observation-logs)

| Posa | Durata | Componenti esaminate | Misure con riferimenti brevi concordi |
| --- | ---: | ---: | ---: |
| jfdp01opq | 400 s | 398 | 0 |
| jfdp01orq | 400 s | 393 | 0 |
| jfdp02vdq | 150 s | 85 | 0 |
| jfdp02vfq | 150 s | 83 | 1 |

Nell'unico caso misurabile, sul chip 1 di jfdp02vfq, le due pose brevi differiscono dello 0,80%. La posa lunga misura il 3,06% in più della loro media. Gli 11 pixel DQ 256 sono tutti dentro l'apertura circolare di 10 px, quindi aggiungere il supporto verticale della scia lascia il risultato invariato. I criteri richiedono una concordanza entro il 2% fra le pose brevi. Tale limite non è stato esteso al confronto lungo-breve. Una singola sorgente con scia contenuta non fornisce una distribuzione di errori o una verifica delle scie oltre l'apertura. I rifiuti rimangono nei rapporti, compresi i flag misti della posa lunga e i flag nei riferimenti brevi.

Per ripetere, preparare una directory con i FITS e le PAM vincolati dai protocolli e usare `verifica.py` con runtime Astropy, runtime SciPy, directory dei dati, protocollo del singolo FLT e nuovo file di uscita. Per i log, usare `verifica-guida.py` con runtime Astropy, directory dei log, directory dei FITS, protocollo di guida e nuovo file di uscita. I riferimenti brevi e le PAM sono nei precedenti archivi H:. [Verifica dei riferimenti brevi](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/0247c695c5370b4780ce726bf2eb51f00903981e/docs/project/bkl046-acs-17656-short-reference-qualification-v1)
