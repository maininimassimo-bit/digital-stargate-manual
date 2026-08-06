# Capitolo 12 - Il ciclo di vita dell'immagine scientifica

## Un file non è ancora un patrimonio

L'immagine astronomica nasce come file, ma il suo valore non è contenuto soltanto nei pixel. Dipende dalla possibilità di sapere da dove proviene, in quali condizioni è stata acquisita, quale strumento l'ha prodotta, se è rimasta integra e quali trasformazioni l'hanno condotta a un risultato successivo.

Un RAW senza contesto può essere visivamente affascinante e scientificamente fragile. Un'immagine finale può essere impeccabile e, nello stesso tempo, impossibile da ricostruire. Tra questi due estremi si colloca il ciclo di vita dell'immagine scientifica.

Digital StarGate affronta questo tema quando il patrimonio osservativo non può più essere considerato un sottoprodotto della notte. I dati devono sopravvivere agli spostamenti di cartelle, agli aggiornamenti software, al cambio delle persone e alle nuove domande. Per riuscirci, il progetto separa identità, contenuto, posizione, integrità, qualità e provenance.

Il principio è esigente ma chiaro: conservare un file non equivale a conservare la conoscenza necessaria a comprenderlo.

## Le classi dell'immagine

Nel linguaggio quotidiano si parla genericamente di “immagini”. Il modello di repository scientifico distingue invece classi con responsabilità diverse.

I RAW originali sono il risultato diretto dell'acquisizione. Non devono essere modificati o sostituiti. I file di calibrazione originali, come bias, dark e flat, conservano anch'essi un legame con configurazione e periodo di validità. I master di calibrazione sono prodotti derivati e richiedono la storia degli input e del processo che li ha generati.

Seguono frame calibrati, registrati e integrati, prodotti intermedi, immagini elaborate e versioni destinate alla pubblicazione. Esistono inoltre asset tecnici e documentali: manifest, report, workflow e note.

La classificazione non serve a creare etichette decorative. Determina regole di immutabilità, retention, accesso, backup, qualità e provenance. Un RAW originale e una preview non richiedono lo stesso trattamento. Un prodotto pubblicabile non deve sostituire il dato dal quale deriva.

Il sistema conserva quindi una famiglia di oggetti collegati. La storia non è una linea nella quale il nuovo cancella il precedente, ma una rete nella quale ogni derivazione mantiene il riferimento alle proprie origini.

## L'immutabilità dei RAW

La prima regola di AP-013 è la RAW immutability. L'originale non viene sovrascritto, corretto o aggiornato in posizione come se fosse un documento di lavoro.

L'immutabilità non significa che il file non possa essere copiato. Significa che ogni copia governata deve rappresentare lo stesso contenuto e che eventuali trasformazioni producono nuovi asset. La distinzione protegge il punto di partenza del processo scientifico.

Se un RAW viene alterato, la catena successiva perde un riferimento stabile. Non è più possibile stabilire se una differenza nel risultato dipenda dal processing o dal cambiamento dell'input. La stessa minaccia esiste quando un file viene rinominato o spostato e il sistema usa il path come unica identità.

Digital StarGate assegna quindi un asset ID indipendente dal luogo fisico. Il path diventa uno storage locator. Lo stesso asset può avere più locator, per esempio una copia nell'archivio attivo e una nel backup. Il cambiamento di posizione non modifica l'identità scientifica.

Questa separazione rende possibile migrare lo storage senza perdere i riferimenti e riconciliare catalogo e file anche dopo una riorganizzazione.

## Il checksum come ancora

Il nome di un file dice come lo chiamiamo. Il checksum aiuta a stabilire se il suo contenuto è rimasto lo stesso.

Applicando un algoritmo dichiarato al contenuto si ottiene un'impronta. Il confronto della stessa impronta in momenti o posizioni differenti permette di rilevare corruzioni e discrepanze. Il checksum non sostituisce backup, autorizzazioni o controlli di qualità, ma fornisce un'ancora per l'integrità.

