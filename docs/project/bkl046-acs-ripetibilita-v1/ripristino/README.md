# BKL-046 – Ripristino dei FITS ACS

Il manifest fissa i 24 prodotti FLT, le loro dimensioni e le impronte SHA-256. La verifica su DSG-Shared ha scaricato tutti e 24 i prodotti da MAST e ne ha confermato le impronte. [Servizio di download MAST](https://mast.stsci.edu/api/v0/MastApiTutorial.html)

Con Python 3.12, esegui il comando in una directory contenente questi allegati.

~~~powershell
python -I -S -B .\ripristina-fits-v1.py .\acquisizione.json .\fits
~~~

Usa l'opzione di verifica offline se i FITS sono già presenti. Per riprodurre la fotometria, copia nella directory dei FITS anche il piano della coorte, il riscontro astrometrico e lo script base di questa directory. La riproduzione storica usa l'ambiente Astropy della VM (Astropy 7.2.0, NumPy 2.3.5 e PyERFA 2.0.1.5). Le due mappe PAM del STScI sono fissate nello script base. Il [supplemento delle aperture](../RIPRODUZIONE-ARCHIVIO.md) contiene gli script e i risultati derivati.

La verifica copre l'identità dei FITS recuperati. Il trasferimento fotometrico tra visite resta da qualificare.
