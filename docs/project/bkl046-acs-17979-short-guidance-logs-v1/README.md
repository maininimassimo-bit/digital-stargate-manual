# BKL-046 · Telemetria di guida delle due pose brevi ACS 17979

Ho associato ciascun FITS scientifico da 40 s ai file di log JIF e JIT per identificativo di esposizione e intervallo UTC. Gli estremi registrati concordano entro 0,47 s. Entrambi i FITS scientifici riportano EXPFLAG NORMAL. [Uso dei log HST](https://hst-docs.stsci.edu/hstdhb/5-observation-logs/5-2-using-observation-logs)

| Esposizione | Guida richiesta / effettiva | Acquisizione guida | Campioni TakeData attivi | RMS guida V2 / V3 |
| --- | --- | --- | ---: | --- |
| jfln02qtq | FINE LOCK / GYRO | NOLOCK | 0/14 | assente |
| jfln02qzq | FINE LOCK / FINE LOCK | acquisita | 14/14 | 2,5 / 2,2 mas |

I puntamenti mediani ricostruiti nel JIT differiscono di 38,79 arcsec. Nel primo caso la guida mancata, il flag TakeData inattivo e la separazione ricostruita spiegano perché il puntamento nominale non costituisce un riferimento affidabile per l'abbinamento. La separazione è una misura della ricostruzione OMS. Non è una registrazione stellare. Escludere jfln02qtq dai riferimenti fotometrici. La coppia breve indipendente e la validazione a gain 2 restano da qualificare.

Per ripetere, passare a `verifica.py` il runtime Astropy, la directory dei log, la directory dei due FLT, il protocollo e un file di uscita nuovo. I due FLT risiedono nell'archivio della preselezione. I log e i FITS sono verificati per SHA-256. [Confronto delle immagini](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/953cc7bd595ada0c4d9d1ecca451e1ab294d47cc/docs/project/bkl046-acs-17979-visit02-short-frame-registration-v1)
