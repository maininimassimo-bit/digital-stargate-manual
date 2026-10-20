# BKL-051: conservazione dell'insieme dei prodotti nativi

`native_publication.py` collega le copie opache al terminale nativo e alla sua
ricevuta di disponibilità. È il componente di conservazione W7 del supervisore
in costruzione. Non avvia PixInsight, non decodifica immagini e non autorizza
la chiusura di processi o nuove esecuzioni.

Il ritorno locale include ora `liveVerification`, un oggetto costruito solo
dopo le verifiche finali. Mantiene la chiusura in memoria con le identità OS
originali di sorgenti, copie, controlli e marker, senza ricostruirle dal JSON.
Non mantiene nuovi handle file aperti: i blocchi nativi in lettura restano un
obbligo separato del supervisore. `verify()` rilegge impronte, identità,
attestazioni, inventari, annullamento e segnali. Un errore resta permanente
nell'oggetto anche quando il file o l'orologio viene ripristinato. Il supervisore
deve propagare l'incertezza e tentare il proprio segnale: una verifica successiva
al ritorno non scrive automaticamente un nuovo record di pubblicazione.

La copia `marker` esportata è indipendente dai record attesi privati; modificarla
non modifica i pin della verifica viva. `marker` e `markerSha256` restano metadati
serializzabili. L'intero risultato locale con l'oggetto vivo non è un protocollo
JSON e non va inviato al portale o persistito per ricostruire una sessione. Non
esiste una factory da marker JSON: il token interno non è un confine di sicurezza
contro memoria ostile nello stesso processo, ma impedisce la ricostruzione tramite
l'API prevista. La futura composizione deve conservare l'istanza esatta restituita.

Il flag del marker descrive il termine osservato alla pubblicazione. Una verifica
viva successiva può registrare un nuovo superamento noto per il solo cleanup,
senza riscrivere il marker o dichiarare accettazione. Un cambiamento del termine
durante la pubblicazione iniziale continua invece a farla fallire. La diagnostica
è memorizzata, non una nuova verifica. Tutti i risultati mantengono false le
autorità di chiusura, nuovo avvio e accettazione della misura. Restano necessari
prova causale, proprietà viva, metadati S6, blocchi, budget e assenza di qualsiasi
incertezza osservata; l'assenza dei file di segnale da sola non prova successo.

Anche `supervision-uncertain.json`, parziale o malformato, blocca prima della
prenotazione e nelle verifiche vive. L'inventario retained viene ricontrollato
dopo l'ultima rilettura del marker, prima di restituire un esito normale.

L'integrazione V2 richiede il keyword `bootstrap_session` vivo e un binding
con cinque campi, incluso `launchControlSha256`. Accetta soltanto il
parent-intent `DSG_NATIVE_LINEAR_PARENT_INTENT_V2`. L'ispettore del controllo
di avvio verifica i sorgenti attestati dalla sessione isolata; le attestazioni
del bootstrap vengono confrontate con il manifest e con i ruoli fissati nel
controllo. La sessione e i file vengono ricontrollati durante la conservazione.
Il callback fidato deve provenire dal bootstrap verificato: un oggetto Python
arbitrario che espone gli stessi metodi non costituisce una prova di esecuzione.

Sigillo, parametri V2 e quattro librerie native devono essere coerenti con il
controllo. Owner e owner-ready vincolano nonce, sessione, PID dichiarato,
impronte e termine del parent. La ricevuta `native-return.json` deve concordare
con terminale, ready e Owner. Il componente verifica questi legami documentali;
la proprietà effettiva del processo e la causalità del ritorno richiedono ancora
il supervisore con il suo handle vivo. Non vengono dedotte dal solo PID o JSON.

Il profilo bundle V2 applica `role=name` ai nomi fissi dei prodotti. Per un
terminale `COMPLETED_CONDITIONAL_COMPUTATION` richiede tutti i dodici prodotti:
avvio, log, risultato, evidenza, checkpoint e sette History. Rifiuta prodotti
di errore, viste dichiarate aperte, superamento nativo del termine e flag
scientifici diversi da null/false, NOT_VALIDATED e zero qualificati. Per altri
stati conserva i prodotti dichiarati anche quando restano viste aperte: tale
conservazione non dimostra completezza della History né chiusura sicura.

Il chiamante locale fidato fornisce le tre directory private dell'operazione,
le impronte del parent-intent e di sigillo/consenso già consumati dal supervisore,
il suo orologio monotono vivo e la scadenza dell'intero tentativo. Il componente
verifica i byte del parent-intent, percorsi canonici e identità delle directory,
sigillo e consenso. Non valida il consenso di avvio o la proprietà del processo:
questi obblighi restano al supervisore. Le identità OS private sono interi Python
fino a 128 bit; non vengono convertite in numeri JavaScript o affidate al nativo.

