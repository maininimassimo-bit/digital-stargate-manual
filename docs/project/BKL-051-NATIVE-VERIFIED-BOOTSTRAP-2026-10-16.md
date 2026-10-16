# BKL-051 — bootstrap verificato del supervisore

Il candidato aggiunge `native_verified_bootstrap.py` al caricatore già
revisionato. La costante `ENTRY` contiene l'intera sorgente letterale da
passare a Python con `-I -S -B -c`. L'invocazione revisionata deve contenere
esternamente il percorso e SHA256 del bootstrap e del suo manifest: generare
nuove impronte dai file correnti non equivale ad approvarli.

Prima di eseguire codice del progetto, l'entry legge al massimo 1 MiB di
sorgente bootstrap, verifica l'impronta e compila proprio quel buffer. Il
bootstrap verifica schema chiuso del manifest, impronta dell'entry, versione
Python esatta ed eseguibile effettivo, sorgente del caricatore e manifest delle
sorgenti. Compila il buffer verificato del caricatore, che verifica a sua volta
ogni sorgente locale prima di importarla. Nessun bytecode o percorso alternativo
viene usato per eseguire codice del progetto.

Il manifest `DSG_NATIVE_BOOTSTRAP_MANIFEST_V1` contiene soltanto protocollo,
`bootstrapSha256`, `entrySha256`, `pythonVersion`, `pythonExecutable`,
`pythonExecutableSha256`, `loaderPath`, `loaderSha256`, `sourcesManifestPath`,
`sourcesManifestSha256`, `entryModule` e `entryCallable`. Il modulo di ingresso
deve essere una sorgente esplicitamente sigillata; il comando di ingresso deve
essere una funzione definita in quel modulo. Riceve una sessione viva con
`assert_intact()`: il controllo verifica i moduli caricati e anche byte e
identità dei file di bootstrap, runtime, caricatore e dei due manifest.
Viene eseguito prima e dopo il comando; il futuro supervisore deve richiamarlo
prima di ciascuna decisione sensibile.

La sessione espone inoltre due attestazioni vive, precedute e seguite dal
medesimo controllo: `attest_sources()` restituisce copie delle impronte dei
buffer approvati, inclusi gli initializer e i due moduli eseguiti dal bootstrap;
`attest_bootstrap()` restituisce le impronte di manifest/entry/sorgenti del
bootstrap e i dati del runtime verificato. L'elenco delle sorgenti comprende
anche i moduli autorizzati non ancora importati; le identità dei moduli
effettivamente caricati sono controllate separatamente dal loader. I namespace
senza sorgente non diventano file inventati. Non viene calcolata una nuova
impronta per accettare un file alterato come codice già eseguito.

Il supervisore dovrà usare queste attestazioni per confrontare il proprio
controllo di avvio, verificando anche i ruoli di runtime e bootstrap. Le copie
restituite non conferiscono autorità fuori dalla sessione viva né sostituiscono
il futuro controllo dell'handle del processo.

Percorsi assoluti canonici, file regolari privati, assenza di alias e limiti
sono verificati. Manifest e sorgenti bootstrap/loader hanno ciascuno limite
1 MiB; eseguibile Python 16 MiB; le sorgenti locali mantengono i limiti del
caricatore. Il runtime standard, il sistema operativo e l'invocazione esterna
revisionata sono il confine fidato. Non è un isolamento da alterazioni ostili
della memoria da parte dello stesso utente. Non sono letti dati astronomici.

## Evidenza e lavoro restante

Le prove avviano soltanto Python isolato su moduli sintetici: successo con
impronte esatte, alterazioni prima e durante il comando, identità sostituite,
runtime errato, schema estraneo, ingresso non sigillato ed eccezione propagata.
Non creano un consenso, un grant o una preparazione di analisi. I manifest
prodotti nei test sono fixture sintetiche, non un'invocazione operativa approvata.

Restano il driver del supervisore, i suoi gate ai confini operativi, la chiusura
delle dipendenze effettive del driver, il controllo del processo posseduto e
il protocollo nativo V2. L'invocazione operativa con esatti file/versioni e il
preflight nativo richiederanno revisione e consenso separati, una volta concreti.
Importare normalmente questo modulo non verifica il bootstrap e la sua funzione
di ingresso rifiuta l'assenza dell'attestazione prodotta dall'entry letterale.

Rollback tramite revert dei tre nuovi file. Nessuna modifica alla pagina
Owner, alle credenziali, al cloud o ai file di immagini. Milestone OPEN /
NOT_VALIDATED, zero nuovi controlli reali qualificati.
