# Capitolo 1 - Prima dell'enterprise

## La notte non comincia con il cielo

Nell'immaginario, un osservatorio astronomico esiste per guardare in alto. La scena sembra semplice: una cupola si apre, una montatura punta un oggetto, una camera raccoglie luce. Quando l'osservatorio diventa remoto, la stessa scena cambia natura. Prima di osservare il cielo bisogna sapere se l'impianto è alimentato, se la rete è raggiungibile, se il meteo consente l'apertura, se il tetto si trova davvero nello stato dichiarato, se la montatura può muoversi senza creare una collisione, se il software ha caricato la configurazione corretta e se esiste una via sicura per interrompere l'operazione.

La notte, quindi, non comincia con il cielo. Comincia con una catena di fiducia.

Digital StarGate nasce dentro questa realtà. Il suo punto di partenza non è un diagramma enterprise, ma un osservatorio concreto: struttura, energia, connettività, computer di campo, montatura, telescopi, camere, software astronomico e procedure. Ciascun elemento può essere compreso singolarmente. Il problema emerge nelle relazioni.

Una rete che funziona bene non garantisce che il computer remoto sia nello stato corretto. Un computer raggiungibile non garantisce che il dato del sensore sia fresco. Un sensore che segnala “aperto” non garantisce da solo che l'intera geometria sia sicura. Una sequenza automatica eseguita senza errori non dimostra che la decisione iniziale fosse appropriata. L'affidabilità del sistema non coincide con la somma delle affidabilità dei componenti.

Questa è la prima lezione del caso Digital StarGate: **la complessità risiede soprattutto negli intervalli tra le cose**.

## Un sistema fisico che parla digitale

Ogni osservatorio remoto vive su due piani.

Il primo è fisico. Comprende gravità, vento, umidità, ostacoli, tolleranze meccaniche, corrente elettrica, temperatura e usura. In questo piano una decisione errata può danneggiare un apparato prima che un operatore riesca a collegarsi.

Il secondo è digitale. Comprende stati, eventi, dashboard, configurazioni, log, notifiche, database e procedure automatizzate. È il piano attraverso il quale l'operatore remoto percepisce e governa il primo.

La difficoltà è che i due piani non coincidono mai perfettamente. La rappresentazione digitale è sempre una dichiarazione sul mondo fisico. Può essere incompleta, ritardata o ambigua. Per questo Digital StarGate ha progressivamente attribuito importanza a concetti come freshness, stato unknown, interlock locale, telemetria e authority. Non sono raffinatezze terminologiche. Sono strumenti per riconoscere che una schermata non è la realtà, ma una sua rappresentazione soggetta a condizioni.

Il principio è trasferibile a molte infrastrutture remote: non si governa ciò che esiste soltanto perché lo si vede su un monitor. Si governa ciò per cui si conoscono origine, attualità, significato e limiti dell'informazione.

## La prima forma di conoscenza: il manuale

Prima di diventare piattaforma enterprise, Digital StarGate ha consolidato la conoscenza in un manuale tecnico. I capitoli dedicati a struttura, impianto elettrico, rete, EAGLE, montatura, ottiche, camere e software hanno dato un nome alle parti del sistema. Le procedure di avvio, acquisizione, emergenza, manutenzione e chiusura hanno trasformato esperienza operativa in sequenze condivisibili.

Questo passaggio può apparire ordinario, ma è fondativo. Finché la conoscenza rimane nella memoria dell'operatore, il sistema dipende dalla presenza di quella persona. Quando la conoscenza viene descritta, revisionata e collegata, diventa patrimonio del progetto.

Un manuale, tuttavia, risponde soprattutto alla domanda “come funziona questo elemento?” o “come si esegue questa procedura?”. Con la crescita del sistema emergono domande diverse:

- chi è responsabile di una decisione?
- quale fonte prevale quando due documenti non concordano?
- come si distingue ciò che esiste da ciò che è pianificato?
- quale prova consente di dichiarare pronta una capacità?
- che cosa accade quando una dipendenza è indisponibile?
- come si preserva il significato dei dati nel tempo?
- quali decisioni può suggerire o prendere un sistema di AI?

Il manuale non perde valore. Cambia posizione: da prodotto finale diventa uno degli strati di una memoria più ampia.

## Il costo nascosto del remoto

La distanza introduce un'asimmetria. In presenza, molti problemi vengono risolti attraverso percezioni e azioni che non compaiono in alcun sistema: un rumore insolito, un cavo allentato, una resistenza meccanica, un odore, una luce inattesa. Da remoto, queste informazioni devono essere sostituite da sensori, telemetria, procedure, ridondanze o visite programmate.

Ogni assenza fisica crea quindi un requisito informativo. Se non posso osservare direttamente una condizione, devo decidere:

1. come rappresentarla;
2. come verificarne l'attualità;
3. quale livello di incertezza accettare;
4. quale comportamento adottare quando l'informazione manca.

Questa logica spiega perché la sicurezza non può essere affidata soltanto all'interfaccia remota. Se la connessione si interrompe, l'autorità di protezione deve restare vicina all'impianto. Il controller locale e gli interlock non sono un ripiego: sono il punto in cui la sicurezza rimane efficace anche quando la parte più sofisticata del sistema non è disponibile.

Nel percorso Digital StarGate questo principio diventa progressivamente esplicito: nessun portale deve comandare direttamente gli apparati; gli stati unknown o stale devono impedire azioni rischiose; la continuità non prevale sulla safety; l'autorizzazione remota non sostituisce l'autorità locale.

## Dalla procedura alla capacità

Una procedura descrive passi. Una capacità descrive un risultato che il sistema deve saper ottenere in modo ripetibile, governato e verificabile.

