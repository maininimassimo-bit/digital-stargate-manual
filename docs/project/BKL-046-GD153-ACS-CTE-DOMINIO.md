# GD153 · Dominio di validità della correzione CTE ACS

Sono stati controllati tutti i 18 FLT ACS/WFC del confronto temporale GD153. È stato misurato il flusso netto nei pixel nativi, in elettroni per posa, entro 3 pixel dal centro verificato. Per confrontare il fondo con il dominio del calcolatore ACS si usa il suo anello di esempio 13–18 pixel. Il riscontro conserva anche il fondo nell'anello 25–40 pixel usato per la fotometria di progetto. Il numero di trasferimenti paralleli è calcolato dalle coordinate del subarray, da LTV2 e dalla convenzione WFC1. [Calcolatore CTE ACS](https://acsphotometriccte.stsci.edu/) · [Convenzione geometrica ACS](https://hst-docs.stsci.edu/acsdhb/chapter-5-acs-data-analysis/5-1-photometry)

| Banda | Conteggio netto nativo a raggio 3, e⁻ | Fondo 13–18 px, e⁻/px |
| --- | ---: | ---: |
| F435W | 291.763–295.985 | 10,60–13,60 |
| F606W | 254.508–262.248 | 8,91–10,42 |
| F814W | 302.932–309.085 | 12,64–14,57 |

Il numero stimato di trasferimenti paralleli è 513,01–514,36. Il calcolatore prescrive misure DRZ e indica il dominio di affidabilità di 50–80.000 elettroni. La pagina tecnica STScI descrive test fino a circa 100.000 elettroni in apertura a 3 pixel. Il flusso misurato su questi FLT eccede entrambi i riferimenti in tutte le pose. Il confronto tra conteggi FLT e intervalli DRZ è diagnostico. Quattro pose F606W hanno inoltre un fondo sotto 10 elettroni/pixel, per cui non si può trasferire automaticamente la stima pubblicata per sorgenti molto brillanti. [Dominio e accuratezza pubblicati](https://www.stsci.edu/hst/instrumentation/acs/performance/photometric-cte-corrections) · [ACS ISR 2022-06](https://www.stsci.edu/files/live/sites/www/files/home/hst/instrumentation/acs/documentation/instrument-science-reports-isrs/_documents/isr2206.pdf)

Tutti i FLT riportano `PCTECORR=OMIT`. Nelle nove associazioni GD153 del campione precedente, MAST ha fornito coppie FLT e RAW e il combinato CRJ, senza controparti FLC o CRC elencate. Il modello fotometrico descritto riguarda la CTE parallela. La verifica non estrapola la correzione, non assume perdite nulle e non stima la CTE seriale. Il confronto a raggio 5 con stime ePSF resta pertanto inalterato. Zero avvii nativi e zero chiusure scientifiche. [Informazioni ACS sulla CTE](https://www.stsci.edu/hst/instrumentation/acs/performance/cte-information)

Replay byte per byte con gli archivi riletti su H:. SHA-256 del riscontro `8d64281164f74345faa8d0f84a8e70815a3225b7dc9e831776d40aa0ff5be1fe`. SHA-256 dell'archivio `6f423cdf2f080c6b59baad109f98bb5926551c2034d3a7fc185815a45337993a`.

[Selezione ACS di GD153](BKL-046-GD153-ACS-CATALOGO.md) · [Stima a raggio 5](BKL-046-GD153-ACS-PSF-STIMA.md).
