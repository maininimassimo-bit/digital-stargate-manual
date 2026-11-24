# BKL-046 · Replica GO14949 su una seconda posa da 400 s

La seconda integrazione F606W, `jdg301byq_flc.fits`, appartiene alla stessa visita e allo stesso campo di `jdg301bwq_flc.fits`. Il confronto riutilizza le 677 associazioni, le due guide da 150 s, la posa di controllo B40, le maschere, il metodo di stima e la partizione spaziale della [prima prova](BKL-046-GO14949-GUIDA-FULLWELL.md). Verifica la ripetibilità fra due integrazioni dello stesso campo. [Archivio STScI](https://spacetelescope.github.io/hst_notebooks/notebooks/ACS/acs_saturation_trails/acs_saturation_trails.html)

| Posa | Sensore | Stelle per stima / verifica | Tasselli per stima / verifica | P90 affine | P90 traslazione |
| --- | --- | ---: | ---: | ---: | ---: |
| jdg301bwq | 1 | 29 / 18 | 13 / 9 | — | — |
| jdg301byq | 1 | 27 / 17 | 14 / 9 | — | — |
| jdg301bwq | 2 | 36 / 40 | 14 / 15 | 0,101571 px | 0,095700 px |
| jdg301byq | 2 | 39 / 41 | 14 / 15 | 0,104281 px | 0,081721 px |

Sul primo sensore entrambe le pose restano sotto le 24 stelle di verifica richieste. Sul secondo il modello affine supera il limite di 0,1 pixel in entrambe le pose. La traslazione, valutata a titolo diagnostico, rientra nel limite su quel sensore in entrambe le pose. I medesimi tre indici di sorgente, 2, 10 e 11, mostrano flag compatibili con il solo full well attorno alle posizioni centrate previste. Restano preliminari, con zero casi ammessi alla prequalifica geometrica.

Per qualificare la traslazione occorre fissare il modello prima di valutare un campo indipendente e raggiungere le quote di verifica su entrambi i sensori. La corrispondenza dei flag in due pose dello stesso campo non dimostra il recupero del flusso. L'asse `SATURATION_BLEND/4` resta aperto. Nessuna chiusura scientifica o esecuzione nativa.

| Evidenza | SHA-256 |
| --- | --- |
| Seconda posa MAST | `9c88ded107cd56fdee309a459a58becdd5b65d75cbd8ab491314390de95f6b94` |
| Protocollo | `4f8c74aac1e22786ffa6e83b0057963a567d120826656e52ccac8a4c0d4ff5fe` |
| Programma | `c600f5f1534619a5dda2696e6d8622c5831597638a2bb0a5fb825f9e2af80b8f` |
| Ricevuta riprodotta con hash identico da H: | `faa34f97a0b216b442504aa7574fe03e3ce4dbf87292b6856d9a43caf66f949b` |
