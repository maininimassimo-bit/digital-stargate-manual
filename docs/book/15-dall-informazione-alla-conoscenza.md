# Capitolo 15 - Dall'informazione alla conoscenza

## Sapere dove cercare

Un'organizzazione può possedere dati integri e informazioni ben strutturate senza riuscire ancora a usarli come conoscenza. I record esistono, i dataset sono validati, i report vengono pubblicati, ma le relazioni restano disperse tra sistemi e documenti.

Per trovare tutte le osservazioni di un target occorre conoscere nomi di cartelle, alias e date. Per risalire da un'immagine finale ai RAW bisogna attraversare manifest, storage e note di processing. Per capire perché una sessione ha prodotto un risultato migliore occorre confrontare configurazione, meteo, qualità e workflow.

Digital StarGate affronta questa distanza con due passi distinti. AP-014 costruisce il Scientific Observation Catalog and Search: una proiezione governata che rende interrogabile il patrimonio. AP-015, ancora pianificato, dovrà costruire il livello semantico che collega entità, relazioni, claim e citazioni.

La distinzione è fondamentale. La ricerca permette di trovare. La conoscenza permette di collegare, interpretare e sostenere un'affermazione con fonti verificabili.

## Dal file all'osservazione

La ricerca tradizionale parte spesso dal nome del file. AP-014 rovescia la prospettiva: observation identity precedes file identity.

Il punto di ingresso diventa il contesto osservativo. Un progetto contiene campagne; una campagna coordina osservazioni; un'osservazione riguarda un target; una sessione realizza una parte dell'intento; le acquisizioni producono asset; processing run e prodotti derivati estendono la catena.

Questo modello consente domande più naturali. Non “in quale directory si trova quel FITS?”, ma “quali sessioni hanno osservato questo target con quel filtro nel periodo indicato?”. Non “come si chiama l'immagine finale?”, ma “quali prodotti derivano da questa campagna e con quali workflow?”.

Il passaggio è organizzativo prima che tecnologico. Richiede identificatori stabili, vocabolari governati e relazioni. Se target e strumenti vengono nominati in modi incompatibili, un motore di ricerca può trovare stringhe ma non costruire una vista coerente.

Il catalogo osservativo rende quindi esplicita la grammatica del patrimonio.

## Il catalogo è una proiezione

AP-014 adotta una regola vincolante: catalog is a projection.

Le fonti autorevoli rimangono AP-013 per asset, checksum, locator e provenance; i registri di sessione per il contesto osservativo; il Warehouse per i data product analitici; GitHub per architettura e documentazione. Il catalogo normalizza e indicizza queste fonti in modalità read-only.

Una proiezione può essere ricostruita. Se l'indice viene perso, la pipeline lo rigenera dagli input. Se cambia lo schema, una nuova versione produce record coerenti. Se una fonte viene corretta, la reconciliation aggiorna la vista senza riscrivere retroattivamente il registro.

Questo boundary protegge la verità. Un'interfaccia di ricerca non può modificare checksum, promuovere un prodotto o cambiare il locator. Il fatto che un risultato sia facile da trovare non gli conferisce uno stato scientifico superiore.

La proiezione è ottimizzata per la domanda; la fonte è ottimizzata per la responsabilità. Confonderle renderebbe comoda la ricerca e fragile la governance.

## Identificatori e vocabolari

La conoscenza non può dipendere soltanto dalla somiglianza delle parole. Lo stesso target può avere catalog reference, nome comune e alias operativi. Lo stesso strumento può apparire con abbreviazioni o denominazioni storiche. Una qualità può essere espressa con scale diverse.

AP-014 introduce identificatori per progetto, campagna, osservazione, sessione, acquisizione, calibration set, catalog item e index build. Il formato è meno importante del principio: l'identità non dipende dal path o dall'etichetta visibile.

I controlled vocabulary regolano categorie, filtri, classi di asset e stati. Non eliminano il linguaggio naturale; lo collegano a concetti stabili. Un alias registry permette di conservare il valore osservato e, quando verificato, associarlo a un'identità canonica.

Un valore non risolto rimane unknown. Questo impedisce che il catalogo costruisca relazioni inesistenti per aumentare artificialmente la copertura.

Il vocabolario è una forma di infrastruttura. Quando manca, ogni integrazione risolve gli stessi sinonimi in modo diverso. Quando è governato, le domande possono attraversare sistemi e tempo.

