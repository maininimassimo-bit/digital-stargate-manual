# Capitolo 2 - Il cambio di prospettiva

## Quando il manuale non basta più

Un buon manuale riduce l'incertezza. Spiega come è composto un impianto, come si avvia una sessione, come si reagisce a un'anomalia e come si mantiene una configurazione. Per Digital StarGate il manuale tecnico è stato il primo grande contenitore della conoscenza: quarantaquattro capitoli capaci di attraversare infrastruttura, astronomia, software, automazione, sicurezza, dati, manutenzione e governance.

La sua crescita ha però rivelato una distinzione decisiva. Documentare il sistema non coincide con governarne l'evoluzione.

Un capitolo può descrivere perfettamente un componente e tuttavia non chiarire se quel componente appartiene allo stato corrente o alla visione futura. Due procedure possono essere corrette nel proprio contesto e produrre un conflitto quando vengono eseguite insieme. Una nuova dashboard può rendere visibile uno stato senza possedere l'autorità per dichiararlo. Una roadmap può mostrare un avanzamento che non corrisponde ancora a un'evidenza tecnica.

Il cambio di prospettiva nasce quando la documentazione smette di essere soltanto una raccolta di spiegazioni e diventa una rete di impegni verificabili.

## Dalla pagina alla relazione

Nella documentazione tradizionale l'unità principale è la pagina. Nella documentazione enterprise l'unità fondamentale è la relazione.

Un requisito è collegato a una capacità. Una capacità è sostenuta da componenti e procedure. Una decisione spiega perché esiste un determinato confine. Un rischio è associato a un controllo. Un controllo richiede evidenze. Una release raccoglie cambiamenti che devono poter essere ricondotti alla roadmap.

La qualità non dipende quindi soltanto dalla correttezza di ogni documento, ma dalla coerenza dei collegamenti.

Digital StarGate ha reso visibile questo passaggio attraverso registri, ADR, assessment, Architecture Package e matrici di tracciabilità. Il repository non contiene più soltanto contenuti da leggere: contiene un modello del progetto.

Questo modo di lavorare produce un effetto importante. Le contraddizioni smettono di essere problemi nascosti nella prosa e diventano elementi rilevabili. Se una capability è dichiarata operativa ma non possiede evidence, il collegamento mancante segnala una lacuna. Se una dashboard presenta uno stato differente dalla roadmap autorevole, la gerarchia delle fonti consente di stabilire quale rappresentazione deve essere corretta.

## La roadmap come cambio di scala

La pubblicazione della Master Roadmap `DSG-MR-001`, il 26 luglio 2026, formalizza un nuovo livello. Il progetto non viene più descritto soltanto attraverso sistemi e procedure, ma come programma 2026-2030.

La roadmap introduce una distinzione che accompagnerà l'intero libro:

- **AS-IS:** ciò che esiste ed è sostenuto dalla documentazione disponibile;
- **Transition:** ciò che sta consolidando il passaggio verso una baseline più governata;
- **TO-BE:** la configurazione target, ancora soggetta a decisioni, dipendenze e validazioni.

Questa distinzione è semplice, ma protegge da uno degli errori più frequenti nella trasformazione digitale: raccontare il futuro usando il tempo presente.

Nel caso Digital StarGate, AI e Knowledge Graph compaiono come ambiti previsti prima di essere piattaforme operative. La loro presenza nella visione è importante perché orienta dati, contratti e governance. Non autorizza però a descriverli come capacità già disponibili.

Allo stesso modo, una reference architecture definisce come una capacità dovrà essere organizzata. Una review “approved with conditions” riconosce la validità del disegno entro condizioni esplicite. Una execution evidence dimostra un comportamento in un perimetro. L'accettazione operativa richiede che i passaggi siano collegati senza salti.

## La gerarchia delle fonti

Con l'aumento dei documenti, la domanda “qual è la versione corretta?” diventa inevitabile. Digital StarGate risponde attraverso una gerarchia.

