# Capitolo 14 - Dal dato all'informazione

## Accumulare non significa comprendere

Un osservatorio digitale produce continuamente tracce: file scientifici, manifest, log, eventi, misure ambientali, stati operativi, configurazioni, report e risultati di processing. La quantità può crescere molto prima della capacità di interpretarli.

Il dato grezzo descrive un fatto nel linguaggio del sistema che lo ha prodotto. Un timestamp, una temperatura o un conteggio di frame non sono ancora un'informazione utile per decidere. Devono essere collocati in un contesto, sottoposti a regole di qualità e collegati a un oggetto riconoscibile.

Digital StarGate attraversa questo passaggio quando analytics e reporting iniziano a elaborare le sessioni. La piattaforma deve rispondere a domande che nessun singolo file risolve: quanta esposizione utile è stata raccolta per target? Quale attrezzatura era associata alle sessioni? Quali condizioni meteo hanno accompagnato i risultati? Dove si concentrano scarti o incompletezze?

Il Warehouse nasce per consolidare dati già interpretati e validati. Non è un luogo nel quale riversare ogni sorgente. È un livello che trasforma output eterogenei in data product coerenti per reporting, dashboard e analisi.

## La separazione dei livelli

L'ADR-003 stabilisce una decisione netta: il Warehouse non rilegge direttamente log, immagini o manifest. Consuma i dataset prodotti e validati dagli Analytics.

La separazione crea una catena di responsabilità.

L'Acquisition Layer produce dati e manifest vicini alla sorgente. Il Session Layer definisce il contesto temporale canonico. Gli Analytics interpretano, normalizzano e applicano regole di dominio. Il Warehouse valida e persiste dataset consolidati. Dashboard, report e altri consumer leggono i prodotti pubblicati.

Ogni livello può essere ripetuto e controllato. Se un parser cambia, l'impatto può essere tracciato fino ai dataset derivati. Se un consumer mostra un valore errato, si può stabilire se il problema appartenga alla sorgente, alla trasformazione, al Warehouse o alla visualizzazione.

Senza questa separazione, ogni dashboard finirebbe per rileggere i log secondo regole proprie. Gli stessi concetti assumerebbero significati diversi e ogni correzione richiederebbe interventi multipli.

La centralizzazione non consiste nel mettere tutto in un database. Consiste nel rendere comuni le interpretazioni autorevoli.

## Il Warehouse come fonte derivata

Il Warehouse è persistente e validato, ma rimane derivato. I suoi dataset possono essere autorevoli per reporting e analytics entro il loro contratto, senza sostituire manifest, asset registry o fonti operative.

Questa precisazione evita un equivoco frequente. Una tabella ottimizzata per l'analisi può denormalizzare, aggregare o classificare. È perfetta per calcolare indicatori, ma non sempre conserva ogni dettaglio della sorgente. Se viene usata per riscrivere il registro scientifico, la proiezione diventa indebitamente autorità.

Digital StarGate mantiene il lineage dalla fonte al data product. Ogni build deve essere riconducibile alla versione degli input, alle trasformazioni e all'esito dei quality gate. Il dataset pubblicato rappresenta quindi una vista controllata, non una verità senza origine.

Lo stesso principio vale per gli aggiornamenti. Se una regola di qualità cambia, una nuova build può produrre valori differenti. Il sistema deve poter spiegare che cosa è cambiato e, quando necessario, conservare la baseline precedente.

L'informazione è affidabile quando è utile al consumo e ancora riconducibile al dato dal quale deriva.

## Data product invece di tabelle anonime

Il Warehouse produce dataset dedicati a sessioni, target, equipment, weather e quality. Ciascuno ha un contratto, una granularità e un uso atteso.

Il dataset delle sessioni rappresenta episodi osservativi aggregati. Quello dei target permette di analizzare l'impegno nel tempo. Equipment collega configurazioni e componenti. Weather conserva condizioni rilevanti. Quality raccoglie indicatori e classificazioni.

Trattarli come data product significa assegnare ownership, schema, versione, criteri di accettazione e consumer. Non sono file generati incidentalmente da uno script. Sono interfacce informative.

Questa impostazione migliora anche la comunicazione tra team. Chi produce il dataset dichiara quali campi sono garantiti, quali possono essere sconosciuti e come vengono calcolati. Chi lo consuma evita di reinterpretare colonne o assumere significati non documentati.

Un data product può essere piccolo. Il carattere enterprise non dipende dal volume, ma dalla responsabilità con cui viene mantenuto.

## La qualità prima della pubblicazione

Il Warehouse applica quality gate agli input e agli output. Un input invalido non viene corretto silenziosamente. Un output non viene pubblicato soltanto perché il processo ha terminato senza eccezioni.

I controlli strutturali verificano presenza dei file, colonne obbligatorie e tipi di dato. I controlli semantici verificano relazioni, identificatori, intervalli, timestamp e coerenza tra sessioni, target, equipment e quality.

