# BKL-051: handle Windows di lettura dei file privati

`native_read_locks.py` implementa il vincolo del contratto supervisore V5 S3:
prima dell'avvio, aprire le copie private con `CreateFileW`, `GENERIC_READ`,
`OPEN_EXISTING` e solo `FILE_SHARE_READ`. Windows rifiuta accessi concorrenti
in scrittura e cancellazione/rinomina incompatibili. Nessun file viene creato,
modificato o cancellato dal componente. Gli handle non sono ereditabili.

`NativeReadLocks(records, guard=...)` richiede una lista chiusa di record
`{path,sha256,byteLength}`: percorsi assoluti canonici POSIX, senza link/reparse,
duplicati o hardlink; massimo 128 file, 512 MiB per file e 544 MiB complessivi.
Questi sono limiti generali della lettura dei pin del codice. Il chiamante deve
applicare anche i limiti più stretti del ruolo e del gruppo di input (200 MiB),
oltre alla propria lista esatta di input, entry e launcher. Non è un selettore
automatico di file da bloccare. Sono consentiti initializer vuoti approvati.

Il componente mantiene l'handle prima di interrogazioni fallibili. Identità,
dimensione, numero di link e tempi di creazione/scrittura vengono letti con
`GetFileInformationByHandle`; l'hash usa `ReadFile` sullo stesso handle, in
blocchi massimi di 65536 byte, senza riaprire il percorso per leggere il codice.
`verify()` ricontrolla pin e identità originali. `guard` è un controllo fidato che
deve sollevare un'eccezione se budget, sessione o segnali non sono validi; il suo
valore di ritorno non è una ricevuta di autorizzazione.

Se la costruzione fallisce, nessun oggetto utilizzabile per un avvio viene
restituito e gli handle già acquisiti vengono chiusi. Dopo la costruzione non
esistono finalizer né context manager che rilascino automaticamente i blocchi
in caso di un'eccezione del supervisore. Il chiamante deve conservarne un
riferimento vivo e chiamare `release()` soltanto quando non può esistere un
avvio, oppure dopo l'uscita effettivamente verificata del processo posseduto.
Un fallimento di verifica deve rendere incerto il supervisore: la funzione non
gestisce la sua macchina a stati. `release()` ritenta solo gli handle la cui
chiusura era fallita e non riapre file. Non prova l'uscita di un processo.

Le prove Windows usano soltanto file sintetici temporanei: lettura concorrente
consentita, scrittura e sostituzione impedite, scrittore preesistente respinto,
pin errato e hardlink rifiutati, rilascio dopo preparazione fallita. Nessun
processo PixInsight è stato avviato. Su altri sistemi queste prove sono escluse;
il componente rifiuta l'acquisizione fuori da Windows. La compatibilità degli
include e delle letture PJSR con questi handle richiede ancora un preflight
nativo distinto e autorizzato. Non è dimostrata dalle letture Python.

Il perimetro assume copie private, un chiamante fidato e nessuna modifica ostile
della memoria del processo. Non costituisce una sandbox contro lo stesso utente,
una prova di caricamento PJSR o una chiusura scientifica. Nessun avvio,
terminazione, grant, chiamata remota o accettazione deriva da questa utilità.
Rollback: revert del codice, senza rimuovere registri o prove di tentativi.

Riferimenti ufficiali consultati:

- [CreateFileW e modalità di condivisione](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [GetFileInformationByHandle](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfileinformationbyhandle)
