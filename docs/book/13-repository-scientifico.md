# Capitolo 13 - Il repository scientifico

## Dal deposito al sistema di fiducia

La parola repository può evocare un luogo ordinato nel quale depositare file. Nel caso scientifico questa immagine è insufficiente. Un vero repository non è definito soltanto dalla capacità di ricevere dati, ma dalla fiducia che consente di attribuire a identità, integrità, relazioni e storia.

Digital StarGate arriva ad AP-013 dopo aver costruito sessioni, analytics, governance e una prima architettura enterprise. Il passaggio non consiste nel scegliere un disco più grande. Consiste nel decidere che le immagini sono asset scientifici con un ciclo di vita governato.

Il repository deve poter rispondere a domande che attraversano più sistemi. Quali RAW appartengono a una sessione? Dove sono le copie? Quale checksum è stato verificato? Quali calibrazioni sono applicabili? Da quali input deriva un prodotto? Quale processing run lo ha generato? Quale qualità è stata misurata? Esiste un backup recuperabile?

Se queste risposte dipendono dalla conoscenza personale di chi ha organizzato le cartelle, esiste un archivio. Se possono essere ricostruite attraverso identificatori, manifest, controlli ed evidence, comincia a esistere un repository scientifico.

## Un'architettura federata

AP-013 separa responsabilità che spesso vengono confuse.

Lo storage scientifico conserva i binari voluminosi. Il Scientific Asset Registry assegna identità e registra metadati, classi, checksum e locator. L'Observation Context collega gli asset a sessioni, target e configurazioni. Il servizio di provenance mantiene processing run e relazioni input-output. I servizi di preservation governano immutabilità, retention, backup e recovery. Il boundary di pubblicazione espone metadati verso il catalogo.

Nessun componente sostituisce gli altri. Lo storage non diventa catalogo solo perché possiede directory leggibili. Il catalogo non diventa storage perché contiene link. GitHub non diventa archivio dei RAW perché conserva manifest. PixInsight non diventa fonte autorevole perché produce un'immagine elaborata.

La federazione richiede più contratti, ma riduce la concentrazione di autorità. Ogni sistema può essere ottimizzato per il proprio compito e le migrazioni diventano possibili senza perdere l'identità logica del patrimonio.

Questa separazione è uno dei caratteri enterprise del modello: non un prodotto monolitico, ma responsabilità esplicite con confini verificabili.

## Il catalogo degli asset

Il Scientific Asset Registry registra ciò che l'organizzazione riconosce come asset governato. Ogni oggetto possiede un identificatore stabile e una classe. I locator indicano dove il contenuto può essere raggiunto. Gli Integrity Record indicano come e quando è stato verificato.

Il registro non deve necessariamente contenere ogni metadato fisico del file. Deve conservare quelli necessari a identità, governo e correlazione. Può riferire manifest più dettagliati e fonti specialistiche.

Un asset può avere più versioni o essere superseded. Può avere locator attivo, archivistico e di backup. Può essere disponibile in una posizione e non in un'altra. Può risultare integro, non ancora verificato o in mismatch.

La possibilità di rappresentare questi stati evita due semplificazioni pericolose: “il file esiste, quindi va bene” e “il path non funziona, quindi il dato è perso”. Il repository distingue esistenza logica, disponibilità fisica e integrità verificata.

Il catalogo degli asset è quindi una mappa di responsabilità, non un semplice indice di directory.

## Inventariare prima di migrare

Quando esiste un archivio storico, la tentazione è spostarlo subito nella nuova struttura. Digital StarGate adotta l'ordine opposto: prima inventory e discovery, poi decisione di migrazione.

L'inventario raccoglie path, dimensioni, estensioni, timestamp e, quando autorizzato, checksum. Classifica priorità e anomalie. Identifica duplicati, formati non riconosciuti, permessi insufficienti e strutture ambigue. Non modifica i file.

AP13-W02 definisce anche profili progressivi. Una scansione può partire dai soli metadati e crescere verso hashing e approfondimenti più costosi. L'autorizzazione alla lettura non implica automaticamente autorizzazione a calcolare tutto, copiare o pubblicare.

Questa gradualità protegge sorgente, prestazioni e riservatezza. Permette inoltre di capire il problema prima di scegliere la soluzione. Il volume reale, la distribuzione dei formati e la qualità dei nomi influenzano storage, tempi, rete e strategia di reconciliation.

Una migrazione senza inventario trasferisce anche ambiguità e duplicazioni. Un inventario senza decisione non risolve il problema, ma produce la mappa necessaria per intervenire consapevolmente.

## Il caso delle undici sessioni

La discovery AP-013 fornisce un esempio concreto. Il processo in sola lettura individua undici sessioni relative a LDN 1320 e ai calibration frame, distribuite tra il 7 e il 17 luglio 2026. Ricostruisce i gruppi, normalizza campi opzionali e verifica la coerenza delle esposizioni LIGHT con numero di frame e durata nominale.

Il dry run finale produce zero warning e zero finding bloccanti. Il parser viene verificato con test automatici. La technical validation della session discovery è dichiarata passata.