Gli esiti possono essere `valid`, `valid_with_warnings`, `invalid` o `not_built`. Questa classificazione permette di distinguere un problema bloccante da una incompletezza ammessa. Il warning non scompare: resta visibile al consumer e alla governance.

La presenza di un valore nel range non dimostra che sia corretto. La qualità semantica richiede anche contesto. Una temperatura plausibile ma attribuita alla sessione sbagliata può superare un controllo numerico e fallire quello relazionale.

Per questo i gate combinano schema, dominio e lineage. La qualità non è un filtro finale; è una proprietà costruita lungo la pipeline.

## Unknown, zero e assente

Una delle regole più semplici e importanti riguarda i valori mancanti. `Unknown`, zero e assente non sono sinonimi.

Zero può essere una misura valida. Assente può significare che il campo non appartiene a quel record. Unknown significa che il valore sarebbe pertinente ma non è conosciuto o non è stato verificato.

Se un campo mancante viene trasformato in zero, le aggregazioni possono produrre conclusioni false. Se viene eliminato, il consumer può non sapere che esiste una lacuna. Se viene stimato senza provenienza, l'ipotesi diventa indistinguibile dal fatto.

Digital StarGate preserva l'incompletezza e, dove necessario, aggiunge uno stato di qualità o una provenienza. Un filtro non registrato rimane unknown. Un alias non risolto rimane ambiguo. Una misura non disponibile non viene sostituita dalla media della sessione.

Questa disciplina può ridurre temporaneamente la bellezza delle dashboard. Aumenta però la loro onestà. Un indicatore completo costruito su correzioni invisibili è meno affidabile di uno parziale che espone le lacune.

## KPI con un contratto

Un KPI non è soltanto una formula. È un'affermazione sintetica che influenza attenzione e decisioni. Per essere governato deve dichiarare scopo, definizione, popolazione, finestra temporale, fonte, frequenza, owner, qualità e limiti.

“Ore di esposizione” può significare durata pianificata, durata acquisita, frame trasferiti, frame validi o integrazione accettata. Senza una definizione, lo stesso numero può raccontare cinque storie.

“Sessioni completate” richiede uno stato canonico. “Qualità media” richiede sapere quali asset e quali misure entrano nel calcolo. “Disponibilità del repository” deve distinguere servizio, locator e integrità del contenuto.

Il catalogo KPI di Digital StarGate collega indicatori a dataset e regole. La dashboard diventa una rappresentazione, non il luogo nel quale viene deciso il significato.

Un KPI maturo include anche una condizione di non calcolabilità. Quando gli input non soddisfano il livello minimo, il risultato dovrebbe essere unknown o non pubblicato, invece di apparire come zero o ultimo valore noto.

## Freshness e fiducia

Un dato corretto può diventare fuorviante se è vecchio. La freshness indica quanto tempo è trascorso dall'aggiornamento e se il valore è ancora utilizzabile per lo scopo.

Nel reporting storico, un dataset di ieri può essere perfettamente valido. In un Operations Center, lo stesso ritardo può rendere pericolosa un'indicazione. Il requisito dipende dal consumer.

Digital StarGate separa la data osservata, la data di elaborazione e la data di pubblicazione. Una dashboard dovrebbe mostrare la freshness della proiezione e non far sembrare live un dato batch.

Anche il Warehouse deve registrare build time, input version e stato. Se l'ultima build fallisce, il consumer può continuare a vedere l'ultima valida, ma deve sapere che non è aggiornata.

La fiducia nasce dalla combinazione di correttezza, completezza e attualità. Nessuna delle tre può essere dedotta semplicemente dal fatto che un numero sia visibile.

## Lineage della pipeline

Il lineage collega un record Warehouse alle fonti e alle trasformazioni che lo hanno prodotto.

Per una sessione aggregata, la catena può includere manifest, versione del parser, dataset analytics, quality gate e build Warehouse. Per un KPI, aggiunge definizione e logica di aggregazione. Per un report, include la versione del data product e il template.

Il lineage rende possibile l'analisi d'impatto. Se cambia una regola temporale della sessione, si possono identificare i dataset e gli indicatori da rigenerare. Se una sorgente viene corretta, si può stabilire quali prodotti siano diventati obsoleti.

Rende anche comparabili le versioni. Due report con numeri diversi possono essere entrambi corretti rispetto a baseline differenti. Senza lineage sembrano una contraddizione; con lineage diventano una storia di evoluzione.

La catena non deve necessariamente essere un grafo sofisticato fin dall'inizio. Può partire da riferimenti, digest e versioni. L'importante è che non venga persa nel passaggio tra livelli.

## Dal file Parquet alla decisione

Il formato di persistenza è utile, ma non è la trasformazione principale. La vera trasformazione avviene quando il dato viene reso comparabile e utilizzabile.

Un consumer non dovrebbe dover conoscere come N.I.N.A. nomina un file, come un log rappresenta un errore o come una cartella attraversa la mezzanotte. Dovrebbe ricevere session ID, target, intervallo, stato e qualità secondo un contratto.

