# BKL-046 — GD153, confronto con CALSPEC all’epoca 2003

Ho integrato lo spettro CALSPEC gd153_stiswfcnic_004.fits nelle tre catene ACS WFC1, interpolando la risposta all’MJD di ciascuna posa. I valori PHOTFLAM ricostruiti concordano con quelli nei FITS entro lo 0,002%. Le quadrature a quattro e otto nodi restituiscono gli stessi integrali entro la tolleranza fissata. [Throughput ACS dipendente dal tempo](https://www.stsci.edu/hst/instrumentation/acs/instrument-design/system-throughputs) · [Fotometria ACS](https://hst-docs.stsci.edu/acsdhb/chapter-5-acs-data-analysis/5-1-photometry)

| Rapporto | Osservato a 3 px | CALSPEC ad apertura infinita | Scarto relativo |
| --- | ---: | ---: | ---: |
| F658N/F660N | 2,551130 | 2,549030 | +0,082% |
| F658N/F606W | 0,0235531 | 0,0231261 | +1,847% |
| F660N/F606W | 0,00923244 | 0,00907250 | +1,763% |

Le misure a tre pixel raccolgono circa il 78,4% del tasso previsto in F606W e il 79,7–80,0% nelle due bande strette. Le frazioni includono gli effetti di apertura e i residui strumentali. L’accordo del rapporto stretto è circoscritto alle sei pose. La calibrazione ACS usa osservazioni di standard che includono GD153. Il confronto non attribuisce lo scarto a una sola causa e non costituisce una validazione assoluta indipendente della catena ACS. [Calibrazione fotometrica ACS](https://www.stsci.edu/hst/instrumentation/acs/data-analysis/zeropoints)

Due esecuzioni offline identiche. Restano da verificare la curva di crescita per banda e il contributo CTE. Nessuna chiusura scientifica.
SHA-256 archivio H: 1fcb13d243fb2ba6c86e56972e1ad965d8d0c5876e32359fe71db55d93cbfe14.
