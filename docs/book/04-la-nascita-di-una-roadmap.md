# Capitolo 4 - La nascita di una roadmap

## Prima della roadmap c'era già un percorso

Una roadmap efficace non inventa la direzione. Rende visibile un percorso che, almeno in parte, è già iniziato.

La cronologia verificabile di Digital StarGate mostra questo con chiarezza. Il 13 luglio 2026 il repository viene configurato come ambiente Docs-as-Code con MkDocs e Pandoc. Nella stessa giornata vengono completati gruppi successivi del manuale: infrastruttura, operations, recovery, governance, dati, affidabilità, engineering, requisiti, rischi e handover.

La velocità della sequenza non autorizza a ricostruire motivazioni non documentate. Consente però di affermare un fatto: prima della roadmap enterprise esisteva già un corpus capace di descrivere l'osservatorio oltre la strumentazione astronomica.

Il manuale includeva continuità, sicurezza, asset, disaster recovery, KPI e release. Il lessico enterprise non era ancora organizzato nella forma successiva, ma il problema era già più ampio dell'acquisizione di immagini.

Il 15 luglio compare nel repository un report di sessione. Tra il 16 e il 17 luglio vengono registrati reporting automatico, analisi di sessione e workflow di validazione analytics. Il progetto inizia quindi a collegare documentazione ed esperienza osservativa.

Il 19 luglio viene aggiunta l'architettura della piattaforma Digital StarGate. Dal 23 luglio il Warehouse introduce dataset per sessioni e target; il 24 luglio si estende a equipment, quality e weather, seguito da assessment integrato e documentazione architetturale.

Questa successione prepara la domanda che una roadmap deve risolvere: come evitare che manuale, automazione, dati, portale e architettura evolvano come iniziative indipendenti?

## Dalla lista alla dipendenza

Una lista di attività ordina lavori. Una roadmap ordina dipendenze e decisioni.

Nella lista, “creare una dashboard”, “automatizzare la chiusura” e “introdurre AI” possono apparire come tre elementi confrontabili. In un sistema reale non lo sono.

La dashboard dipende da dati autorevoli, freshness e un modello di stato. La chiusura automatica dipende da sensori, authority, idempotenza, conferma e interlock. L'AI dipende da fonti, contratti, lineage, policy, audit e casi d'uso.

Il valore della roadmap consiste nel mostrare che alcune iniziative non possono essere iniziate responsabilmente prima di altre. Non è una previsione di calendario. È una dichiarazione di causalità.

Il capitolo 33 del manuale aveva già espresso una forma di roadmap evolutiva: ogni iniziativa doveva rispondere a un'esigenza, avere un owner, prevedere test e rollback e aggiornare inventario e manuale. La sequenza del Weather Safety Interlock introduceva inoltre un progresso controllato: validazione, simulatori, shadow mode, blocco apertura, chiusura automatica e decisione separata sulla riapertura.

La roadmap enterprise amplia questa logica dal singolo cambiamento all'intero programma.

## La svolta del 26 luglio

Il 26 luglio 2026 `DSG-MR-001` formalizza la Master Roadmap 2026-2030. Nello stesso giorno vengono pubblicate la baseline architetturale EAM/DSRA, il portfolio, i registri e il framework di governance.

Il passaggio fondamentale non è il numero di documenti. È la comparsa di una gerarchia.

`DSG-MR-001` distingue:

- stato AS-IS;
- fase di transizione;
- target TO-BE;
- obiettivi strategici;
- ambiti inclusi ed esclusi;
- criteri di successo;
- processi di change management;
- relazione tra PC Principale ed EAGLE.

Questa struttura trasforma iniziative differenti in un programma. Manuale, warehouse, analytics, portale, AI e knowledge graph non sono più soltanto temi. Diventano parti di una traiettoria governata.

La roadmap dichiara anche ciò che non deve accadere: nuovi programmi non registrati, piattaforme non approvate, configurazioni non documentate e decisioni architetturali informali. Il confine dell'ambito protegge il progetto dalla crescita opportunistica.

## Roadmap e verità del presente

Una roadmap può diventare pericolosa quando il futuro è più dettagliato del presente. Le rappresentazioni target sono visivamente convincenti; lo stato reale è spesso incompleto.

Digital StarGate affronta il problema usando marcature quali `TBD` e “Da validare”. Il meccanismo non è una debolezza editoriale. È un controllo.

