# Capitolo 3 - Il modello DSG-EOM

## Un modello nato dal percorso

Il Digital StarGate Enterprise Observatory Model, `DSG-EOM`, è la sintesi interpretativa proposta da questo libro. Non sostituisce la Master Roadmap, gli Architecture Package o gli ADR. Serve a rendere trasferibile il percorso: mostra quali dimensioni devono rimanere coerenti quando un osservatorio remoto evolve da impianto tecnico a piattaforma scientifica governata.

Il modello non nasce da un disegno teorico applicato a posteriori. Nasce osservando una sequenza reale:

- un manuale tecnico rende esplicito il sistema fisico e operativo;
- una roadmap distingue presente, transizione e target;
- l'Enterprise Architecture organizza domini, capability e responsabilità;
- safety, security e authority diventano vincoli strutturali;
- dati e immagini vengono trattati come patrimonio scientifico;
- review ed evidence separano il disegno dalla capacità dimostrata;
- il portale rende leggibile la piattaforma senza acquisire autorità sugli apparati;
- BootAI trasforma il repository in memoria ricostruibile;
- l'AI entra come capacità governata, non come livello sovrano.

Il DSG-EOM conserva questa direzione. Si legge dall'interno verso l'esterno e attraverso tre cicli.

## Il centro: autorità sicura

Al centro del modello non si trova la tecnologia più avanzata. Si trova l'autorità sicura.

L'autorità sicura è la combinazione di responsabilità umana, controller locale, interlock e regole che determinano chi può fare cosa, in quali condizioni e con quale possibilità di arresto. È il nucleo che deve continuare a proteggere l'impianto anche quando rete, portale, analytics o AI non sono disponibili.

Questo centro impone cinque invarianti:

1. la safety prevale sulla continuità;
2. uno stato sconosciuto o non aggiornato non autorizza un'azione rischiosa;
3. il portale non comanda direttamente un apparato;
4. l'automazione opera entro precondizioni e stop condition;
5. l'AI non può ampliare la propria authority attraverso una raccomandazione.

La centralità dell'autorità evita un errore comune: disegnare il sistema a partire dall'interfaccia più visibile. Nel DSG-EOM la dashboard è lontana dal centro quanto basta per essere utile senza diventare sovrana.

## Dominio 1 - Purpose and Governance

Ogni sistema enterprise deve sapere perché esiste e chi può cambiarlo.

Questo dominio comprende visione, missione, ownership, roadmap, processi decisionali, registri, release e change management. Nel caso Digital StarGate è rappresentato da `DSG-MR-001`, dal Project Governance Center, dalla roadmap `AMP-002`, dagli ADR e dai registri.

La governance non descrive soltanto chi approva. Stabilisce la grammatica del cambiamento:

- quali documenti sono autorevoli;
- come nasce una decisione;
- come viene registrato un rischio;
- come si distingue una correzione da una variazione architetturale;
- quali condizioni consentono una release;
- come una capacità viene ritirata o sostituita.

Senza questo dominio, ogni evoluzione ricomincia da una discussione. Con questo dominio, il progetto può mantenere una direzione anche quando cambiano strumenti, collaboratori e priorità.

**Domanda di controllo:** l'organizzazione può spiegare perché una capacità esiste e quale decisione ne ha autorizzato la forma corrente?

## Dominio 2 - Physical Observatory

Questo dominio comprende ciò che occupa spazio, consuma energia, subisce l'ambiente e può danneggiarsi: struttura, cupola o tetto, alimentazione, rete di campo, computer, montatura, ottiche, camere, sensori e collegamenti.

Nel modello non è uno strato “basso” da nascondere dietro il software. È il luogo nel quale le ipotesi digitali vengono messe alla prova.

Un progetto maturo conosce almeno:

- identità e configurazione degli asset;
- dipendenze fisiche ed elettriche;
- limiti ambientali;
- stati sicuri;
- modalità di manutenzione e recovery;
- obsolescenza e parti critiche;
- differenze tra stato misurato, inferito e dichiarato.

La qualità dell'AI o dell'automazione non può superare la qualità con cui questo dominio viene osservato e rappresentato.

**Domanda di controllo:** quale condizione fisica potrebbe rendere pericolosa una decisione digitalmente plausibile?

## Dominio 3 - Safe Operations

Le operazioni collegano scopo e realtà. Comprendono preparazione, avvio, acquisizione, sospensione, chiusura, emergenza, manutenzione, incident management e ritorno allo stato normale.

Il termine “safe” è intenzionale. L'efficienza viene dopo la capacità di riconoscere e mantenere condizioni accettabili.

Nel caso Digital StarGate, SOP, runbook, authority model, stato meteo, allarmi ed Enterprise Operations Center convergono in questo dominio. La baseline read-only del portale mostra un principio utile: prima di concedere potere di comando, occorre dimostrare qualità dello stato, autorizzazione, audit, four-eyes e comportamento degradato.

