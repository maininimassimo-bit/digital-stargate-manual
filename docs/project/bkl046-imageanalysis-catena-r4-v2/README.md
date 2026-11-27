# BKL-046 — Prova della catena ImageAnalysis e R4

Sono state eseguite due prove su DSG‑Shared in registri R4 isolati. Gli script della candidata comunicavano con il padre tramite file NTFS. Il padre e il testimone erano processi Windows distinti e sono stati osservati tramite i loro handle originali. Le misure ImageAnalysis sono state simulate.

- **Ricevuta coerente.** Il padre ha verificato richiesta, conferma e ricevuta, poi ha trattenuto i file fino all’uscita del testimone. Il coordinatore ha scritto il rilascio dopo aver osservato l’uscita del padre con codice zero.
- **Ricevuta alterata.** Dopo la pubblicazione del segnale di ritorno, il collaudo ha alterato l’impronta delle misure nella ricevuta. Il padre l’ha respinta, anche se il testimone è uscito con codice zero. Il padre è uscito con codice 7. R4 ha lasciato intatto il record attivo e il collaudo ha confermato l’assenza di una ricevuta di rilascio.

Il registro di produzione non è stato modificato e PixInsight è rimasto chiuso. Restano da verificare la console reale e le misure native dopo revisione e ammissione. [Impronte e risultati](riscontro.json)