Nel modello Digital StarGate, l'Integrity Record collega asset, algoritmo, valore, timestamp e risultato della verifica. Questo dettaglio evita di trattare il checksum come una stringa eterna priva di contesto. Algoritmi, profili e politiche possono evolvere; la verifica deve rimanere interpretabile.

Anche i manifest e gli evidence bundle possono avere checksum. In quel caso l'impronta protegge la rappresentazione canonica dell'oggetto e aiuta a dimostrare che il set esaminato non è cambiato dopo la review.

Il checksum risponde alla domanda “è lo stesso contenuto?”. Non risponde a “è un buon dato?”, “è stato acquisito correttamente?” o “è autorizzato?”. Integrità, qualità e governance restano dimensioni distinte.

## Spostare senza perdere

Il trasferimento è uno dei momenti più delicati del ciclo. Si parte da una sorgente vicina all'acquisizione e si raggiunge un archivio destinato alla conservazione e al processing. Una copia incompleta o una collisione silenziosa può compromettere il patrimonio pur lasciando apparentemente presenti i file.

Digital StarGate progetta il Session Importer come processo pull-based: il PC principale legge una condivisione EAGLE autorizzata. Nel pilot, la sorgente è read-only e la cancellazione è esclusa. Prima di qualsiasi copia vengono controllati attività di acquisizione, stabilità della sessione, raggiungibilità, spazio disponibile, collisioni e possibilità di scrivere log ed evidence.

Il trasferimento non pubblica immediatamente i file come sessione completata. Usa un'area di staging. Solo dopo la verifica, il contenuto può essere promosso alla destinazione finale.

La collision policy impedisce di affidarsi al nome. Se esiste un oggetto con stesso nome e stesso checksum, può essere riconosciuto come duplicato confermato. Se il nome coincide ma dimensione o hash differiscono, il processo si blocca. Nel pilot non rinomina automaticamente per “far funzionare” la copia.

L'idempotenza garantisce che ripetere la stessa operazione non generi copie incontrollate. Una seconda esecuzione deve riconoscere ciò che è già stato verificato, identificare i candidati duplicati o fermarsi davanti a un conflitto.

## Copy-only come scelta di maturità

La modalità iniziale è `COPY_ONLY`. Non è una limitazione accidentale, ma una decisione architetturale.

La copia è reversibile: se qualcosa non è corretto, la sorgente conserva gli originali. La cancellazione cambia invece il profilo di rischio. Richiede retention, backup, recovery verificato, authority distinta e una prova molto più forte.

Il Transfer Readiness Gate stabilisce condizioni non derogabili: permessi sulla destinazione, protezione dalla fuga del path, collision handling, spazio, stability check, manifest immutabile, evidence bundle, pilot limitato e four-eyes approval. La prima esecuzione reale deve riguardare al massimo una sessione approvata e prevedere revisione manuale.

La source cleanup rimane una decisione separata e successiva. Anche se il pilot di copia dovesse passare, non sarebbe automaticamente autorizzata la cancellazione dall'EAGLE.

Questo è un esempio di progressione controllata. Il sistema ottiene valore presto, perché può scoprire e copiare, senza assumere immediatamente la responsabilità irreversibile della rimozione.

## Il lifecycle non è una lista di cartelle

Una rappresentazione ingenua del ciclo potrebbe essere: RAW, calibrato, registrato, integrato, finale. È utile per orientarsi, ma non basta.

Ogni passaggio può avere più tentativi, parametri, versioni e decisioni di qualità. Uno stesso RAW può partecipare a processing run differenti. Un master può essere sostituito da una versione migliore senza cancellare il precedente. Un prodotto finale può essere superseded, mantenendo la storia che spiega perché.

