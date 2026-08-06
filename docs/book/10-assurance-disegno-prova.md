# Capitolo 10 - Assurance: dal disegno alla prova

## Un'architettura convincente non è ancora una capacità

Un documento può descrivere con precisione come dovrebbe comportarsi un sistema. Può definire stati, responsabilità, controlli, errori e recovery. Può essere coerente e superare una review indipendente. Tutto questo produce valore, ma non dimostra ancora che il comportamento esista nel runtime.

Digital StarGate rende esplicita questa distanza attraverso l'assurance: l'insieme di pratiche che collegano affermazioni, rischio, verifica, validazione, review e accettazione.

La domanda cambia. Non basta chiedere “il disegno è corretto?”. Occorre chiedere “quale prova sarebbe proporzionata all'affermazione che vogliamo fare?”.

Una policy può essere dimostrata da un documento approvato. Una regola applicativa richiede test. Un'integrazione richiede evidence nell'ambiente pertinente. Un comando su un apparato fisico richiede scenari controllati, autorità nominate, stop condition e osservazione dell'esito. Una capacità operativa richiede anche persone, procedure, recovery e accettazione.

L'assurance impedisce che la qualità della descrizione venga scambiata per qualità del comportamento.

## Verification e validation

Verification e validation rispondono a domande vicine ma differenti.

La verification controlla che un artefatto sia stato realizzato secondo il disegno e i requisiti. Una regola deny-by-default può essere verificata con test che mostrano il rifiuto di richieste non conformi. Un manifest può essere verificato confrontando checksum. Un workflow può essere verificato attraversando le transizioni previste.

La validation controlla che il sistema risponda correttamente al bisogno nel contesto d'uso. Non chiede soltanto se la regola funziona, ma se le condizioni, gli attori, le dipendenze e gli esiti rappresentano il mondo in cui la capacità dovrà operare.

Un simulatore può verificare che lo stato stale blocchi un comando. Non valida automaticamente il sensore reale, la latenza, il controller locale o il comportamento della cupola. Un ambiente isolato può dimostrare che i test continuano senza rete. Non valida da solo la perdita WAN dell'osservatorio, il routing reale o la chiusura fisica.

Digital StarGate usa entrambi i concetti senza fonderli. Una prova può essere corretta e importante anche quando non è sufficiente per l'uso operativo. Dichiararne il perimetro è parte dell'assurance.

## Evidence non significa allegato

Nel linguaggio comune, una evidence può sembrare un file aggiunto a fine lavoro. Nel modello enterprise è un oggetto governato.

Deve possedere identificatore, data, versione, owner, metodo, risultato, limitazioni e collegamenti a requisito, rischio, controllo o capability. Quando l'integrità è rilevante, conserva checksum e riferimenti immutabili. Quando descrive un'esecuzione, dichiara ambiente, configurazione, input e risultato.

La qualità non dipende dalla quantità di screenshot o log. Dipende dalla capacità di rispondere a domande precise: quale affermazione sostiene? In quale ambiente? Con quali esclusioni? Il risultato è ripetibile? Chi lo ha esaminato? Che cosa resta non dimostrato?

Digital StarGate adotta una tassonomia che distingue evidence documentali, configurative, sorgente, test, integrazione, operazioni e governance. La classificazione evita che un tipo di prova venga usato al posto di un altro. La presenza del codice non equivale a un test; il test non equivale a operazione; l'approvazione non equivale a esecuzione.

Una evidence forte rende più preciso il risultato e più visibili i suoi limiti.

## Il valore di un test che fallisce

La disciplina dell'assurance non richiede una storia senza errori. Richiede che gli errori siano conservati e interpretati.

Nella validazione integrata di AP-012, un workflow fallì inizialmente durante la build per alcune proprietà del simulatore. La correzione modificò soltanto quella qualità del codice, senza rilassare scenari, assertion o regole safety. Il nuovo run passò.

La sequenza fallimento, diagnosi, correzione e riesecuzione produce più fiducia di un risultato positivo privo di storia. Mostra che il quality gate ha rilevato un problema, che la remediation è circoscritta e che la prova è stata ripetuta.

Un progetto maturo non nasconde il tentativo fallito per rendere lineare il racconto. Conserva il difetto quando spiega l'evoluzione della prova. Al tempo stesso, non usa il successo successivo per estendere il significato del test oltre il suo scope.

L'evidence è credibile quando il progetto registra sia ciò che ha confermato sia il modo in cui ha reagito a ciò che non funzionava.

## Il perimetro ENV-011

ENV-011 è uno degli esempi più istruttivi del percorso Digital StarGate. L'esecuzione del 3 agosto 2026 avviene in ambiente Hyper-V isolato, con sistema guest identificato, baseline applicativa immutabile e modalità simulator-only.

Quattro test di dominio passano online e vengono ripetuti dopo la disconnessione dell'adapter di rete. La trascrizione registra assenza di route operativa e fallimento della connettività esterna. Manifest e fixture hanno checksum verificati; l'accesso a dispositivi fisici è dichiarato falso; non risultano credenziali Git persistite; la sincronizzazione temporale viene verificata.

