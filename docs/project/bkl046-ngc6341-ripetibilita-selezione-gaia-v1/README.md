# BKL-046 · Ripetibilità ACS fuori dal campione Gaia di NGC 6341

Il confronto riproduce i rapporti Gaia del 2002 e ACS del 2006 con gli input congelati. Incrocia gli esiti mediante gli identificativi dei centroidi originali. Nel 2006 considera ripetibile una coppia di misure che differisce al massimo di 0,3 pixel una volta riportata sulla griglia del 2002.

| Chip | Selezione Gaia 2002 | Centroidi del gruppo | Corrispondenze nelle due pose 2006 | Ripetibili |
| --- | --- | ---: | ---: | ---: |
| 1 | Stessa identità nelle due pose | 44 | 12 | 12 |
| 1 | Nessuna associazione nelle due pose | 297 | 95 | 94 |
| 2 | Stessa identità nelle due pose | 71 | 14 | 14 |
| 2 | Nessuna associazione nelle due pose | 324 | 71 | 71 |

Limitarsi alle associazioni Gaia del pilot escluderebbe 165 dei 191 centroidi con controparte ripetibile nelle due pose successive. Le immagini 2006 sono acquisizioni distinte. La registrazione riusa le posizioni storiche e il campione è soggetto a copertura e selezione. Questi risultati misurano la copertura di un sottoinsieme ripetibile. L'identità assoluta e la completezza Gaia sull'intera coorte restano da determinare.

Eseguire `confronto.py` con la copia di replay dei moti propri che contiene le directory acs, gaia, match e centroids, le directory FITS 2002 e 2006, il JSON dei centroidi, la directory dei pacchetti Python e un nuovo percorso di uscita.
