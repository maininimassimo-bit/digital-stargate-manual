# BKL-046 · Secondo campo Bayer, Nebulosa Cuore IC 1805

Il pacchetto di Santiago Rodriguez contiene 84 CR2 decodificabili come mosaici Bayer RGGB da 3908 × 2602, senza incremento di scala o demosaicizzazione. Il catalogo identifica la fotocamera come Canon EOS 40Da. Il campo modello EXIF in tutti i CR2 riporta Canon EOS 40D. Le immagini restano nell'orientamento del rivelatore. [Catalogo originale](https://amor.cms.hu-berlin.de/~rodrigus/datasets.html)

| Gruppo originale | File | Modalità EXIF |
| --- | ---: | --- |
| Luci | 39 | ISO 800, 60 s |
| Dark | 17 | ISO 800, 60 s |
| Flat | 17 | ISO 100, 2,5 s |
| Bias | 11 | 10 a ISO 800 e 1 s, uno a ISO 800 e 60 s |

Le luci e i dark corrispondono per ISO e durata. L'archivio non contiene una serie dark-flat a ISO 100 e 2,5 s. Il file da 60 s nella cartella bias deve essere escluso da un eventuale gruppo di offset. Questi riscontri provengono dagli EXIF, che non attestano il trattamento della luce durante l'acquisizione. Nessun master viene prodotto.

La correlazione subpixel su quattro regioni, con la stessa regola di accordo fra regioni già applicata alle pose di M8 e M20, lascia fuori ricerca almeno una regione in tre pose. Nelle 36 pose con quattro stime disponibili, la mediana del massimo disaccordo regionale è 55,76 px. Solo la posa di riferimento passa il criterio di parità. I massimi discordanti non sono spostamenti astrometrici verificati. La posa di riferimento confrontata con sé stessa non costituisce una conferma indipendente. Il test respinge quindi il metodo diretto a quattro regioni per questo campo. Servono corrispondenze stellari per inizializzare la registrazione e una strategia di calibrazione qualificata per l'accoppiamento dei flat.

Si conserva lo ZIP originale insieme alle impronte dei singoli CR2, al protocollo e al wheel rawpy 0.25.1 verificato rispetto a PyPI. Zero chiusure scientifiche e zero avvii PixInsight. [Distribuzione rawpy](https://pypi.org/project/rawpy/0.25.1/)

SHA-256 della ricevuta `582a3adcdeb5509b4c4e9434b252726cf0473c86fdd6da272a69aa4358bc705f`.
