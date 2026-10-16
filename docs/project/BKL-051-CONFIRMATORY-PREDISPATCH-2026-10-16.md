# BKL-051 — collegamento confermativo prima dell'invio

Stato: **implementazione in corso, R09 aperto / NOT_VALIDATED**. Zero controlli
scientifici qualificati. Nessuna attivazione, credenziale, analisi nativa o spesa
autorizzata da questo documento o dal codice.

## Risultato richiesto

Il piano congelato, il riferimento del caso e le tre esposizioni ordinate devono
essere vincolati prima degli invii. Gli intenti devono essere persistiti prima
delle richieste; una risposta persa lascia un tentativo da riconciliare mediante
sole letture, senza reinvio. Un processo incerto o un annullamento soltanto
richiesto impediscono il successivo avvio. `record_execution` conserva il proprio
ruolo di registrazione degli esiti, distinto dall'ammissione all'esecuzione e
dall'accettazione scientifica Owner.

## Prerequisito implementato

`ConfirmatoryCampaigns.dispatch_context` restituisce una fotografia coerente del
registro della campagna: hash del piano e dell'evento FREEZE, revisione congelata
degli input, hash del riferimento e del rapporto degli input, tre frame ordinati,
algoritmo e contratto con identificativi e hash. L'hash del contesto include questi
campi. Il contesto resta stabile quando si registrano altri casi del medesimo
piano; il current head non sostituisce l'identità immutabile del congelamento.

La lettura rifiuta piani non congelati, revocati o bloccati, riferimenti non
selezionati, revisioni degli input diverse da quelle congelate e casi con esito
già registrato. Non cambia il registro e non crea job. Restituisce sempre
`launchAuthorized:false` e `scientificValidation:NOT_VALIDATED`.

Il percorso privato Owner è:

`GET /v1/transient-analysis/campaigns/<planRef>/inputs/<witnessRef>/dispatch-context`

Riusa l'autenticazione Owner esistente. La credenziale Worker non accede a questo
percorso e nessun percorso equivalente Worker è aggiunto. La composizione runtime
delle campagne conserva il valore disabilitato esistente. Non sono aggiunti
percorsi locali, file originali, token o lease alla risposta.

## Registro di ammissione locale in verifica

Le application port `prepare_dispatch`, `admit_frame`, `close_frame` e
`dispatch_receipt` sono implementate nel servizio della campagna e **non sono
esposte via HTTP**. Non creano o prenotano job e non avviano processi nativi.
L'intento Owner vincola il contesto completo, tre binding ordinati e request ID
distinti, worker/root e hash dell'archivio privato dichiarato. Il registro impedisce
di preparare nuovamente lo stesso caso o riutilizzare request ID tra campagne.

L'ammissione usa lo stesso CAS della revoca e mantiene un solo avvio in volo o
incerto per il worker nel registro configurato. Non viene riemessa dopo una
risposta persa: la ripetizione esatta restituisce `RECONCILIATION_REQUIRED` senza
ammissione. La revoca prima del commit impedisce l'ammissione; se il commit
dell'ammissione precede la revoca, la ricevuta conserva `STOP_PENDING_RECONCILIATION`.
Questo ordine non attesta l'istante di creazione o arresto del processo OS.

La chiusura conserva il digest delle evidenze di arresto **riportate dal Worker**,
insieme a job, attempt, binding, root, cronologia e rapporto tecnico esatti. Il
confronto con lo snapshot tecnico della coda avviene fuori dal callback CAS. Una
chiusura `COMPLETED` richiede misure complete e almeno una misura. Solo una chiusura
completata del frame precedente permette l'ammissione del successivo; errore,
annullamento o recupero incerto non completano la tripletta. Queste dichiarazioni
non sono attestazioni indipendenti: il coordinatore locale dovrà verificare i
file e l'effettiva chiusura del processo prima di inviarle.

