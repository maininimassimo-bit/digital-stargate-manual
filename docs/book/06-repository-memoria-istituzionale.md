# Capitolo 6 - Il repository come memoria istituzionale

## Ricordare non basta

Ogni progetto possiede una memoria, anche quando non l'ha progettata. Può vivere nella testa di una persona, nelle cartelle di un computer, in messaggi, note, nomi di file, cronologie di modifiche e consuetudini mai scritte. Questa memoria informale funziona finché le persone ricordano il contesto e restano disponibili. Diventa fragile quando il lavoro attraversa settimane, strumenti, collaboratori e decisioni collegate.

In un osservatorio remoto la perdita di contesto non è soltanto un disagio amministrativo. Può rendere incerta una configurazione, nascondere una condizione safety, interrompere il lineage di un'immagine o far ripetere un cambiamento già scartato. Più il sistema diventa automatizzato, più una memoria affidabile diventa parte della sua capacità operativa.

Digital StarGate affronta questo problema trasformando il repository da contenitore di documenti a memoria istituzionale. L'espressione non significa che il repository ricordi tutto. Significa che conserva abbastanza struttura da permettere a una persona o a un assistente di ricostruire lo stato corrente senza dipendere dalla continuità della conversazione.

La differenza è profonda. Ricordare significa avere ancora in mente una risposta. Ricostruire significa poter mostrare da quali fonti quella risposta deriva.

## Dal deposito alla fonte autorevole

Un deposito raccoglie file. Una fonte autorevole assegna loro ruoli, precedenze e regole di aggiornamento.

Se un repository contiene una roadmap, una dashboard, una release note e un assessment, può accadere che descrivano lo stesso oggetto in momenti differenti. Senza una gerarchia, il lettore tende a fidarsi del documento più recente, più visibile o più convincente. Nessuno di questi criteri garantisce che sia quello corretto.

La baseline Digital StarGate dichiara quindi che il repository GitHub è la fonte autorevole e specifica l'ordine con cui leggere le fonti al suo interno. Package, ADR, capability e standard approvati precedono assessment ed evidence; la roadmap autorevole ordina le evoluzioni; release e commit dimostrano ciò che è stato pubblicato; contratti versionati preservano gli scambi; dataset e dashboard restano proiezioni; il Project Governance Center orienta senza sostituire gli artefatti primari.

La gerarchia non afferma che un documento “alto” sia sempre più nuovo o più dettagliato. Stabilisce quale tipo di artefatto possiede una determinata affermazione. Un package può definire il disegno, ma una evidence descrive l'esito di una prova. Una roadmap può assegnare un orizzonte, ma un commit dimostra la presenza di una modifica. Una dashboard può facilitare la lettura, ma non corregge silenziosamente la fonte da cui dovrebbe derivare.

La memoria istituzionale nasce quando il progetto sa non soltanto dove cercare, ma anche come risolvere un conflitto.

## Una mappa per non confondere il territorio

Con l'aumento dei contenuti, il problema non è più l'assenza di informazioni. È la difficoltà di sapere quale informazione serve.

La Repository Knowledge Map di Digital StarGate organizza il patrimonio in quattro prodotti correlati: manuale tecnico dell'osservatorio, repository di Enterprise Architecture, Enterprise Portal e Developer Foundation. La distinzione impedisce che un singolo punto di vista diventi il progetto intero.

Il manuale spiega apparati, procedure, manutenzione e sicurezza operativa. L'architettura governa capability, confini, decisioni, rischi ed evidence. Il portale presenta e collega. La foundation contiene contratti, componenti e strumenti di validazione. Ogni prodotto contribuisce alla memoria, ma nessuno può sostituire gli altri.

La mappa aggiunge un secondo livello: indica i domini, gli artefatti principali e le regole di prevalenza. Non prova il contenuto di ogni documento; riduce il tempo necessario per trovare la fonte che può farlo.

Questa è una proprietà importante della memoria istituzionale. Non deve contenere una copia di tutto, perché le copie divergono. Deve contenere percorsi affidabili verso ciò che conta. Una buona mappa non replica il territorio: conserva orientamento, confini e punti di ingresso.

## BootAI come protocollo di ripresa

Nel percorso Digital StarGate, `AI_BOOTSTRAP.md` diventa il punto di ingresso obbligatorio per una nuova sessione di lavoro, per un collaboratore e per un assistente AI. La sua funzione non è fornire un riassunto definitivo del progetto. È prescrivere un metodo di ripresa.

Il protocollo chiede di verificare repository, branch, commit, file e workflow; indica una sequenza di lettura; distingue le fonti primarie dalle proiezioni; elenca principi che non possono essere negoziati. Richiede inoltre che ogni intervento riporti file modificati, commit, validazioni, limiti, rischi residui e prossimo passo.

