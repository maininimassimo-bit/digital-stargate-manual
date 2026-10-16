# BKL-051: composizione del ciclo di vita lineare V5

Stato: candidato di codice, senza CLI, preparatore o attivazione. Nessun nuovo
avvio/chiusura PixInsight, chiamata provider o cloud autorizzati da questo file.
Milestone aperta, `NOT_VALIDATED`, zero nuovi controlli reali qualificati.

`LinearNativeSupervisor` compone i registri monouso, i blocchi in lettura,
il binding dello stesso handle, i segnali, la conservazione, la verifica S6 e
la ricevuta di uscita S7. Richiede gli oggetti originali `NativeRunRecords`,
`NativeSupervisionSignals` e i gruppi statici `NativeReadLocks`. Non offre una
factory da JSON, directory o PID e non autentica il consenso attraverso dati.
Il futuro preparatore deve ottenere consenso fresco prima di ogni preparazione
o grant, creare il budget prima del primo IO e produrre le copie private, entry,
manifest, seal e controllo verificati. Non usare i vecchi grant o preparativi
come autorizzazione a chiamare questo componente.

La costruzione verifica contesto intatto, assenza di avvii/Owner precedenti,
tempo originale e copertura esatta dei blocchi statici. Una sola istanza è
ammessa sui registri. Non avvia processi; raggiunge `PREPARED_LIVE` soltanto
quando i gate del contesto fornito passano. Non dimostra da sola provenienza
scientifica, creazione preventiva del budget o autenticità del consenso: questi
restano obblighi espliciti del preparatore/driver ancora da costruire.

`start()` consuma il tentativo in memoria prima di ogni verifica operativa,
scrive e rilegge il registro di consumo prima dell'unico Popen, verifica ancora
i gate e assegna immediatamente il risultato Popen al supervisore prima di
qualunque diagnostica fallibile. Usa argv esatto e finestra nascosta, shell
disabilitata e DEVNULL senza pipe da drenare. Stdout non determina completamento.
Adotta il riferimento held nei segnali prima della cattura di PID/FILETIME,
scrive l'handshake Owner con ready nativo per ultimo e acquisisce i due blocchi
dinamici Owner. La guardia dei blocchi consente l'osservazione dopo scadenza nota;
i gate prima dell'avvio richiedono separatamente budget ancora valido.

`tick(cancel=False)` è esplicito: non esiste servizio dormiente, scheduler o
ricomposizione automatica. Scadenza monotona/UTC o annullamento esplicito portano
a `RETENTION_ONLY` e a una sola richiesta cooperativa di cancellazione. Essa
non prova arresto. Senza ritorno causale, un processo ancora attivo viene soltanto
osservato. Un processo già uscito senza ritorno resta prova incompleta, con il
fatto dell'uscita e il codice effettivo conservati.

Quando il ritorno è presente, la pubblicazione può essere tentata una sola volta.
Il risultato vivo passa alla verifica integrata e poi alla chiusura posseduta;
solo la ricevuta di uscita confermata porta a `CLOSED_RETAINED`. Un file di ritorno
parziale o incoerente causa incertezza, non un nuovo tentativo. Un esito positivo
non conta come accettazione scientifica o controllo nullo qualificato.

Ogni eccezione mantiene Popen, held, blocchi e risultati intermedi. L'incertezza
viene fissata prima di tentare una sola cancellazione e un solo record S7 di
incertezza, senza riparazioni, sovrascritture o crescita su ogni tick. Fallimenti
di queste scritture non riabilitano il contesto. In stato incerto i tick fanno
soltanto osservazioni limitate dell'handle già posseduto; non pubblicano, chiudono
o avviano di nuovo. Se l'uscita è stata effettivamente osservata ma una ricevuta
o verifica fallisce, lo stato è `EXIT_VERIFIED_EVIDENCE_UNCERTAIN`, senza fingere
che il processo sia ancora vivo. Perdita del genitore o EOF del futuro driver
non può produrre ripresa da PID: serve riconciliazione separata.

Le prove sono simulate: Popen è un oggetto fittizio senza processo, i blocchi e
le interrogazioni Windows sono sostituiti. Il percorso completo crea e verifica
byte sintetici opachi, metadati S6 e ricevuta S7, senza leggere pixel reali o
avviare/attendere/terminare PixInsight. Nessun risultato dimostra compatibilità
PJSR, esecuzione reale, modello fisico completo o indipendenza dei controlli.

Restano preparatore/driver, packaging e consenso fresco sul pacchetto esatto,
preflight nativo reale, controllo del mantenimento dei riferimenti nel driver,
rilascio esplicito dei blocchi dopo uscita verificata e gate R01–R14. Le risorse
restano riferimenti forti: questo componente non le libera implicitamente dopo
un errore. Rollback tramite revert del solo codice/test/documento, preservando
gli esiti incerti e senza autorizzare ripetizioni o cancellazioni.
