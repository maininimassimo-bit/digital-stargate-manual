# BKL-046 · Ammissibilità fotometrica di tre visite WFC3/UVIS su P330E

La selezione MAST conserva tre visite del programma 17361 con F438W, F606W e F814W. Per ciascuna banda e visita sono stati acquisiti i due prodotti FLC originali CALWF3, per 18 esposizioni. Il protocollo ammette solo immagini stazionarie con telemetria nominale, correzioni CTE e FLUXCORR complete e supporto dell'apertura senza flag DQ. La fotometria prevista usa mappe dell'area pixel specifiche per sensore e il PHOTFLAM delle immagini già scalate. [Pixel Area Map per le sottofinestre UVIS](https://spacetelescope.github.io/hst_notebooks/notebooks/WFC3/uvis_pam_corrections/WFC3_UVIS_Pixel_Area_Map_Corrections_for_Subarrays.html) · [Fotometria WFC3](https://hst-docs.stsci.edu/wfc3dhb/chapter-9-wfc3-data-analysis/9-1-photometry)

| Visita | Sensore | Fotogrammi | Esito |
| --- | ---: | ---: | --- |
| if6h12 | 1 | 6 | Tutti recano il flag `TDF-DOWN AT EXPSTART` |
| if6h13 | 2 | 6 | Tutti respinti per DQ 16 nel nucleo |
| if6h62 | 1 | 6 | Tutti respinti per DQ 16 nel nucleo |

La rilettura dei 12 nuclei respinti ha trovato fra 5 e 8 pixel caldi per nucleo da 7 × 7 pixel. Le parole DQ del nucleo contengono soltanto 0 e 16. Il veto osservato è quindi attribuito ai pixel caldi. Il programma conserva tutte le esclusioni e nessuna terna valida. La ripetibilità dei colori resta non misurata. [Definizioni DQ UVIS](https://hst-docs.stsci.edu/wfc3dhb/chapter-3-wfc3-data-calibration/3-2-uvis-data-calibration-steps)

`FILTER_COLOR/2` resta aperto. Servono visite con esposizioni ammissibili e posizioni del bersaglio che offrano un nucleo pulito. Anche con terne valide, un confronto fra visite su sensori diversi deve considerare tempo, geometria e calibrazione. Nessuna prova nativa o chiusura scientifica.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Protocollo, associazioni e impronte degli input | `2a27de573312e411a69079a3ffd7b5f3a703aa8326c8250082fa385846099097` |
| Ricevuta delle 18 esposizioni | `8efea2431311ca3545b7163e4b6a29988ddd9343b65547182abdf6a4653a5aa3` |
| Esame dei 12 nuclei DQ | `7da57bc6466726d3dd661a9c006daef40e787a866e742a4c4d859e40dc7209e4` |
