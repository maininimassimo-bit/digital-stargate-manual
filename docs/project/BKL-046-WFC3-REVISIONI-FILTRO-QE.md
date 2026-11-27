# BKL-046 · Effetto delle revisioni filtro e QE WFC3/UVIS

Il confronto usa le tabelle Synphot 002 e 003 di F438W, F606W, F814W, UVIS1 e UVIS2. Gli header delle tre coppie filtro distinguono la trasmissione misurata a terra dalla correzione di zeropoint basata sulle osservazioni in volo. Gli header QE descrivono invece due revisioni della calibrazione a terra, la seconda con ricalibrazione dei rivelatori di riferimento dopo TV3. Le componenti sono confrontate separatamente. [Cronologia STScI della calibrazione UVIS](https://www.stsci.edu/hst/instrumentation/wfc3/data-analysis/photometric-calibration/uvis-photometric-calibration.html)

Nell'intervallo comune da 2.000 a 10.900 Å, sui nodi sopra l'1% del picco della curva 002, la correzione filtro è compatibile con una moltiplicazione scalare entro 4,7 × 10⁻⁸ in frazione. I fattori sono 0,9923, 0,9930 e 1,0111. La revisione QE si discosta dalla moltiplicazione scalare fino a circa il 21% sui nodi considerati. Questo è uno scarto fra due revisioni calibrate, senza interpretazione come incertezza o deriva in volo.

L'integrazione usa interpolazione lineare sui nodi originali e quadratura gaussiana per il peso fotonico λ × Fλ × filtro × QE. Le ottiche comuni sono omesse in tutti i casi. I valori descrivono il contributo delle due componenti, con tre spettri CALSPEC fissi e due sensori. GD153 e GD71 sono modelli, P330E è un prodotto spettrofotometrico composito. [CALSPEC STScI](https://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec)

| Colore | Solo correzione filtro in volo | Solo ricalibrazione QE a terra | Entrambe le revisioni |
| --- | ---: | ---: | ---: |
| F438W−F606W | +0,766 mmag | da −34,447 a −33,080 mmag | da −33,681 a −32,314 mmag |
| F438W−F814W | +20,378 mmag | da −31,083 a −29,809 mmag | da −10,706 a −9,431 mmag |
| F606W−F814W | +19,612 mmag | da +2,065 a +4,625 mmag | da +21,678 a +24,237 mmag |

Il risultato quantifica l'effetto di sostituire curve di provenienza documentata. Non stabilisce una calibrazione separata dei componenti in volo, un limite di incertezza o una prestazione nativa. `FILTER_COLOR/2` resta aperto.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Protocollo e impronte dei tredici FITS | `189c81558830fef860ed69339a1ee5abdc01811d2a0f5851a16c94abc351ea17` |
| Programma | `af46449c0edcdfd4fd5cf1e78da7e13e68997dce6f114fba220fe20373de96ed` |
| Ricevuta con provenienza, bande e colori | `95f2a8a67a125f194eb1d85b71973f23c5e9f25fb6fe96044409836983b0ac0b` |
