# Comparatore diagnostico XDRZ per la registrazione pesata di M8–M20

Il comparatore lega il ritaglio CFA 14-1-0 agli archivi di ingressi e oracolo e verifica l’impronta dei 14 descrittori della selezione. Confronta intensità, pesi RGB e supporto sul ritaglio di 29 × 29 pixel. La scala dei pesi è fornita esplicitamente e il comparatore non la stima dai risultati.

Il collaudo accetta 32 coppie di FITS sintetici, confrontando entrambe le geometrie, le due calibrazioni, i due depositi, le due origini e le due ipotesi di rigetto. Respinge dieci casi di alterazione o configurazione incoerente. Il collaudo della riga di comando verifica un confronto completo di file forniti e respinge un’impronta della richiesta errata, un FITS alterato e un percorso esterno alla directory della richiesta.

Il confronto di file forniti registra un esito numerico senza attestazione di provenienza. La selezione operativa di origine, coordinate di rigetto e scala RGB richiede il risultato autentico del controllo nativo. La prova con PixInsight richiede anche revisione e ammissione del coordinatore.

Per l’autotest eseguire `compara.py <protocollo.json> <comparatore-precedente.py> <kit-ingressi-oracolo> <zip-calibrati> <pacchetti-Python> <nuovo-riscontro.json>`. Per confrontare i file aggiungere `--request <richiesta.json> --request-sha256 <impronta>`. Lo script `collaudo-cli.py` esercita quest’ultima modalità.
