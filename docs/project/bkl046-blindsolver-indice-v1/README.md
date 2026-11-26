# BKL-046 · BlindSolver 1.9.6 e selezione dell'indice Gaia

Il test estrae due metodi dal sorgente installato di `BlindSolverEngine.js` dopo averne verificato lo SHA-256. Esegue i metodi in Node con sostituti controllati per il processo Gaia e l'accesso al file system.

| Caso | Esito |
| --- | --- |
| Gaia assente, errore di `get-info` oppure percorso vuoto | Indice indisponibile. Il controllo del file non parte. |
| Indice inizialmente assente e poi presente | Il primo tentativo fallisce e quello successivo ripete l'interrogazione e riesce. |
| Eccezione nel controllo file | L'eccezione si propaga e il percorso resta senza valore in cache. |
| Percorso con spazi esterni e poi cambio della configurazione | Gli spazi vengono rimossi. La stessa istanza restituisce il primo percorso senza una nuova interrogazione o verifica. |

Il risultato rende verificabile la selezione del percorso a livello JavaScript. Per una successiva prova nativa occorre fissare l'identità dell'indice e del campo di prova e acquisire una ricevuta legata all'istanza che ha eseguito la soluzione. Il test non legge l'indice e non misura accuratezza, falsi positivi o effetti sulle coordinate WCS.

Eseguire `node test-indice.cjs PERCORSO_ENGINE RISCONTRO_NUOVO.json` con lo stesso sorgente. Il JSON registra versione Node, versione V8, digest delle due porzioni di sorgente ed esiti con le chiamate osservate.