Questo abbassa il costo delle domande. La dashboard può concentrarsi sulla visualizzazione. Il report può spiegare trend. L'analytics può confrontare sessioni e configurazioni. Il portale può federare la ricerca.

Ma l'astrazione non deve cancellare l'accesso all'evidence. Quando un numero influenza una decisione, il lettore deve poter scendere verso i record e le fonti pertinenti.

Digital StarGate combina quindi due movimenti: semplifica verso l'alto e conserva la tracciabilità verso il basso.

## Dashboard come proiezione

Una dashboard produce una sensazione di immediatezza. Colori, percentuali e trend sembrano descrivere direttamente la realtà. Invece rappresentano query, trasformazioni, filtri e scelte grafiche.

Il modello enterprise tratta la dashboard come consumer read-only. Non diventa fonte autorevole e non corregge i dati. Se rileva un'anomalia, apre un percorso verso la sorgente o un data issue.

Questo boundary è importante soprattutto quando la stessa interfaccia contiene elementi operativi. Stato osservativo, scientifico e tecnico devono essere distinti. Un KPI di qualità non deve essere scambiato per safety state. Un dato storico non deve autorizzare un comando.

La dashboard è potente quando riduce il tempo necessario a comprendere. Diventa pericolosa quando nasconde freshness, scope o qualità per apparire più completa.

Il buon design informativo non elimina l'incertezza; la rende leggibile.

## Correzione e rigenerazione

I dati evolvono. Un alias viene normalizzato, una regola corretta, un record completato. Il Warehouse deve poter rigenerare i data product in modo deterministico.

La rigenerazione non implica cancellare la storia. La build registra input, versione e risultato. Quando una correzione cambia un numero pubblicato, il change log spiega la ragione e l'impatto.

L'idempotenza garantisce che lo stesso insieme di input e la stessa logica producano lo stesso risultato. Se non accade, esiste una dipendenza non controllata o una fonte variabile da rendere esplicita.

Questo criterio diventa fondamentale quando l'AI partecipa all'enrichment. Un modello può suggerire una classificazione, ma il valore deve essere marcato come inferito, collegato alla versione del modello e separato dall'osservazione. La rigenerazione con un modello diverso non deve riscrivere retroattivamente il fatto.

La piattaforma conserva così sia la capacità di migliorare sia la possibilità di spiegare perché il risultato è cambiato.

## Errori che diventano informazione

Una pipeline matura non registra soltanto i dati validi. Registra perché alcuni record non sono entrati nel prodotto.

Un identificatore mancante, una relazione incoerente o un timestamp ambiguo diventano finding. La loro distribuzione può rivelare un problema di processo o di contratto. Se molte sessioni hanno equipment sconosciuto, non serve soltanto correggere il dataset: occorre migliorare la cattura della configurazione.

Il quality backlog è quindi una fonte di apprendimento architetturale. Mostra dove il sistema perde significato. Può guidare roadmap, controlli e priorità di automazione.

Nascondere gli errori per ottenere una build verde produce una pipeline apparentemente stabile e organizzativamente cieca. Esporli con severità e ownership permette di migliorare senza bloccare tutto indiscriminatamente.

L'informazione nasce anche dalla capacità di comprendere ciò che non ha superato il gate.

## Lezione trasferibile

Il passaggio dal dato all'informazione richiede tre discipline.

La prima è la separazione: sorgente, interpretazione, consolidamento e visualizzazione hanno responsabilità diverse. La seconda è il contratto: dataset e KPI dichiarano significato e qualità. La terza è la tracciabilità: ogni prodotto resta riconducibile a input e trasformazioni.

Non occorre iniziare con un grande data warehouse. È possibile partire da pochi data product ben definiti e da quality gate chiari. La maturità cresce quando nuove domande riusano significati comuni invece di ricostruirli ogni volta.

Il dato diventa informazione quando può sostenere una decisione senza nascondere da dove proviene e quanto possiamo fidarci.

## Verifica per il lettore

- Acquisition, Analytics, Warehouse e consumer hanno confini distinti?
- Il Warehouse consuma dati validati invece di reinterpretare ogni sorgente?
- Ogni dataset ha owner, schema, granularità e criteri di qualità?
- Unknown, zero e assente mantengono significati differenti?
- I KPI dichiarano popolazione, finestra, fonte e condizione di non calcolabilità?
- Le dashboard mostrano freshness e qualità?
- Una correzione può essere rigenerata e spiegata?
- Gli errori scartati alimentano un backlog di miglioramento?

Quando il numero è disponibile ma la sua definizione non lo è, l'organizzazione possiede una metrica e non ancora un'informazione.

## Fonti del capitolo

- `ADR-001`, Session Layer;
- `ADR-003`, Warehouse Engine;
- Architettura del Warehouse: overview, data flow, dataset e schema;
- Warehouse Validation and Quality Gates;
- `EA-002`, Integrated Repository and Warehouse Assessment;
- `AP-002`, Enterprise Data Governance;
- `AP-011`, Enterprise Analytics Platform Architecture;
- Analytics Data Pipeline Reference e Analytics KPI Catalog.
