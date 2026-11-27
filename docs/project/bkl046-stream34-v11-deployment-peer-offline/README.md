# BKL-046 · Collaudo offline del deployment Stream34 v11 e del peer

Il collaudo rilegge i 64 membri del soggetto Stream34 v11 e carica dagli stessi byte l’entrypoint di deployment. Il pacchetto di revisione originale conserva 70 membri complessivi. La prova usa chiavi effimere, verbali di prova e una finestra simulata. Un heartbeat firmato attraversa l’entrypoint e riceve una risposta dal peer, senza accedere a finestre reali.

L’entrypoint respinge impronta di deployment errata, host diverso, percorso relativo e soggetto diverso. Il peer respinge chiave diversa e iscrizione scaduta. L’operatore rifiuta il file segnaposto al controllo dell’impronta Python. Il peer respinge anche la dichiarazione di fine firmata dall’operatore quando manca l’osservazione della chiusura. Il collaudo non raggiunge il coordinatore né avvia processi nativi.

Per riprodurre, estrarre la candidata v11 con SHA-256 `e23818ac9858c00a6fd113764e22e1db203a2fd5c4b12c5cacc2b677a0bdf367`. Eseguire su DSG-Shared `node collaudo.cjs <directory-candidata> <nuova-directory-fixture> <nuovo-rapporto.json>` con percorsi assoluti. L’archivio del collaudo conserva il codice e il rapporto senza chiavi o verbali effimeri.

Per passare alla prova reale servono ancora trust autenticato, verbali indipendenti ARB e RQ, approvazione di deployment e iscrizione effettiva. Dopo la verifica di questi ingressi, il coordinatore deve ammettere la prova. Nessuna apertura PixInsight e nessuna chiusura scientifica.