Nella baseline più recente, Architecture Package, ADR, capability e standard approvati prevalgono sulle rappresentazioni derivate. Assessment, validation record ed evidence precisano lo stato di assurance. La roadmap autorevole `AMP-002` ordina le evoluzioni. Release e commit dimostrano ciò che è stato effettivamente pubblicato. Dataset e dashboard restano proiezioni.

Questa gerarchia evita che l'elemento più visibile diventi automaticamente il più autorevole. Una dashboard può essere aggiornata in ritardo. Un file JSON può contenere una proiezione non allineata. Una conversazione può ricordare uno stato superato. Il repository, letto secondo le sue fonti, rimane il punto di ricostruzione.

La scelta è particolarmente rilevante per l'AI. Un assistente che usa la conversazione come memoria primaria rischia di continuare un progetto immaginario. Un assistente che segue la gerarchia delle fonti può ricostruire lo stato, segnalare divergenze e lasciare traccia delle modifiche.

## BootAI: non una memoria, ma un metodo di lettura

`AI_BOOTSTRAP.md` appare nella fase più recente dell'evoluzione come punto di ingresso obbligatorio per persone e assistenti AI. Il nome può suggerire un documento dedicato alla tecnologia; in realtà la sua funzione è di governance.

BootAI stabilisce che il repository è l'unica fonte autorevole. Definisce una sequenza di lettura, richiede la verifica di branch, commit, file e workflow e distingue le fonti primarie dalle proiezioni. Elenca principi non negoziabili: safety prima della continuità, nessun comando diretto dal portale agli apparati, responsabilità modulari, nessuna affermazione di test o rilascio senza verifica.

Il suo contributo più interessante non è “insegnare il progetto all'AI”. È insegnare a chiunque come ricostruire il progetto.

In questa prospettiva BootAI diventa una forma di continuità cognitiva. Riduce la dipendenza dalla memoria individuale e dalla storia della conversazione. Permette di iniziare una nuova sessione senza fingere che il contesto sia completo. Obbliga il collaboratore a distinguere ciò che ricorda da ciò che può dimostrare.

Il metodo è applicabile oltre l'AI. Ogni organizzazione complessa ha bisogno di un punto di ingresso che dica:

- quali fonti leggere;
- in quale ordine;
- quali regole non possono essere violate;
- come verificare lo stato corrente;
- come lasciare il sistema più comprensibile di prima.

## Il Project Governance Center

La creazione della sezione `docs/project/` consolida questa funzione. Enterprise Architecture Context, Repository Knowledge Map, Backlog, Technical Debt, Decision Log, Development Workflow e Release Playbook hanno responsabilità distinte.

La separazione è intenzionale.

Il Context orienta. La Knowledge Map descrive il territorio. Il Backlog registra il lavoro pianificato. Il Technical Debt rende visibili i compromessi. Il Decision Log conserva le scelte operative reversibili. Gli ADR proteggono le decisioni strutturali. Il Release Playbook definisce il passaggio alla pubblicazione.

Mescolare questi contenuti in un unico documento produrrebbe un file apparentemente completo ma difficile da mantenere. Separarli consente a ciascun registro di cambiare con il proprio ritmo e preserva l'ownership.

Questo è un esempio concreto di architettura applicata alla documentazione: la modularità non riguarda solo il software. Riguarda ogni sistema di conoscenza che deve evolvere senza perdere significato.

## Dal documento all'evidenza

La fase enterprise modifica anche il significato della parola “completato”.

In un approccio centrato sui documenti, un deliverable può sembrare completo quando il testo è scritto e approvato. In un approccio evidence-driven, la completezza dipende dal tipo di affermazione.

Se il deliverable è una visione, l'approvazione del documento può essere sufficiente. Se dichiara un comportamento del sistema, serve una prova. Se autorizza un'attività operativa, servono anche responsabilità, condizioni e accettazione.

