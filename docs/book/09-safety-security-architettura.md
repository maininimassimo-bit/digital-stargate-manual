# Capitolo 9 - Safety e security come architettura

## Due parole che proteggono cose diverse

Safety e security vengono spesso accostate fino a sembrare sinonimi. In un osservatorio remoto proteggono aspetti differenti e devono collaborare senza sostituirsi.

La safety protegge persone, apparati e ambiente dalle conseguenze di stati o azioni pericolose, indipendentemente dal fatto che l'origine sia un guasto, un errore o una condizione naturale. La security protegge identità, accessi, sistemi e informazioni da uso non autorizzato, compromissione o abuso.

Un sistema può essere sicuro dal punto di vista degli accessi e tuttavia pericoloso: un operatore perfettamente autenticato può richiedere un movimento incompatibile con la geometria fisica. Può anche essere protetto dalla safety ma debole sul piano security: un interlock impedisce una collisione, mentre un account condiviso rende impossibile attribuire chi abbia tentato l'azione.

Digital StarGate tratta i due domini come architetture correlate. AP-005 governa identità, privilegi, sessioni e secret. AP-010 governa hazard, safe state, autorità locale, contratti safety ed evidence. Il punto di incontro è il comando fisico: deve essere legittimo secondo la security e consentito secondo la safety.

Nessuno dei due consensi può essere dedotto dall'altro.

## La safety precede la continuità

La notte osservativa crea una pressione naturale verso la continuità. Una finestra di cielo può essere breve, una sessione può aver richiesto preparazione e un'interruzione può compromettere il risultato. In questa situazione è facile considerare il mantenimento dell'attività come misura principale dell'affidabilità.

Digital StarGate adotta una priorità differente: safety before availability. Un sistema che prosegue in condizioni non interpretabili non è resiliente. È incapace di riconoscere quando deve fermarsi.

Il principio determina l'ordine delle decisioni. Una condizione meteo unsafe prevale sulla schedulazione. Un dato stale impedisce una nuova apertura. La perdita di comunicazione non deve rendere inefficace la chiusura locale. Il ritorno della rete non autorizza automaticamente la ripresa. Dopo un evento, il sistema entra in recovery hold finché condizioni, verifica e responsabilità non consentono il ritorno al servizio.

Questa scelta comporta un costo: più interruzioni conservative, necessità di conferme e possibili osservazioni perdute. Il costo è intenzionale. Protegge un patrimonio fisico e scientifico che una falsa continuità potrebbe danneggiare.

La safety non massimizza il tempo di attività. Massimizza la capacità di interrompere correttamente quando il rischio non è accettabile.

## Una gerarchia vicina al rischio

In un sistema distribuito, l'autorità safety deve rimanere efficace anche quando le parti remote non sono disponibili. Digital StarGate ordina la prevalenza partendo dalle protezioni più vicine al mondo fisico: interlock hardware, controller locale, supervisore locale, automazione, integrazione, Operations Center, analytics e AI.

Un livello superiore può richiedere un'azione, ma non annullare il veto di un livello inferiore con maggiore autorità safety. La gerarchia può sembrare invertita rispetto alla complessità tecnologica: l'AI e il portale sono sofisticati, ma restano lontani dal punto in cui una decisione diventa movimento, energia o collisione.

La vicinanza non è soltanto geografica. È anche dipendenza. Un finecorsa continua a proteggere senza Internet. Un controller locale può reagire quando il portale non riceve telemetria. Una regola remota dipende invece da rete, sessione, servizi, dati e tempo affidabile.

L'autorità viene quindi collocata dove possiede la latenza minore rispetto al pericolo e il minor numero di dipendenze necessarie per agire.

Questo principio rende possibile adottare componenti più evoluti senza trasferire loro una sovranità implicita. Il sistema può diventare intelligente al centro e prudente al bordo.

## Unknown non è una terza risposta innocua

Molti sistemi presentano tre stati: vero, falso e non disponibile. L'interfaccia può trattare il terzo come un problema temporaneo di visualizzazione. In un sistema cyber-fisico, unknown è una condizione decisionale.

Se non è noto che il tetto sia chiuso, il sistema non può dichiararlo protetto. Se la misura meteo è stale, non può essere trattata come favorevole. Se due sensori sono discordanti, scegliere quello più comodo non risolve il conflitto. Se l'esito di un comando è incerto, ripeterlo alla cieca può produrre un secondo movimento.

AP-010 stabilisce che unknown non è safe. Ciò non significa che ogni incertezza produca la stessa emergenza. Significa che le azioni dipendenti da quella conoscenza vengono inibite o condotte verso un comportamento conservativo definito.

