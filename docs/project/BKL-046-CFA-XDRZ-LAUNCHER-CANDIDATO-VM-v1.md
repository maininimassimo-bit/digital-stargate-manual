# BKL-046 · Pacchetto CFA per revisione del launcher

Il manifest del launcher lega i cinque controlli sintetici, i sorgenti Node e Python, i runtime di DSG-Shared, i file installati di R4 e le identità delle directory O: e H:. Il launcher verifica un'attestazione di distribuzione ricevuta per canale autenticato e due ricevute firmate da ruoli distinti, con RQ vincolata esattamente alla ricevuta ARB, prima di caricare il percorso operativo R4.

Due collaudi hanno verificato un'attestazione interamente di prova e respinto sette varianti: scadenza, soggetto diverso, RQ mancante, chiave estranea, rilievo bloccante, riferimento ARB diverso e chiave condivisa fra i ruoli. L'entrypoint avviato senza attestazione si è arrestato prima del gate. Il preflight effettivo ha verificato i percorsi e l'inventario Windows senza richiedere ammissione.

**Soggetto per revisione** SHA-256 `495a59e2b75e7a9a92585f081c37ecfc568d4b4f1a13c4ceba29bf1c146146f4`. Le firme del collaudo sono temporanee. Restano l'approvazione ARB, la successiva RQ, l'autenticazione del pin di distribuzione e l'ammissione dal coordinatore. PixInsight è rimasto chiuso. Esecuzioni native e chiusure scientifiche a zero.
SHA-256 archivio H: fe318d684f45634ae3e157823b07651cb213ba2aca5b8228b363c970634ff30f.
