# BKL-046 · Verifica candidata del messaggio R4 per il parent CFA

Il coordinatore R4 ammette un parent originale distinto dal custode. L'adattatore attende LEASE_READY prima di creare il parent, poi usa FD3 per legare PID e istante di creazione all'handle originale. Questo candidato aggiunge la verifica, dal parent, del successivo messaggio di continuazione per i controlli CFA. Il messaggio vincola l'operazione, il caso sintetico, le impronte del piano e del soggetto e le impronte dei record di prenotazione. Il parent verifica la propria identità, confronta acquisizione e stato attivo e rilegge il record originale prima di restituire il contesto.

Il collaudo ha usato processi Windows reali e un registro temporaneo. Ha accettato una continuazione coerente e respinto dieci varianti, incluse operazione, piano, soggetto, caso e PID estranei, record mancante o alterato, chiusura anticipata del canale e messaggio duplicato. Le ricevute delle due esecuzioni coincidono. Il testimone stampa il contesto verificato e non include un avvio di PixInsight.

Il modulo candidato copre il confine di ingresso del parent. Restano da integrare e far revisionare il lancio PJSR dopo il binding, la custodia della finestra originale, la verifica delle esportazioni e la sequenza di uscita e rilascio. Il registro canonico è rimasto fuori dal collaudo. Zero ammissioni e zero esecuzioni native.

Ricevuta SHA-256 `90076b291cf44c649656e6f63deff4d1f2e46d240e148dbaf5842f48142978a9`.
