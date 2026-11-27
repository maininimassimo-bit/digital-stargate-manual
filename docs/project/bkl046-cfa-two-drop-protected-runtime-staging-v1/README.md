# Launcher candidato con runtime incluso nella posa protetta

Il launcher BKL-046 carica ora il comparatore dalla propria directory runtime. Il preflight verifica i 3.824 file della copia inclusa e i 24 ingressi CFA. La copia è verificata byte per byte contro l’inventario precedente. Il controllo dell’attivazione riproduce le verifiche con chiavi di prova e il rifiuto dell’ingresso senza attivazione.

Il token ordinario di DSG-Shared ha accesso di modifica ai 34 file del payload esaminati nella copia di staging su O:. Lo stesso vale per i tre campioni Python, PYD e DLL. Il controllo in sola lettura ha verificato che il token non può creare la destinazione sotto Program Files. Il percorso DigitalStarGate sotto Program Files risulta assente.

Questo pacchetto può essere posato come installazione inattiva. La destinazione finale deve essere riletta dal token ordinario per verificare che codice, directory runtime e attivazione siano protetti. Servono ancora revisione ARB e RQ sul nuovo soggetto, registrazione delle autorità e ammissione R4. PixInsight non è stato avviato.

Per preparare lo staging, eseguire `prepara-posa.py <zip-launcher-precedente> <runtime-fissato> <directory-vuota>`. Per il preflight e il collaudo di attivazione, eseguire il test Node incluso. Il rapporto ACL riguarda la copia di staging.
