# Capitolo 5 - L'architettura come linguaggio comune

## La stessa parola, sistemi diversi

Quando persone con competenze differenti osservano un osservatorio remoto, vedono sistemi differenti. L'astronomo vede una notte utile, un target, una sequenza e un risultato scientifico. L'operatore vede condizioni meteo, finestre temporali, allarmi e procedure. Chi cura l'infrastruttura vede alimentazione, rete, computer e dipendenze. Chi si occupa dei dati vede sessioni, file, metadati, qualità e conservazione. Chi governa il progetto vede responsabilità, rischi, costi e priorità.

Nessuno di questi punti di vista è sbagliato. Il problema nasce quando ciascuno usa le stesse parole per indicare cose diverse oppure parole diverse per indicare la stessa cosa. “Sistema”, “piattaforma”, “operativo”, “sicuro”, “sessione” e perfino “dato” possono cambiare significato a seconda della conversazione. Finché il progetto è piccolo, l'ambiguità viene compensata dalla conoscenza reciproca. Quando cresce, diventa una fonte di decisioni incompatibili.

Digital StarGate incontra questa soglia nel passaggio dal manuale tecnico al programma enterprise. I documenti descrivono già molte parti dell'osservatorio, ma serve un modo comune per parlare delle relazioni. L'architettura assume allora la sua funzione più importante: non disegnare scatole, ma rendere possibile una conversazione verificabile sul sistema.

Un linguaggio comune non elimina le specializzazioni. Permette loro di incontrarsi senza perdere precisione.

## Il problema non è il diagramma

L'architettura viene spesso identificata con un diagramma. Il diagramma è utile quando riduce la complessità e mostra un rapporto che la prosa renderebbe faticoso. Diventa pericoloso quando suggerisce che il sistema sia esaurito dalle forme rappresentate.

Una scatola chiamata “Operations Center” non dice chi possiede lo stato mostrato, quanto è recente, che cosa accade quando manca e se l'interfaccia può inviare un comando. Una freccia fra “AI” e “Osservatorio” non chiarisce se il collegamento rappresenti lettura, suggerimento, autorizzazione o controllo fisico. Una nuvola chiamata “Data Platform” non spiega quali dati siano autorevoli, quali derivati e quali ricostruibili.

Il valore del diagramma dipende quindi dal vocabolario che lo sostiene. Per questo la baseline enterprise di Digital StarGate introduce un metamodel: una grammatica minima che definisce concetti come capability, Architecture Package, decisione, assessment, review, evidence, release, piattaforma digitale, asset scientifico e proiezione.

Il metamodel non è un dizionario ornamentale. Stabilisce ciò che può essere affermato. Se una capability descrive ciò che il sistema sa o deve saper fare, non può essere confusa con la presenza di una pagina. Se una evidence dimostra un comportamento entro un perimetro, non può essere sostituita da un'intenzione. Se il portale è un confine di presentazione, non può diventare implicitamente autorità sul dominio fisico.

La grammatica protegge il progetto dalle scorciatoie linguistiche che anticipano risultati non ancora ottenuti.

## Dalle cose alle capacità

L'elenco degli apparati è un punto di partenza naturale. Cupola, montatura, telescopio, camera, computer, router, sensori e software sono oggetti riconoscibili. L'impresa, però, non investe negli oggetti per la loro sola esistenza. Investe nella capacità di produrre risultati.

Una capability risponde a una domanda diversa: che cosa deve riuscire a fare il sistema, con quale affidabilità e sotto quali condizioni?

“Raccogliere una sessione osservativa completa” non coincide con possedere una camera. Richiede preparazione, configurazione, scelta del target, verifica delle condizioni, acquisizione, gestione delle anomalie, chiusura, conservazione e possibilità di ricostruire l'esito. “Proteggere l'osservatorio da condizioni meteo non sicure” non coincide con possedere un sensore. Richiede una politica, stati interpretabili, freshness, una decisione locale, un comportamento in assenza di dati e una prova del ritorno allo stato sicuro.

Il passaggio dalle cose alle capacità produce tre benefici.

Il primo è la neutralità tecnologica. La capacità rimane comprensibile anche quando cambia un prodotto. Il secondo è la responsabilità: una capacità può avere un owner, criteri di accettazione e rischi. Il terzo è la composizione: una sessione osservativa può dipendere da capacità di sicurezza, connettività, configurazione, acquisizione e gestione dati senza confonderle in un unico blocco.

Nel caso Digital StarGate, questa lettura consente di distinguere ciò che è documentato, ciò che è parzialmente realizzato, ciò che è approvato con condizioni e ciò che è pianificato. L'architettura non serve a colorare una mappa di avanzamento. Serve a impedire che un risultato locale venga scambiato per una capacità completa.

## Confini che rendono possibile la collaborazione