Digital StarGate rappresenta quindi il lifecycle come stati e relazioni. Gli asset derivati indicano i parent. Le processing run consumano input e producono output. Gli eventi registrano transizioni, attore, motivazione ed evidence. La supersession non riscrive il passato: collega una nuova versione a quella precedente.

Lo stato `deleted` non è considerato ordinario. Una cancellazione richiede policy, autorizzazione, retention e audit. Questa scelta cambia il comportamento dell'organizzazione: prima di liberare spazio occorre conoscere il ruolo dell'asset, le copie disponibili e il rischio di perdere una parte della catena.

## Provenance: la storia delle trasformazioni

La provenance risponde a una domanda che il solo file finale non può risolvere: come siamo arrivati qui?

Ogni Processing Run dovrebbe identificare gli input, gli output, il workflow, i passaggi, i parametri disponibili, l'ambiente software, l'operatore, i timestamp e lo stato. Gli step manuali non vengono nascosti; sono dichiarati. I valori non acquisibili restano sconosciuti o vengono inseriti con provenienza esplicita.

Il modello non pretende che ogni gesto storico possa essere ricostruito retroattivamente. Sarebbe pericoloso completare la catena inventando ciò che manca. La provenance futura può diventare più ricca; quella passata conserva i propri limiti.

Questa disciplina permette di confrontare risultati. Se due integrazioni della stessa sessione producono esiti differenti, il lineage aiuta a distinguere cambiamenti negli input, nel workflow, nei parametri o nell'ambiente. Senza provenance, il confronto resta affidato alla memoria e alla somiglianza visiva.

La riproducibilità non significa necessariamente che ogni processing manuale possa essere eseguito in modo identico. Significa almeno che le condizioni note, le scelte e le lacune sono sufficientemente documentate per comprendere il percorso.

## PixInsight dentro un boundary governato

PixInsight è centrale nel processing, ma non diventa per questo la fonte autorevole del catalogo. Digital StarGate introduce un boundary di sincronizzazione.

Un exporter può produrre un manifest dichiarativo dal workspace. L'adapter valida schema e dimensioni, normalizza i valori, riconcilia identificatori con AP-013 e AP-014 e registra l'esito. I riferimenti a input e output sono dichiarazioni della fonte finché non vengono confrontati con asset e checksum governati.

Lo stesso manifest ripresentato non deve creare una nuova storia. L'idempotency key consente di riconoscere un duplicato. Lo stesso identificatore con contenuto diverso produce un conflitto, non una sovrascrittura.

Gli esiti possono essere matched, partially matched, unresolved, conflict, rejected o duplicate-noop. Nessuno di essi promuove automaticamente un prodotto ad accepted. Un conflitto con la provenance autorevole viene registrato e AP-013 prevale.

Il valore del boundary consiste nel far entrare informazione senza trasferire autorità. PixInsight contribuisce alla storia del processing; non può modificare checksum, stato di acceptance o verità degli asset.

## Qualità lungo il ciclo

La qualità non appare soltanto alla fine. Può essere osservata durante acquisizione, trasferimento, calibrazione, registrazione, integrazione e review.

Una misura come FWHM ha significato nel proprio contesto: strumento, filtro, esposizione, condizioni e metodo. Un flag di qualità deve indicare a quale asset o sessione si riferisce e quale regola lo ha prodotto. La stessa metrica può essere utile per selezionare frame, confrontare notti o valutare il risultato di un workflow.

Il modello separa misurazione e decisione. Una misura registra un'osservazione. Una quality review interpreta più segnali e assegna uno stato secondo criteri. Un prodotto non diventa valido soltanto perché possiede molte metriche.

Anche l'assenza di qualità è informazione. Un asset privo di misure non viene promosso sulla base di una media di sessione o di un valore stimato. Può essere catalogato con stato non valutato e diventare oggetto di un backlog di enrichment.

Questa onestà permette agli analytics futuri di distinguere tra cattiva qualità e qualità non conosciuta.

## Conservazione, backup e recovery