Un job `RECOVERY_REQUIRED` può chiudere il blocco tecnico soltanto dopo la
`recoveryClosure` Owner già prevista dalla coda, validata con le stesse regole e
con un hash dell'evidenza uguale a quello riportato dal Worker. La chiusura Owner
viene conservata nella ricevuta. Il caso mantiene `RECOVERY_REQUIRED` e non
consente il frame successivo della stessa tripletta; può liberare il worker per
un diverso intento Owner valido. Non è un'attestazione indipendente di arresto.

## Coda protetta interna in verifica

`CampaignQueue` collega esplicitamente il registro e una coda isolata con profilo
campagna, stessa identità Worker e stesso oggetto storage configurato. Il namespace
vincola le chiavi dei due registri e l'Owner; non introduce un nuovo firmatario o
un'API di autenticazione. I metodi interni della coda richiedono la capacità
in-process della composizione, che non può essere fornita da JSON HTTP.

La proiezione conserva sul nuovo job un marcatore interno immutabile con contesto,
intento, piano, FREEZE, riferimento, input, algoritmo, contratto, ordinale,
binding e worker/root. Un job precedente non viene adottato o migrato. Marker
malformati o di versione sconosciuta bloccano la lettura. Marcatore e metadati
della prenotazione sono rimossi dalle viste esterne; gli schemi esistenti di
`ReservationIntent`, rapporti e ricevute Worker restano invariati.

`admit_and_reserve` ottiene un'ammissione appena creata dal registro e poi esegue
la prenotazione protetta della coda fuori dal callback CAS. La prenotazione
registra insieme ammissione, intento, attempt e lease. Solo il primo risultato
creato restituisce la lease: ripetizioni e conflitti concorrenti non la recuperano.
Un errore della coda dopo l'ammissione conserva il blocco nel registro, anche
quando la risposta è persa dopo un commit. Le letture non autorizzano reinvii.

I percorsi legacy `create`, `claim` e `reserve_once` rifiutano i job marcati. Il
controllo di `claim` copre anche il ritorno di job già RESERVED/RUNNING o in
recupero, prima che una vista possa rivelare una lease esistente. Dopo una
chiusura di recupero Owner, il job resta RECOVERY_REQUIRED e nessuna lettura
restituisce la sua vecchia lease.

Questi collegamenti restano application port interne: nessun nuovo percorso HTTP
protetto è esposto, nessuna composizione runtime è attivata e nessun processo
nativo è avviato. La verifica completa del coordinatore locale resta necessaria.

## Namespace e chiusura senza attempt in verifica

La preparazione Owner passa ora attraverso `CampaignQueue.prepare_dispatch`.
La composizione aggiunge il namespace canonico; il chiamante non può fornirlo
come campo JSON o usare il metodo diretto per aggirare la configurazione. Il primo
intento esplicito conserva il namespace nel registro, nell'intento e poi
nell'ammissione. Una diversa chiave coda non può preparare, proiettare, prenotare
o riconciliare quell'intento, anche con lo stesso Worker. La composizione fissa
anche il lettore dei job alla coda esatta e rifiuta una sua sostituzione.
Il vincolo copre anche il precedente `record_execution`: su un registro vincolato
la coda configurata viene verificata prima di qualunque lettura dei job; servono
l'intento Owner del caso e i suoi tre job esatti. Un esito diverso da INCONCLUSIVE
richiede inoltre le tre ammissioni con chiusure COMPLETED e attempt/rapporti
corrispondenti. La chiusura di un frame verifica la provenienza prima di leggere
la coda e di nuovo nel CAS. Questi controlli non trasformano i rapporti Worker in
attestazioni scientifiche né sostituiscono la revisione Owner.
Non viene assegnato automaticamente un namespace agli intenti storici non
vincolati, che restano leggibili ma non vengono adottati dai nuovi flussi.

