# Capitolo 7 - Decidere in modo tracciabile

## Ogni sistema contiene decisioni

Un osservatorio remoto contiene decisioni anche quando nessuno le ha chiamate così. La scelta di un apparato, il comportamento in assenza di rete, la posizione di un interlock, la conservazione di un file, la responsabilità di un allarme e il significato di “pronto” sono decisioni incorporate nel sistema.

Quando non vengono registrate, continuano comunque a produrre conseguenze. Soltanto, diventano difficili da vedere. Una persona nuova può interpretare una limitazione intenzionale come un difetto. Un aggiornamento può rimuovere una protezione perché non ne conosce la motivazione. Due gruppi possono risolvere lo stesso problema in modi incompatibili. Una scelta temporanea può sopravvivere abbastanza a lungo da sembrare permanente.

Digital StarGate trasforma progressivamente le decisioni implicite in artefatti collegati. Non per documentare ogni dettaglio, ma per proteggere le scelte che definiscono confini, responsabilità, rischi e direzione.

La tracciabilità non è la capacità di trovare un documento. È la capacità di seguire il percorso che va dal problema alla decisione, dalla decisione al cambiamento e dal cambiamento alla prova.

## Non tutte le decisioni hanno lo stesso peso

Trattare ogni scelta come una decisione architetturale renderebbe il processo ingestibile. Trattare ogni scelta come una nota informale renderebbe il sistema fragile. Serve una soglia.

Nel modello Digital StarGate, un ADR viene usato quando la scelta modifica un principio, introduce un confine, cambia un contratto pubblico, assegna authority, tocca safety o security oppure condiziona più release e capability. Il Decision Log conserva invece scelte operative reversibili, circoscritte a processo, organizzazione, naming o implementazione.

La distinzione riguarda il costo del cambiamento. Un ADR protegge una decisione la cui revisione richiede analisi delle conseguenze e spesso una nuova review. Una voce nel Decision Log può essere superata in modo più leggero, purché la sostituzione rimanga visibile.

Esistono poi altre categorie. Un compromesso accettato che produrrà costo futuro appartiene al Technical Debt Register. Un lavoro da eseguire appartiene al Backlog. Un difetto appartiene al sistema di issue tracking. Una variazione dell'ordine architetturale deve modificare la roadmap autorevole prima delle sue proiezioni.

Questa classificazione evita che la stessa informazione venga distribuita in luoghi differenti. La responsabilità di un registro è chiara proprio perché esclude ciò che appartiene agli altri.

## La domanda prima della risposta

Una buona decisione conserva il problema che cercava di risolvere. Senza contesto, la soluzione può apparire arbitraria.

Prendiamo il principio “nessun comando diretto dal portale agli apparati”. Letto come una regola isolata, può sembrare una complicazione. Ricondotto al contesto, rivela il proprio significato: il portale è esposto a evoluzioni di interfaccia, dipendenze di rete e rappresentazioni potenzialmente stale; gli apparati fisici richiedono precondizioni, audit, autorizzazione e protezioni locali. Collegare direttamente i due piani concentrerebbe troppa authority nel punto più visibile e più distante dal rischio fisico.

La decisione non è quindi “aggiungere un livello”. È preservare la separazione fra intenzione, autorizzazione, orchestrazione e controllo locale. Il livello è una conseguenza.

Registrare il contesto aiuta anche quando le condizioni cambiano. Se in futuro una nuova infrastruttura riducesse alcuni rischi, il progetto potrebbe rivalutare la scelta conoscendo il motivo originario. Senza contesto, resterebbero soltanto obbedienza o rimozione.

La tracciabilità rende le decisioni discutibili nel senso migliore: consente di riesaminarle con elementi nuovi senza cancellare il ragionamento precedente.

## Alternative e conseguenze

Una decisione acquista qualità quando dichiara almeno le alternative realistiche e le conseguenze accettate. Non serve un catalogo infinito. Serve dimostrare che la scelta non è stata presentata come inevitabile.

Nel caso della memoria istituzionale, un'alternativa potrebbe essere mantenere il contesto principale nella conversazione. È più immediata e richiede meno disciplina. Le conseguenze sono dipendenza dalla sessione, difficoltà di verifica e rischio di continuare da una baseline superata. La decisione di usare il repository come fonte autorevole accetta un costo: prima di agire bisogna leggere e verificare. In cambio, il contesto diventa ricostruibile.

Nel caso dei dati scientifici, un'alternativa potrebbe essere spostare rapidamente tutti i file e ripulire la sorgente. La scelta `COPY_ONLY` è più lenta e conserva duplicazioni temporanee, ma protegge l'irreversibilità finché integrità, manifest, readiness ed evidence non sostengono passi successivi.

Rendere esplicite le conseguenze impedisce di raccontare ogni decisione come vantaggio puro. Una buona architettura non elimina i trade-off; li rende governabili.

## Dal rischio alla decisione

Le decisioni più importanti non nascono soltanto da requisiti positivi. Nascono dai modi in cui il sistema può fallire.

