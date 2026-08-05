# Capitolo 8 - Autorità, responsabilità e separazione dei ruoli

## La domanda che precede il comando

In un sistema remoto, la domanda più importante non è “possiamo farlo?”. È “chi ha l'autorità per decidere che debba essere fatto, in queste condizioni?”.

La tecnologia rende molte azioni disponibili. Un'interfaccia può mostrare un pulsante, una rete può raggiungere un computer, un account può possedere privilegi elevati e un'automazione può conoscere la sequenza corretta. Nessuna di queste condizioni, presa da sola, stabilisce che l'azione sia legittima.

Digital StarGate incontra questa distinzione nel passaggio dal controllo remoto alla governance delle operazioni. La raggiungibilità non equivale al permesso. L'autenticazione non equivale all'autorizzazione. L'autorizzazione operativa non equivale al consenso safety. L'esecuzione non equivale alla conferma dell'esito fisico.

Quattro passaggi che, in un impianto semplice, possono essere affidati alla stessa persona diventano responsabilità separabili. L'operatore esprime un'intenzione. Il sistema verifica identità, ruolo, contesto e stato. Un approvatore interviene quando il rischio lo richiede. La Safety Authority locale conserva la facoltà di negare o arrestare.

Il comando è quindi l'ultimo tratto visibile di una decisione più ampia.

## Autorità non significa privilegio tecnico

Un account amministrativo può modificare configurazioni, creare utenti o intervenire sull'infrastruttura. Questo potere tecnico non lo rende automaticamente competente a dichiarare sicura l'apertura della cupola. Allo stesso modo, chi possiede l'esperienza astronomica per condurre una sessione non acquisisce implicitamente il diritto di cambiare policy di rete o disattivare un controllo.

Digital StarGate distingue classi di privilegio: lettura, operatività, configurazione, amministrazione, override ed emergenza. La distinzione protegge sia il sistema sia le persone. Un ruolo deve ricevere soltanto le capacità necessarie allo scopo e per il tempo necessario.

Questa separazione evita due concentrazioni pericolose. La prima è tecnica: lo stesso account può vedere, modificare e cancellare senza una barriera. La seconda è decisionale: la stessa persona può richiedere, approvare, eseguire e certificare l'esito di un'azione ad alto impatto.

Il principio enterprise non presume che ogni organizzazione disponga di molti individui. Chiede però che le responsabilità restino distinguibili anche quando una persona ricopre più ruoli. Il conflitto deve essere dichiarato, il perimetro limitato e la verifica indipendente introdotta dove il rischio non consente autocontrollo.

L'autorità è una relazione governata fra persona, ruolo, azione, contesto e tempo. Non è una proprietà permanente dell'account più potente.

## Una catena di decisioni

Il modello del Digital StarGate Operations Center separa sei piani: presentazione, coordinamento operativo, autorizzazione dei comandi, integrazione, safety ed evidence. La separazione permette di seguire una richiesta senza attribuire al punto di ingresso un'autorità che non possiede.

Una console presenta lo stato e raccoglie l'intenzione. Il coordinamento collega l'azione a una sessione, un incidente, una manutenzione o un altro motivo. Il piano di autorizzazione verifica identità, ruolo, delega, rischio, freshness, lock e approvazioni. L'integrazione trasporta la richiesta attraverso contratti governati. La safety decide se le condizioni fisiche consentono l'esecuzione. L'evidence registra decisione, transizioni ed esito.

Un comando può quindi essere corretto in un piano e negato nel successivo. Un operatore può essere autorizzato a richiedere la chiusura, ma il sistema deve comunque verificare la geometria compatibile. Un amministratore può accedere a una configurazione, ma non può usare quel privilegio per aggirare un interlock. Una sequenza può essere stata approvata, ma un dato meteo stale deve impedirne l'avvio.

La negazione non indica necessariamente un malfunzionamento. È spesso la prova che le autorità stanno collaborando senza confondersi.

## Ruoli che descrivono responsabilità

I documenti Digital StarGate distinguono ruoli operativi, tecnici, architetturali e di assurance. L'Operator conduce attività consentite. Il Maintainer interviene sugli asset entro una finestra governata. L'Incident Coordinator coordina il ripristino senza acquisire automaticamente privilegi tecnici. La Security Authority governa accessi privilegiati e break-glass. La Safety Authority decide permit, deny, stop e safe state. L'Auditor legge le evidenze senza poter comandare.