Questi elementi formano una evidence tecnica sostanziale. Dimostrano che, nella configurazione descritta, i test deterministici continuano a passare senza rete e che il perimetro simulator-only è preservato.

Non dimostrano accesso alla produzione, identity system reali, routing dell'osservatorio, audit storage operativo, dispositivi, interlock, comandi C2-C4 o break-glass. Non autorizzano credenziali reali o controllo fisico. Inoltre, nella registrazione dell'esecuzione, l'attestazione indipendente nominativa rimane pending.

Il valore di ENV-011 deriva dalla precisione di entrambe le liste: ciò che prova e ciò che non prova.

## Simulazione come strumento di apprendimento

La simulazione consente di esplorare failure e condizioni rare senza esporre l'impianto al rischio. Può verificare transizioni, policy, blocchi, correlazione e recovery logic. Permette di ripetere scenari con input controllati e conservare evidence comparabili.

Digital StarGate usa fixture integrate per dimostrare che stati unknown o stale bloccano authorization e dispatch, che il failure di una dipendenza produce stato degraded e record correlati, che il ritorno al servizio resta negato finché stabilità, verifica safety indipendente e audit completeness non sono soddisfatti, e che una singola identità non può auto-approvare operazioni critiche.

Questi test confermano coerenza interna. Non sostituiscono l'organizzazione reale. Se tutte le identità nominate appartengono ancora alla stessa persona, il four-eyes non è operativo. Non sostituiscono nemmeno infrastruttura e fisica: un adapter disabilitato non prova il comportamento di un apparato.

La simulazione è potente quando viene usata come gradino, non come scorciatoia. Riduce l'incertezza prima dell'esposizione al rischio e identifica le condizioni necessarie per il test successivo.

## Review indipendente e punteggi

Una review indipendente valuta il package e le evidence rispetto a criteri dichiarati. Può produrre finding, condizioni, punteggi e decisioni. Il suo compito non è premiare il progetto, ma stabilire quale affermazione sia sostenibile.

ARB-010 assegna un punteggio molto alto al framework safety e lo approva con condizioni. La review dichiara però di essere documentale: non certifica sensori, soglie, collisioni, emergency transition o recovery. Le condizioni richiedono hazard register, validation plan, matrice di tracciabilità, failure injection ed evidence annex.

La final re-review ARB-012 riconosce la solidità degli scenari simulati e non operativi, con forte coerenza architetturale e safety integrity. Il punteggio enterprise/runtime è molto più basso, perché identità, routing, storage, trusted time, infrastruttura, apparati e autorità indipendenti non sono validati.

Il punteggio non è una media da usare come semaforo universale. Ogni dimensione conserva il proprio significato. Un 96 sulla safety integrity simulata non annulla un 55 sulla runtime readiness.

La decisione della review vale nella frase completa: approved with conditions, simulated and non-operational scope only.

## Le condizioni come parte del risultato

Una condizione aperta non è un dettaglio amministrativo dopo l'approvazione. È parte della decisione.

Per ARB-012, C04 rimane bloccata perché requester, approver, Safety Authority, Security Authority e audit indipendente non sono assegnati a identità distinte. Altre condizioni risultano passate soltanto in scope simulato. Le integrazioni operative, i comandi fisici e il recovery reale restano fuori evidence.

La disposition protegge il progetto da una lettura selettiva. È possibile affermare che la validazione integrata non operativa è passata. Non è possibile usare quella frase per abilitare runtime, break-glass o bypass locali.

Le condizioni devono restare collegate a owner, trattamento ed evidence attesa. Se scompaiono dalla dashboard o dalla release, la memoria del rischio viene interrotta.

L'assurance tratta quindi l'approvazione non come punto finale, ma come stato con confini. Una nuova evidence può chiudere una condizione; un cambiamento può riaprirla; una violazione può rendere nulla la decisione precedente.

## Dalla prova all'accettazione

La prova tecnica e l'accettazione operativa rispondono a autorità differenti.

Un team tecnico può confermare che i test passano. Un revisore può attestare che l'evidence è coerente. L'Architecture Review Board può approvare il package entro uno scope. Per entrare in operazione servono inoltre owner nominati, formazione, runbook, infrastruttura, access review, recovery, monitoraggio, rischio residuo e una decisione esplicita di readiness.

Digital StarGate mantiene separate queste soglie. ENV-011 registra technical evidence complete ma formal acceptance pending. La final re-review accetta lo scope simulato e vieta runtime enablement. La prevenzione consiste nel mantenere disabilitati adapter fisici e dispatch critici.

Questo approccio evita il passaggio implicito “il test è verde, quindi possiamo accendere”. Il verde appartiene a un ambiente, un commit, un insieme di scenari e un'autorità. L'operazione reale è un'affermazione più ampia e richiede una prova più ampia.