La prenotazione esclusiva `publication-intent.json` precede la lettura delle
ricevute. Qualsiasi `publication-uncertain.json` già presente, anche parziale o
malformato e senza prenotazione, blocca prima della creazione di nuovi file.
L'assenza della prenotazione non dimostra che il tentativo sia disponibile.
L'incertezza viene ricontrollata anche nelle verifiche finali. Un errore
successivo non rende disponibile il tentativo. La ricevuta
ready deve fissare l'impronta grezza del terminale, che dichiara prodotti unici
con nome, ruolo, impronta e dimensione. Il limite aggregato di 192 MiB e 20 file
include terminale, ready, native-return, Owner, owner-ready e marker finale
(per quest'ultimo è riservato 1 MiB). I metadati effettivi della directory del
parent hanno un limite separato di 16 MiB. Gli input sigillati, Owner e consenso,
con una riserva per l'annullamento, rispettano 200 MiB. L'inventario di lavoro
deve essere esatto: file estranei o variazioni dell'annullamento durante la copia
producono incertezza. Si applicano anche limiti per ruolo: risultato 8 MiB,
singola History 4 MiB, log 32 MiB, controlli JSON 1 MiB. I file immagine restano
byte opachi e non possono superare da soli il limite aggregato.

I limiti JSON profondità8/array20/stringa192/oggetto32 riguardano soltanto i
controlli del parent e terminale/ready. Il parser rifiuta duplicati decodificati,
chiavi di prototipo, float e costanti non finite. Risultato, evidenza nativa,
ricevuta di avvio, History e immagini sono copiati come byte opachi: il limite
array20 non viene imposto ai vettori del core. La validazione dei loro contenuti,
dei confronti nativi e delle History effettive resta al wrapper e al collaudo.

Ogni copia usa la creazione esclusiva e la verifica del componente di retention.
Prima e dopo il marker finale, tutti i file sorgente e conservati vengono riletti
con hash, dimensione e identità originali; vengono ricontrollati anche gli input
del parent, la prenotazione della pubblicazione e gli inventari. Il marker viene
riletto anche con l'identità originale del descrittore che l'ha scritto.
Sono richieste directory private quiescenti e un solo
scrittore nativo. Non si promette immunità da modifiche ostili concorrenti o
durabilità assoluta dopo perdita di alimentazione.

Ogni eccezione conserva file e prenotazione e tenta una sola scrittura esclusiva
di `publication-uncertain.json`. Anche il fallimento di questa scrittura viene
riportato al chiamante; non produce un esito positivo. Un errore dopo la scrittura
del marker può lasciare un marker apparentemente positivo insieme all'incertezza.
Il supervisore deve trattare questo caso come incerto: il marker da solo non
autorizza chiusura, recupero o un altro avvio.

La scadenza viene controllata prima e dopo la scrittura del marker. Un tentativo
già scaduto conserva soltanto le prove con overrun dichiarato. Se la scadenza
viene attraversata durante la scrittura, la funzione fallisce, preservando il
marker precedente e l'incertezza. Il supervisore deve comunque verificare il
proprio tempo vivo prima di qualsiasi decisione sul processo.

Il ritorno attesta soltanto l'insieme dei byte dichiarati e include sempre
`measurementAccepted:false`, `processClosureAuthorized:false` e
`newNativeStartAllowed:false`. I dodici nomi presenti non provano che il loro
contenuto sia un checkpoint valido o una History completa. Nessuna composizione
di produzione, accettazione scientifica o chiusura R01-R14 deriva da questo
componente. Le prove usano soltanto prodotti sintetici, compresi payload
deliberatamente opachi che non vengono presentati come file XISF validi.

Il profilo dell'adattatore nativo V2 aggiunge il segnale scratch
`native-publication-uncertain.json`: anche se parziale o malformato, blocca
prima della prenotazione e nelle verifiche prima e dopo il marker. Entrambi i
segnali, nativo e parent, sono ricontrollati anche dopo l'ultima rilettura e dopo
il controllo finale di tempo e directory, prima di restituire la ricevuta. Il segnale
non viene incluso tra i prodotti accettati. Se una sua scrittura fallisce,
l'assenza del file non dimostra il successo dell'esecuzione: questa funzione
non sostituisce il controllo dell'esito effettivo e del processo da parte del
supervisore.