Il modello include stati come `SAFE_PROTECTED`, `NORMAL_AUTHORIZED`, `EMERGENCY_TRANSITION`, `RECOVERY_HOLD` e `UNKNOWN`. L'importanza non risiede nei nomi, ma nel fatto che l'incertezza abbia conseguenze progettate.

Una buona architettura non nasconde il dato mancante dietro l'ultimo valore conosciuto. Mostra qualità e freshness, limita ciò che può ancora essere fatto e conserva una via di recovery.

## Safe state non significa semplicemente spento

Lo stato sicuro dipende dall'hazard. Spegnere tutto può essere appropriato in una condizione e pericoloso in un'altra. Una montatura in posizione incompatibile, una struttura aperta o un movimento incompleto richiedono transizioni governate.

Digital StarGate distingue almeno protezione confermata, manutenzione controllata, transizione di emergenza, recovery hold, operatività autorizzata e unknown. La safety viene così descritta come macchina a stati, non come interruttore.

Ogni transizione dovrebbe dichiarare trigger, precondizioni, timeout, condizioni di abort, risultato atteso e fonti di conferma. Il fatto che un comando sia stato accettato non dimostra che lo stato sicuro sia stato raggiunto. La conferma deve provenire da sorgenti appropriate e sufficientemente recenti.

Questa distinzione è decisiva nelle operazioni remote. “Chiusura inviata” e “osservatorio protetto” sono eventi differenti. Fra i due esistono movimento, sensori, possibili ostacoli, timeout e failure.

Progettare il safe state significa progettare anche il percorso che vi conduce, il modo in cui viene confermato e le condizioni necessarie per uscirne.

## L'hazard come oggetto governato

Un hazard non è soltanto una voce in una lista di rischi. È un oggetto che attraversa identificazione, valutazione, controllo, verifica, validazione, operazione e riesame.

AP-010 richiede per ciascun hazard cause, conseguenze, gravità, probabilità, rischio iniziale, controlli, rischio residuo, owner, evidence e stato. Questa struttura collega il mondo fisico alla roadmap del cambiamento.

La pioggia durante un'acquisizione non viene trattata come generico “rischio meteo”. Motiva sensori, regole, interlock, chiusura, eventi, test e procedure di recovery. La perdita WAN motiva l'indipendenza dell'autorità locale. Una collisione potenziale motiva precondizioni fra montatura e cupola. Un override motiva scadenza, audit e post-review.

La review ARB-010 approva il framework con condizioni proprio perché il disegno è forte ma hazard owner, soglie, collision envelope, failure injection, power loss, override ed emergency drill non risultano ancora dimostrati.

Il registro hazard permette di sapere quale parte della safety è architettura, quale è controllo implementato e quale richiede ancora evidenza. Senza questa distinzione, il termine “sicuro” diventa troppo ampio per guidare una decisione.

## Security: l'identità non basta

La security del remoto inizia dall'identità attribuibile, ma non termina con il login. AP-005 separa authentication, authorization, sessione, privilegio e outcome fisico.

Una VPN crea un canale; non assegna il diritto di operare. Un'autenticazione forte dimostra chi è l'utente; non decide quale comando possa inviare. Un ruolo autorizza uno scope; non elimina la verifica dello stato. Una sessione privilegiata deve avere inizio, fine, motivo, timeout, revoca e audit. Secret e certificati devono possedere owner, scadenza, rotazione e recovery senza entrare nel repository o nei log.

Questa catena impedisce che la security venga ridotta a una porta d'ingresso. Il sistema deve governare anche ciò che accade dopo l'accesso e ciò che rimane quando l'accesso termina.

La perdita della VPN non deve disabilitare la safety locale. La perdita dell'audit store non deve concedere implicitamente un comando. La scadenza di un certificato non deve indurre una scorciatoia permanente. Un account compromesso deve poter essere revocato senza perdere la capacità locale di recovery.

La security matura non promette che nessun accesso fallirà. Progetta revoca, degrado e ripristino senza trasformare l'emergenza in un bypass invisibile.

## Dove safety e security si incontrano

Safety e security si incontrano nel modello di comando, ma pongono domande differenti.

La security chiede: il principal è autenticato? Possiede ruolo e delega? Il target e l'operazione rientrano nello scope? Le approvazioni sono complete? Il token è valido, limitato e non scaduto?

La safety chiede: lo stato fisico è noto e recente? Esistono hazard attivi? Le precondizioni sono soddisfatte? Un interlock concede il movimento? Quale risultato sicuro deve essere confermato?