Ma l'evidence conserva anche i limiti. Il merge di sessioni attraverso la mezzanotte non è ancora implementato. Il calcolo dei checksum degli asset sorgente non appartiene a quello scope. Gli artefatti finali devono ancora essere acquisiti in un evidence bundle immutabile. Soprattutto, il transfer non è autorizzato.

Questo episodio mostra come il repository cresce attraverso affermazioni circoscritte. Esiste evidence che la discovery funziona su quel perimetro. Non esiste ancora la prova complessiva di preservation, restore e operational acceptance.

La forza del caso non sta nel presentare il repository come finito. Sta nel mostrare come una capacità viene resa dimostrabile senza anticipare lo stato successivo.

## Gate prima della copia

Il Transfer Readiness Gate traduce il rischio in condizioni verificabili. Prima di passare dalla discovery alla copia reale devono essere chiusi criteri su accesso, destinazione, stabilità, spazio, collisioni, manifest, evidence, rollback e responsabilità.

La sorgente resta read-only. La destinazione è confinata a una root governata. Un path che tenti di uscire dal perimetro deve essere rifiutato. Una collisione non può causare overwrite silenzioso. Ogni esecuzione produce log, manifest e checksum dell'evidence bundle.

Il pilot è limitato a una sessione. La review separa esecutore e revisore. La verifica finale include conteggi, dimensioni e un campione dei file secondo il livello autorizzato.

Questi controlli trasformano la copia da comando tecnico a operazione governata. Anche se l'implementazione del motore è disponibile, il gate resta l'autorità sulla sua attivazione. Il fatto che una funzione possa essere eseguita non significa che debba esserlo.

La distinzione tra implementazione e enablement è una delle lezioni più importanti di AP-013.

## Una strada protetta verso l'operazione

L'evoluzione successiva del repository aggiunge un motore `COPY_ONLY`, uno scheduler protetto e una prima evidence limitata. La roadmap riconosce questo avanzamento, ma mantiene AP-013 in stato active.

Restano aperti Architecture Review finale, Operational Acceptance Test e Operational Acceptance. La nota di stato non svaluta il lavoro effettuato; impedisce che una prova locale venga usata come certificazione dell'intera capability.

Il modello distingue almeno quattro livelli:

1. architettura e contratti definiti;
2. implementazione disponibile;
3. evidence tecnica su uno scope limitato;
4. servizio accettato operativamente.

AP-013 attraversa questi livelli in modo progressivo. Una copia limitata può dimostrare collision handling, verifica e assenza di cleanup. Non dimostra automaticamente durabilità a lungo termine, recovery dell'intero archivio, capacità operativa continua o segregazione completa dei ruoli.

Questa lettura protegge anche la comunicazione del progetto. “Motore completato” e “repository operativo” non sono sinonimi.

## Il repository come sistema di record

In un ambiente federato occorre dichiarare quale sistema sia autorevole per ciascuna informazione.

Lo storage è autorevole per la disponibilità del contenuto binario in una posizione. Il registro AP-013 è autorevole per identità, checksum, locator e provenance governata. GitHub è autorevole per architettura, contratti, workflow versionati ed evidence pubblicate. Il Warehouse è autorevole per i data product analitici curati. AP-014 costruisce proiezioni per discovery e ricerca.

Questa pluralità non significa relativismo. Al contrario, risolve i conflitti attraverso regole di precedenza. Se un adapter PixInsight dichiara un checksum diverso da AP-013, il record entra in conflict; l'adapter non sovrascrive la fonte. Se l'indice di ricerca contiene un record non più coerente, viene ricostruito dalle fonti autorevoli.

Il repository scientifico è affidabile quando ogni informazione sa da dove proviene e quale autorità può cambiarla.

## Reconciliation: riconciliare senza inventare

Catalogo e storage possono divergere. Una copia può essere spostata, un locator diventare obsoleto, un manifest arrivare in ritardo o un duplicato essere rilevato dopo l'ingestione.

La reconciliation confronta le rappresentazioni e classifica l'esito. Può confermare una corrispondenza, aggiungere un locator, segnalare un asset mancante, aprire un conflitto o mettere un record in quarantena.

Non corregge silenziosamente la fonte più debole copiando il valore più comodo. Registra il confronto, la regola applicata e l'eventuale decisione umana. Un valore non risolvibile rimane `unknown` o `unresolved`.

La reconciliation rende sostenibile la federazione. Senza di essa, la separazione tra sistemi produrrebbe lentamente copie incoerenti della verità. Con essa, le divergenze diventano osservabili e trattabili.

Anche l'indice di ricerca segue questo principio. È una proiezione ricostruibile. Se viene perso o corrotto, non deve diventare la fonte dalla quale ricostruire il registro.

## Conservazione e costo

Il patrimonio scientifico cresce rapidamente. La governance non può ignorare capacità, prestazioni e costi.

Non tutti gli asset devono risiedere nello stesso tier. I RAW originali richiedono durabilità e protezione. Alcuni intermedi possono essere rigenerabili, se il lineage e gli input sono completi. Preview e cache hanno un valore differente. I prodotti finali possono richiedere accesso rapido e versioni conservate.

