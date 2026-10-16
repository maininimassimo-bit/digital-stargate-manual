# BKL-051 — passaggio offline dalle ricevute Owner al Worker

Stato: candidato tecnico, **R09 aperto / NOT_VALIDATED**, zero controlli reali qualificati.

Il modulo `tools.scientific_transients.owner_handoff` confronta una ricevuta di preparazione e tre ricevute di proiezione con il pacchetto locale registrato. Verifica le quattro operazioni staged conservate nel medesimo archivio locale, compresi richiesta, percorso, conferma, chiave semantica e impronte. Nessun dato arbitrario della ricevuta può sostituire i tre input o il loro ordine: identità e associazioni sono derivate dal pacchetto e dal contesto congelato riverificati.

Le ricevute del browser sono dati di correlazione. Non sono credenziali o attestazioni di autenticità autonome. `projectionObserved:true` conferma l'esistenza registrata nella lettura autenticata che ha prodotto la ricevuta; `reservationFreshness:NOT_ATTESTED` non dimostra disponibilità corrente o diritto a un nuovo tentativo. Il passaggio al Worker mantiene `launchAuthorized:false` e `scientificValidation:NOT_VALIDATED`.

## Uso del comando offline

`python -m tools.scientific_transients.owner_handoff --help` mostra gli argomenti. Servono configurazione privata e impronta SHA256, ricevuta di preparazione e impronta del file, tre coppie `--projection-receipt PATH SHA256` nell'ordine dei file, e `--output` con percorso assoluto di un nuovo file esterno agli archivi e alle radici protette. Non esiste un'opzione di avvio. Il comando non legge credenziali, non crea trasporti di rete e non avvia processi nativi.

L'esportazione conserva intento, copie delle ricevute, handoff e completamento in una cartella esclusiva accanto ai pacchetti, senza alterare il contenuto del pacchetto registrato. Le scritture usano creazione esclusiva, flush, fsync e rilettura. Immediatamente prima dell'esportazione e dopo la rilettura della copia esterna vengono nuovamente controllate le sorgenti locali. Un file esterno già esistente resta invariato. Un'esportazione incerta conserva evidenze e blocco; non viene ripetuta implicitamente e richiede recupero assistito separato.

Il blocco di esportazione protegge la provenienza locale. Non sostituisce i controlli contro il replay del Worker. L'esecuzione Worker richiede ancora autorizzazione esplicita distinta, pacchetto mai avviato, confronto autenticato dei tre job correnti e nuova verifica prima di ogni frame. Una ricevuta di proiezione stabile può riguardare un job già consumato: il confronto Worker deve rifiutarlo come non fresco.

## Verifiche del candidato

Dodici test coprono associazione con i contesti tecnici applicativi sintetici, tre ricevute ordinate, namespace, campi inattesi, concessioni di avvio non ammesse, alias numerici dei booleani, operazioni staged incerte, esportazione esclusiva, errore di scrittura, output esistente, cambiamento delle sorgenti e delle copie conservate durante l'esportazione, riapertura del pacchetto registrato, comando offline e impronta del file ricevuta non corrispondente. La configurazione privata viene iniettata nei test CLI ed e verificata separatamente dai contratti del caricatore esistente. Il completamento richiede un'ultima rilettura coerente delle tre copie conservate, dell'output esterno e delle sorgenti; una discordanza conserva lo stato incerto e non viene ignorata.

Queste prove usano trasporti e dati sintetici. Non dimostrano autenticazione reale, avvio scientifico o qualificazione di controlli. Revisioni del candidato, CI sull'esatto commit e collegamento al flusso operativo completo restano gate distinti. Il recupero assistito di un processo o di un'esportazione incerta è ancora aperto.