## Una pipeline deterministica

Il Catalog Projection Pipeline trasforma le fonti in record indicizzabili. La stessa baseline e la stessa versione dell'algoritmo devono produrre lo stesso indice.

La determinazione non è soltanto una proprietà tecnica. Rende spiegabile la differenza tra due build. Ogni index build possiede versione, timestamp, input digest e risultato. Se il contenuto cambia senza una variazione degli input o della logica, esiste una dipendenza nascosta.

La pipeline valida relazioni, normalizza vocabolari, conserva unknown e produce reconciliation record. Un item incompleto può essere indicizzato con stato di qualità appropriato; non viene completato inventando dati.

Il progetto ha portato questa idea oltre la baseline documentale. Al 5 agosto 2026 esistono una proiezione del catalogo, un indice scientifico versionato, servizi di ricerca e test protetti dal workflow. Questa evidence sostiene i work package AP14-W01-W05 e parte del percorso successivo.

La presenza dell'indice, tuttavia, non chiude l'Architecture Package. L'operational acceptance resta una condizione distinta.

## Cercare e spiegare

Il Search Service supporta testo libero e query strutturate. È possibile filtrare per target, periodo, progetto, campagna, strumento, camera, filtro, qualità, classe dell'asset e stato del processing.

La combinazione permette di partire da un ricordo approssimativo o da una domanda precisa. Il testo libero favorisce la scoperta; i filtri riducono l'ambiguità; le facet mostrano la distribuzione dei risultati.

Il ranking deve essere explainable. Una corrispondenza esatta sul target o sull'identificatore ha un peso diverso da una nota testuale. Completezza, qualità e stato possono influire, mentre record superseded o non riconciliati possono essere penalizzati.

Ogni risultato dovrebbe esporre i fattori principali e la fonte autorevole. L'utente non riceve soltanto un ordine, ma un motivo sufficiente per comprenderlo.

Questa trasparenza prepara anche il futuro uso dell'AI. Un sistema che non sa spiegare il ranking tradizionale difficilmente governerà in modo credibile risultati prodotti da modelli più complessi.

## Discovery senza modifica

AP-014 mantiene la ricerca read-only. Query, filtri, ranking e navigazione non cambiano gli asset o la provenance.

Il principio appare ovvio, ma molte interfacce mescolano ricerca, editing e promozione. L'utente trova un record, corregge un campo e il catalogo diventa implicitamente il luogo autorevole. Oppure un risultato viene marcato come preferito e quel gesto influenza lo stato scientifico senza un processo di review.

Digital StarGate separa la discovery dalla cura. Un errore rilevato può generare un data issue o una proposta di correzione verso la fonte responsabile. La modifica segue ownership, validation e audit. L'indice viene poi rigenerato.

Questo percorso è più lento di un edit diretto, ma conserva la coerenza. Soprattutto, impedisce che differenti consumer correggano la stessa informazione in proiezioni incompatibili.

La ricerca aiuta a vedere il patrimonio. Non acquisisce il diritto di riscriverlo.

## L'Enterprise Search Center

Il catalogo scientifico non vive isolato. Digital StarGate integra la ricerca scientifica con l'Enterprise Search Center, che già indicizza documentazione e contenuti della piattaforma.

L'esperienza federata consente di trovare una sessione insieme ai documenti che ne spiegano il contesto, oppure un Architecture Package insieme alle evidenze e alle capacità collegate. I risultati mantengono tipo, fonte e boundary.

La federazione non appiattisce tutto in un elenco indistinto. Un documento, un asset reference e un KPI possiedono autorità differenti. L'interfaccia deve aiutare a riconoscere la natura del risultato e il percorso verso la fonte.

URL condivisibili, deep link, filtri e dettaglio migliorano la collaborazione. Una review può riferire una ricerca ripetibile invece di descrivere manualmente dove fare clic. La storia delle query può sostenere casi d'uso, purché retention e privacy siano governate.

Il Search Center diventa un accesso comune alla memoria senza trasformarsi nella memoria stessa.

## Il boundary PixInsight

Il processing produce conoscenza preziosa: workflow, input, output, parametri e ambiente. AP14-W06 definisce come questa informazione possa entrare nel catalogo.

