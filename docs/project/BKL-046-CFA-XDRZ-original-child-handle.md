# BKL-046 · Identità e uscita del child originale su Windows

Il modulo candidato riusa la primitiva di custodia già congelata per impedire lanci ripetuti e conservare l'oggetto Popen originale con i relativi canali. Legge PID, istante di creazione e codice di uscita dall'handle Windows di quello stesso oggetto. Un messaggio di disponibilità viene accettato solo se PID e istante corrispondono al processo ancora attivo. Il punto di accesso all'handle usa l'attributo privato di Popen su CPython 3.12.14, quindi resta vincolato a quel runtime per la qualifica.

Tre processi testimone hanno verificato esito zero, uscita 23 e messaggio con PID estraneo. In tutti i casi un tentativo di secondo lancio è stato respinto. Alla scadenza della prima osservazione il controllo ha mantenuto l'handle e atteso la stessa istanza. Solo il caso con identità coerente e uscita zero può passare alla verifica successiva. Due esecuzioni hanno prodotto ricevute identiche.

Il test attesta la custodia dell'handle del testimone. La selezione della finestra PixInsight, il legame con gli output del batch e l'integrazione nel launcher revisionato restano aperti. Nessuna ammissione o avvio nativo è stato richiesto.

Ricevuta SHA-256 `db45df7e32b1a076d2bac2bead434ec2753961141d56ceb4e3930dc5eff0fec2`.