Un confine architetturale viene talvolta percepito come un ostacolo. In realtà, un buon confine riduce il numero di cose che una parte del sistema deve conoscere per collaborare con le altre.

Digital StarGate adotta una separazione concettuale fra dominio, applicazione, presentazione e infrastruttura. Il dominio custodisce stati, regole e fatti significativi dell'osservatorio. L'applicazione orchestra casi d'uso, autorizzazioni e interazioni. La presentazione rende visibile lo stato e raccoglie intenzioni. L'infrastruttura collega rete, storage, driver e servizi esterni.

Il lettore non ha bisogno di conoscere l'implementazione per cogliere il principio. Una schermata può mostrare “meteo sicuro”, ma non dovrebbe inventare il significato di sicuro. Un servizio può coordinare la richiesta di apertura, ma non dovrebbe aggirare l'interlock locale. Un adapter può parlare con un apparato, ma non dovrebbe decidere la politica operativa. Ogni responsabilità viene collocata dove può essere compresa, provata e sostituita senza trascinare con sé l'intero sistema.

Questa separazione non è soltanto software. Esiste anche nei documenti. La roadmap decide l'ordine del cambiamento; un Architecture Package governa uno scope; un ADR protegge una scelta strutturale; una review valuta; una evidence dimostra; una release aggrega ciò che è stato verificato. Mescolare queste funzioni in un unico documento produrrebbe lo stesso problema di un componente che cerca di fare tutto.

La modularità, in altre parole, è una disciplina cognitiva prima di essere una tecnica.

## Relazioni prima delle gerarchie

Un sistema enterprise non è leggibile attraverso un solo albero organizzativo. Le relazioni importanti attraversano domini differenti.

Un rischio motiva una capability. Una capability viene governata da un package. Una decisione stabilisce un confine. Un'implementazione viene sostenuta da evidence. Una review valuta la sufficienza delle prove. Una release raccoglie cambiamenti approvati. Una dashboard presenta una proiezione derivata da fonti che restano altrove.

Il metamodel Digital StarGate rende esplicite queste relazioni. Il risultato è simile a una rete di impegni: ogni affermazione importante deve poter rispondere alla domanda “da che cosa dipende e che cosa la dimostra?”.

La relazione conta più della quantità dei documenti. Dieci documenti isolati possono produrre meno governo di tre artefatti ben collegati. Un requisito senza owner non crea responsabilità. Un rischio senza controllo rimane una constatazione. Un controllo senza evidence rimane una promessa. Una capability senza confine diventa una parola elastica che assorbe qualunque iniziativa.

Nel libro questa idea è una delle basi del modello DSG-EOM: la qualità enterprise emerge dalla continuità fra scopo, mondo fisico, operazioni sicure, piattaforma digitale, dati scientifici, conoscenza e assurance. Nessun dominio può dichiararsi completo ignorando gli altri.

## Il portale non è il sistema

L'evoluzione del portale Digital StarGate rende particolarmente visibile il valore dei confini. Un portale enterprise può aggregare documentazione, roadmap, architettura, sessioni scientifiche, stato e intelligence di repository. Proprio perché è visibile e comodo, rischia di apparire come il luogo in cui risiede la verità.

L'architettura stabilisce invece che il portale è un presentation boundary. Presenta, collega e facilita l'accesso. Non sostituisce le fonti, non inventa invarianti e non acquisisce autorità safety. I dataset che alimentano alcune viste sono proiezioni ricostruibili; la loro leggibilità non li rende più autorevoli dei package, delle evidence o dei dati governati da cui derivano.

Questa separazione è essenziale per due motivi. Primo, una vista può essere temporaneamente incompleta o non aggiornata senza alterare il significato della fonte primaria. Secondo, il progetto può cambiare interfaccia senza riscrivere le regole dell'osservatorio.

Lo stesso principio vale per qualunque centro operativo. Rendere un comando disponibile su uno schermo non assegna allo schermo il diritto di eseguirlo. La catena di autorizzazione deve attraversare casi d'uso, policy, audit e precondizioni, mentre il controller locale conserva l'autorità finale sulla protezione fisica.

Una buona architettura rende visibile questa distanza fra rappresentare e governare.

## I nomi come contratti

Nel lavoro quotidiano, nominare sembra un'attività secondaria. In un sistema complesso è una forma di progettazione. Un nome stabilisce che due conversazioni parlano dello stesso oggetto e che gli attributi associati mantengono il medesimo significato.

Digital StarGate usa identificatori stabili per package, decisioni, rischi, evidence, capability e documenti. L'identificatore non serve soltanto a ordinare i file. Permette di seguire una decisione mentre attraversa roadmap, review, registro di tracciabilità e release.

La stabilità è particolarmente importante quando il sistema evolve. Rinominare retroattivamente ciò che è già stato citato rende fragile la memoria. Aggiungere una nuova relazione o estendere un concetto è spesso preferibile a riscrivere la storia. Il metamodel, infatti, può essere esteso senza rinumerare gli identificatori esistenti.

