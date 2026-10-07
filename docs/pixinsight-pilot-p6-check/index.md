# Collaudo privato P6 — ambiente isolato

**Collaudo concluso; ambiente isolato sospeso.** Le prove reali del 7 ottobre 2026 sono conservate nel [dossier operativo](../project/PIAI-P6-OPERATIONAL-ACCEPTANCE-2026-10-07.md). P6 resta aperta per accettazione operativa Owner.

Richieste concorrenti Owner su HTTPS reale: un solo job sintetico, annullato senza pubblicazione. Interruzione controllata di una nuova istanza PixInsight su copie sintetiche, nuovo processo worker e stessa prenotazione: **RECOVERY_REQUIRED**, secondo job **QUEUED**. Offline oltre 120 secondi, restart e rollback/forward del servizio di prova hanno conservato lo stato.

L’accesso esterno al servizio di prova è bloccato; archivi, bucket e prenotazioni sono conservati. Nessuna mutazione della coda operativa, nessuna fotografia caricata o pubblicata. Questa pagina non offre più azioni di login o creazione job e non contatta il servizio di prova.

Il servizio serializza le richieste: due chiamate client contemporanee non attestano un interleaving CAS interno. Il collaudo non dimostra perdita di alimentazione, ripartenza del desktop o recupero automatico.

[Perimetro P6 e prove storiche](../project/PIAI-P6-CANDIDATE-2026-10-06.md). La chiusura richiede l’accettazione operativa finale Owner e i gate di consegna.