L'accettazione non ripete la verification. Stabilisce che l'insieme di tecnologia, persone e processi è pronto per il rischio dichiarato.

## Una scala progressiva di assurance

Il percorso può essere organizzato come una scala.

1. **Coerenza documentale.** Il modello definisce concetti, confini, responsabilità e criteri.
2. **Review architetturale.** Un soggetto distinto valuta il disegno e registra condizioni.
3. **Verification isolata.** Test deterministici dimostrano regole in un ambiente controllato.
4. **Validation integrata non operativa.** Più componenti e failure mode vengono verificati insieme senza runtime reale.
5. **Pilot limitato.** Un perimetro non distruttivo usa integrazioni più vicine alla realtà.
6. **Validation operativa controllata.** Attori, infrastruttura, recovery e, quando autorizzato, apparati vengono provati con stop condition.
7. **Accettazione e rilascio.** Authority competente accetta rischio residuo, migrazione e rollback.
8. **Assurance continua.** Incidenti, cambiamenti, drift e nuove evidence alimentano il riesame.

Non ogni capability richiede la stessa altezza della scala. Un catalogo read-only ha un profilo diverso da un comando di chiusura. La proporzionalità dipende dall'impatto e dalla reversibilità.

Il salto di un gradino deve essere una decisione esplicita, non una conseguenza dell'entusiasmo per il risultato precedente.

## Evidence by design

Quando la prova viene pensata alla fine, il sistema può non conservare gli stati, gli eventi o le correlazioni necessari per dimostrare il comportamento. Evidence by design significa progettare fin dall'inizio ciò che dovrà essere osservabile.

Un comando deve possedere identificatore e correlation ID. Le transizioni devono registrare attore, policy, stato precedente, decisione safety e outcome. Una sessione deve conservare configurazione e condizioni. Un test deve sapere quale requirement e hazard copre. Un recovery deve distinguere evento cessato e ritorno autorizzato.

Questa disciplina migliora anche l'operatività. Le stesse informazioni che servono al revisore aiutano l'operatore a comprendere un diniego, l'Incident Coordinator a ricostruire una sequenza e l'architect a decidere una remediation.

L'assurance non è quindi un livello esterno che controlla il sistema dopo la costruzione. È una proprietà dell'architettura che rende il comportamento interpretabile e discutibile.

## AI e assurance

L'AI può accelerare la raccolta e il confronto delle evidence. Può individuare riferimenti mancanti, confrontare risultati con acceptance criteria, riassumere limitazioni e segnalare una dichiarazione più ampia del perimetro dimostrato.

Non può trasformare una propria revisione tecnica in accettazione indipendente quando l'autorità richiesta è umana e nominativa. Nel caso ENV-011, una re-review AI può valutare la completezza tecnica del set; non sostituisce l'attestazione attribuibile prevista né la decisione ARB.

La distinzione preserva due valori. L'AI contribuisce senza essere esclusa dal processo; l'assurance conserva responsabilità, indipendenza e authority. Anche le analisi dell'AI devono indicare fonti, metodo, limiti e stato di approvazione.

Un sistema di assurance governato usa l'AI per aumentare la qualità della verifica, non per abbreviare artificialmente la catena di fiducia.

## Lezione trasferibile

Per ogni affermazione di readiness occorre poter compilare una frase completa:

> Abbiamo dimostrato **questo comportamento**, su **questa baseline**, in **questo ambiente**, con **questi scenari**, ottenendo **questo risultato**, entro **queste limitazioni**, esaminato da **questa autorità**.

Se un elemento manca, l'affermazione deve restringersi. Se cambia baseline o ambiente, la prova può richiedere ripetizione. Se il rischio cresce, deve crescere anche l'indipendenza e la concretezza dell'evidence.

L'assurance non rallenta il rilascio. Evita che un risultato locale autorizzi un rischio globale.

## Verifica per il lettore

- Verification, validation e acceptance sono distinte?
- Ogni evidence dichiara ambiente, baseline, metodo e limiti?
- I tentativi falliti e le correzioni restano tracciabili?
- I risultati di simulazione sono chiaramente separati dal runtime?
- Le condizioni aperte rimangono visibili dopo l'approvazione?
- I punteggi di review vengono letti per dimensione e scope?
- L'AI supporta la verifica senza sostituire l'autorità indipendente?

Quando una prova viene citata senza ambiente, esclusioni e autorità, il progetto conserva un risultato ma perde il significato che lo rende affidabile.

## Fonti del capitolo

- Enterprise Metamodel e Architecture Traceability Register;
- `AP-010` e `ARB-010`, Safety Assurance Architecture;
- `AP-012`, Enterprise Operations Center Architecture;
- `E-ARB012-INT-01`, Integrated Non-Operational Execution Evidence;
- `ARB-012-C04-W06`, ENV-011 Execution Result;
- `ARB-012-FRR-001`, Final Independent Re-Review;
- `ABC-001`, Architecture Baseline Certificate ed Evidence Annex;
- `AI_BOOTSTRAP.md`.
