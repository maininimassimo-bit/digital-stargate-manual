# BKL-046 — Rifiuto della chiusura in presenza di un dialogo reale

Nella sessione interattiva di DSG-Shared, un testimone WinForms ha aperto un dialogo modale e disabilitato la propria finestra principale. Il supervisore ha osservato due finestre visibili del medesimo PID, ha rifiutato l'associazione a un'unica finestra e non ha inviato richieste di chiusura. L'handle attestava il processo ancora attivo al momento del rifiuto. Il collaudo ha poi terminato soltanto il processo di prova da lui avviato.

Una seconda esecuzione senza dialogo ha usato lo stesso supervisore per acquisire la finestra, leggere la console, inviare una sola chiusura ordinaria e attestare l'uscita a zero dell'originale. Questo confronto qualifica il rifiuto di un dialogo Win32 visibile del testimone. La documentazione PixInsight installata indica che in modalità contenuta alcuni dialoghi possono vivere dentro la finestra principale. L'enumerazione Win32 non dimostra quindi assenza globale di dialoghi, documenti non salvati o attività del motore di PixInsight.

Nessun avvio PixInsight o modifica al registro R4.