Un'operazione governata possiede:

- un trigger;
- un responsabile;
- precondizioni verificabili;
- una sequenza comprensibile;
- criteri di successo;
- stop condition;
- evidenze;
- una via di recovery.

**Domanda di controllo:** quando una dipendenza diventa incerta, il sistema sa fermarsi in modo comprensibile?

## Dominio 4 - Digital Platform

La piattaforma digitale integra servizi, contratti, osservabilità, portale, analytics e automazioni. Il suo compito non è sostituire il sistema fisico, ma renderlo leggibile e coordinabile.

Digital StarGate mostra una progressione da MkDocs come manuale a Enterprise Portal con centri tematici, cataloghi, roadmap, intelligence e mission control. In parallelo, la Developer Foundation introduce boundary applicativi e contratti.

Il DSG-EOM richiede che ogni componente digitale dichiari la propria responsabilità. Il Navigation Manager gestisce la navigazione; il Theme Manager gestisce il tema; lo Scientific Data Engine fornisce accesso condiviso ai dati scientifici. Questa separazione evita che un componente cresca fino a possedere comportamenti non correlati.

Principi del dominio:

- responsabilità singola;
- contratti espliciti;
- proiezioni distinguibili dalle fonti;
- inizializzazione idempotente;
- osservabilità del comportamento;
- degrado controllato;
- nessun accoppiamento diretto tra presentazione e apparati.

**Domanda di controllo:** se un componente digitale scompare, è chiaro quale capacità viene persa e quale autorità rimane?

## Dominio 5 - Scientific Data

Un osservatorio produce file, ma il patrimonio scientifico è più ampio dei file. Comprende sessioni, target, strumenti, parametri, condizioni, qualità, trasformazioni, provenance e relazioni.

AP-013 rende concreto questo passaggio. L'inventario delle sorgenti, il modello DSDM, i manifest, gli hash e il trasferimento `COPY_ONLY` non sono soltanto meccanismi tecnici. Sono modi per proteggere identità, integrità e ricostruibilità.

Il dominio Scientific Data deve rispondere a quattro domande:

1. che cosa è stato osservato?
2. in quali condizioni e con quale configurazione?
3. quali trasformazioni ha attraversato il dato?
4. quale evidenza consente di fidarsi del risultato?

La sessione osservativa diventa l'unità che collega operazione e conoscenza. L'immagine finale resta importante, ma il suo valore aumenta quando può essere ricondotta alla propria storia.

**Domanda di controllo:** un risultato scientifico può essere compreso senza dipendere dalla memoria di chi lo ha prodotto?

## Dominio 6 - Knowledge and AI

I dati diventano conoscenza quando sono collegati, contestualizzati e interrogabili. L'AI diventa utile quando può operare su questa conoscenza senza confondere correlazione, raccomandazione e autorità.

Nel percorso Digital StarGate, cataloghi, lineage, Repository Knowledge Map, Scientific Intelligence e visione AP-015 preparano questo dominio. BootAI ne rappresenta una prima applicazione organizzativa: l'assistente non parte da una memoria opaca, ma da fonti ordinate.

Il dominio distingue quattro livelli:

- ricerca e recupero delle fonti;
- sintesi e spiegazione;
- correlazione e generazione di insight;
- raccomandazione entro boundary definiti.

Il comando fisico non appartiene implicitamente a questa scala. Per raggiungerlo servirebbero authority, safety case, validazione, audit e responsabilità che non possono essere dedotti dalla sola qualità del modello.

Principi:

- la risposta deve poter essere ricondotta alle fonti;
- l'incertezza deve essere visibile;
- le proiezioni non prevalgono sulle fonti primarie;
- l'AI non dichiara test o stati non verificati;
- ogni autonomia deve essere esplicitamente autorizzata;
- il diritto di suggerire non equivale al diritto di eseguire.

**Domanda di controllo:** l'AI può spiegare non solo la propria conclusione, ma anche quali fonti e limiti l'hanno prodotta?

## Dominio 7 - Assurance and Evolution

L'ultimo dominio circonda gli altri perché ogni parte del sistema deve poter essere verificata e cambiata.

Assurance comprende assessment, review indipendenti, piani di test, evidence, gate, acceptance e certificazioni. Evolution comprende roadmap, backlog, debito tecnico, release, feedback e supersession delle decisioni.

Nel caso Digital StarGate, la sequenza Architecture Package, ARB, condizioni, execution evidence e re-review impedisce che il disegno venga confuso con l'operatività. La validazione ENV-011 dimostra un comportamento su ambiente isolato e simulatore; il pilot AP-013 dimostra discovery e trasferimento protetto entro limiti dichiarati. Entrambi producono progresso senza cancellare le condizioni residue.

Il dominio usa una regola semplice:

> Ogni affermazione importante deve avere una forma di prova proporzionata al rischio e al tipo di capacità.

