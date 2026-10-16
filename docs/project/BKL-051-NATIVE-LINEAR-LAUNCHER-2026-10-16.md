# BKL-051 — launcher nativo e ricevuta causale

`native_linear_launcher.jsh` definisce `DSGNativeLinearLaunch(root, expected)`
senza eseguirlo al caricamento. È il template da includere dall'entry privata
del genitore, separato dalle quattro librerie e dagli input sigillati. Il
futuro genitore deve verificarne tutta la chiusura delle sorgenti e mantenere
gli handle di sola lettura che impediscono modifiche degli include fino al
termine. Il launcher non crea processi, consensi o autorizzazioni.

Gli argomenti letterali chiusi sono operazione, nonce, sessione, impronte di
sigillo/consenso/wrapper e termine UTC del genitore. Il launcher verifica le
impronte effettive e aspetta il controllo Owner ready, a intervalli di 10 ms,
entro il minore fra termine parent e 180 secondi dall'ingresso. Il budget
monotono è pari al residuo UTC all'ingresso, limitato a 180 secondi:
anche con UTC fermo, il timer non concede nuovi 180 secondi. Il launcher passa
al wrapper una funzione fidata viva di controllo del medesimo budget. Il
wrapper la consulta insieme al proprio timer durante calcolo e conservazione,
senza azzerare il residuo dopo l'attesa. È un parametro interno fra sorgenti
revisionate, mai una funzione caricata da JSON. I controlli sono
controlli cooperativi, senza promessa di interruzione forzata di una API.
Annullamento, regressione dell'orologio o segnale d'incertezza interrompono
l'attesa. Nessuna immagine viene creata durante l'attesa.

Il controllo nativo Owner confronta il PID effettivo e i vincoli di sessione
prima della chiamata al wrapper. Il termine Owner deve coincidere con quello
letterale dell'entry. Il wrapper esegue poi il proprio controllo indipendente.
Gli effettivi handle posseduti e l'autenticità di questi controlli rimangono
obblighi del supervisore futuro: un PID scritto in un file non basta.

Solo il ritorno effettivo della chiamata al wrapper permette di costruire
`native-return.json`. Il valore restituito completo deve coincidere con il
terminale riletto, il ready deve fissare quegli stessi byte e i controlli
Owner/sorgente devono mantenere le impronte iniziali. La ricevuta causale
`DSG_NATIVE_LINEAR_RETURNED_V1` fissa terminale, ready, wrapper, sigillo,
controlli Owner, PID e sessione. Non è inclusa fra i prodotti del terminale.

Il file prova soltanto che la chiamata è tornata. Non prova che il launcher
abbia terminato, che il processo sia uscito o che sia sicuro chiuderlo. Un
terminale fallito/incerto può avere una ricevuta causale valida; il supervisore
deve ancora applicare i controlli sullo stato, History/checkpoint, conservazione,
scadenze, segnali d'incertezza e handle vivo. Dopo un ritorno effettivo i soli
metadati possono essere conservati anche oltre il termine, per consentire il
successivo ripristino: ciò non autorizza un successo tecnico tardivo.

Il runtime viene inventariato entro 20 file e 192 MiB, includendo la ricevuta;
sono rifiutati nomi estranei, alias e aggregati eccedenti. Le letture dei
controlli hanno limite 1 MiB. La scrittura nativa è una scrittura scratch
protetta da assenza e singolo writer, non una creazione atomica esclusiva.
Qualsiasi errore tenta una sola scrittura del segnale d'incertezza senza
sostituirne uno esistente, conserva i file e rilancia l'errore; non ripete la
chiamata o la scrittura della ricevuta. File parziali e ricevute positive
precedenti non prevalgono sull'incertezza. I limiti sono verifiche di protocollo,
non una quota del filesystem o una sandbox contro lo stesso utente ostile.

## Prove e lavoro restante

Le prove usano File, ImageWindow, tempo, PID e attesa simulati, dati sintetici
e il core matematico reale. Alcune controprove modificano deliberatamente la
funzione simulata dopo l'esecuzione del wrapper per introdurre eccezioni o
file tardivi; non attestano l'identità del codice caricato in PJSR. Nessuna
immagine astronomica è elaborata e nessun processo PixInsight viene avviato.
Le precedenti prove dell'adattatore restano parte della regressione.

Restano entry CRLF e manifest operativi esatti, blocchi Windows sugli include,
pubblicazione parent V2 e supervisore completo con handle vivo. La compatibilità
reale PJSR e le sue risorse richiedono un preflight sintetico nativo con consenso
fresco separato, una volta revisionato il percorso completo. Nessuna nuova
esecuzione è autorizzata da questo componente. Rollback tramite revert dei
soli file di codice/test/documentazione, preservando ogni evidenza di tentativi.

Milestone OPEN / NOT_VALIDATED, varianza fisica completa e significatività
ancora sconosciute, zero nuovi controlli reali qualificati.
