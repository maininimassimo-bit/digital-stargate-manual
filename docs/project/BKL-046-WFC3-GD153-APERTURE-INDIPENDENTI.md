# GD153 · Verifica numerica indipendente delle aperture WFC3

La seconda implementazione usa gli stessi 48 FLC e le posizioni individuate tramite dither, con un nuovo centro pesato su 5×5 pixel e integrazione per centri di pixel. Conserva i controlli di provenienza, i DQ, la PAM e il limite di 0,05 giorni tra le tre bande. Per le 18 aperture ammesse da entrambi i misuratori, a parità di raggio di 10 pixel e anello locale 16–22, la differenza di flusso è compresa tra −0,0286% e +0,0607%. L'indipendenza riguarda il calcolo di apertura. Le immagini, le posizioni iniziali e la calibrazione sono condivise.

Per confrontare le scelte con WFC3 ISR 2009-31, §4 e tabella 3, è stato introdotto anche un anello 75–125 pixel. Sono state calcolate sia la mediana sia una stima della moda con campione troncato a quattro sigma robusti. I colori ST derivati da PHOTFLAM sono stati calcolati prima e dopo la correzione con le frazioni di encircled energy della tabella. La riduzione storica usa FLT e rimozione dei raggi cosmici. La prova qui usa FLC moderni e respinge le aperture con pixel DQ non nulli. [STScI, WFC3 ISR 2009-31](https://www.stsci.edu/files/live/sites/www/files/home/hst/instrumentation/wfc3/documentation/instrument-science-reports-isrs/_documents/2009/WFC3-2009-31.pdf)

| Raggio (pixel) | Aperture valide | Terne valide entro 0,05 giorni |
| --- | ---: | ---: |
| 5 | 44 | 10 |
| 10 | 20 | 4 |
| 20 | 4 | 0 |

Nelle quattro terne comuni a 5 e 10 pixel, il cambio di raggio, dopo la rispettiva correzione di encircled energy, sposta i colori di un massimo di 9,78 millimagnitudini. A 10 pixel, mediana e stima della moda nell'anello ampio differiscono al massimo di 5,65 millimagnitudini. I quattro confronti a 10 pixel provengono da due sole visite, due terne per visita. I pixel inclusi al bordo dell’apertura differiscono fra l'integrazione binaria e quella frazionaria e spiegano perché le rispettive selezioni DQ non coincidono necessariamente. I confronti non forniscono una validazione indipendente tra strumenti o pipeline. L'asse `FILTER_COLOR/2` resta aperto, con zero avvii nativi e zero chiusure scientifiche.

Replay byte per byte dagli archivi riletti su H:. Riscontro SHA-256 `5408d94a2a530b111fd2953cd1789b8f3a6f69a2ae6fe8a4266cacc221b9e4ab`. Archivio SHA-256 `548371fdcae54b5b896153e1bb29530f3a42b0730cb486157f87e61a8493e9b3`.

[Misure di riferimento per dither](BKL-046-WFC3-GD153-DITHER.md).
