# BKL-046 · Verifica stellare della registrazione Bayer M8 e M20

Il confronto riusa i due modelli geometrici stimati sui riquadri pari e misura i centroidi stellari nei soli otto riquadri dispari, esclusi dal fit. La selezione avviene sulla prima posa. Si cerca il massimo in ciascuna sottoregione, con filtri di saturazione, contrasto locale e dominanza del picco. Il centro è il baricentro dei pesi positivi dopo sottrazione del fondo, nella previsualizzazione a metà scala generata dai due verdi del RAW RGGB. Nelle altre pose la corrispondenza si cerca in una finestra fissata attorno alla sorgente di riferimento, indipendente dalle due predizioni. Un controllo gaussiano sintetico verifica il calcolo del baricentro. [Serie originale di Colmic](https://siril.org/tutorials/tuto-scripts/index.html)

Passano i filtri iniziali 59 candidati. I modelli sono confrontati sullo stesso insieme di 54 stelle seguite in tutte le 14 pose successive, per 756 residui radiali. Si escludono le tracce incomplete. Gli otto riquadri di test sono tutti rappresentati.

| Predizione | P90 sui 756 residui (pixel nativi) | Pose con P90 ≤ 0,30 px |
| --- | ---: | ---: |
| Traslazione | 0,636 | 1/14 |
| Affine | 0,437 | 1/14 |

Il modello affine riduce il P90 stellare in 13 pose su 14. Il risultato regionale affine precedente era 10/14 pose entro soglia. La misura stellare lascia 13/14 pose oltre soglia per lo stesso modello. I residui includono il rumore dei centroidi, l'effetto della fase sulla previsualizzazione e l'incertezza di associazione locale. Le misure riusano stelle e pose, quindi 756 è un conteggio di residui e non di osservazioni indipendenti. Il criterio riguarda questa specifica sequenza senza nuova calibrazione radiometrica. Rimangono aperte la qualifica della registrazione stellare e la valutazione di flusso e rumore dopo ricostruzione CFA a scala comune.

SHA-256 della ricevuta `29aec711f14fc71aae8936575243eec70cdca8271d53e95f7e6a35f3eef151d7`.