Altri ruoli presidiano l'evoluzione: il Project Owner sostiene il programma e accetta rischi entro il proprio mandato; il Chief Architect mantiene coerenza e confini; l'Architecture Review Board valuta in modo indipendente; il Documentation Governor preserva naming, navigazione e tracciabilità.

L'elenco non deve essere interpretato come organigramma obbligatorio. È una mappa delle responsabilità che non dovrebbero scomparire. In una piccola organizzazione alcune persone possono indossare più cappelli, ma il sistema deve ancora sapere quale cappello è attivo e quali combinazioni richiedono mitigazioni.

Una matrice RACI aiuta a distinguere chi esegue, chi risponde del risultato, chi viene consultato e chi informato. Non risolve da sola i conflitti. Rende però visibile quando due ruoli risultano accountable per la stessa decisione o quando nessuno lo è.

La responsabilità diventa concreta quando possiede un nome, uno scope, una durata e un criterio di sostituzione.

## Four-eyes: il secondo sguardo

Il principio four-eyes richiede che determinate azioni non dipendano dalla sola valutazione di chi le richiede o le esegue. Un secondo soggetto verifica contesto, rischio e condizioni prima dell'autorizzazione.

Digital StarGate lo collega soprattutto alle classi di comando safety-relevant ed emergency. Il requester e l'approver devono essere distinti; chi modifica una policy non approva la stessa modifica; chi esegue manutenzione non certifica da solo il ritorno in servizio; l'auditor non possiede privilegi di dispatch.

Il valore del secondo sguardo non è soltanto trovare errori tecnici. Riduce la pressione cognitiva durante un'anomalia, contrasta l'abitudine e rende esplicita l'accettazione del rischio.

Il caso ARB-012 mostra anche il limite organizzativo. Le regole simulate possono impedire a una singola identità di auto-approvare un comando critico. Ma se i ruoli reali restano concentrati in una sola persona, la segregazione organizzativa non è dimostrata. Il controllo logico funziona nel test; la capacità operativa resta bloccata.

Questa distinzione impedisce di dichiarare risolto un problema umano attraverso una regola software. Il four-eyes diventa reale soltanto quando esistono identità distinte, formazione, deleghe, sostituti e access review verificabili.

## La delega non trasferisce tutto

La delega permette a un sistema piccolo di continuare a operare quando il responsabile principale non è disponibile. Senza regole, può diventare un'autorizzazione generica difficile da revocare.

Una delega governata dichiara delegante, delegato, ruolo, azioni e target consentiti, validità, motivo, approvatore e stato di revoca. Per le operazioni ad alto rischio non può essere permanente o aperta.

La delega trasferisce uno scope, non l'intera autorità della persona. Un operatore delegato per una sessione non diventa amministratore. Un maintainer autorizzato su un apparato non acquisisce il potere di approvare il proprio return-to-service. Un servizio automatico può eseguire workflow pre-autorizzati, ma non riceve la facoltà di ampliare da solo il proprio mandato.

Questo principio è decisivo anche per l'AI. Un assistente può ricevere autonomia per analizzare il repository, preparare documenti, applicare modifiche previste e verificare workflow. La delega non lo rende accountable, Safety Authority o approvatore di un cambiamento che modifica boundary, contratti o rischio fisico.

L'autonomia utile è sempre descrivibile come una delega limitata e revocabile.

## Break-glass senza scorciatoie permanenti

Le emergenze richiedono talvolta accessi o azioni che non appartengono al percorso ordinario. Il modello break-glass offre una via eccezionale, ma proprio per questo deve essere più visibile, non meno governata.

Digital StarGate richiede identità nominata, motivazione, scope, durata, registrazione rafforzata, revoca e post-review. L'eccezione non può diventare un account condiviso usato per comodità. Non può annullare le protezioni locali. Non deve sopravvivere oltre la condizione che l'ha resa necessaria.

La sicurezza enterprise riconosce un paradosso: una procedura di emergenza troppo rigida può impedire il recovery; una procedura troppo facile può trasformarsi nel percorso normale. La soluzione non è eliminare l'eccezione, ma progettare la sua apertura e la sua chiusura.

AP-005 descrive questa architettura, mentre la review ARB-007 mantiene aperte le condizioni operative: custodia, approvazioni, durata, revoca, rotazione ed esercitazione non risultavano ancora dimostrate. Il modello è approvato; il break-glass runtime non lo è.

