# BKL-046 · Registrazione regionale nelle pose Bayer M8 e M20

Le 15 pose RGGB da 180 s della sequenza di Colmic sono rilette dallo ZIP archiviato. La prima è il riferimento. Per ciascuna delle altre 14 pose si misurano gli spostamenti in 16 riquadri fissi di 384 × 384 pixel nativi, usando la media dei due verdi per cella Bayer. Otto riquadri a scacchiera stimano la traslazione media e il campo affine degli spostamenti. Gli altri otto misurano l'errore radiale di previsione. I due modelli usano gli stessi riquadri, senza eliminare misure a posteriori. Un controllo numerico recupera un campo affine noto sui riquadri esclusi. [Serie originale](https://siril.org/tutorials/tuto-scripts/index.html)

| Modello | P90 dei 112 residui regionali (px) | Pose con P90 ≤ 0,30 px |
| --- | ---: | ---: |
| Traslazione media | 0,516 | 1/14 |
| Campo affine | 0,353 | 10/14 |

Il modello affine riduce il P90 in 13 pose su 14. Restano quattro pose oltre soglia, con P90 da 0,301 a 0,356 px. I 112 residui condividono lo stesso campo e lo stesso riferimento. Le misure riguardano gli spostamenti regionali stimati dalla correlazione e includono il suo errore. Non stimano l'accuratezza astrometrica per sorgente. La soglia è un criterio diagnostico fissato per questo confronto. Il risultato individua dove un'unica traslazione è insufficiente, ma lascia aperti la validazione a livello di stella e il confronto a scala comune fra ricostruzioni CFA, con misure di flusso e rumore.

SHA-256 della ricevuta `ff52f15b3fb8d1475971c8686438d1c0636ee5849da9fc0728bbdce45c9500ec`.
