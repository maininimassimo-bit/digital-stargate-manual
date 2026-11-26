# BKL-046 · Effetto della griglia di campionamento Gaia XP sui rapporti ACS

GaiaXPy 2.2.0 ricostruisce lo spettro delle due stelle dai coefficienti continui. La griglia predefinita riproduce i flussi e gli errori marginali Gaia entro le tolleranze fissate. Griglie personalizzate da 1, 0,5 e 0,25 nm coprono gli stessi estremi. Per tutte le griglie si integrano le stesse curve ACS all'epoca di ciascuna posa, con quadrature a quattro e otto nodi. [Calibrazione GaiaXPy](https://gaia-dpci.github.io/GaiaXPy-website/tutorials/Calibrator%20tutorial.html)

| Sorgente | F658N/F660N pubblicato, 2 nm | Ricostruito a 0,25 nm | Variazione | ACS a 3 px rispetto a 0,25 nm |
| --- | ---: | ---: | ---: | ---: |
| GD71 | 2,638386 | 2,639020 | +0,0240% | −3,83% |
| GD153 | 2,644750 | 2,645351 | +0,0227% | −3,56% |

I risultati a 0,5 e 0,25 nm differiscono di circa lo 0,0011–0,0012%. La scelta della griglia spiega quindi solo una frazione limitata degli scarti osservati. La griglia più fitta descrive lo stesso modello spettrale continuo. La risoluzione strumentale resta quella del prodotto Gaia XP. Per stimare l'effetto della risposta a una riga serve un modello diretto della dispersione, della trasmissione e della funzione di diffusione spettrale. [Calibrazione esterna Gaia DR3](https://doi.org/10.1051/0004-6361/202243880)

L'installazione locale usa i wheel archiviati e verificati per SHA-256. Il calcolo blocca le connessioni attraverso l'audit Python e ha registrato zero tentativi. Per ripetere passare protocollo, runtime installato dai wheel, manifesto dei wheel, directory dei coefficienti, spettro campionato, directory del confronto fotometrico, protocollo ACS, ricevute delle pose GD71 e GD153 e un nuovo percorso di uscita. Nessuna chiusura scientifica.
