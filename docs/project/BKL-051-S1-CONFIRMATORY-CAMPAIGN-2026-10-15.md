# BKL-051 — candidato del registro confermativo autenticato

## Stato e finalità

BKL-051 resta **OPEN / NOT_VALIDATED**, con **zero controlli reali qualificati**.
Il candidato aggiunge un registro separato per il collaudo confermativo; non
modifica i contratti preliminari e non li promuove a validazione scientifica.
La composizione applicativa di produzione non istanzia il registro: le nuove
rotte restano disabilitate finché non viene fornito esplicitamente l'adattatore.
Nessun deploy, risorsa, permesso, credenziale o costo cloud è attivato.

## Autorità e prove

`confirmatory_campaign.py` espone porte applicative riservate all'adattatore HTTP.
L'autenticazione resta quella esistente: Google per l'Owner configurato e
credenziale worker dedicata. Identità, orario e autorità delle decisioni non
provengono dal documento inviato dal client. Il worker registra testimonianze
degli input ed esiti; non legge le decisioni Owner e non può approvare o congelare.

Una testimonianza deve descrivere tre esposizioni scientifiche cronologiche,
con impronte, provenienza temporale, banda e dichiarazioni esplicite sul modello
di calibrazione e incertezza. Valori sconosciuti sono conservati e bloccano
l'idoneità. Ricerca, template e differenza non diventano tre epoche scientifiche.
L'Owner deve esaminare le prove private corrispondenti alle esatte impronte:
riferimento nullo, indipendenza, modello scientifico e separazione dallo sviluppo.
Queste revisioni sono vincolate alle impronte di algoritmo e regole del piano.

Il registro conserva dichiarazioni di un worker autenticato, **non attestazioni
indipendenti dell'esecuzione**. Un hash identifica i byte, non dimostra la verità
scientifica del contenuto. Le decisioni Owner non sostituiscono le prove mancanti.
Checksum dello stato e catena degli eventi rilevano alterazioni incoerenti;
non garantiscono immutabilità contro un amministratore privilegiato.

## Congelamento ed esecuzioni

Il piano V1 richiede esattamente 59 controlli, con gruppi di correlazione distinti
e 177 esposizioni e impronte distinte. Le sole etichette distinte non dimostrano
indipendenza: il congelamento richiede anche la revisione globale documentata
dell'indipendenza e della separazione dallo sviluppo. Include impronta del piano,
delle revisioni selezionate e del registro corrente. Riutilizzi successivi per
sviluppo non riscrivono lo snapshot; nuove informazioni invalidanti richiedono
una revoca esplicita, conservata nella cronologia.
Il riuso confronta sia gli hash dei file sia gli identificativi stabili di
immagine ed esposizione contro lo sviluppo e i campioni già congelati: una
ricodifica con byte diversi non rende indipendente la stessa osservazione.
L'insieme di esclusione congelato comprende sia `DEVELOPMENT` sia `SYNTHETIC`:
un nuovo witness dichiarato reale non può riqualificare osservazioni già note
come sintetiche. Il nome V1 `developmentWitnessRefsAtFreeze` identifica questo
insieme di esclusione completo, non la sola categoria di sviluppo.

Ogni esito collega tre job e attempt effettivi della coda, creati dopo il
congelamento, con input, algoritmo, regole, report e binding corrispondenti.
Il registro non crea job e non avvia PixInsight. Esiti incompleti, falliti o
incerti restano inconcludenti. V1 accetta una sola sintesi di esecuzione per caso:
ritentare la stessa richiesta è idempotente, sostituire una sintesi è rifiutato.
La gestione operativa di nuove esecuzioni autorizzate e riconciliazioni resta
un requisito distinto; questo candidato non completa R09.

L'Owner rivede l'impronta esatta dell'esito. Cinquantotto controlli completati
restano visibili ma non soddisfano il piano. Una falsa segnalazione fa fallire
il criterio a zero eventi e non può sparire scegliendo un altro tentativo.
Solo 59 esiti validi, rivisti e senza false segnalazioni consentono il limite
binomiale unilaterale al 95%: `1 - 0.05 ** (1 / 59)` (circa 4,95076%).
Il risultato resta condizionato alle regole congelate e alle prove esaminate.
La decisione finale riguarda esclusivamente la campagna dichiarata, mai l'intera
milestone, una scoperta o un invio astronomico. Una revoca conserva gli eventi
e rimuove l'idoneità corrente al risultato statistico.

## Interfacce e conservazione

Le rotte Owner sotto `/v1/transient-analysis/campaigns` permettono creazione,
lettura, revisione input, congelamento, revisione esito, decisione finale e revoca.
Le sole rotte worker sotto `/v1/transient-analysis/worker/campaigns` permettono
registrazione input ed esecuzioni. Non esiste dispatch implicito.
Il registro privato usa una chiave separata versionata e aggiornamenti CAS;
ritenta soltanto conflitti sui metadati, senza ripetere operazioni scientifiche.
Non migra né modifica registri preliminari o stati legacy. Limiti V1: 500
testimonianze, otto piani, stato massimo 8 MiB; il limite HTTP esistente resta.

Il successivo candidato di interfaccia aggiunge la lettura Owner
`GET /v1/transient-analysis/campaigns/<planRef>/review-receipt`: una sola lettura
coerente restituisce piano, riepilogo, cronologia ed esecuzioni con decisioni.
La ricevuta `BKL051_CONFIRMATORY_OWNER_RECEIPT_V1` permette di confrontare una
richiesta di metadati con il relativo evento dopo una risposta persa; la lettura
non ripete la richiesta e non avvia job. La presenza di un evento diverso non
conferma una richiesta: identificativo e contenuto esatto devono corrispondere.
I dati restano una vista autenticata del servizio, con `localBytesVerified=false`;
non attestano i file privati sul PC. Nessun lease token o credenziale è incluso.
Il worker non può leggere la ricevuta e la rotta non accetta scritture. La
composizione di produzione resta disabilitata. L'interfaccia operativa completa
e la sua verifica restano da implementare sul candidato successivo.

Il ritorno alla composizione senza adattatore disabilita le nuove rotte senza
cancellare lo stato. Un'eventuale attivazione richiede separata valutazione di
configurazione, capacità, permessi e costi; non è autorizzata da questo documento.

## Verifica e lavoro residuo

I test usano esclusivamente metadati sintetici e coda in memoria. Coprono
separazione Owner/worker, input incompleti e correlati, snapshot e impronte,
collegamento ai job, casi inconcludenti, falsi allarmi, idempotenza, conflitti,
revoche e confine statistico 58/59. Il caso positivo sintetico non qualifica
alcun dato astronomico reale. Gli esiti della suite e le review indipendenti
devono essere acquisiti sul candidato esatto prima dell'integrazione.

Restano da completare interfaccia operativa, adattatori delle evidenze reali,
orchestrazione e recupero autorizzati, campione reale indipendente con verità
nulla verificabile, modello scientifico completo, revisione Owner autenticata
e tutti gli altri requisiti R01–R14. Nessun requisito complessivo è dichiarato
completo sulla sola base di questo incremento.
