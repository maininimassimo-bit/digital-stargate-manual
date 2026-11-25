# BKL-046 — Riferimento fotometrico pubblicato per Tempel 1

Ho verificato i checksum PDS della tabella scientifica e di quella di navigazione e riletto 595 e 2.419 righe rispettivamente. L'associazione per identità della posa ritrova tutte le 595 righe scientifiche nell'indice grezzo, con 535 immagini in modalità 3 e 60 in modalità 2. Nessuna appartiene alle cinque pose a pieno formato del [test sulla correzione overscan](BKL-046-MRI-TEMPEL1-OVERSCAN.md). Le tabelle usano aperture circolari di diametro 5–30 px e terminano prima di quelle cinque pose. La geometria e l'intervallo del riferimento lasciano aperto il riscontro dell'anello 48–96 px. [Tabella di fotometria NASA](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-C-MRI-5-TEMPEL1-PHOTOMETRY-V1.0)

Ho comunque verificato il confronto di apertura nella regione coperta dalla tabella. Il piano seleziona le sei posizioni cronologiche prefissate tra le 116 immagini idonee in modalità 3, e l'unica immagine idonea in modalità 2. Sono tutte CLEAR1, con centro a distanza di almeno 20 px dalla giunzione orizzontale tra quadranti. Le misure usano i centri pubblicati, aperture subpixel con maschera PDS e le radiance RADREV v3. Le tabelle originali derivano da RADREV v2. Ho confrontato i rapporti rispetto al diametro 30 px, che consentono il confronto senza convertire la radiance in DN/s.

Nei sei sottoquadri da 256 px, il fondo stimato per riga da una fascia laterale produce scarti medi assoluti tra 0,03% e 0,21% sulle sei aperture più piccole. Nessuno di questi scarti supera lo 0,33%. Nel sottoquadro da 512 px lo scarto medio è 4,97% e il massimo 7,29%. Usando invece un fondo costante stimato nella corona locale, gli scarti medi assoluti sono fra 15,70% e 24,13% nei sette esempi. Il dato mostra la sensibilità al fondo e alla geometria. La procedura pubblicata usa anch'essa una stima per riga per la fotometria scientifica. [Descrizione del metodo PDS](https://pds-smallbodies.astro.umd.edu/holdings/dif-c-mri-5-tempel1-photometry-v1.0/document/photometry_report.asc)

Il confronto copre le curve normalizzate di sette pose di approccio selezionate lontano dalla giunzione. Rimangono aperti il flusso assoluto, le immagini a pieno formato, le aperture diffuse maggiori e il confronto nativo.

| Evidenza | SHA-256 |
| --- | --- |
| Ricevuta dei sette prodotti abbinati | 35ac8edc6f2bc4902633a9afdf9c100c6118a3c635d70bab48858a6748f39f3c |
| Riscontro numerico e replay identico | 6b7fa632c9a6010814b085a30b807d125f44fb5dc196288fe9df199d64bd3260 |
| Archivio riletto su H: | d0056434c893a7193b43d300078cdca4e1bd5d543d58260057109664e03b6ba3 |

Zero chiusure scientifiche e zero esecuzioni native in questo incremento.
