# Launcher gestito candidato CFA a due depositi

Il nuovo soggetto BKL-046 riunisce il batch dei 12 casi, il padre che conserva la custodia e il verificatore dei FITS. Include gli oracoli intero e frazionario. Il launcher usa il coordinatore R4 installato. Il preflight verifica le identità storage, i 24 ingressi, tre file PixInsight e l’inventario dei 3.824 file del runtime del comparatore.

Il collaudo riconosce una coppia di firme di prova e respinge dodici casi, tra cui una firma non registrata, una revisione RQ riferita a un altro verbale ARB, il tentativo di fornire approvazioni dalla riga di comando e l’avvio senza attivazione. Il collaudo usa chiavi generate per la prova e chiama il preflight senza chiedere ammissione.

Il pacchetto è in staging su O: con l’attivazione nulla. La destinazione protetta, il controllo del token ordinario, la registrazione delle autorità e le revisioni indipendenti sul soggetto esatto restano da verificare prima dell’avvio. La catena operativa completa del nuovo soggetto resta da qualificare. PixInsight non è stato avviato.

Per ripetere il collaudo eseguire `node collaudo-attivazione.cjs <python.exe> <nuovo-riscontro.json>` dal pacchetto estratto. L’assemblatore verifica gli ZIP sorgente prima di copiare i membri.