Una buona roadmap deve poter affermare:

- questo esiste ed è verificato;
- questo esiste ma richiede consolidamento;
- questo è approvato come disegno;
- questo è pianificato;
- questo dipende da una decisione;
- questo non è autorizzato.

La precisione del linguaggio impedisce che una casella colorata su una dashboard acquisisca il valore di un'evidenza.

Il principio diventerà ancora più esplicito nei documenti successivi: repository truth, evidence before status, unknown is not safe e read-only before control. La roadmap non serve soltanto a promettere. Serve a limitare la promessa a ciò che il sistema può sostenere.

## Il passaggio dai progetti alle capability

Una roadmap tradizionale può organizzare progetti: dashboard, data warehouse, portale, automazione. Il problema è che un progetto termina mentre la capacità deve continuare.

Digital StarGate evolve verso un modello di capability. “Observation Session” non è soltanto un deliverable software. È un concetto che collega dominio, contratti, API, dati, eventi e documentazione. “Weather Safety Interlock” non è soltanto uno script. È una capacità con stati, condizioni, autorità, evidenze e limiti.

Il passaggio si rende visibile tra il 28 e il 29 luglio.

La Release 1.5 Developer Edition introduce una foundation, contratti canonici e il primo vertical slice Observation Session. Il documento è attento a ciò che non include: database, event bus e integrazioni astronomiche avanzate.

La Release 2.0 Safety Foundation rimane invece una proposta architetturale. Nessuna capability runtime viene dichiarata implementata. Il piano separa simulatori, shadow mode, blocco apertura e chiusura automatica.

Due release vicine nel tempo rappresentano due stati differenti. Una contiene componenti implementati; l'altra ordina una progressione futura di safety. La roadmap deve preservare la differenza.

## Assessment prima di espansione

Il 24 luglio l'assessment EA-002 aveva già introdotto un principio che tornerà nella roadmap: consolidare ciò che esiste prima di creare fondazioni duplicate.

EA-002 verifica che il Warehouse legge dataset Analytics validati, persiste dati curati e dispone di schema, metadata, controlli e test. Identifica anche ciò che manca, come l'integrazione formale del reporting e alcuni consumer.

La conclusione è istruttiva: il passo corretto non è creare un nuovo Warehouse. È consolidare la piattaforma, formalizzare l'architettura e integrare i consumer in modo controllato.

Una roadmap matura non è una collezione di nuove costruzioni. Contiene anche:

- consolidamento;
- ritiro di duplicazioni;
- gestione del debito;
- migrazione;
- evidenze;
- revisione delle decisioni;
- limiti temporanei.

Questi elementi sono meno spettacolari delle nuove funzionalità, ma determinano la sostenibilità.

## Dal master plan al riallineamento

Il 30 luglio `AMP-001` traduce la baseline architetturale in un piano multi-release. Separa consolidamento, implementazione, integrazione, deployment e verifica operativa. Introduce wave dipendenti e una regola forte: le fondazioni già presenti non devono essere ricostruite.

Nello stesso giorno `AMP-002` riallinea la roadmap al programma effettivamente realizzato. Conserva gli Architecture Package esistenti, supera la numerazione futura di `AMP-001` e diventa la fonte autorevole per la sequenza successiva.

Questo passaggio contiene una lezione importante: una roadmap non perde autorevolezza quando viene corretta. La perde quando il progetto cambia e la roadmap finge di essere ancora attuale.

Il riallineamento non cancella `AMP-001`. Lo conserva come fonte storica per principi, gate e baseline iniziale. Cambia la sua autorità sulla numerazione futura.

Il rapporto tra i due documenti dimostra una forma sana di supersession:

1. preservare la decisione precedente;
2. dichiarare ciò che rimane valido;
3. identificare ciò che viene superato;
4. motivare il riallineamento;
5. aggiornare le proiezioni.

## Le wave come catena di readiness

`AMP-002` organizza il programma in wave:

- foundation;
- enterprise operations;
- integration;
- infrastructure;
- safety;
- digital platforms;
- scientific image and processing heritage;
- scientific knowledge platform.

L'ordine non rappresenta soltanto una preferenza. Esprime readiness.

L'Operations Center dipende da automation, observability, identity, configuration, operations, integration, infrastructure e safety. Il repository scientifico dipende da data governance, asset management, integrazione e storage. La Knowledge Platform dipende da catalogo, dati, analytics, provenance e query target.