Una prova documentale può bastare per una policy. Un test automatizzato può bastare per una regola applicativa. Un comando su apparato fisico richiede condizioni molto più rigorose.

**Domanda di controllo:** quale evidenza sarebbe necessaria per trasformare la prossima promessa in una capacità accettata?

## I tre cicli

I sette domini non formano una gerarchia statica. Sono attraversati da tre cicli.

### Ciclo operativo

**Osservare, decidere, agire, proteggere, registrare.**

È il ciclo della notte osservativa. Parte dalle condizioni, attraversa l'autorità e termina con uno stato e un'evidenza. Quando qualcosa devia, la protezione interrompe o degrada l'attività.

### Ciclo informativo

**Acquisire, qualificare, conservare, collegare, comprendere.**

È il ciclo del dato. Un file acquista identità, qualità, lineage e contesto fino a poter sostenere ricerca, analytics e conoscenza.

### Ciclo evolutivo

**Valutare, decidere, progettare, provare, rilasciare, apprendere.**

È il ciclo dell'architettura. Collega gap assessment, roadmap, Architecture Package, evidence, release e aggiornamento delle fonti.

La maturità emerge quando i cicli comunicano. Un incidente operativo alimenta una decisione evolutiva. Una modifica architetturale aggiorna procedure e controlli. Un dato scientifico rivela un requisito per la piattaforma. Un insight di AI genera una proposta, non un cambiamento silenzioso.

## Le quattro condizioni di maturità

Il DSG-EOM valuta la maturità attraverso quattro condizioni, senza trasformarle in un punteggio competitivo.

### Coerenza

Fonti, stati, responsabilità e rappresentazioni non si contraddicono senza che la divergenza sia visibile.

### Controllabilità

Ogni azione rilevante possiede authority, precondizioni, stop condition e audit adeguati.

### Ricostruibilità

Decisioni, sessioni, dati e release possono essere ricondotti alle evidenze che ne spiegano origine e risultato.

### Evolvibilità

Il sistema può cambiare senza perdere sicurezza, significato o memoria.

Una piattaforma ricca di funzionalità ma priva di ricostruibilità non è matura. Un sistema sicuro ma impossibile da evolvere non è completo. Un'AI efficace ma priva di controllabilità non è pronta per l'impresa.

## Una roadmap in quattro orizzonti

Il modello suggerisce un percorso generale.

**Orizzonte 1 - Rendere esplicito.** Inventario, manuale, fonti, owner, rischi e stati sicuri.

**Orizzonte 2 - Rendere osservabile.** Telemetria, freshness, eventi, qualità, procedure ed evidence.

**Orizzonte 3 - Rendere governabile.** Capability, authority, contratti, roadmap, review e release.

**Orizzonte 4 - Rendere conoscitivo.** Cataloghi, lineage, analytics, knowledge graph e AI governata.

Gli orizzonti non sono fasi che si chiudono per sempre. Ogni nuova capability ripercorre il ciclo. L'errore consiste nel saltare direttamente al quarto orizzonte perché è più visibile o attraente.

## Che cosa rende nuovo l'approccio

Il DSG-EOM non propone una nuova tecnologia. Propone un nuovo ordine delle priorità.

- Non parte dall'AI, ma dalla verità del sistema.
- Non parte dalla dashboard, ma dall'autorità.
- Non parte dal file, ma dalla sessione e dal lineage.
- Non parte dall'automazione, ma dalle precondizioni e dal recovery.
- Non considera la documentazione un risultato secondario, ma una parte della piattaforma.
- Non considera la prova un atto finale, ma un elemento progettuale.

In questo senso il modello può essere applicato a stazioni ambientali, laboratori remoti, infrastrutture energetiche distribuite e altri sistemi cyber-fisici di piccola scala ma alta criticità.

## Verifica per il lettore

Per ciascuno dei sette domini, prova a indicare:

- l'owner;
- la fonte autorevole;
- il rischio principale;
- la condizione che blocca l'azione;
- l'evidenza minima;
- il prossimo cambiamento previsto.

Se una casella resta vuota, hai trovato un possibile punto di lavoro. Se più domini assegnano la stessa autorità, hai trovato un conflitto. Se l'AI appare prima delle fonti e delle evidenze, hai trovato un'inversione di priorità.

## Fonti del capitolo

- `DSG-MR-001` e `DSG-EAM-001`;
- `DSRA-000` e `DSRA-001`;
- Architecture Package `AP-001`-`AP-013`;
- roadmap `AMP-002`;
- [Enterprise Architecture Context](../project/ENTERPRISE_ARCHITECTURE_CONTEXT.md);
- [Repository Knowledge Map](../project/REPOSITORY_KNOWLEDGE_MAP.md);
- `AI_BOOTSTRAP.md`;
- evidence `ARB-012` e AP-013;
- manuale tecnico e registri enterprise.