PixInsight esporta un manifest dichiarativo. Un controlled import drop riceve il pacchetto senza eseguire script. Il validator controlla schema e limiti. Il normalization adapter converte i valori nel contratto canonico. Il reconciliation service confronta identificatori e riferimenti con AP-013 e AP-014 in sola lettura.

Ogni tentativo produce un audit record. I duplicati sono no-op. I conflitti vengono isolati. I record parziali rimangono unresolved o partially matched. Gli output sono prodotti candidati, non automaticamente accepted.

Al 5 agosto, la roadmap evidence registra il documento di soluzione AP14-W06 tra gli elementi presenti. Questo dimostra il boundary architetturale e l'avanzamento del package; la formal operational acceptance prevista da AP14-W07 rimane mancante.

La distinzione evita di confondere una buona integrazione con una capacità completamente accettata.

## Quando l'informazione diventa relazione

Il catalogo risponde bene a domande su entità e attributi. La conoscenza richiede anche relazioni che attraversano domini.

Una sessione usa una configurazione. Produce asset. Un processing run consuma quegli asset e genera un prodotto. Un report formula una conclusione. Un KPI sintetizza una popolazione. Un finding segnala una lacuna. Una decisione architetturale modifica il modo in cui la pipeline interpreterà le sessioni future.

Queste relazioni esistono già, ma sono distribuite. La Scientific Knowledge Layer prevista da AP-015 dovrà renderle interrogabili senza sostituire le fonti.

Il concetto chiave è Knowledge Entity: un target, una sessione, un asset, uno strumento, un workflow o un report identificato semanticamente. Le Knowledge Relation collegano le entità con tipi e versioni. Le Knowledge Projection producono viste per ricerca, analytics e AI.

Il valore non sta nel creare un grafo perché la tecnologia è interessante. Sta nel preservare una rete di significati che oggi richiede attraversamenti manuali.

## Claim e citazioni

La Knowledge Layer introduce anche lo Scientific Claim: un'affermazione derivata da evidenze, con fonte, metodo e livello di confidenza.

Un claim non è un campo copiato. Può affermare, per esempio, che una configurazione ha prodotto risultati migliori in un insieme di sessioni secondo una metrica e una finestra definite. Per essere governato deve collegare dataset, query, metodo e baseline.

Il Citation Locator permette di risalire al documento, manifest, checksum, asset o data product pertinente. In questo modo un report o un assistente AI può fornire non soltanto una risposta, ma il percorso verificabile che la sostiene.

La citabilità è il confine tra sintesi e autorità. Una sintesi può essere utile e ancora incerta. Diventa knowledge governata quando dichiara su quali fonti si basa e quale processo l'ha prodotta.

Questo approccio riduce il rischio che un insight venga ripetuto fino a sembrare un fatto indipendente dalla propria origine.

## AP-015 come visione, non realtà

La Scientific Knowledge Layer è approvata per la pianificazione. AP-015 è registrato come planned. Non esistono ancora proof of concept di knowledge graph, semantic index, ingestione o query.

La vision stabilisce boundary e casi d'uso, ma rinvia la scelta tecnologica. Il livello potrebbe usare un indice documentale, un grafo o un modello ibrido. La decisione deve seguire stabilizzazione dei contratti, conoscenza dei volumi e validazione dei bisogni.

Questa prudenza evita la scelta prematura di graph database, vector database o piattaforme AI. La tecnologia non può compensare identificatori instabili, metadata storici deboli o ownership assente sul vocabolario.

AP-015 dipende da data governance, asset management, integrazione, analytics, repository scientifico e catalogo. Può iniziare soltanto quando le fonti sono sufficientemente governate da sostenere relazioni affidabili.

Nel libro, quindi, la Knowledge Platform è raccontata come direzione architetturale. Il catalogo AP-014 possiede evidence concreta ma non ancora acceptance finale; AP-015 rimane una capacità futura.

## AI read-only e conoscenza citabile

La Knowledge Layer prevede un futuro AI Assistant in modalità read-only. Il boundary è coerente con il resto del progetto.

L'AI può attraversare documenti, catalogo e data product per rispondere a domande, confrontare sessioni e segnalare provenance incompleta. Può proporre relazioni candidate o riassumere claim. Non modifica silenziosamente le fonti e non acquisisce autorità operativa.