L'AI read-only appare a valle della conoscenza governata. Non perché l'AI sia marginale, ma perché la sua affidabilità eredita l'affidabilità delle fonti e dei confini che la precedono.

La roadmap diventa così una struttura di autorizzazione progressiva. Ogni wave crea le condizioni per la successiva, mentre review ed evidence possono rallentare o bloccare il passaggio.

## La roadmap pubblicata non è la roadmap autorevole

Il progetto comprende viste dinamiche e dataset JSON che rendono la roadmap accessibile nel portale. Sono utili per comunicare stato, priorità e relazioni. Restano proiezioni.

La fonte autorevole è il documento governato. Questa separazione evita che una modifica dell'interfaccia riscriva implicitamente il programma.

BootAI formalizzerà l'ordine di prevalenza: Architecture Package e ADR, evidence, `AMP-002`, release, contratti, proiezioni, contesto e conversazioni.

Il principio può essere espresso in modo semplice: **la vista deve derivare dalla decisione; la decisione non deve essere ricostruita dalla vista**.

## Una roadmap per una piccola organizzazione

La dimensione del progetto non riduce il bisogno di roadmap. Lo rende più selettivo.

In una grande organizzazione, attività parallele possono essere sostenute da team differenti. In una realtà più piccola, il costo del context switching è elevato. Una dipendenza ignorata produce lavoro duplicato o una capability priva delle fondazioni necessarie.

La roadmap deve quindi proteggere tre risorse scarse:

- attenzione;
- capacità di verifica;
- memoria del progetto.

Per farlo non serve un piano immobile. Serve una sequenza esplicita, aggiornata e collegata alle evidenze.

## Quattro domande per costruire la roadmap

Il caso Digital StarGate suggerisce quattro domande.

### Che cosa esiste davvero?

Inventario, assessment e repository truth precedono la pianificazione. Le capability esistenti vengono consolidate.

### Quale rischio decide l'ordine?

Safety, dati, authority e dipendenze determinano la sequenza più del fascino della funzionalità.

### Quale evidenza consente il passaggio?

Ogni milestone deve avere criteri osservabili: documento approvato, test, esecuzione limitata, acceptance o evidenza operativa.

### Come viene corretto il piano?

Supersession, riallineamento e change management devono essere previsti. La roadmap è governata anche quando cambia.

## Lezione trasferibile

Una roadmap enterprise non è un calendario illustrato. È un modello delle condizioni necessarie per evolvere senza perdere verità, sicurezza e memoria.

Deve mostrare almeno:

- baseline;
- target;
- dipendenze;
- authority;
- rischi;
- evidence gate;
- esclusioni;
- regola di aggiornamento.

Il suo valore non si misura dal numero di iniziative, ma dalla quantità di lavoro prematuro che riesce a evitare.

## Verifica per il lettore

- La roadmap distingue chiaramente implementato, approvato, pianificato e operativo?
- Le iniziative sono ordinate per dipendenza o per desiderabilità?
- Esiste un assessment verificabile dello stato attuale?
- Le capability già presenti vengono consolidate prima di duplicarle?
- Ogni milestone dichiara l'evidenza richiesta?
- Le viste e le dashboard sono riconoscibili come proiezioni?
- È chiaro come una roadmap venga superata senza cancellare la storia?
- L'AI appare dopo le fonti e la governance di cui dipende?

## Fonti del capitolo

- commit `cf4535f` del 13/07/2026, Docs-as-Code con MkDocs e Pandoc;
- commit di completamento dei capitoli del 13/07/2026;
- commit `d96150a`, `9d976b9` e `b87700e` su session reporting e analytics;
- commit `8669bb4` e successivi sul Warehouse;
- commit `10e0edf` sulla platform architecture;
- [EA-002 - Integrated Repository and Warehouse Assessment](../architecture/assessments/EA-002-Integrated-Repository-and-Warehouse-Assessment.md);
- `DSG-MR-001` e baseline enterprise del 26/07/2026;
- [Release 1.5 - Developer Edition](../releases/release-1.5-developer-edition.md);
- [Release 2.0 - Safety Foundation](../releases/release-2.0-safety-foundation.md);
- [AMP-001 - Architecture Master Plan](../architecture/assessments/AMP-001-Architecture-Master-Plan.md);
- [AMP-002 - Architecture Program Roadmap Realignment](../architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md).
