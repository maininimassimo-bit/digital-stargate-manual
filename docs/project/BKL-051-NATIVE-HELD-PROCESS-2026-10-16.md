# BKL-051: identità del processo conservata nella sessione viva

`native_held_process.py` prepara il vincolo del supervisore V5 S5. Non avvia,
riapre, enumera, attende o termina processi e non legge PID da file. Il chiamante
deve aver già assegnato al supervisore l'esatto oggetto restituito dall'unico
`subprocess.Popen` autorizzato, prima di qualsiasi interrogazione fallibile.

`HeldNativeProcess(process)` conserva un riferimento forte a quell'oggetto;
accetta solo il tipo Popen esatto, non PID, dizionari o sue sottoclassi. Questo
controllo di tipo non dimostra comando, provenienza dell'avvio o consenso:
restano responsabilità della futura composizione fidata del supervisore.

`capture()` è monouso anche quando fallisce. Legge l'handle Windows posseduto
dall'oggetto, interroga `GetProcessId` e `GetProcessTimes` sullo stesso valore,
e confronta il PID con quello di Popen. Il tempo di creazione FILETIME è
conservato come stringa esadecimale di 16 caratteri, senza conversione in float.
Il tempo di uscita FILETIME non viene interpretato. L'API restituisce zero in
caso di errore e il componente solleva l'errore Windows, senza aprire un PID.

`verify()` ricontrolla identità dell'oggetto handle, valore, PID e creazione.
Una sostituzione dello stesso valore numerico con un diverso oggetto handle
non viene accettata. `identity()` restituisce una copia dei due metadati dopo
la verifica; i metadati serializzati non consentono di ricostruire l'oggetto.

`observe()` interroga sempre il valore dell'handle originale conservato, anche
dopo un errore di cattura dell'identità; non usa `Popen.poll`, che leggerebbe
l'eventuale handle sostituito dentro Popen. Il riferimento forte all'oggetto
handle originale viene mantenuto. Usa `WaitForSingleObject` con timeout zero e
legge `GetExitCodeProcess` soltanto dopo il segnale di uscita. Un codice 259 è
quindi un codice d'uscita effettivo, non la sola costante STILL_ACTIVE.
Senza un handle catturato valido, l'osservazione fallisce senza dichiarare uscita.
Ricontrolla l'identità prima e dopo il poll quando è ancora
fidata; un errore di identità resta permanente ma non nasconde un'uscita
effettivamente osservata sull'handle originale. Nessuna osservazione cancella l'incertezza
o permette una nuova cattura. Un codice d'uscita osservato deve restare stabile;
un successivo ritorno a running, un booleano o altro valore invalido fallisce.
Un errore del poll resta un'eccezione, senza perdere il riferimento al processo.

Il risultato separa `HELD_RUNNING`/`HELD_EXITED`, codice di uscita e fiducia
nell'identità. Include sempre `newNativeStartAllowed:false` e
`processClosureAuthorized:false`. L'uscita non prova completamento, correttezza
del risultato o conservazione. Una cattura fallita deve rendere incerto il
supervisore: continuano soltanto osservazione e annullamento cooperativo nei
limiti approvati. Il componente non scrive ricevute e non decide chiusure.

Le prove usano oggetti Popen sintetici non avviati e interrogazioni simulate.
Un test Windows interroga soltanto il processo Python corrente tramite pseudo
handle, per verificare i binding ctypes senza avviare o riaprire processi.
Non dimostra il percorso di un vero Popen PixInsight. Compatibilità PJSR,
handshake Owner, registri esclusivi, budget e macchina a stati devono ancora
essere integrati e verificati prima del preflight nativo autorizzato.

Il componente assume chiamante fidato, Popen standard e memoria non ostile.
Non è una sandbox contro lo stesso utente e non autentica consenso. Rollback:
revert del codice preservando le prove e i registri dei tentativi precedenti.

Riferimenti ufficiali consultati:

- [GetProcessId](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getprocessid)
- [GetProcessTimes](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getprocesstimes)
- [WaitForSingleObject](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject)
- [GetExitCodeProcess](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getexitcodeprocess)