Un repository scientifico non è pronto soltanto perché riceve file. Deve dimostrare che può conservarli e recuperarli.

La durabilità richiede copie indipendenti, controlli periodici di integrità, retention e restore testato. Un backup non verificato è una promessa. Un restore senza confronto dei checksum può restituire file presenti ma alterati.

Lo storage può essere organizzato in livelli diversi: archivio attivo per il lavoro corrente, capacità più economica per la conservazione, copia protetta per il recovery. Il catalogo mantiene locator logici e stato delle copie senza confondere disponibilità immediata con esistenza dell'asset.

Quando un locator non è raggiungibile, l'identità dell'asset non scompare. Il sistema può esporre che il contenuto è noto ma temporaneamente indisponibile. Quando una verifica rileva mismatch, apre un finding e impedisce di trattare quella copia come integra.

Il repository diventa affidabile quando il ciclo include anche la prova di poter tornare indietro dopo una perdita.

## GitHub conserva conoscenza, non pixel

La vision SIR-VIS-001 stabilisce un confine importante. GitHub mantiene architettura, contratti, manifest, workflow, checksum, riferimenti allo storage e storia delle elaborazioni. I binari voluminosi restano nello storage scientifico esterno.

Questa separazione evita di trasformare il repository documentale in un archivio inadatto. Allo stesso tempo, impedisce che lo storage diventi una scatola opaca. Le informazioni necessarie a capire gli asset rimangono versionate e revisionabili.

Il catalogo può quindi essere ricostruito e confrontato. Gli asset sono accessibili tramite locator, ma la loro identità non dipende dal singolo percorso. La documentazione spiega i contratti e le decisioni; i manifest rappresentano le istanze; l'evidence sostiene le affermazioni.

Non esiste un unico luogo che debba fare tutto. Esiste una federazione di responsabilità collegate da identificatori e provenance.

## Lezione trasferibile

Il ciclo di vita insegna che la conservazione è un problema di significato prima che di capacità disco.

Un'organizzazione può possedere molte copie e non sapere quale sia autorevole. Può calcolare checksum e non aver mai provato un restore. Può conservare il prodotto finale e perdere la possibilità di spiegare le trasformazioni. Può raccogliere metadati ricchi e concedere a un tool di processing un'autorità che non dovrebbe avere.

Il modello replicabile parte da poche regole: originali immutabili, identità stabili, locator separati, checksum dichiarati, derivazioni con provenance, trasferimenti idempotenti, cancellazione come atto eccezionale e recovery verificato.

Il patrimonio nasce quando questi elementi consentono al dato di attraversare il tempo senza diventare anonimo.

## Verifica per il lettore

- Gli originali sono realmente distinti dai prodotti derivati?
- Un asset mantiene la propria identità quando cambia path?
- I checksum indicano algoritmo, momento ed esito della verifica?
- Il trasferimento usa staging, collision policy e idempotenza?
- Il pilot iniziale è copy-only e privo di cancellazione alla fonte?
- Ogni prodotto derivato conserva input, workflow e processing run?
- Gli step manuali e i valori sconosciuti restano visibili?
- Lo strumento di processing contribuisce senza diventare autorità?
- Backup e restore sono provati, non soltanto configurati?

Se il file finale può essere mostrato ma non ricondotto ai propri input, il ciclo ha prodotto un'immagine e perso una parte della conoscenza.

## Fonti del capitolo

- `SIR-VIS-001`, Scientific Image Lifecycle and Processing Provenance Vision;
- `AP-013`, Scientific Image Repository Architecture;
- `DSDM-001`, Scientific Data Manager Conceptual Model;
- `DSDM-003`, Contract and Manifest Model;
- `DSDM-004`, Session Importer Architecture and Safe Transfer Design;
- `AP-013`, Transfer Readiness Gate;
- `AP14-W06`, PixInsight Synchronization Adapter;
- Enterprise Data Governance Standard e `AP-002`.
