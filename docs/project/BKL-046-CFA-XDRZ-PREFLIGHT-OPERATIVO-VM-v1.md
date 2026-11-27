# BKL-046 · Preflight operativo CFA su DSG-Shared

Dalla catena Node/Python della sessione interattiva 2, il custode R4 installato ha riconosciuto il chiamante e completato tre volte l'inventario Windows usato per l'ammissione. Il controllo ha verificato le impronte di coordinatore e CURRENT.json. Nessun processo PixInsight o prenotazione canonica attiva è risultato visibile durante i controlli. La chiamata era di preflight e non ha richiesto ammissione.

Sono state predisposte la directory di lavoro CFA su O: e la directory di pubblicazione CFA su H:. Due collaudi hanno confermato le identità dei percorsi e la scrittura con sincronizzazione e rilettura. Il percorso mappato e quello UNC dell'archivio puntano allo stesso oggetto. Un handle di lettura con condivisione limitata ha bloccato l'apertura in scrittura anche attraverso l'alias UNC. Alla chiusura dell'handle la scrittura torna consentita. I file di prova sono stati rimossi.

Il risultato permette di usare le due directory nel launcher e di applicare il blocco in lettura durante l'ultimo controllo. La protezione persistente richiede una verifica distinta. Restano l'integrazione finale, le revisioni e l'ammissione. Esecuzioni native e chiusure scientifiche a zero.
SHA-256 archivio H: 3ce02696c068c0d33b8f8f6a4a8f2dfc6dce66937bc4e6ea90e4b167794608d8.
