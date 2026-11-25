# BKL-046 · PSF empirica e ordine del fondo su M8/M20

Ho costruito un profilo empirico per ciascuna banda con 15 stelle di stima della calibrazione A. Le immagini ricentrate sono normalizzate al flusso entro 6 px dopo sottrazione di un piano stimato nell'anello 9–13 px. Dalla mediana dei campioni ho costruito una griglia a passo 1 px, con supporto 8 px e bordo attenuato. Il profilo descrive le immagini CFA ricostruite per parità a questa scala. La prova non stima una ePSF sovracampionata del rivelatore. [Costruzione di profili empirici](https://docs.astropy.org/projects/photutils/en/stable/user_guide/epsf_building.html)

I modelli congiunti provano entrambe le PSF, Moffat ed empirica, con fondo planare oppure quadratico. Mantengono le stesse posizioni Gaia, gli stessi pixel entro 10 px e la stessa stima di un unico zero cromatico nella calibrazione A. Le zone di stima (1, 3, 9, 11) sono disgiunte da quelle di verifica (4, 6, 12, 14). Tutte le 19 stelle di verifica sono utilizzabili in entrambe le calibrazioni. Apertura e Moffat planare riproducono le metriche precedenti.

| Metodo | Sony UV/IR + L-Pro, P90 A/B (mag) | IMX571 Siril + L-Pro, P90 A/B (mag) |
| --- | ---: | ---: |
| Apertura a 6 px | 0,126 / 0,122 | 0,103 / 0,111 |
| Moffat, fondo planare | 0,440 / 0,448 | 0,449 / 0,447 |
| PSF empirica, fondo planare | 0,396 / 0,411 | 0,410 / 0,408 |
| Moffat, fondo quadratico | 0,579 / 0,592 | 0,585 / 0,588 |
| PSF empirica, fondo quadratico | 0,517 / 0,526 | 0,522 / 0,523 |

La PSF empirica planare riduce il P90 cromatico di 0,037–0,044 mag rispetto a Moffat, ma rimane distante dalla fotometria d'apertura. Nel nucleo blu, il P90 dell'RMS per pixel, normalizzato al flusso di apertura, scende da circa 0,0072 a 0,0064. Il miglioramento in rosso è minore. Il fondo quadratico può diminuire l'RMS per pixel e peggiorare contemporaneamente il colore. I residui in pixel quindi non bastano per qualificare i flussi stellari. Restano da verificare separatamente la forma locale della PSF, la struttura del fondo e la risposta spettrale. FILTER_COLOR/3 resta aperto.

- SHA-256 della ricevuta `3ecf8e80873f0ddef41693aad987aac7f339db2b6e7abfaa7543a4060b7d86db`.
- Archivio H: `Produzione/2026-10-13/Digital-StarGate-PixInsight/archives/BKL046-M8-PSF-empirica-3ecf8e80873f.zip`.
- Zero chiusure scientifiche e zero avvii nativi.