Ogni risposta importante dovrebbe riferire Citation Locator e distinguere fatti, inferenze e dati mancanti. Il modello o la pipeline usati per produrre un'inferenza devono essere versionati. Un nuovo modello può generare una nuova projection; non riscrive la storia come se la conclusione fosse sempre esistita.

L'AI arriva quindi dopo identità, lineage e catalogo. Senza queste fondamenta potrebbe produrre testi convincenti su record ambigui. Con esse può diventare uno strumento di navigazione della conoscenza.

La Parte V approfondirà questo rapporto. Qui è sufficiente fissare il principio: l'AI non crea la fonte che le manca.

## Conflitti come oggetti di conoscenza

Le fonti possono contraddirsi. Un manifest PixInsight può indicare un output non presente nel registro. Un report può citare una sessione con alias non riconciliato. Il Warehouse può conservare una classificazione prodotta prima della correzione della sorgente.

La Knowledge Layer non deve scegliere automaticamente la versione più recente o più frequente. Registra un knowledge conflict, le fonti coinvolte, la regola di precedenza e lo stato della revisione.

Il conflitto diventa esso stesso conoscenza. Mostra un punto nel quale il sistema non possiede ancora una risposta condivisa. Può alimentare un data issue, una decisione o una nuova evidence.

Nascondere il conflitto crea un'apparenza di coerenza. Esporlo consente all'organizzazione di apprendere dove contratti e processi devono migliorare.

La maturità non consiste nell'avere una risposta unica a ogni costo, ma nel sapere quando la risposta non è ancora autorizzata.

## Dalla domanda alla prova

Il percorso completo può essere letto come una catena.

La sessione fornisce l'unità di senso. Il repository conserva identità, integrità e provenance. Il Warehouse produce informazione validata. Il catalogo rende entità e attributi ricercabili. La Knowledge Layer collegherà relazioni e claim. L'AI potrà assistere l'esplorazione.

In ogni passaggio aumenta l'astrazione. Per evitare che aumenti anche la distanza dalla realtà, il lineage deve rimanere percorribile nella direzione opposta.

Da un claim si deve arrivare al data product; dal data product agli input; dagli input alla sessione e agli asset; dagli asset ai checksum e ai locator; dalla sessione alla configurazione e alle condizioni.

La conoscenza enterprise non è quindi il punto più alto di una piramide che dimentica la base. È la capacità di muoversi tra sintesi e prova.

## Lezione trasferibile

Prima di investire in semantic search o AI, un'organizzazione dovrebbe verificare quattro condizioni.

Le entità hanno identificatori stabili? Le fonti autorevoli sono dichiarate? Le proiezioni sono ricostruibili? Le affermazioni possono citare dati ed evidence?

Se la risposta è negativa, l'intelligenza aggiunta rischia di amplificare incoerenze esistenti. Se la risposta è positiva, anche strumenti semplici possono produrre grande valore perché attraversano un patrimonio già comprensibile.

La conoscenza non nasce dall'algoritmo che trova più relazioni. Nasce dal governo che permette di distinguere una relazione osservata, una relazione derivata e una relazione soltanto ipotizzata.

## Verifica per il lettore

- La ricerca parte dall'osservazione o soltanto dal nome del file?
- Catalogo e indice sono dichiarati come proiezioni ricostruibili?
- Identificatori e vocabolari sono stabili e governati?
- Il ranking può spiegare i fattori principali?
- La discovery rimane read-only rispetto alle fonti?
- PixInsight contribuisce attraverso validation e reconciliation?
- Stato active di AP-014 e stato planned di AP-015 sono distinti?
- Claim, inferenze e fatti hanno citation locator e livelli di confidenza?
- I conflitti vengono esposti invece di essere risolti silenziosamente?

Quando una risposta non può mostrare il percorso verso la propria fonte, può essere un'intuizione utile ma non è ancora conoscenza governata.

## Fonti del capitolo

- `AP-014`, Scientific Observation Catalog and Search;
- Observation Catalog Conceptual Model e Logical Data Model;
- Catalog Projection and Index Build;
- Search Query and Ranking Contract;
- Enterprise Search Center integration e relativi test;
- `AP14-W06`, PixInsight Synchronization Adapter;
- evidence manifest AP-014 e roadmap `AMP-002`;
- `SKL-VIS-001`, Scientific Knowledge Layer Vision;
- `AP-015`, Scientific Knowledge Platform Architecture, stato planned;
- `AP-013`, Scientific Image Repository Architecture.
