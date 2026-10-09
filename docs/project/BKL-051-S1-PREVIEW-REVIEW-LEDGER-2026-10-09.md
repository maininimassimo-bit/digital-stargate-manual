# BKL-051 — cronologia privata delle revisioni delle anteprime

Incremento locale nel perimetro reporting già autorizzato. Il contratto `DSG_PRIVATE_PREVIEW_REVIEW_LEDGER_V1` conserva una copia verificata di un export CBAT, MPC, TNS o VSX e una sequenza di revisioni private. Non costituisce consenso all'invio, autenticazione dell'Owner, accettazione scientifica o ricevuta del provider.

## Anteprima congelata e provenienza

Il chiamante locale fidato deve fornire il SHA256 indipendente della ricevuta dell'export. Sono ammessi soltanto i contratti locali documentati, nella directory completa con i tre file previsti. Ricevuta, dati e testo/XML vengono verificati per byte, dimensione, hash, stato e canale. Il controllo XML riguarda qui l'identità dei byte già esportati: non ripete la validazione dello schema MPC e non estende l'accettazione del provider.

La preparazione crea una nuova directory esclusiva e una snapshot dei tre file. Una seconda verifica dell'origine precede la creazione dell'ancora. Origine e destinazione devono essere disgiunte; collegamenti e percorsi non sicuri vengono rifiutati. Una preparazione incompleta conserva i file e una ricevuta di fallimento, senza retry sullo stesso identificatore. I dati scientifici originali e le dipendenze restano esterni: la snapshot non è un archivio scientifico autonomo.

## Eventi e revoca

Ogni apertura richiede il digest indipendente dell'ancora; ogni lettura o modifica richiede anche il digest atteso della testa. Gli eventi sono numerati, create-only e concatenati per SHA256. Le azioni ammesse sono `KEEP_FOR_REVIEW`, `REJECT_CANDIDATE`, `FOLLOW_UP` e `REVOKE_REVIEW`. La revoca aggiunge un evento riferito a una revisione precedente e ne conserva integralmente i byte; non ritira segnalazioni esterne.

Identificativo dell'attore, UTC e nota sono dichiarazioni del chiamante, senza attestazione della sua identità. L'ordinamento controlla gli UTC dichiarati, senza attestare l'ora reale. Capacità massima di 128 eventi e limiti testuali sono limiti operativi, non soglie scientifiche. Una richiesta identica può essere riconosciuta solo sulla testa corrente verificata; stesso identificatore con contenuto diverso viene rifiutato.

Due scrittori che usano la stessa testa competono per lo stesso file esclusivo: uno può riuscire e l'altro riceve errore, senza retry automatico. Se una verifica fallisce dopo la scrittura durevole, l'evento resta conservato e richiede riconciliazione esplicita. Il contratto presume file locali posseduti e letture senza modifiche concorrenti della snapshot: non offre firme digitali, protezione contro un amministratore del filesystem o autenticità senza una testa conservata indipendentemente.

## Export e cambiamento della scheda

La cronologia si esporta in JSON e testo UTF-8 con una nuova ricevuta verificata; nessun percorso, token o destinatario viene inviato a un servizio. `verify_current_preview` confronta l'export corrente con la snapshot: una scheda cambiata non può riutilizzare le revisioni precedenti. La cronologia congelata rimane leggibile come storia anche se l'origine cambia o scompare.

L'API è esplicita e locale, senza integrazione nel portale o nel servizio cloud. Gli stati restano `NOT_VALIDATED`, `submissionAuthorized=false`, `scientificAcceptance=false`, `externalSubmission=NONE`, `providerAcknowledgement=NONE`.

## Verifica e residui

Venti prove offline usano esclusivamente dati e decisioni sintetici. Coprono tutti e quattro gli exporter reali con rete vietata, alterazioni di origine/snapshot/ancora/eventi, testa arretrata, file mancanti, copie parziali, concorrenza, idempotenza, revoca, UTF-8, UTC, limiti, cambiamento della scheda ed export incompleto. Le prove del prototipo sono preparazione; CI sul commit esatto, ARB poi RQ e verifiche post-merge restano necessarie al rilascio.

BKL-051 resta OPEN / NOT_VALIDATED. Restano validazione scientifica completa, risposta tecnica IRSA, incertezze e covarianze, astrometria e timing, validazione cieca e falsi positivi, oggetti mobili e tracklet, integrazione privata autenticata, policy Owner, formati provider e trasporto/duplicati/esiti, S4 e S5. La cronologia locale non chiude questi requisiti. P6 Accepted nei suoi limiti; F4 attende il lifecycle reale, F5 segue F4 e BKL-050 resta conclusiva.
