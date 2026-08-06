# Capitolo 3 - Quando il remoto cambia tutto

## La distanza non è un dettaglio logistico

Un osservatorio presidiato e un osservatorio remoto possono condividere gli stessi strumenti, ma non sono lo stesso sistema. La distanza non modifica soltanto il modo in cui l'operatore accede agli apparati. Modifica il significato di visibilità, controllo, errore e tempo.

In presenza, molte informazioni arrivano senza essere richieste. Un rumore, una vibrazione, una luce, una resistenza meccanica o una variazione improvvisa del vento diventano segnali. L'operatore integra ciò che vede sullo schermo con ciò che percepisce nell'ambiente.

Da remoto, il sistema deve trasformare quella percezione diffusa in informazioni esplicite. Ciò che non è rappresentato rischia di non esistere per chi opera. Ciò che è rappresentato male rischia di apparire più certo della realtà.

Per questo la distanza non è un requisito secondario. È una proprietà architetturale.

## Il problema della presenza sostituita

Ogni azione remota sostituisce una presenza fisica con una catena di mediazioni:

- un sensore osserva una condizione;
- un controller interpreta il segnale;
- una rete trasporta lo stato;
- un servizio lo normalizza;
- un'interfaccia lo rappresenta;
- una persona o un'automazione decide;
- un comando percorre il tragitto inverso;
- un'attuazione modifica il mondo fisico;
- una nuova osservazione dovrebbe confermare il risultato.

In questa catena, “comando inviato” e “azione completata” sono due fatti diversi. Anche “sensore raggiungibile” e “informazione affidabile” sono fatti diversi.

Il lavoro remoto richiede quindi una disciplina di conferma. Non basta sapere che un messaggio è partito. Occorre sapere che l'azione è stata accettata, che il mondo fisico ha raggiunto lo stato atteso e che la conferma è sufficientemente recente.

Digital StarGate ha progressivamente espresso questa disciplina attraverso concetti come stato `CLOSED` confermato, comando idempotente, freshness, correlation, allarme e rollback. Il libro non entra nei dettagli implementativi. Ne conserva il significato: una decisione remota deve includere il modo in cui il sistema riconosce l'esito e reagisce all'assenza di conferma.

## La latenza del soccorso

Quando un operatore è presente, una piccola anomalia può essere corretta prima che diventi incidente. Da remoto esiste una latenza di intervento, anche quando la connessione è veloce.

La latenza non è soltanto il tempo di rete. Comprende:

1. tempo necessario perché l'anomalia venga osservata;
2. tempo per distinguerla da un falso allarme;
3. tempo per decidere;
4. tempo per eseguire un'azione remota;
5. tempo per ottenere conferma;
6. tempo per raggiungere fisicamente il sito, se il controllo remoto non basta.

Questa sequenza cambia il criterio di progettazione. Un sistema remoto non deve soltanto segnalare bene. Deve saper limitare il danno mentre l'operatore comprende la situazione.

La safety locale risponde a questa esigenza. Interlock, safe state e controller locali non sono sostituti primitivi dell'automazione centrale. Sono la parte del sistema progettata per avere la latenza più breve rispetto al rischio fisico.

L'Enterprise Architecture di Digital StarGate rende questa priorità esplicita: portale, cloud e AI non sostituiscono l'autorità locale; lo stato unknown non è safe; la perdita di una dipendenza deve condurre a un comportamento degradato prevedibile.

## Connettività: canale e dipendenza

La rete è spesso descritta come mezzo di accesso. In un osservatorio remoto è anche una dipendenza operativa e una possibile fonte di ambiguità.

Una connessione può essere:

- disponibile ma instabile;
- sufficiente per visualizzare una pagina ma non per mantenere una sessione;
- attiva verso un nodo e interrotta verso un altro;
- lenta al punto da rendere obsolete le informazioni;
- nominalmente ridondata ma priva di failover verificato.

Progettare la rete significa quindi progettare le conseguenze della sua perdita. Quali operazioni continuano? Quali si arrestano? Quale stato viene mantenuto? Quale componente prende l'ultima decisione? Che cosa vedrà l'operatore quando il collegamento ritorna?

