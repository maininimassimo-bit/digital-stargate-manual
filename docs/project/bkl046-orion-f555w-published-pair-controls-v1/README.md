# BKL-046 — Controlli su coppie pubblicate in Orione, ACS/WFC F555W

Il protocollo verifica su dati astronomici se un modello a due componenti recupera separazione e rapporto di flusso pubblicati da De Furio et al. (2019, tabella 1). Le cinque coppie sono quelle con almeno due esposizioni candidate nella verifica geometrica precedente. Il campione selezionato contiene soltanto coppie già note. La pubblicazione usa ACS/WFC F555W dello stesso programma HST GO10246. Il confronto misura la riproducibilità sullo stesso programma osservativo.

L'identità di ciascuna stella è verificata tramite l'identificativo esatto 2MASS e un'associazione Gaia DR3 univoca in SIMBAD. Dei 11 tentativi di estrazione, nove hanno un centro utilizzabile privo di flag DQ 256 e 2048 entro 3 pixel dal picco registrato. Due posizioni cadono fuori dai chip. Il fit usa la libreria STScI ePSF ACS/WFC F555W pre-SM4, distribuita separatamente per SHA-256 nel precedente dossier ePSF.

Per superare il controllo per esposizione, il modello a due componenti deve migliorare il punteggio in entrambe le partizioni alternate dei pixel tenuti fuori dal fit. In entrambe la separazione deve concordare entro il massimo tra 20 mas e il 20% del valore pubblicato e il rapporto di flusso entro il 30%. La conversione nominale usa 50 mas/pixel. Le due partizioni provengono dalla stessa immagine.

| Riga della tabella | Separazione pubblicata | Esposizioni conformi |
|---|---|---|
| 2 | 43 mas | 1 su 2 |
| 3 | 60 mas | 1 su 2 |
| 8 | 100 mas | 2 su 2 |
| 10 | 165 mas | 1 su 1 utilizzabile |
| 14 | 273 mas | 0 su 2 |

Per la riga 8 il fit restituisce 101,6–104,3 mas e rapporti di flusso 0,317–0,348 contro 0,33 di riferimento. Per la riga 14 il modello a due componenti peggiora il punteggio in entrambe le esposizioni e in entrambe le partizioni. Il controllo numerico senza rumore usa la stessa libreria del fit e recupera 1,477 px contro 1,473 px attesi.

Il risultato documenta la ripetibilità su una delle cinque coppie selezionate. Mancano un campione indipendente, controlli negativi e una qualifica del tasso di errore. Esecuzioni native e chiusure scientifiche in questo incremento: zero.

Le misure di riferimento sono nella [tabella 1 di De Furio et al.](https://arxiv.org/abs/1910.02092).

I report e i relativi protocolli conservano impronte dei dati, risultati per esposizione, maschere e soglie. Gli intervalli FITS, le risposte SIMBAD e i riquadri numerici sono conservati nell'archivio privato H:. Per replicare il fit servono anche il catalogo di riferimento e la libreria ePSF conservati nei rispettivi dossier precedenti.