Questa struttura affronta un problema tipico dell'AI generativa: la continuità apparente. Un assistente può produrre una risposta fluida anche quando il proprio contesto è incompleto o superato. BootAI sostituisce la fiducia nella fluidità con una disciplina di verifica. L'AI non deve “sentire” di conoscere il progetto; deve dimostrare di aver ricostruito la baseline necessaria.

Il principio vale anche per le persone. Una riunione ricordata non è una decisione registrata. Una convinzione condivisa non è una baseline. Un file visto settimane prima non è necessariamente lo stato corrente. Il protocollo rende accettabile dire “non lo so ancora” e indica come trasformare l'incertezza in una risposta verificabile.

BootAI è quindi interpretabile come continuità cognitiva: non una memoria che conserva ogni pensiero, ma un sistema che permette di riattivare il contesto con un costo prevedibile.

## Memoria, stato e storia

Una memoria di progetto deve rispondere a due domande differenti: qual è lo stato corrente e come ci siamo arrivati?

Lo stato corrente serve per agire. Deve indicare la baseline autorevole, le condizioni aperte, il lavoro pronto e i vincoli attivi. La storia serve per comprendere. Deve conservare decisioni, alternative, sostituzioni e motivazioni senza obbligare il presente a ripetere ogni discussione.

Confondere le due funzioni produce errori opposti. Se il repository conserva soltanto lo stato, una decisione può apparire arbitraria e venire riaperta senza nuovi elementi. Se conserva soltanto la storia, il collaboratore deve attraversare tutto il passato per capire cosa fare oggi.

Digital StarGate separa i ruoli. L'Enterprise Architecture Context orienta la ripresa. Il Backlog ordina il lavoro pianificato. Il Technical Debt registra compromessi con costo futuro. Il Decision Log conserva scelte operative reversibili. Gli ADR proteggono scelte strutturali. Le roadmap descrivono l'ordine del cambiamento. Commit e release conservano la sequenza pubblicata.

Questa separazione crea una memoria a più velocità. Il contesto può essere aggiornato quando cambia una milestone; una decisione strutturale cambia più raramente; il backlog evolve spesso; una evidence rimane immutabile nel proprio perimetro. Ogni artefatto viene mantenuto secondo il ritmo della responsabilità che possiede.

## Il valore dei commit

Un commit è una registrazione precisa di una modifica al repository. Mostra quali file sono cambiati, in quale sequenza e con quale messaggio. Questa precisione lo rende una fonte preziosa per ricostruire l'evoluzione verificabile di Digital StarGate.

Il commit, tuttavia, ha limiti chiari. Dimostra che un contenuto è stato registrato; non dimostra da solo che sia stato distribuito, usato, accettato o eseguito sull'impianto fisico. Non conserva necessariamente la motivazione completa. Non trasforma un disegno in capacità runtime.

La cronologia editoriale del progetto usa quindi i commit con prudenza. Può affermare che il 13 luglio la struttura Docs-as-Code e un insieme di capitoli sono entrati nel repository. Può seguire l'aggiunta di report, pipeline, architettura e package. Non può dedurre da quelle date quando sia nato l'osservatorio fisico o quale esperienza personale abbia motivato ogni scelta.

Questo limite aumenta, non diminuisce, il valore della fonte. Una memoria istituzionale affidabile dichiara ciò che una registrazione dimostra e ciò che lascia aperto. Le testimonianze dell'autore potranno completare la storia, ma resteranno distinguibili dalle evidenze tecniche.

## Proiezioni leggibili, fonti preservate

Quando la quantità di informazioni cresce, il progetto crea viste più facili da esplorare: dashboard, cataloghi, centri tematici, riepiloghi e indicatori. Queste proiezioni sono essenziali per l'uso quotidiano. Il rischio nasce quando la comodità viene confusa con authority.

Digital StarGate tratta i dataset del portale come proiezioni ricostruibili. La scelta produce un rapporto sano fra fonte e interfaccia. La fonte conserva il significato; la proiezione ottimizza una domanda. Se cambia il bisogno informativo, la vista può essere rigenerata senza modificare retroattivamente l'origine.

Lo stesso vale per i dati scientifici. Un catalogo può facilitare la ricerca delle sessioni, mentre manifest, checksum e provenance conservano l'identità e la storia degli asset. Una visualizzazione può presentare un KPI, mentre il dato governato mantiene formula, grain, owner, freshness e validità.

La memoria istituzionale non rifiuta le sintesi. Chiede che ogni sintesi possa indicare da dove proviene, quando è stata prodotta e quali limiti possiede.

## Onboarding come prova dell'architettura

Un sistema di conoscenza viene spesso valutato da chi lo ha costruito. Questa prospettiva è indulgente: l'autore sa già dove sono le eccezioni e completa mentalmente ciò che manca. Un test più severo consiste nell'osservare una persona nuova.

Quanto tempo impiega a capire che cosa sia Digital StarGate? Riesce a distinguere il manuale dal portale e dalle piattaforme future? Trova la roadmap autorevole? Comprende quali capability siano parziali e quali soltanto pianificate? Sa quali principi non può violare? Può proporre una modifica senza duplicare una responsabilità esistente?

