# BKL-046 — Controllo degli argomenti di avvio ImageAnalysis

Il controllo usa lo staging NTFS effettivo e vincola eseguibile, argomenti di avvio ed entry PJSR alle impronte rilette. Consente solo una nuova istanza, senza script di startup, controllo aggiornamenti o acquisizione automatica del focus. Il test usa un margine residuo prudenziale di 30 secondi sulla scadenza configurata di 120 secondi. Il margine dovrà essere confermato sul runtime nativo.

La guida CLI installata precisa che `-n` apre una nuova istanza e che `--automation-mode` accetta le risposte predefinite dei messaggi modali, salvo quelli di licenza. Il controllo respinge automation mode, uscita forzata, cessione a un'altra istanza, aggiunta di un progetto e sostituzioni di eseguibile o entry. Una nuova istanza non dimostra l'isolamento delle preferenze. Il controllo resta preliminare al launcher, alla revisione e all'ammissione.

Due collaudi hanno verificato uno staging valido ciascuno e gli stessi nove rifiuti. I due staging sono distinti e producono impronte di entry e configurazione diverse. Nessuna esecuzione PixInsight.