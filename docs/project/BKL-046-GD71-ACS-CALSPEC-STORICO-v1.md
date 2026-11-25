# BKL-046 — GD71, confronto con due riferimenti CALSPEC all’epoca 2003

La risposta ACS WFC1 è interpolata separatamente all’MJD di ogni posa. La catena riproduce PHOTFLAM dei FITS entro lo 0,01%. Sono stati integrati lo spettro CALSPEC gd71_stiswfcnic_004 e il modello gd71_mod_012, entrambi fissati per SHA-256. Le quadrature a quattro e otto nodi concordano entro la tolleranza. [CALSPEC STScI](https://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec) · [Throughput ACS](https://www.stsci.edu/hst/instrumentation/acs/instrument-design/system-throughputs)

| Raggio | F658N/F660N osservato | Scarto dallo spettro | Scarto dal modello |
| --- | ---: | ---: | ---: |
| 3 px | 2,537887 | +0,616% | +1,287% |
| 5 px | 2,554702 | +1,283% | +1,958% |
| 10 px | 2,564698 | +1,679% | +2,357% |

A tre e cinque pixel ci sono due pose per banda. A dieci pixel la banda F660N ha una sola posa accettata. Le previsioni ad apertura infinita sono 2,522350 dallo spettro e 2,505634 dal modello. Il cambio di riferimento CALSPEC e il cambio di raggio incidono in modo comparabile sul rapporto. Il rapporto a tre pixel dista dallo spettro CALSPEC più di quanto osservato per GD153. [Confronto GD153](BKL-046-GD153-ACS-CALSPEC-STORICO-v1.md)

Due esecuzioni identiche. Le due stelle condividono il programma e la configurazione ACS. La calibrazione strumentale stessa usa standard CALSPEC. Il confronto costituisce un controllo di sensibilità e non separa correzione di apertura, CTE e calibrazione assoluta. Nessuna chiusura scientifica.
SHA-256 archivio H: dc57f262fb7decc08aeffef0ad448f7f8bd5cf3726899819623543fa2e79c68d.