BootAI, Context e Knowledge Map trasformano l'onboarding in una proprietà progettata. Non eliminano il bisogno di apprendimento, ma rendono esplicito il percorso. Un nuovo collaboratore non riceve soltanto una lista di file: riceve un ordine di lettura e regole per interpretare ciò che trova.

La qualità dell'onboarding misura indirettamente la qualità dell'architettura. Se per agire in sicurezza è indispensabile una spiegazione orale non registrata, esiste una dipendenza nascosta. Se il nuovo arrivato trova due owner per la stessa decisione, esiste una sovrapposizione. Se non riesce a distinguere una visione da un runtime, la memoria non conserva abbastanza stato.

Ogni difficoltà di onboarding è un sensore della struttura.

## L'AI come lettore, non come fonte

L'introduzione dell'AI cambia la scala con cui la memoria può essere interrogata. Un assistente può cercare relazioni, confrontare documenti, riassumere condizioni aperte e preparare aggiornamenti coerenti. Questa capacità rende ancora più importante stabilire la fonte dell'autorità.

Un testo generato dall'AI può essere utile, ma non diventa vero perché è plausibile. Una correlazione può suggerire un problema, ma non sostituisce una evidence. Un riassunto può accelerare una review, ma deve permettere al revisore di raggiungere i riferimenti primari.

La baseline Digital StarGate colloca quindi l'AI nel ruolo di lettore disciplinato e collaboratore governato. Può usare il repository, applicare la gerarchia delle fonti, proporre modifiche entro boundary approvati e lasciare traccia del proprio intervento. Non può promuovere una proiezione a verità, dichiarare test non eseguiti o oltrepassare i confini safety.

Questa impostazione evita due estremi. L'AI non viene trattata come un semplice motore di testo privo di responsabilità sul metodo. Ma non viene nemmeno trasformata in una nuova fonte primaria. La sua affidabilità dipende dalla capacità di citare, verificare e rispettare il sistema di conoscenza che la precede.

## Mantenere viva la memoria

Una memoria istituzionale può diventare obsoleta. Accade quando i documenti di orientamento non vengono aggiornati, le decisioni restano scollegate, il backlog non riflette le dipendenze o le proiezioni continuano a mostrare stati superati.

Per questo Digital StarGate collega la manutenzione della memoria al processo di delivery. Una milestone non termina con la sola modifica. Richiede validazione, commit, verifica del workflow e aggiornamento degli artefatti di contesto quando cambia una regola stabile, una condizione o una priorità.

Il requisito è semplice da formulare: ogni intervento dovrebbe lasciare il progetto almeno altrettanto comprensibile di come lo ha trovato.

In pratica, ciò significa evitare documenti duplicati, aggiornare i riferimenti, registrare il debito, non nascondere condizioni aperte e mantenere separati i registri. Significa anche ritirare o marcare come superate le rappresentazioni che non devono più guidare il lavoro.

La memoria non è un archivio immobile. È una capacità di conservare identità mentre lo stato cambia.

## Lezione trasferibile

Per trasformare un repository in memoria istituzionale non occorre iniziare da una piattaforma sofisticata. Servono cinque elementi minimi:

1. una dichiarazione della fonte autorevole;
2. una gerarchia per risolvere le divergenze;
3. una mappa che orienti verso le fonti senza duplicarle;
4. registri distinti per stato, lavoro, decisioni e debito;
5. un protocollo di onboarding e ripresa verificabile.

Il sistema deve essere progettato per la ricostruzione. Un collaboratore dovrebbe poter determinare quale baseline usa, quali limiti restano aperti, perché una decisione esiste e quale sarà il prossimo passo. Se la risposta dipende da una conversazione privata, la memoria è ancora personale.

La misura del successo non è il numero di file, ma la riduzione del tempo e dell'incertezza necessari per riprendere il lavoro correttamente.

## Verifica per il lettore

- Una persona nuova sa quale fonte prevale quando due viste divergono?
- Stato corrente e storia delle decisioni sono separati ma collegati?
- Le dashboard dichiarano origine, freshness e limiti?
- Le modifiche lasciano una traccia sufficiente senza fingere deployment o acceptance?
- L'AI può raggiungere le fonti primarie di ogni affermazione importante?
- Il protocollo di ripresa funziona anche dopo una lunga interruzione?

Se il progetto può continuare soltanto perché qualcuno “si ricorda come stanno le cose”, possiede esperienza, ma non ancora memoria istituzionale.

## Fonti del capitolo

- `AI_BOOTSTRAP.md`;
- Enterprise Architecture Context `DSG-CTX-001`;
- Repository Knowledge Map `DSG-GOV-KM-001`;
- Project Governance Center;
- Decision Log `DSG-GOV-DEC-001`;
- Development Workflow e Release Playbook;
- Architecture Traceability Register;
- cronologia verificata del progetto Digital StarGate.
