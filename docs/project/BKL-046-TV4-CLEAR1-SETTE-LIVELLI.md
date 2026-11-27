# BKL-046 — Trasferimento fotonico esplorativo su sette livelli TV4

Dai gruppi CL–CR precedenti al riallineamento della sfera ho selezionato dieci posizioni cronologiche a ogni livello prima di leggere i pixel. Ho verificato i 70 FITS e le 70 etichette con i checksum PDS. Cinque fotogrammi privi di conferma del filtro dal sensore Hall sono esclusi dal calcolo e conservati nella ricevuta. Le due regole di accoppiamento conservano da due a cinque coppie disgiunte per livello. Le regole riusano gli stessi fotogrammi. [Registro MRI](https://pds-smallbodies.astro.umd.edu/holdings/dif-cal-hrii_hriv_mri-2-ground-tv4-v1.0/document/imagelog/tv4_mri.asc) · [Indice dei checksum PDS](https://pds-smallbodies.astro.umd.edu/holdings/dif-cal-hrii_hriv_mri-2-ground-tv4-v1.0/index/checksum.tab)

I tempi comandati da 0 a 7.500 ms corrispondono a 3,5–7.503,5 ms di integrazione. A comando zero, il segnale medio della regione centrale dopo sottrazione dell'overscan è circa −10 DN e la varianza appaiata è 1,09–1,19 DN². Il comando zero conserva una breve integrazione e il livello medio centrale dipende dalla scelta del riferimento di offset.

| Regione centrale, singolo pixel | Coppie adiacenti | Coppie a distanza |
| --- | ---: | ---: |
| Guadagno condizionato, pendenza del modello lineare | 28,25 e⁻/DN | 28,17 e⁻/DN |
| Errore RMS di varianza su livello trattenuto, lineare | 1,655 DN² | 1,825 DN² |
| Errore RMS di varianza su livello trattenuto, quadratico | 0,441 DN² | 0,454 DN² |

Il confronto predittivo usa i sette livelli e trattiene un livello per volta. L'errore quadratico minore sul singolo pixel si ripete con entrambe le regole entro la stessa sessione. Alle aperture più grandi, il risultato dipende dalla regola e dalla dimensione dell'apertura, in accordo con la [sensibilità già osservata sulle somme](BKL-046-TV4-CLEAR1-RUMORE-ABBA.md). La pendenza lineare al centro cade nell'intervallo 27,9–28,7 e⁻/DN della calibrazione pubblicata per i quattro quadranti MRI. L'accordo è circoscritto a questa misura e a questa scala. [Calibrazione Deep Impact](https://archive.stsci.edu/files/live/sites/mast/files/home/missions-and-data/epoch-1/_documents/calibration_paper_draft.pdf)

L'ordine temporale e il livello restano associati. Mancano una misura di dose indipendente per fotogramma e una replica del protocollo in un'altra sessione. La verifica riguarda la relazione fra varianza e segnale osservato. La causa della curvatura e la linearità assoluta restano aperte. Zero chiusure scientifiche e zero esecuzioni native.

| Evidenza | SHA-256 |
| --- | --- |
| Selezione dei 70 fotogrammi | 57328477ed146a5fde899b49d40fa5be993b1fe7a16bfd8b055ee0bed3f1fefa |
| Cattura verificata | 375f141f244086d92054a86c211624144dfcb7ed13b613156acdc961e06f239d |
| Riscontro e replay identico | 35b63f2e6508cd96bf8f9c732d33eabf720ac072effee89df0439dd06f2f7050 |
| Archivio riletto su H: | 48af79ebce8989f99c14cb4a4ca0b9d29299018101199f84df5266cd415f74f9 |