Una policy di retention deve quindi partire dalla classificazione e dalla possibilità di ricostruzione. Eliminare un intermedio può essere accettabile soltanto se il workflow, gli input e l'ambiente necessari sono davvero disponibili. Dichiararlo rigenerabile senza aver provato la ricostruzione è un'assunzione.

Il costo non viene risolto cancellando indiscriminatamente. Viene governato distinguendo valore, rischio, frequenza d'uso e reversibilità. Anche la decisione di mantenere tutto per sempre crea rischi: costi crescenti, indici ingestibili e copie non controllate.

Il repository enterprise rende queste scelte esplicite e revisionabili.

## Sicurezza senza confondere safety

Il repository richiede access control, least privilege, secret handling e audit. Le identità che leggono la sorgente non devono necessariamente amministrare lo storage. I manifest non contengono password o token. Le aree di staging, pubblicazione e conservazione hanno permessi distinti.

Questa sicurezza protegge i dati, ma non attribuisce al repository authority sugli apparati. AP-013 non invia comandi a cupola, montatura o camera. Il database che registra una sessione non decide se l'osservatorio possa aprire.

La separazione riduce il blast radius. Un problema nel catalogo non deve trasformarsi in un percorso di comando. Un consumer analytics legge metadati in modalità read-only. Il portale può mostrare stato e incidenti del repository senza modificare la verità scientifica.

Il repository è parte dell'ecosistema operativo, ma conserva un boundary netto rispetto alla safety authority.

## Evidence del repository

Un repository non si accetta attraverso una sola dimostrazione. Le evidence devono coprire dimensioni diverse.

L'inventario dimostra che il patrimonio corrente è stato caratterizzato. I test di immutabilità mostrano che i RAW non possono essere sovrascritti attraverso i percorsi previsti. Le verifiche checksum dimostrano la capacità di rilevare mismatch. I transfer test coprono copy, collisioni, resume e failure. La reconciliation confronta storage e catalogo. I restore test dimostrano il recovery. Le review valutano contratti, rischi e responsabilità.

La completezza dell'evidence dipende dall'affermazione. Per un pilot basta un perimetro limitato e non distruttivo. Per dichiarare il repository operativo servono continuità, runbook, monitoraggio, retention, backup, restore, authority e accettazione.

La roadmap AP-013 mantiene visibili proprio le evidence mancanti. L'assenza non è una nota marginale: determina lo stato della capability.

## Dal repository al catalogo osservativo

AP-013 governa la verità degli asset. AP-014 ne governa la discoverability.

Il repository deve poter pubblicare metadati senza esporre credenziali o path sensibili. Gli identificatori stabili permettono al catalogo di collegare sessioni, target, acquisizioni e processing run. I checksum e la provenance restano sotto AP-013; AP-014 li consuma in sola lettura.

Questo boundary impedisce che l'esperienza di ricerca modifichi ciò che trova. Una query può filtrare, ordinare e spiegare il ranking. Non può promuovere un asset, riscrivere un manifest o cambiare un locator.

La separazione prepara il passaggio successivo del libro. Prima si costruisce un patrimonio affidabile; poi lo si rende interrogabile. La ricerca non deve compensare una fonte debole, ma proiettare una fonte governata.

## Lezione trasferibile

Un repository enterprise può essere valutato con cinque domande.

Possiede identità indipendenti dai path? Distingue storage e catalogo? Conserva integrità e provenance? Può riconciliare le divergenze? Ha dimostrato recovery e autorità operativa?

Molte soluzioni rispondono bene alle prime due e assumono le altre. Digital StarGate mostra invece una progressione nella quale ogni risposta richiede un artefatto e una prova proporzionata.

Il repository scientifico non è un prodotto che si installa. È un patto di continuità tra dati, sistemi e persone.

## Verifica per il lettore

- È chiaro quale sistema governa asset, locator, checksum e provenance?
- L'inventario precede la migrazione?
- Discovery, copia, cleanup e accettazione hanno gate distinti?
- Il pilot è circoscritto e reversibile?
- Le divergenze tra storage, registro e catalogo vengono riconciliate?
- Le retention policy dipendono dalla classe e dalla rigenerabilità provata?
- Gli accessi al repository restano separati dal controllo degli apparati?
- L'evidence copre anche restore e operatività, non soltanto la copia?

Quando il repository viene descritto soltanto attraverso lo spazio disponibile, la tecnologia ha già nascosto il problema più importante: chi garantirà il significato nel tempo.

## Fonti del capitolo

- `AP-013`, Scientific Image Repository Architecture;
- `AP13-W02`, Current-State Scientific Asset Inventory Specification;
- `DSDM-001`-`DSDM-004`;
- `E-AP013-SD-001`, Session Discovery Execution Evidence;
- `AP-013`, Transfer Readiness Gate;
- `SIR-VIS-001`, Scientific Image Lifecycle and Processing Provenance Vision;
- roadmap `AMP-002` e proiezione evidence AP-013;
- `AP-014`, Scientific Observation Catalog and Search.
