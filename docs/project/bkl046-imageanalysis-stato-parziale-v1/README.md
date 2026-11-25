# BKL-046 — Osservazione parziale dello stato ImageAnalysis

Il candidato PJSR correla la risposta al PID riportato da CoreApplication, alla prenotazione, all'entry PJSR, alla ricevuta di ritorno e a una richiesta con validità massima di due secondi. Riferisce il numero di finestre immagine, comprese quelle nascoste o modificate, e il numero di icone di processo nel workspace corrente. Il lettore confronta il PID con quello del processo custodito e rifiuta risposte scadute, estranee o incoerenti.

La documentazione PJSR installata distingue ImageWindow.windows da ImageWindow.openWindows e limita ProcessInstance.icons() al workspace corrente. Una risposta con inventario vuoto conserva come sconosciuti lo stato del motore, i documenti non salvati e i dialoghi. Il formato della risposta preclude l'autorizzazione alla chiusura. Un'osservazione globale richiede evidenze ulteriori prima dell'integrazione nel supervisore.

Verificati due stati simulati, quattro rifiuti in Node e sette in Python. I due replay Python coincidono byte per byte. Nessuna esecuzione PJSR nativa.