Per un'ammissione consumata senza attempt, `unreserved_context` legge uno snapshot
privato della coda. Deve essere esattamente CANCELLED, con richiesta di
annullamento, sequenza zero e senza alcun campo attempt, root, lease,
prenotazione o recupero, neppure con valore null. Il marcatore completo deve
corrispondere all'intento, all'ammissione e al namespace. Una lettura QUEUED o un
job assente non sono prove sufficienti.

La cancellazione è una barriera stabile della coda: se vince prima del commit di
prenotazione, il CAS obsoleto perde e non può emettere una lease; se la
prenotazione vince, esiste un attempt e questo percorso rifiuta la chiusura.
La barriera può precedere anche l'ammissione logica, purché la cronologia del job
sia coerente: il job terminale resta non prenotabile da tutte le API previste.

`close_unreserved` è una application port Owner, ancora non esposta via HTTP.
Rilegge lo snapshot fuori dal CAS del registro e conserva l'evento distinto
UNRESERVED_FENCED_CLOSURE con stato NOT_STARTED_FENCED, hash dello snapshot ed
evidenza dell'annullamento dichiarata dall'Owner. Non inventa un attempt, non
attesta un arresto OS e non produce COMPLETED. Libera soltanto l'ammissione esatta:
il frame successivo dello stesso caso resta bloccato. La pulizia è ammessa dopo
revoca senza riabilitare nuovi avvii. Intenti durabili prima dei futuri POST di
annullamento e chiusura, riconciliazione delle risposte perse e autenticazione
Owner restano requisiti dell'integrazione HTTP/coordinatore.

## Integrazione ancora da implementare e verificare

L'intento della tripletta e l'ammissione di ogni avvio devono usare il medesimo
registro autorevole della revoca. Le chiamate alla coda devono avvenire fuori dai
callback CAS, che possono essere ripetuti durante la risoluzione dei conflitti.
Gli identificativi deterministici permettono letture esatte dopo una risposta
persa; un GET 404 non autorizza a reinviare una richiesta potenzialmente in volo.

Due CAS separati, o una lettura immediatamente prima di creare il processo,
non costituiscono una transazione tra revoca remota e avvio del sistema operativo.
L'ordine ammissione/revoca deve essere esplicito: un'ammissione già emessa resta
in volo o incerta fino alle evidenze di chiusura, anche dopo revoca. Nessuna
revoca o scadenza prova da sola l'arresto di PixInsight. La lettura del contesto
qui implementata non risolve questo requisito e non consente ancora avvii.

Restano da verificare indipendentemente la proiezione protetta della coda e da
completare il coordinatore locale
sequenziale con intenti durabili, le riconciliazioni, i collegamenti dei rapporti,
la vista Owner e il collaudo integrato. Il flusso diagnostico singolo esistente
resta distinto. Nessun controllo confermativo è stato eseguito.

## Evidenze locali

Le suite `test_confirmatory_dispatch_context`, `test_confirmatory_campaign` e
`test_confirmatory_http` hanno superato 45 prove locali, comprese otto nuove prove
sul contesto e sui confini HTTP. Sono fixture sintetiche e non dimostrano
accettazione scientifica, dispatch completo, CI sull'exact HEAD, rilascio o
accettazione operativa. ARB e RQ esatte restano gate separati.

Le prime 20 prove sintetiche del registro di ammissione sono passate, comprese
revoca concorrente forzata durante il CAS, risposta persa, ordine dei frame,
annullamento richiesto distinto dall'arresto, risultati incompleti e lettura della
coda eseguita una sola volta anche durante un retry del CAS. Una prova ulteriore
di capienza ha registrato 59 intenti e 177 ammissioni/chiusure simulate: 415 eventi
complessivi entro il limite di 8 MiB, con zero qualificati. Le quattro suite
contestuali hanno superato 64 prove; la nuova prova di capienza è passata
separatamente, per 65 prove complessive. Non dimostrano il dispatch dei job, il
coordinatore locale o un avvio reale.

