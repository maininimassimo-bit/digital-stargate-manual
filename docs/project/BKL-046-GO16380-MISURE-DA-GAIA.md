# BKL-046 · Misura delle pose brevi GO16380 a partire da Gaia

Questa prova parte dalle posizioni Gaia DR3 propagate all'epoca dell'immagine e conserva i filtri di catalogo della [prova precedente](BKL-046-GO16380-COPERTURA-GAIA.md). Usa la soluzione WCS alternativa A e lo scarto di semina ottenuto dai soli tasselli pari. Sono ammessi i riferimenti distanti almeno 8 pixel dalle altre sorgenti Gaia accettate e almeno 56 pixel dai bordi dei tasselli. Il centroide A40 è rimisurato con i controlli DQ e di segnale congelati. La seconda posa deve confermare il centro entro 0,7 pixel nel sistema A40.

| Sensore | Sorgenti Gaia dopo isolamento e margine | Centroidi A40 misurati | Coppia valida, stima / verifica | Tasselli di stima / verifica | Stelle in comune con il campione appaiato di 40 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 278 | 48 | 20 / 23 | 11 / 11 | 2 |
| 2 | 270 | 46 | 17 / 20 | 10 / 11 | 0 |

Il principale punto di esclusione è il controllo di qualità del centroide A40, con 230 e 224 rifiuti. La sola classe di rifiuto non distingue saturazione, altre maschere DQ e problemi del fondo. Nessun sensore raggiunge i 24 riferimenti richiesti in entrambe le partizioni. Il fit affine e il P90 Gaia sui tasselli riservati restano non valutati. L'intersezione con il campione appaiato è stata conteggiata indipendentemente dal fit dai centroidi misurati e non fornisce copertura sufficiente a spiegare il residuo che si ripete.

L'asse `SATURATION_BLEND/4` resta aperto. Nessuna sostituzione di pixel, prova nativa o chiusura scientifica.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Protocollo | `e66929e66a3f07d408e1b041aba0ffd68d48a369aadff6748b42d711584a3fff` |
| Programma | `449502f4eff064a2bb2eab4ca457cb680948608de0c031cdc6d55e31e7a5ec1f` |
| Ricevuta | `12fba94a250c3ba68852c897a7291eb45fd5851f89fdb9d2f95ae77cc3392eb4` |