Il caso Digital StarGate comprende PC Principale, EAGLE, connettività remota e componenti infrastrutturali che hanno ruoli differenti. La roadmap enterprise distingue le responsabilità: il PC Principale sostiene sviluppo, documentazione, analytics e release; EAGLE sostiene gestione dell'osservatorio, acquisizione, controllo e telemetria sul campo.

La separazione non è soltanto organizzativa. Riduce il rischio che un problema nella piattaforma di engineering acquisisca autorità implicita sul sistema fisico.

## Il meteo come autorità esterna

Il meteo ricorda che non tutte le condizioni sono controllabili. Pioggia, vento, umidità e copertura nuvolosa non rispondono alla qualità del software.

In un sistema remoto il meteo deve essere tradotto in decisioni, ma questa traduzione presenta tre difficoltà.

La prima è la qualità della misura. Un sensore può essere guasto, incoerente o non aggiornato.

La seconda è la qualità della regola. Una soglia non validata può produrre falsi stati safe o interrompere inutilmente le operazioni.

La terza è l'autorità dell'eccezione. Un operatore può ignorare un allarme? In quali circostanze? Chi registra la decisione? Quali condizioni non possono essere bypassate?

La proposta della Release 2.0 Safety Foundation mostra un approccio progressivo: contratti e simulatori, shadow mode, blocco dell'apertura, chiusura automatica e soltanto in futuro eventuali decisioni ulteriori. La riapertura automatica è trattata separatamente. Le soglie non validate non vengono inventate.

Questa sequenza contiene una lezione generale: l'automazione di sicurezza deve guadagnare autorità attraverso evidenze progressive.

## Progettare per l'unknown

Molti sistemi trattano lo stato sconosciuto come un problema di visualizzazione: un indicatore grigio, un trattino o un messaggio temporaneo. In un sistema cyber-fisico lo stato unknown è una condizione decisionale.

Se il sistema non conosce lo stato del tetto, non può comportarsi come se fosse chiuso. Se il dato meteo è stale, non può comportarsi come se fosse favorevole. Se una chiusura non è confermata, non può dichiarare conclusa l'emergenza.

Il principio “unknown is not safe” non significa che ogni incertezza produca panico. Significa che l'incertezza è modellata e associata a un comportamento conservativo.

Il modello richiede almeno:

- riconoscere l'assenza del dato;
- distinguere unknown da unsafe;
- impedire che un valore precedente venga interpretato come corrente;
- dichiarare quali azioni sono ancora consentite;
- generare un'evidenza dell'anomalia;
- definire una via di recovery.

Questa è una delle differenze tra monitoraggio e controllo. Il monitoraggio mostra che qualcosa non è noto. Il controllo decide che cosa non deve accadere finché l'informazione non torna affidabile.

## L'idempotenza come qualità operativa

Un comando è idempotente quando può essere ripetuto senza produrre conseguenze aggiuntive indesiderate. In un ambiente remoto questa proprietà diventa concreta.

Se la rete cade durante una richiesta di chiusura, l'operatore può non sapere se il comando è stato ricevuto. La possibilità di ripeterlo in sicurezza riduce l'ambiguità. Se invece ogni ripetizione può generare un comportamento differente, la perdita di conferma diventa un rischio.

L'idempotenza non risolve ogni problema. Non sostituisce la verifica fisica dello stato. Ma consente di progettare retry, recovery e procedure più semplici.

La lezione più ampia è che una qualità apparentemente tecnica può avere valore organizzativo. Un comando ripetibile riduce la pressione sull'operatore. Una correlation rende ricostruibile una sequenza. Una conferma esplicita riduce interpretazioni. Il buon design non si limita a far funzionare la macchina: rende più sicura la decisione umana.

## Osservabilità: sapere abbastanza per decidere

La telemetria produce dati; l'osservabilità rende il comportamento interpretabile.

In un osservatorio remoto non serve mostrare tutto nello stesso momento. Serve mostrare ciò che permette di rispondere alle domande operative:

- il sistema è raggiungibile?
- i dati sono freschi?
- quale modalità è attiva?
- esiste un rischio in evoluzione?
- quale dipendenza è degradata?
- l'ultima azione ha raggiunto lo stato atteso?
- quale runbook è applicabile?
- chi ha preso la decisione?

Una dashboard ricca ma priva di authority e freshness può aumentare l'illusione di controllo. Una vista più sobria, capace di distinguere misura, inferenza, allarme ed evidenza, sostiene decisioni migliori.

Per questo l'Operations Center di Digital StarGate è stato concepito inizialmente come read-only. Prima si rende visibile e verificabile il sistema. Solo dopo, attraverso authorization, audit, four-eyes e safety review, si può valutare l'introduzione del comando.

Read-only non è assenza di ambizione. È una fase di apprendimento controllato.

## La notte come transazione lunga

Una sessione osservativa può durare ore. Attraversa cambi di temperatura, altezza del target, qualità di guida, condizioni meteo, disponibilità della rete e stato degli apparati. Non è una singola operazione: è una transazione lunga nel mondo fisico.

A differenza di una transazione informatica, non può sempre essere annullata. Il tempo trascorso non torna indietro, una finestra di osservazione può chiudersi e un apparato può aver subito una sollecitazione.

La progettazione deve quindi privilegiare:

- checkpoint comprensibili;
- stati intermedi espliciti;
- possibilità di sospensione;
- chiusura sicura;
- conservazione delle evidenze già prodotte;
- ripresa controllata, quando consentita.

Il valore della sessione come oggetto governato nasce anche da qui. Permette di collegare intenzione, condizioni, esecuzione, file ed esito senza ridurre tutto a “successo” o “fallimento”.

## Operare nel degrado

Un sistema resiliente non è quello che continua sempre. È quello che degrada senza perdere i propri invarianti.

Le modalità degradate possono includere:

- continuare l'acquisizione locale senza servizi centrali;
- sospendere nuove azioni e mantenere lo stato corrente;
- chiudere l'osservatorio e attendere;
- passare dalla modalità automatica a quella manuale;
- conservare dati localmente per una sincronizzazione successiva;
- disabilitare funzioni non essenziali;
- richiedere un intervento fisico.

Ogni modalità deve dichiarare ciò che rimane vero. La protezione locale resta attiva. Le azioni non autorizzate restano proibite. Le evidenze non vengono fabricate. Il ritorno alla normalità richiede condizioni, non soltanto il ripristino della connessione.

## Lezione trasferibile

La distanza trasforma ogni assunzione in un contratto.

Se si presume che la rete sarà disponibile, occorre definire cosa accade quando non lo è. Se si presume che un sensore rappresenti il mondo, occorre definirne freshness e failure mode. Se si presume che un comando venga eseguito, occorre una conferma. Se si presume che un operatore possa intervenire, occorre considerare la latenza reale.

Il remote-by-design non consiste nell'aggiungere accesso remoto a un impianto. Consiste nel progettare il sistema affinché la perdita di presenza non cancelli sicurezza, comprensibilità e responsabilità.

## Verifica per il lettore

- Quali percezioni umane non sono ancora rappresentate dal sistema?
- Quanto tempo passa tra un'anomalia e un intervento fisico?
- Quali decisioni rimangono locali quando la rete cade?
- I dati mostrati dichiarano la propria freshness?
- I comandi critici sono ripetibili e confermabili?
- Lo stato unknown produce un comportamento definito?
- Le modalità degradate hanno criteri di ingresso e uscita?
- Il ritorno alla normalità richiede una verifica?

## Fonti del capitolo

- manuale tecnico, capitoli su rete, EAGLE, automazione, meteo, emergenze e chiusura;
- [Release 2.0 - Safety Foundation](../releases/release-2.0-safety-foundation.md);
- `ADR-005` e Capability 002 Weather Safety Interlock;
- Architecture Package `AP-003`, `AP-004`, `AP-009`, `AP-010` e `AP-012`;
- `DSG-MR-001`, modello di interazione PC Principale/EAGLE;
- documenti `ARB-012` su comportamento degradato, audit e authorization.