Due ulteriori prove sul recupero Owner sono passate: chiusura esatta mantenendo
il caso non completato e rifiuto di evidenze discordanti con conservazione del
blocco. La suite del registro comprende ora 22 prove; il successivo controllo
contestuale dei 67 casi complessivi è passato in 66,232 secondi sul candidato
locale. Non sostituisce CI e revisioni sull'esatto commit finale.

La coda protetta ha superato 17 prime prove sintetiche, una prova separata su 59
triplette/177 job marcati con rapporti e chiusure dichiarati (415 eventi nel
registro, entrambi i registri entro 8 MiB), e una prova HTTP contro il recupero
della lease attraverso i percorsi precedenti. Sono passate anche 61 prove di
regressione su coda, capienza, ReservationIntent e OperatorPlan. I riferimenti di
arresto della prova di capienza sono fixture dichiarate, non evidenze OS né
controlli scientifici. Il successivo controllo contestuale campagna/HTTP e le
revisioni esatte sono gate separati.

Le prime 15 prove sintetiche di namespace e chiusura senza attempt sono passate:
concorrenza forzata cancel/reserve, barriera precedente all'ammissione, rifiuto di
attempt presenti anche dopo CANCELLED, namespace estranei, campi null inattesi,
revoca, ripetizione di decisioni e lettura dello snapshot una sola volta fuori
dal callback CAS. Le regressioni sull'esatto candidato e ARB/RQ restano separate.

La prima revisione ha rilevato che il precedente percorso di registrazione degli
esiti non applicava ancora il namespace. Il candidato è stato corretto prima
del commit; quattro ulteriori controprove verificano rifiuto della coda estranea
senza letture, obbligo dei job Owner, obbligo delle tre chiusure e mantenimento
dello stato Worker-reported. Quel candidato comprendeva 19 prove di riconciliazione;
la prima regressione di 105 casi è passata, ma precede la correzione seguente.

Il secondo riesame ha rilevato letture della coda dentro il callback CAS della
registrazione degli esiti. Gli snapshot sono stati spostati fuori dal callback:
autorità e binding sono verificati prima delle letture e ricontrollati ad ogni
retry del CAS. Tre job producono tre letture anche con conflitto, mentre una
decisione già registrata non rilegge la coda. Una richiesta di chiusura malformata
viene inoltre rifiutata prima di acquisire lo snapshot privato. La suite di
riconciliazione comprende ora 21 prove e la regressione completa richiede 107
casi, oltre a nuova ARB/RQ e CI sull'esatto commit.

## Candidato HTTP protetto (non attivato)

`handler_for` accetta una composizione `campaign_queue` esplicita, disabilitata
per default. Verifica l'identità dei servizi effettivi e il namespace senza
creare stato. I nuovi percorsi Owner permettono intento, ricevuta, proiezione e
chiusura con barriera; i percorsi Worker permettono prenotazione singola e
chiusura tecnica. I ruoli restano distinti e non esistono fallback legacy.
La risposta Worker di chiusura è una ricevuta tecnica minimizzata: hash della
chiusura e dell'ammissione, stato dichiarato e assenza di attestazione scientifica.
La dichiarazione di riconciliazione Owner resta nel registro e nella ricevuta
Owner, senza essere restituita al Worker. Questa separazione corregge il P2
rilevato dalla prima ARB; il candidato precedente e il rapporto sono conservati.

La prenotazione protetta restituisce `DSG_CAMPAIGN_RESERVATION_V1`, con il solo
hash dell'ammissione appena creata e il job nel formato precedente. Una richiesta
ripetuta restituisce `RECONCILIATION_REQUIRED`, hash e job nulli. Il metodo interno
precedente conserva il formato esatto `{disposition, job}`. La ricevuta Owner è
metadato di riconciliazione e non autorizza avvii o recupero della lease.

Questo candidato richiede ancora gate completi e revisioni indipendenti. Il
coordinatore locale durevole e il suo adattatore non sono ancora implementati;
nessuna composizione di produzione è modificata. R09 resta aperto, la milestone
`NOT_VALIDATED` e i controlli qualificati reali restano zero.
