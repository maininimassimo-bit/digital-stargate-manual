# BKL-046 – Astrometria GD71 e fotometria GRW+70D5824

La WCS principale dei FITS colloca il picco di GD71 a 3,76–3,81″ dal riferimento CALSPEC della visita 03 e a 2,89–2,95″ nella 04. Con le WCS alternative lo scarto minimo è 2,42″. Astropy segnala incongruenze SIP per le soluzioni alternative. [Riscontro WCS](gd71-wcs.json) · [Guida STScI](https://hst-docs.stsci.edu/drizzpac/chapter-4-astrometric-information-in-the-header/4-5-absolute-astrometry)

Il catalogo HSC v3 associa il candidato GD71 più brillante in F606W e F658N nella visita 03, con correzione astrometrica assoluta. La visita 04 è priva di quella correzione. Le ricerche per i mosaici F660N non restituiscono rilevazioni. Tolto il candidato GD71, nelle pose F606W si trova un solo riferimento HSC con correzione assoluta e flag zero nella visita 03, e zero nella 04. Entrambe restano escluse dalla fotometria a tre filtri. [Riscontro HSC](gd71-hsc.json) · [Stelle di campo](gd71-stelle-campo.json) · [HSC](https://catalogs.mast.stsci.edu/docs/hsc.html)

Per GRW+70D5824, con spettro CALSPEC e profili SVO fissi, la variazione di PHOTFLAM prevede +0,00004% per F658N/F660N tra visite. L'apertura frazionaria misura +0,513% a 3 pixel e +0,532% a 5 pixel. PHOTFLAM da sola lascia quasi tutto lo scarto da spiegare. Restano aperte la qualifica della correzione d'apertura e quella del trasferimento di carica. [Riscontro PHOTFLAM](grw-photflam.json) · [CALSPEC](https://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec.html)

Gli input originali HSC, SVO e CALSPEC e gli script restano archiviati su H:. I FITS sono recuperabili con la procedura pubblicata. Restano zero controlli qualificati e zero chiusure scientifiche. [Ripristino dai FITS](../ripristino/README.md)
