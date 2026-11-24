# BKL-046 · Verifica della traslazione su stelle fuori dal primo puntamento GO14949

Il secondo puntamento usa due pose corte da 40 s, due guide da 150 s e una posa profonda da 400 s in ACS/WFC F606W. Il protocollo ha escluso le sorgenti che cadono entro il contorno di uno dei due sensori della prima posa corta, allargato di 24 pixel. Ha selezionato le sorgenti dalla sola posa A40 e ha congelato la traslazione mediana sui tasselli pari da 512 pixel. Il criterio richiede almeno 24 stelle e 8 tasselli in ogni partizione per sensore, con P90 radiale ≤ 0,1 pixel sui tasselli dispari. [Catalogo delle pose STScI](https://spacetelescope.github.io/hst_notebooks/notebooks/ACS/acs_saturation_trails/acs_saturation_trails.html)

| Sensore | Sorgenti fuori dal primo puntamento | Valide in B40 | Valide in entrambe le guide e in L400 | Valide in tutte le pose |
| --- | ---: | ---: | ---: | ---: |
| 1 | 265 | 1 | 77 | 0 |
| 2 | 270 | 1 | 78 | 0 |

Nella B40, `jdg302cvq_flc.fits`, 282 dei 535 riferimenti sono stati respinti per segnale e 227 per qualità. Altri 22 hanno avuto un picco decentrato e due uno spostamento eccessivo. L'intersezione valida è vuota. Il P90 della traslazione è quindi non valutabile con questo puntamento. Escludendo B40, la copertura diagnostica conterebbe 48 e 35 stelle nei tasselli di verifica. Il protocollo richiede B40 e il risultato resta aperto.

La verifica fornisce una selezione riproducibile di sorgenti fuori dal primo puntamento. La prossima selezione deve qualificare in anticipo la coppia breve anche per qualità e segnale delle sorgenti comuni. Il risultato non attribuisce i rifiuti a una causa strumentale specifica. Nessuna prova nativa o chiusura scientifica.

- Protocollo SHA-256 `1271eaa79ea206c1da5f23fc2ddb3f5f5d53636c41a710f47e8e58a72a8ff7db`
- Programma SHA-256 `28f69e280b3df1e9ce0d7ffd9019739477add1a2561d9d4f7863cd41ebd63edc`
- Ricevuta con 535 righe e replay identico da H: SHA-256 `c7ec09530e84efdf140f95200391574d5251d03887856e3621508c6579b4ee66`