Se uno stato meteo può essere stale, la decisione deve stabilire come viene rappresentata l'incertezza. Se una connessione può interrompersi durante un'operazione, la responsabilità della sicurezza non può risiedere esclusivamente nel remoto. Se un indicatore può essere interpretato come safe quando manca il dato, il modello degli stati deve distinguere unknown. Se un operatore può avviare un'azione ad alto impatto, authorization, four-eyes e audit diventano parti del disegno.

Digital StarGate collega driver e rischi alle capability e agli Architecture Package. Questo passaggio evita che il rischio rimanga confinato in un registro separato dal cambiamento. Un rischio deve motivare una capacità, un controllo o una condizione. A sua volta, il controllo deve poter produrre evidence.

La catena è semplice:

1. una condizione può produrre un danno o un'informazione falsa;
2. una decisione assegna il trattamento e l'autorità;
3. un cambiamento realizza il comportamento previsto;
4. una prova verifica il comportamento entro un perimetro;
5. una review valuta se il rischio residuo è accettabile.

Quando manca un passaggio, la tracciabilità segnala un debito reale. Un controllo senza prova non è ancora affidabile. Una prova senza rischio dichiarato può verificare il comportamento sbagliato.

## Assessment: distinguere fatto e giudizio

Prima di decidere, spesso occorre comprendere la baseline. Gli assessment Digital StarGate hanno questa funzione: osservano uno scope definito e distinguono fatti verificati, inferenze, raccomandazioni e validazioni non eseguite.

La distinzione è essenziale. Un file presente nel repository è un fatto verificabile. La conclusione che il sistema sia pronto può essere un'inferenza. La proposta di introdurre una capability è una raccomandazione. L'assenza di un ambiente o di un test è un limite della valutazione.

Se queste categorie vengono mescolate, la decisione eredita un livello di certezza fittizio. Una raccomandazione può essere citata come requisito già approvato. Una lettura del codice può essere narrata come comportamento runtime. Un punteggio elevato può nascondere condizioni ancora aperte.

Nel percorso Digital StarGate, assessment e review indipendenti rendono visibili questi confini. L'indipendenza non richiede necessariamente una grande organizzazione. Richiede che il ruolo di chi valuta sia distinto, nel momento della valutazione, dal ruolo di chi ha prodotto il package e che i criteri siano espliciti.

L'assessment non decide automaticamente. Prepara una decisione mostrando quale terreno è solido e quale richiede ancora verifica.

## Review e decisione non sono la stessa cosa

Una review architetturale valuta coerenza, completezza, rischio, operabilità, tracciabilità e qualità delle evidenze. Può approvare, approvare con condizioni o richiedere cambiamenti. La review non implementa e non sostituisce l'accettazione operativa.

Questa distinzione diventa evidente nelle baseline “approved with conditions”. L'espressione non è una formula diplomatica. Significa che il disegno ha superato un gate entro condizioni che restano identificabili e obbligatorie. Il valore della review dipende dalla permanenza di quelle condizioni nella memoria del progetto.

Se un package ottiene un punteggio alto ma mantiene aperti test di failure, ownership, audit o recovery, la tracciabilità deve impedire che il punteggio venga usato come certificato runtime. Digital StarGate conserva le condizioni nel registro e le collega a evidence e piani di chiusura.

La review decide sullo stato dell'artefatto architetturale. L'accettazione decide se una capacità può entrare nel perimetro operativo dichiarato. Tra le due possono esistere implementazione, test, evidence, re-review e autorizzazioni.

Separare i passaggi impedisce di saltare dalla qualità del disegno alla fiducia nel comportamento.

## Il registro di tracciabilità

Quando capability, package, decisioni, evidence e review aumentano, la memoria lineare non è sufficiente. Serve un registro capace di mostrare le relazioni e soprattutto le assenze.

L'Architecture Traceability Register di Digital StarGate descrive lo stato verificato di ciascuna capability, la fonte autorevole, l'implementazione o evidence disponibile, la review e la disposizione. Le righe non dichiarano soltanto ciò che esiste. Registrano ciò che non è ancora stato dimostrato.

Una capability può risultare parziale; un package può essere approvato con condizioni; un ambiente di simulazione può produrre evidence limitata; un comando runtime può restare non autorizzato. La precisione del registro impedisce che la maturità di un elemento venga trasferita per prossimità agli altri.

Il registro è particolarmente utile nei passaggi di handover. Un nuovo responsabile non deve rileggere tutto il corpus per scoprire che una condizione di audit è ancora aperta. Può raggiungerla dal punto in cui influisce sulla capability e poi verificare la fonte dettagliata.

Una matrice di tracciabilità non sostituisce il giudizio. Rende però costoso nascondere un salto logico.

## Decisioni reversibili e irreversibili

La velocità corretta di una decisione dipende dalla sua reversibilità. Cambiare l'organizzazione di una pagina è diverso dall'autorizzare la cancellazione di dati alla fonte. Sostituire un'etichetta è diverso dal modificare l'autorità di un interlock.

