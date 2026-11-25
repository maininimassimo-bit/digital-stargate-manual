# BKL-046 — Custodia della prova ImageAnalysis

Il padre candidato apre handle NTFS per i quattro FITS e i cinque file della prova. Tiene anche aperte le directory dell'operazione e degli input. Prima della conferma confronta la richiesta con configurazione ed entrypoint sotto blocco e rilegge l'identità della prenotazione. Pubblica la conferma con una rinomina sullo stesso volume, che su Windows rifiuta la sostituzione di un file già presente.

Alla restituzione, ricalcola le differenze tra i due ordini e verifica le impronte di risultati e ricevuta. Il rilascio richiede un riscontro del processo originale. Il collaudo ha esercitato handle Windows reali con atti R4 e uscite simulati. Cinque test hanno verificato la sequenza positiva, la contesa sui file, il rifiuto di una richiesta alterata, di una conferma già presente, di una prenotazione cambiata e di una differenza incoerente. [Riscontro](riscontro.json)

Resta da collegare la verifica della prenotazione R4 su DSG‑Shared e l'osservazione dello stesso handle PixInsight fino alla chiusura. La custodia delle directory ha impedito la rinomina nel collaudo. Il pacchetto finale deve anche mantenere la directory operativa riservata ai processi previsti. [Codice](imageanalysis_custody.py) · [Test](verifica-custodia.py)
