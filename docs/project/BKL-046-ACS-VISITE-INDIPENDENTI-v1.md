# BKL-046 — Visite ACS esterne al programma 10054

La ricerca CADC ha individuato quattro visite con almeno due esposizioni FLT distinte per ciascuna delle bande F606W, F658N e F660N. La rilettura su H: fisico ha verificato impronte e struttura FITS dei 24 prodotti. Tutti sono subarray 512 × 512, con PCTECORR=OMIT. Il flag DQ 256 è assente nei piani verificati. [Archivio CADC](https://www1.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/doc/tap/)

Per GRW+70D5824 il riferimento CALSPEC riportato all'epoca delle immagini ha permesso di misurare le due visite sul chip WFC1. Le due repliche per banda superano i controlli a 3 e 5 pixel. Una sola visita supera i controlli a 10 pixel. Le mappe STScI sono state applicate al chip corrispondente. [Astrometria CALSPEC](https://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec.html) · [Mappe d'area ACS](https://www.stsci.edu/hst/instrumentation/acs/data-analysis/pixel-area-maps)

| Rapporto | Visita 06 rispetto alla 03 a 3 px | Visita 06 rispetto alla 03 a 5 px |
| --- | ---: | ---: |
| F658N/F606W | +1,386% | +0,648% |
| F658N/F660N | +1,398% | +0,615% |
| F660N/F606W | −0,012% | +0,033% |

Per GD71 il confronto con Gaia DR3, riportato all'epoca delle immagini, lascia distanze di circa 81 e 60 pixel fra la posizione prevista e il candidato più luminoso nelle due visite. I quattro subarray F606W non offrono altri riferimenti Gaia dotati di moto proprio entro l'impronta WCS nominale. Le due visite GD71 sono escluse dal confronto. [Gaia@AIP](https://gaia.aip.de/cms/services/scripted-access/)

Il confronto descrive due visite di una stella sullo stesso chip. La verifica su chip diversi, la caratterizzazione CTE e la correzione a un'apertura angolare di riferimento restano da qualificare. Controlli qualificati e chiusure scientifiche restano a zero.

Riscontri archiviati su H: fisico e verificati dopo la rilettura.

- Struttura e impronte FITS: `8cc28526a5a12b65dbe4138dfc5241d14494c7dc7ead62107af10b4c52f9b6f7`
- Fotometria con riferimento CALSPEC: `8a6394cdc9d700f66ba3e44b86390b451b2b343b36f162e65db78e1ec9781d6c`
- Confronto delle visite GRW: `60a09794141ed7ac26e88cfc094720beb6925c9d3fd35acf1e25877d623c108c`
- Supporto astrometrico Gaia per GD71: `f9d28f68a0c25513e8693626a20c64db126e0a3ec9572b7dfe96aad66b845884`