Digital StarGate applica implicitamente questa logica in più domini. Le scelte operative reversibili entrano nel Decision Log. Le scelte strutturali richiedono ADR. I trasferimenti scientifici iniziano con una modalità conservativa. I comandi remoti restano esclusi finché condizioni ed evidence non sostengono un ampliamento.

Il principio può essere espresso così: più una decisione è difficile da annullare, più deve essere forte la catena fra contesto, authority, evidence e review.

Questa regola contrasta una tendenza frequente dell'automazione. Un'azione facile da eseguire tramite software può essere difficile da invertire nel mondo fisico o informativo. Un clic può aprire una struttura, sovrascrivere una configurazione o cancellare un file. La semplicità dell'interfaccia non riduce l'irreversibilità dell'effetto.

La tracciabilità restituisce peso alla conseguenza, indipendentemente dalla facilità del gesto.

## Quando una decisione cambia

Un registro affidabile non cancella le decisioni superate. Le marca come sostituite, ritirate o rifiutate e collega la nuova scelta. Questo preserva la storia senza lasciare ambiguità sullo stato corrente.

La sostituzione deve dichiarare che cosa è cambiato: il contesto, il rischio, la tecnologia, la capacità o l'autorità. Se una scelta viene aggiornata soltanto perché il team ha dimenticato la precedente, il sistema non sta apprendendo; sta ripetendo.

In Digital StarGate, le decisioni che cambiano boundary, contratti, safety, security o data ownership richiedono una nuova valutazione formale. Le proiezioni vengono aggiornate dopo la fonte autorevole, non prima. Gli identificatori esistenti non vengono rinumerati per far apparire lineare un'evoluzione che non lo è stata.

Questa disciplina protegge il valore del case study. Il progetto non viene raccontato come se avesse conosciuto fin dall'inizio la forma finale. Le correzioni, le condizioni e i riallineamenti rimangono leggibili. È proprio questa imperfezione tracciata a rendere il modello trasferibile.

## AI e decisioni

L'AI può ampliare la capacità di confrontare fonti, individuare incoerenze, preparare alternative e verificare che una decisione tocchi registri correlati. Può aiutare a seguire una capability attraverso più documenti e segnalare affermazioni prive di evidence.

Non per questo diventa l'autorità della decisione. La qualità linguistica di una proposta non sostituisce ownership, rischio e accettazione. Un modello può suggerire che due fonti siano in conflitto; il sistema di governance deve stabilire quale prevale e chi può modificarla. Può formulare un ADR; il responsabile deve valutarne conseguenze e approvarlo secondo il processo.

La baseline Digital StarGate autorizza l'AI come collaboratore di engineering entro roadmap e boundary approvati. L'autonomia riguarda l'esecuzione del lavoro documentale e tecnico autorizzato, non la facoltà di cambiare unilateralmente authority, safety o contratti pubblici.

Questa distinzione anticipa un principio generale: l'AI può accelerare il ciclo decisionale soltanto se il ciclo esiste già. In assenza di registri, fonti e owner, accelera soprattutto la produzione di scelte difficili da ricostruire.

## Lezione trasferibile

Un sistema minimo di decisioni tracciabili può essere costruito con pochi artefatti ben separati:

1. un template per le decisioni strutturali con contesto, alternative e conseguenze;
2. un log per le scelte operative reversibili;
3. un registro di rischi e debito;
4. una roadmap che ordini il cambiamento;
5. una matrice che colleghi decisioni, implementazione, evidence e review;
6. stati espliciti per decisioni proposte, accettate, sostituite, rifiutate e ritirate.

La domanda di controllo è sempre la stessa: una persona che non ha partecipato alla discussione può capire perché la scelta esiste, quale versione è corrente, che cosa ha modificato e quali prove ne sostengono gli effetti?

Se la risposta è no, la decisione può essere corretta oggi ma resterà fragile domani.

## Verifica per il lettore

- Sai quali scelte richiedono un ADR e quali appartengono a un log operativo?
- Le alternative scartate e le conseguenze accettate sono visibili?
- I rischi motivano controlli e capability oppure vivono in un registro isolato?
- Una review con condizioni mantiene quelle condizioni collegate alla capability?
- Le decisioni superate restano rintracciabili senza confondere lo stato corrente?
- L'AI propone e verifica senza diventare implicitamente l'owner?

Quando una decisione non può essere ricostruita, il sistema conserva il risultato ma perde la propria capacità di apprendere.

## Fonti del capitolo

- Decision Log `DSG-GOV-DEC-001`;
- Architecture Decision Record `ADR-001`-`ADR-005`;
- Enterprise Metamodel e Architecture Traceability Register;
- assessment `EA-*` e `PAA-*`;
- review indipendenti `ARB-002`-`ARB-012`;
- Architecture Baseline Certificate `ABC-001`;
- `AP-010`, Enterprise Safety Assurance Architecture;
- `AP-012`, Enterprise Operations Center Architecture;
- `AP-013`, Scientific Image Repository Architecture;
- `AI_BOOTSTRAP.md`.