“Aprire la cupola” è un'azione. “Preparare in sicurezza l'osservatorio per una sessione remota” è una capacità. La seconda comprende condizioni meteo, stato dell'impianto, disponibilità degli strumenti, autorizzazione, sequenza, telemetria, gestione delle anomalie e prova dell'esito.

Questo passaggio dalla procedura alla capacità è uno dei segnali dell'evoluzione enterprise. Non elimina le istruzioni operative, ma le colloca dentro un contesto:

- un trigger spiega perché la procedura inizia;
- un owner chiarisce chi ne risponde;
- le precondizioni definiscono quando è lecita;
- le evidenze consentono di dimostrare che è avvenuta;
- le eccezioni descrivono cosa fare quando la realtà non segue il percorso ideale;
- la revisione collega l'esperienza al miglioramento futuro.

L'osservatorio smette così di essere una collezione di apparecchi e diventa un insieme di capacità coordinate.

## Il primo errore da evitare: digitalizzare la frammentazione

Quando un sistema cresce, la tentazione è aggiungere strumenti: una nuova dashboard, un nuovo script, un nuovo database, un nuovo assistente. Ogni aggiunta promette di risolvere una difficoltà locale. Senza un disegno comune, però, il risultato può essere una frammentazione più veloce.

Digitalizzare un processo ambiguo non lo rende chiaro. Automatizzare una responsabilità non assegnata non elimina l'ambiguità. Applicare AI a fonti incoerenti non produce conoscenza affidabile. Aggiungere una dashboard a stati privi di authority non crea controllo.

Il percorso enterprise parte quindi da una scelta meno spettacolare: rendere esplicite le relazioni. Qual è la fonte primaria? Chi possiede un dato? Quale componente può prendere una decisione? Quale evento deve essere conservato? Quale condizione blocca l'azione? Quale prova chiude una milestone?

Prima dell'enterprise, molte di queste risposte possono essere implicite nella pratica. Dopo il salto di scala, devono diventare proprietà del sistema.

## Piccola organizzazione, disciplina enterprise

Il termine enterprise viene spesso associato a grandi organizzazioni, comitati e processi pesanti. Nel caso Digital StarGate assume un significato differente. Una piccola realtà può avere bisogno di disciplina enterprise proprio perché dispone di poche persone.

Quando le risorse sono limitate, non è possibile compensare l'ambiguità con un reparto dedicato. La documentazione deve ridurre il tempo necessario per ricostruire il contesto. Le decisioni devono lasciare traccia. Le verifiche devono essere ripetibili. I confini devono impedire a un errore locale di propagarsi.

La disciplina utile non consiste nel produrre documenti per ogni attività. Consiste nel produrre l'artefatto minimo che conserva una decisione, un rischio, una responsabilità o un'evidenza che altrimenti andrebbero persi.

Questa proporzionalità è centrale nel modello che il libro svilupperà. Enterprise non significa burocratico. Significa governabile.

## La soglia

Un osservatorio attraversa la soglia enterprise quando le domande sul sistema non possono più essere risolte guardando un singolo componente.

Se per comprendere una sessione bisogna collegare meteo, configurazione, target, strumento, file, qualità ed esito, siamo davanti a un problema di architettura dell'informazione. Se per autorizzare un'azione bisogna collegare identità, ruolo, stato, rischio e interlock, siamo davanti a un problema di governance operativa. Se per introdurre AI bisogna collegare fonti, lineage, limiti, audit e responsabilità, siamo davanti a un problema di architettura enterprise.

Digital StarGate ha attraversato questa soglia passando dal manuale alla roadmap, dalla roadmap agli Architecture Package, dagli Architecture Package alle review e alle evidence, dai dati alle piattaforme scientifiche e dalla documentazione alla continuità cognitiva di BootAI.

Il passaggio non è stato un singolo progetto. È stato un cambio nel modo di vedere l'osservatorio.

## Lezione trasferibile

Prima di progettare una piattaforma, occorre riconoscere quale sistema esiste già. Il sistema reale comprende anche pratiche informali, dipendenze, conoscenze personali e condizioni ambientali. L'architettura enterprise non parte cancellando questa storia; parte rendendola leggibile.

Tre domande aiutano a individuare il punto di partenza:

1. Quali condizioni fisiche possono rendere falsa o pericolosa una rappresentazione digitale?
2. Quale conoscenza andrebbe persa se domani cambiasse l'operatore principale?
3. Quali decisioni oggi dipendono da informazioni prive di owner, freshness o evidenza?

Le risposte definiscono il primo perimetro del lavoro.

## Verifica per il lettore

- Riesci a descrivere il tuo sistema senza limitarti all'elenco degli apparati?
- Sai quali informazioni sono misure e quali sono interpretazioni?
- Esiste un'autorità locale che mantiene la sicurezza quando la rete non è disponibile?
- Le procedure dichiarano precondizioni, eccezioni ed evidenze?
- La documentazione permette a una persona nuova di ricostruire lo stato corrente?
- Le capacità future sono chiaramente distinte da quelle operative?

Se una risposta è incerta, il problema non richiede necessariamente più tecnologia. Richiede prima una migliore rappresentazione del sistema.

## Fonti del capitolo

- capitoli 1-44 del manuale tecnico Digital StarGate;
- `DSG-MR-001`, sezioni AS-IS, Transition e TO-BE;
- [Repository Knowledge Map](../project/REPOSITORY_KNOWLEDGE_MAP.md);
- Architecture Package `AP-003`, `AP-004`, `AP-009` e `AP-010`;
- documentazione dell'Enterprise Operations Center e dei modelli di safety;
- `AI_BOOTSTRAP.md`, principi non negoziabili.
