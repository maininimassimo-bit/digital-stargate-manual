# BKL-046 · Verifica dei verbali Stream34 v11

La verifica accetta soltanto il soggetto `0b029846da0412875e26595e2ead8361bc35fcef2c882ec2be95303b9582bdd1`. Rilegge il file di trust confrontandolo con l'impronta ottenuta per canale autenticato. Per ogni ruolo verifica la firma Ed25519, l'impronta del verbale, il perimetro e l'assenza di rilievi bloccanti. RQ deve indicare l'impronta esatta del verbale ARB e provenire da un revisore distinto.

Il collaudo accetta ARB da solo come esito intermedio e accetta la coppia coerente. Respinge 13 varianti, tra cui soggetto storico, chiavi riutilizzate, firma di ruolo errato, verbale alterato, ARB con rilievi e RQ senza legame al verbale ARB. Le chiavi di prova sono effimere e il rapporto non le conserva.

La verifica legge i verbali e produce un riscontro locale. Non genera firme, non iscrive i ruoli e non concede l'ammissione. Servono ancora i verbali autentici ARB e RQ, le rispettive attestazioni di provenienza e l'impronta autenticata del file di trust. Un'approvazione precedente è circoscritta al suo soggetto esatto. L'attivazione richiede anche la propria autorizzazione e l'iscrizione dei ruoli previste dal launcher.

Per replicare il test, eseguire `node collaudo.cjs protocollo.json riscontro-replica.json`. Per verificare verbali effettivi, `verifica.cjs` riceve la directory dei verbali, l'impronta del soggetto, il percorso del file di trust, la sua impronta ottenuta dal canale autenticato e il percorso di un nuovo rapporto.