Un'eccezione sicura lascia una traccia più forte dell'operazione ordinaria e obbliga il sistema a imparare dall'evento.

## L'operatore e l'automazione

Automatizzare una sequenza sposta il punto in cui interviene la responsabilità. L'operatore non esegue più ogni passo, ma decide quando la sequenza può iniziare, controlla le condizioni e interpreta le eccezioni. Il servizio automatico esegue soltanto ciò che è stato pre-autorizzato.

Questo rapporto richiede confini chiari. L'automazione non deve usare un errore come occasione per acquisire più privilegi. Non può interpretare l'assenza di risposta come approvazione. Non deve ripetere alla cieca un comando dal risultato incerto. Un retry è ammesso soltanto quando l'operazione è progettata per essere idempotente e le condizioni restano valide.

L'operatore, a sua volta, non può trattare l'automazione come un soggetto responsabile. Se una sequenza è stata configurata male o avviata fuori condizioni, dire “lo ha fatto il sistema” non chiude la catena di accountability.

Nel modello Digital StarGate, AI, dashboard e automazioni non possono essere accountable in una matrice RACI. Possono proporre, presentare ed eseguire entro mandato. La responsabilità rimane assegnata a ruoli umani e autorità istituzionali.

## Stato, freshness e diritto di agire

L'autorità non è determinata soltanto dall'identità. Dipende dallo stato osservato e dalla sua qualità.

Un operatore correttamente autenticato può non avere il diritto di aprire se il meteo è stale. Un approvatore distinto può non autorizzare una manutenzione se esiste un lock. Una delega valida può essere insufficiente se la finestra temporale è scaduta. Il comando deve essere valutato nel momento dell'esecuzione, non soltanto quando è stato richiesto.

Questa logica rende l'autorizzazione dinamica. Identità, ruolo, target, operazione, canale, assurance della sessione, stato, approvazioni, scadenza e motivo partecipano alla decisione. Il primo controllo fallito produce un diniego o una richiesta esplicita di rimedio.

La mancanza di risposta non vale come approvazione. Lo stato unknown non vale come safe. Un token valido non vale come consenso permanente. Ogni diritto di agire ha un perimetro e un tempo.

Il sistema diventa così capace di spiegare non soltanto chi ha agito, ma perché l'azione era consentita in quel momento.

## Lezione trasferibile

Progettare l'autorità richiede di separare almeno cinque domande:

1. Chi può formulare la richiesta?
2. Chi deve approvarla?
3. Quale sistema può eseguirla?
4. Quale autorità può negarla o arrestarla?
5. Chi verifica l'esito e accetta il ritorno al servizio?

Per le azioni ad alto rischio, la stessa persona o componente non dovrebbe possedere tutte le risposte. Quando la dimensione dell'organizzazione impone sovrapposizioni, queste devono essere dichiarate e compensate con limiti, scadenze, evidence o review indipendente.

Il controllo non nasce dal moltiplicare i ruoli sulla carta. Nasce dal collegare ogni responsabilità a identità, scope, decisione ed evidenza.

## Verifica per il lettore

- La raggiungibilità remota è chiaramente distinta dal permesso operativo?
- Gli account amministrativi sono separati dai ruoli di operazione e safety?
- Le azioni critiche impediscono l'auto-approvazione?
- Le deleghe dichiarano scope, durata e revoca?
- Il break-glass viene esercitato e riesaminato?
- L'automazione opera entro workflow pre-autorizzati senza diventare accountable?
- Il ritorno in servizio richiede una responsabilità distinta dall'esecuzione della manutenzione?

Se il soggetto più privilegiato è anche l'unica fonte di autorizzazione, esecuzione e verifica, il sistema possiede potere ma non ancora separazione dei ruoli.

## Fonti del capitolo

- `AP-005`, Identity, Access and Remote Operations Security Architecture;
- `ARB-007`, independent review di AP-005;
- `AP-012`, Enterprise Operations Center Architecture;
- `OPSC-CMD-001`, Command Authorization Model;
- `OPSC-RACI-001`, Operations Responsibility Matrix;
- `ARB-012-FRR-001`, Final Independent Re-Review;
- Enterprise Architecture Context e `AI_BOOTSTRAP.md`.