La campagna di validazione dell'Enterprise Operations Center rende visibile questa differenza. L'esecuzione ENV-011 in ambiente Hyper-V isolato e in modalità simulatore fornisce evidenza tecnica entro un perimetro definito. Non autorizza automaticamente l'accesso alla produzione, l'uso di credenziali reali o il controllo degli apparati fisici. Il valore dell'evidenza aumenta proprio perché dichiara i propri limiti.

Lo stesso avviene con AP-013. La session discovery e il trasferimento protetto `COPY_ONLY` dimostrano progressi concreti, mentre bulk transfer e cancellazione alla fonte rimangono esclusi fino a nuove evidence e review.

Il limite non diminuisce il risultato. Lo rende affidabile.

## Il repository come prodotto

Con il nuovo approccio, il repository Digital StarGate contiene quattro prodotti correlati:

1. manuale tecnico dell'osservatorio;
2. repository di Enterprise Architecture;
3. Enterprise Portal;
4. Developer Foundation.

Questa lettura cambia il modo di valutare il lavoro. Una modifica al portale può essere tecnicamente corretta ma incoerente con l'architettura. Una nuova capability può essere ben progettata ma priva di documentazione operativa. Un aggiornamento della roadmap può risultare elegante ma non corrispondere allo stato dei workflow.

Il repository è quindi un prodotto composto, con confini e responsabilità. La documentazione non è un allegato del software; il software non è un'illustrazione della documentazione. Entrambi sono parti della stessa baseline, ma ogni affermazione deve essere sostenuta dal tipo di evidenza appropriato.

## Il principio della verità operativa

Il filo che unisce roadmap, BootAI, registri ed evidence può essere chiamato “verità operativa”: la capacità di descrivere il sistema in modo proporzionato a ciò che è realmente noto e autorizzato.

La verità operativa non richiede certezza assoluta. Richiede che l'incertezza sia esplicita.

- Un dato non confermato viene marcato da validare.
- Una capacità pianificata viene descritta al futuro.
- Una prova limitata dichiara il proprio ambiente.
- Una condizione aperta rimane visibile.
- Una proiezione non sostituisce la fonte primaria.
- Una decisione nuova non viene nascosta dentro un aggiornamento editoriale.

Questa disciplina è il prerequisito dell'automazione e dell'AI. Senza di essa, sistemi più veloci producono soltanto errori più convincenti.

## Lezione trasferibile

Il passaggio enterprise non consiste nel creare più documenti. Consiste nel progettare un sistema di conoscenza nel quale ogni artefatto abbia uno scopo, un owner, una relazione e una regola di aggiornamento.

Per iniziare sono sufficienti pochi elementi:

1. una fonte autorevole dichiarata;
2. una mappa delle fonti e delle responsabilità;
3. una roadmap che separi presente, transizione e futuro;
4. un registro delle decisioni;
5. un registro dei rischi o del debito;
6. una regola che impedisca di dichiarare risultati senza evidenza;
7. un percorso di onboarding verificabile.

La quantità cresce soltanto quando la complessità lo richiede.

## Verifica per il lettore

- La tua organizzazione sa distinguere una fonte primaria da una dashboard?
- Le persone nuove ricevono un percorso di lettura o una raccolta casuale di link?
- Una decisione strutturale può essere ricostruita mesi dopo?
- “Completato” ha criteri diversi per documento, software e capacità operativa?
- Le prove dichiarano ambiente, limiti e condizioni?
- Le visioni future sono riconoscibili come tali?
- L'AI utilizza fonti verificabili o dipende dalla memoria della conversazione?

## Fonti del capitolo

- `DSG-MR-001`, Master Roadmap;
- [Enterprise Architecture Context](../project/ENTERPRISE_ARCHITECTURE_CONTEXT.md);
- [Repository Knowledge Map](../project/REPOSITORY_KNOWLEDGE_MAP.md);
- [Decision Log](../project/DECISION_LOG.md);
- `AI_BOOTSTRAP.md`;
- [AMP-002 - Architecture Program Roadmap Realignment](../architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md);
- documentazione di validazione `ARB-012-C04`;
- Architecture Package `AP-013` e relative evidence.
