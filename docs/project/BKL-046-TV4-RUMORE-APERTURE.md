# BKL‑046 · Orientazione delle aperture e rumore di rivelatore TV4

Il controllo usa otto frame del rivelatore MRI di Deep Impact, acquisiti nel test termovuoto TV4. Forma quattro differenze tra frame adiacenti, normalizzate per √2. Le prime due stimano la covarianza spaziale nelle cinque regioni congelate. Le altre due misurano la varianza delle somme su aperture con supporti disgiunti. I risultati descrivono una sequenza di calibrazione di laboratorio. [Dataset NASA PDS](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-HRII%2FHRIV%2FMRI-2-GROUND-TV4-V1.0)

Il confronto usa aperture da 64 pixel a orientazioni diverse e tre trasformazioni controllate. La previsione con covarianza usa i pesi effettivi dell’apertura e del ricampionamento. Per ogni apertura si verifica anche che il ricampionamento esplicito produca la stessa somma del calcolo a pesi effettivi.

| Trasformazione | Rapporto mediano di varianza 4 × 16 / 16 × 4 (Y × X) | Errore mediano del modello con covarianza, 4 × 16 | Errore mediano, 16 × 4 | Errore mediano, 8 × 8 |
| --- | ---: | ---: | ---: | ---: |
| Identità | 2,392 | 24,75% | 33,89% | 24,47% |
| Mezzo pixel lungo X | 2,517 | 25,54% | 33,88% | 25,45% |
| Mezzo pixel lungo Y | 2,172 | 26,73% | 35,09% | 23,00% |

Il modello con covarianza riduce l’errore mediano rispetto a quello con input bianco e sovrapposizione dei pesi in tutti i nove confronti. Nessuno rientra nel limite congelato del 15%. La differenza fra aperture ruotate è già presente senza ricampionamento. In questa sequenza un fattore basato sulla sola area perde quindi informazione sulla forma dell’apertura.

Le regioni condividono le acquisizioni e supporti disgiunti possono restare correlati. La stima di covarianza è normalizzata per le coppie disponibili a ogni lag dopo sottrazione della media regionale. Il risultato non copre scene astronomiche, maschere irregolari o ricampionamento nativo PixInsight. L’asse `NOISE_FLUX/3` resta aperto.

SHA‑256 della ricevuta `1b3f86616433543967e01c9d161bd5ba85d8eaebb78500eb63ed1c16cc113240`.