L'ordine è importante. Una decisione di authorization può consentire che il comando raggiunga il punto di dispatch, ma il Safety Plane deve valutarlo ancora al momento dell'esecuzione. Il contesto può essere cambiato fra richiesta e movimento.

Nessun ruolo IAM può annullare il veto locale. Nessun dato analytics può diventare permit. Nessuna urgenza scientifica rende safe uno stato unknown. D'altra parte, la safety non deve distribuire privilegi o custodire secret: resta distinta dalla security.

Le due architetture collaborano attraverso un contratto esplicito, non attraverso un'autorità fusa.

## L'override come rischio visibile

L'override è necessario in alcune manutenzioni ed emergenze. Se viene progettato come eccezione informale, diventa il punto in cui safety e security perdono simultaneamente efficacia.

Digital StarGate richiede ruolo nominato, motivo, durata, scope, approvazione, eventi di audit, scadenza e recovery hold. Un override non può essere permanente, invisibile o capace di cancellare un interlock fisico.

Il sistema deve distinguere maintenance mode dalla normale operatività. Un apparato accessibile per intervento non è automaticamente pronto per una sessione. Il ritorno al servizio richiede checklist, verifica delle protezioni e responsabilità separata.

La review ARB-010 mantiene aperta la prova dell'override e della sua scadenza; ARB-007 mantiene aperto il break-glass. La sovrapposizione è istruttiva: un accesso emergency può essere security-compliant ma ancora safety-inadeguato, oppure viceversa.

L'eccezione deve attraversare entrambi i domini e lasciare evidence sufficiente per spiegare chi ha fatto cosa, perché e con quale stato finale.

## AI: advisory only

L'AI può riconoscere pattern, correlare eventi, riassumere una situazione e suggerire un runbook. Può aiutare a individuare dati discordanti o una condizione che richiede attenzione. Queste capacità non la trasformano in Safety Authority o principal autorizzativo.

Una raccomandazione dipende dalla qualità delle fonti e può essere errata. Un modello non percepisce direttamente il mondo fisico; interpreta rappresentazioni. Non possiede responsabilità legale o operativa. Non deve ampliare la propria authority perché una risposta appare sicura.

Digital StarGate colloca analytics e AI in fondo alla gerarchia safety e le esclude dall'approvazione dei comandi. Possono suggerire, mai autorizzare o bypassare. Qualunque futura autonomia richiederebbe decisione, hazard analysis, contratti, evidence e review dedicate; non può emergere come conseguenza accidentale di un'interfaccia più intelligente.

Questo limite non riduce il valore dell'AI. Le assegna il ruolo in cui può essere utile senza trasformare in azione fisica una correlazione non verificata.

## Lezione trasferibile

Safety e security devono essere progettate come proprietà del sistema, non aggiunte come controlli finali. Per ogni azione significativa occorre sapere:

1. quale identità e quale privilegio la richiedono;
2. quale hazard può attivare;
3. quale stato e freshness sono necessari;
4. quale autorità può negarla;
5. quale safe outcome deve essere confermato;
6. quale evidence conserva decisione ed esito;
7. come avvengono revoca, recovery e ritorno al servizio.

Il sistema è maturo quando la perdita di rete, identità, telemetria o servizio non produce un'autorizzazione implicita e non indebolisce le protezioni locali.

## Verifica per il lettore

- Safety e security possiedono authority distinte e coordinate?
- La disponibilità non prevale sulla protezione fisica?
- Unknown, stale e conflicting producono comportamenti espliciti?
- Ogni safe state ha un percorso di ingresso, conferma e uscita?
- La VPN è trattata come canale e non come permesso?
- Override e break-glass sono temporanei, auditati e collaudati?
- L'AI rimane advisory e priva di authority safety?

Se un solo controllo cerca di dimostrare contemporaneamente identità, permesso e sicurezza fisica, il sistema sta comprimendo tre decisioni differenti in una risposta troppo semplice.

## Fonti del capitolo

- `AP-005` e `ARB-007`, Identity, Access and Remote Operations Security;
- `AP-010`, Enterprise Safety Assurance Architecture;
- `SAF-CAT-001`, Safety Hazard and State Catalog;
- `ARB-010`, independent review di AP-010;
- `AP-012`, Enterprise Operations Center Architecture;
- `OPSC-CMD-001`, Command Authorization Model;
- manuale tecnico Digital StarGate, capitoli su meteo, emergenza, rete e accesso remoto.
