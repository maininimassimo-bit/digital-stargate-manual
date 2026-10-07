# P6 — collaudo cloud isolato approvato

| Campo | Valore |
|---|---|
| ID | DSG-PIAI-P6-ISOLATED-OAT-20261007 |
| Versione | 1.0 |
| Stato | Attivazione approvata; ambiente isolato attivo; collaudo reale ancora da eseguire |
| Data | 2026-10-07 |
| Package | BKL-049-EXT-PIAI/P6 — In Progress |

## Evidenza riconciliata

Il 7 ottobre sono stati riverificati originali e ricevute CFA locali e collegati al portale, la ricetta SHO nativa e i file dell'ultima SHO Drizzle2 accettata privatamente. Tutti i 43 checkpoint della nuova SHO e i suoi tre master più il riferimento Owner corrispondono alle impronte conservate. Non è stata ripetuta alcuna elaborazione conclusa.

Accesso Google Owner reale sulla pagina scientifica, anteprima CFA e workflow di 27 operazioni confermati. Tutti e tre i download CFA sono stati salvati realmente sul PC: workflow identico all'export nativo, correlazioni conformi all'export minimizzato governato, impronte di entrambi conformi alla ricevuta immutabile. Le correlazioni minimizzate non sono identiche al journal privato completo, per progettazione. La prova CFA usa una singola esposizione calibrata RGGB, non un master integrato; discrepanza temporale con le sessioni dichiarate e valutazione scientifica ancora pendente restano esplicite. La valutazione privata M31 ACCEPT_PRIVATE è stata riconfermata nella UI.

Queste prove superano le precedenti note di dati CFA/SHO non selezionati e aggiungono riscontro browser corrente; non riscrivono il precedente guasto download, non dichiarano History a monte completa e non certificano automaticamente HOO o ogni campo LRGB. Un temporaneo grigio di un tentativo SHO fallito non fu esportato separatamente: journal/input e ramo successivo restano disponibili, senza History nativa retroattiva.

## Approvazione e isolamento

L'Owner ha approvato esplicitamente la proposta di collaudo isolato con «Approvo», dopo presentazione di servizio, due bucket privati, identità e credenziale di prova dedicate e costi infrastrutturali senza hard spending cap. Risorse create nel progetto già autorizzato `digital-stargate-telemetry`, regione `europe-west1`: servizio/identità `dsg-piai-p6-oat`, bucket `dsg-piai-p6-oat-private-183451329061` e `dsg-piai-p6-oat-backup-183451329061`.

Immagine immutabile già rilasciata, senza nuova build: `sha256:33547c26692f639cc4bf580ba4899dd97e253fde1ed8e4546c3c9d3ae7cc7d3d`, codice di origine merge `f2afb30f9fafb906895e7c937ba8b23f51357452`. Revisione iniziale di prova `dsg-piai-p6-oat-p6-oat-01`. Una CPU, 512 MiB, min=0/max=1, concurrency=1, timeout 60 s, billing per richiesta. Bucket con accesso pubblico impedito, accesso uniforme e versioning; nessuna cancellazione automatica.

L'identità di prova legge/crea solo nei propri bucket; può modificare esclusivamente `control/piai-state.json` nel primario tramite condizione IAM. Backup senza delete/overwrite. Il registry esistente concede solo reader all'identità di prova. Nessun accesso ai bucket del pilota o alle fotografie. Credenziale dedicata 256 bit protetta con Windows User DPAPI; solo SHA256 al server. Google Owner/client esistenti, nessun token browser estratto. Credenziali, sorgenti sintetiche, configurazione locale e ricevute grezze restano private su F.

Il servizio operativo, il suo traffico, la sua credenziale, la sua identità/IAM e la sua coda/root non sono modificati. La nuova pagina diagnostica è fissata al solo endpoint isolato, non consente un indirizzo arbitrario né avvia PixInsight. Nessuna API IA a pagamento, dispositivo, Safety Authority o automazione periodica.

## Protocollo e criteri verificabili

1. Login Owner nella [pagina di collaudo](../pixinsight-pilot-p6-check/index.md). Due create HTTP contemporanee con identico requestId restituiscono un solo job; due cancel contemporanei terminano CANCELLED/NONE. Retry nella stessa pagina conserva le identità, anche dopo risposta persa. La serializzazione del servizio è mantenuta: non si attribuisce interleaving CAS al server.
2. Owner crea due job di recupero distinti. Un nuovo worker root riceve il primo con la sola credenziale di prova; copia fixture sintetiche già disponibili. L'operatore avvia esplicitamente una nuova istanza PixInsight isolata.
3. Dopo un evento process-started reale e prima della ricevuta terminale, terminare soltanto il PID di quella istanza. `native-stopped` invia RECOVERY_REQUIRED via HTTPS reale; nessuna raccolta COMPLETED senza ricevuta valida.
4. Avviare un nuovo processo OS del worker sul root conservato: stessa claim e binding, prima prenotazione RECOVERY_REQUIRED e secondo job QUEUED, file/input invariati, nessun replay o riassegnazione.
5. Offline oltre 120 s senza expiry, restart sul medesimo digest e rollback/forward del solo servizio isolato: stato primario e backup verificati, nessuna restaurazione di stato vecchio o coda operativa.
6. Conservare ricevute/minimizzare esiti; sospendere invocazioni e accesso al servizio di prova, mantenere bucket e archivi. Nessuna cancellazione autorizzata.

Una prova interrotta resta FAILED/PENDING, mai promossa a PASS. Non sono dimostrati perdita di alimentazione, crash desktop o auto-recovery. Il fence operativo protegge l'ambiguità e lascia deliberatamente bloccato il solo ambiente isolato; non è una funzione di sblocco della coda.

## Gate e rollback

La pagina richiede CI sull'head esatto, ARB e Release Quality separate, merge protetto dall'expected head e Pages verificata prima del collaudo reale. La prova deve riferire anche il digest backend precedente, distinto dall'head frontend. P6 resta aperta fino a riconciliazione finale dei residui/profili, disposition dei limiti e accettazione operativa Owner. BKL-051 resta Planned; nessuna pubblicazione gallery.

Rollback: revert governato della sola pagina diagnostica e relativi script/test; sospendere accesso e invocazioni al servizio isolato conservando tutte le risorse e ricevute. Non ripristinare la coda del pilota, non modificare prenotazioni native o decisioni scientifiche immutabili. La chiusura finale manterrà la distinzione fra accettazione privata e operativa, BKL-043 F4/F5 invariati e BKL-050 conclusiva.
