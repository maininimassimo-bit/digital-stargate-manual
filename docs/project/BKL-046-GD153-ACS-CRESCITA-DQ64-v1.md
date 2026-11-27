# BKL-046 — Crescita dell’apertura e pixel tiepidi in GD153

La nuova misura usa gli stessi sei FITS, centri e mappa d’area. Nell’apertura ammette i pixel con DQ esattamente 64, identificati da STScI come pixel tiepidi. Il fondo continua a usare solo DQ zero. Per ciascuna posa viene registrato anche il tasso con i pixel 64 omessi. Il controllo riproduce la misura precedente a tre pixel, dove il flag è assente. [Flag DQ ACS](https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps)

| Raggio | Pose misurate | F658N/F660N | Scarto da CALSPEC ad apertura infinita |
| --- | ---: | ---: | ---: |
| 3 px | 6 | 2,551130 | +0,082% |
| 5 px | 6 | 2,578371 | +1,151% |
| 10 px | 6 | 2,583248 | +1,342% |
| 15 e 20 px | 0 | — | — |

A dieci pixel la somma dei pixel 64 è al massimo lo 0,115% del flusso in ciascuna posa. Trattenerli invece di ometterli cambia il rapporto stretto di −0,00134%. La scelta del raggio cambia il rapporto di circa 1,26% fra tre e dieci pixel. L’accordo a tre pixel non si riproduce alle altre aperture. A quindici pixel sono presenti altri flag DQ e il criterio di qualità esclude tutte le pose. [Confronto con CALSPEC](BKL-046-GD153-ACS-CALSPEC-STORICO-v1.md)

Due esecuzioni identiche. L’effetto osservato dipende dal raggio, con possibili contributi di profilo PSF e CTE. Restano da verificare l’energia racchiusa per banda e la correzione CTE. Nessuna chiusura scientifica.
SHA-256 archivio H: 48f2e0264ae473900fa37e52481b7e8ee69a0b68ba5505f397c8f6872176563b.
