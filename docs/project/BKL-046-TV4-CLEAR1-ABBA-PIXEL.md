# BKL-046 — Deriva nel test TV4 a esposizione invertita

Il [disegno ABBA](BKL-046-TV4-CLEAR1-ABBA.md) fissa quattro gruppi indipendenti come unità dell'analisi, con integrazioni da 7.503,5 e 15.003,5 ms. Dopo il primo tentativo di acquisizione, abbiamo recuperato tutti gli otto FITS previsti e poi i 32 fotogrammi intermedi degli stessi gruppi. Identità, ora, integrazione, modalità, posizione del filtro e dimensioni sono state riscontrate tra indice PDS, etichetta e testata FITS. Abbiamo misurato 1.280 blocchi in cinque regioni interne fisse per fotogramma, oltre a due controlli di overscan. [Dataset TV4 della NASA](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-HRII%2FHRIV%2FMRI-2-GROUND-TV4-V1.0)

| Serie sulle 40 immagini | Contrasto con deriva lineare | Contrasto con deriva quadratica |
| --- | ---: | ---: |
| Pixel grezzi | 4.023,82 DN | 3.748,01 DN |
| Separazione con overscan seriale | 4.022,76 DN | 3.746,12 DN |
| Separazione con overscan parallelo | 4.023,70 DN | 3.747,62 DN |

Nel modello lineare, usare tutti i fotogrammi al posto degli estremi cambia il contrasto di 0,87–1,19 DN a seconda del controllo. Nel modello quadratico il cambiamento è 8,93–10,05 DN. La sola scelta fra deriva lineare e quadratica sposta il contrasto di circa 276 DN. Con quattro gruppi, il modello quadratico esaurisce i gradi di libertà residui.

A parità di esposizione, il tasso medio dopo sottrazione dell'overscan parallelo cresce del 2,52% a 7.503,5 ms e del 2,51% a 15.003,5 ms fra i gruppi iniziali e quelli finali. Abbiamo poi previsto ogni gruppo usando gli altri tre e confrontato due modelli con due parametri ciascuno. Con overscan parallelo, il modello proporzionale alla durata con tasso variabile linearmente nel tempo ha RMS predittivo di 25,40 DN, contro 157,66 DN per il modello stazionario a due livelli. Il confronto grezzo dà 268,33 e 158,11 DN rispettivamente. Il miglioramento predittivo richiede quindi il trattamento dell'offset in questa sequenza.

Quattro gruppi condividono la stessa sessione di laboratorio. Manca una misura indipendente di dose per fotogramma. I dati documentano la deriva temporale e la sensibilità alla correzione dell'offset. La separazione fisica fra sorgente, sensibilità e non linearità resta aperta. Zero chiusure scientifiche e zero esecuzioni native in questo incremento.

| Evidenza | SHA-256 |
| --- | --- |
| Riscontro sugli otto fotogrammi agli estremi | 3cb166d1bd92f4e88a4c0de5922e5fb961827c94f4d0f206f9091aa7e1a70a61 |
| Riscontro sui 40 FITS e rilettura identica | 5cc3749b5b4337f62303ca8aba3889d08ecedcffcd1f84cd4f1843043653aea2 |
| Confronto predittivo e rilettura identica | 36e54c8ad3b0c3b03396aa642b70044ea9db259f6c6f50d02063de5dfb8fe00c |
| Archivio riletto su H: | d6d5e0b68f7b5c4f896d8d30a9569ad9afc24020e4f34aeb44cf4a8d92ea9a7a |