Questo approccio evita anche un errore comune: usare la maturità del nome per suggerire la maturità della capacità. Chiamare una pagina “Scientific Intelligence” non dimostra l'esistenza di una piattaforma di conoscenza completa. Il nome orienta la visione; stato, fonti ed evidence dichiarano ciò che è realmente disponibile.

I nomi sono contratti soltanto quando il progetto conserva anche il loro stato.

## L'architettura come strumento di riduzione

Il corpus Digital StarGate è ampio: manuale, roadmap, package, assessment, registri, piattaforme e procedure. Una lettura superficiale potrebbe concludere che l'approccio enterprise consista nell'aumentare il numero degli artefatti. La funzione dell'architettura è in realtà opposta: ridurre ciò che ogni decisione deve tenere simultaneamente in mente.

Una mappa delle fonti riduce la ricerca. Un confine riduce le dipendenze. Una capability riduce l'attenzione agli apparati specifici. Un registro riduce la ricostruzione storica. Un criterio di evidence riduce le discussioni su cosa significhi “pronto”. Una gerarchia di authority riduce l'ambiguità durante un'anomalia.

L'artefatto è giustificato quando riduce un costo cognitivo o un rischio reale. Se una nuova classificazione non cambia alcuna decisione, può essere evitata. Se due registri conservano la stessa responsabilità, devono essere consolidati. Se un diagramma richiede più spiegazioni della relazione che rappresenta, non sta svolgendo il proprio lavoro.

Questa proporzionalità protegge il progetto dalla burocrazia. L'architettura utile non massimizza la documentazione; massimizza la comprensibilità delle decisioni importanti.

## Una scena di convergenza

Immaginiamo una nuova esigenza: consentire a un operatore di comprendere perché una sessione non può iniziare. Senza linguaggio comune, la richiesta può diventare una nuova schermata con un indicatore rosso. Con il linguaggio architetturale, la conversazione cambia.

Quale capability viene migliorata? Quali stati fisici contribuiscono alla decisione? Qual è la fonte autorevole per ciascuno stato? Quanto deve essere recente? Chi determina che una condizione è bloccante? La schermata presenta una decisione o la prende? Che cosa accade quando una dipendenza non risponde? Quale evento deve essere conservato per spiegare il diniego? Quale evidence dimostra il comportamento?

Le domande non rallentano lo sviluppo. Evitano di costruire una risposta visivamente convincente ma operativamente ambigua. Consentono inoltre a astronomo, operatore, architect e responsabile safety di lavorare sulla stessa esigenza senza rinunciare al proprio punto di vista.

Questa è l'architettura come linguaggio comune: un modo di trasformare una richiesta locale in una decisione coerente con l'intero sistema.

## Lezione trasferibile

Un'organizzazione può iniziare senza adottare un framework complesso. È sufficiente costruire un vocabolario condiviso attorno a poche domande:

1. Quale risultato chiamiamo capability?
2. Quale parte del sistema possiede le regole?
3. Quale parte presenta soltanto lo stato?
4. Quale fonte è autorevole?
5. Quale relazione collega decisione, cambiamento e prova?
6. Quale condizione impedisce di dichiarare una capacità pronta?

Le risposte devono essere comprensibili a più ruoli, non soltanto agli specialisti. Se una definizione non cambia il modo di decidere, probabilmente è troppo astratta. Se un confine non chiarisce una responsabilità, probabilmente è tracciato nel punto sbagliato.

Il linguaggio comune è riuscito quando riduce le traduzioni, rende visibili i conflitti e consente di discutere il sistema senza confondere ciò che appare con ciò che governa.

## Verifica per il lettore

- Nella tua organizzazione “operativo” ha un significato condiviso e verificabile?
- Le capability sono distinte dai prodotti e dalle interfacce che le realizzano?
- Esiste un confine chiaro fra presentazione, decisione e controllo fisico?
- Ogni relazione critica può essere seguita da esigenza a evidence?
- I nomi restano stabili mentre lo stato viene aggiornato?
- I documenti riducono il costo cognitivo oppure lo aumentano?

Se due ruoli rispondono in modo incompatibile alla stessa domanda, non serve ancora un nuovo strumento. Serve prima un linguaggio comune.

## Fonti del capitolo

- `DSG-EAM-001`, Enterprise Architecture Model;
- `AP-001`, Enterprise Metamodel and Repository Information Architecture;
- Digital StarGate Enterprise Metamodel;
- Architecture Traceability Register;
- `ARB-003`, independent review di AP-001;
- `ABC-001`, Architecture Baseline Certificate;
- Enterprise Architecture Context;
- Repository Knowledge Map;
- `AI_BOOTSTRAP.md`.
