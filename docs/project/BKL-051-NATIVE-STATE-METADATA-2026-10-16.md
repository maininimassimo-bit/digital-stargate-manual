# BKL-051: controlli dei metadati di conservazione per stato

`native_state_metadata.py` implementa la parte semantica S6 del contratto V5.
È una funzione pura: non legge file, non decodifica immagini, non calcola
varianze, non osserva o chiude processi. `check_state_metadata` riceve terminale,
ricevuta started, evidenza nativa e binding attesi. Il futuro supervisore deve
ottenere questi oggetti dai byte immutabili già verificati, con parser passivo
e limitato. Oggetti JSON concordanti non provano che quei byte esistano.

I binding attesi sono uno schema chiuso: operazione, parametri, sigillo, fonte,
kernel, lineage, quattro dipendenze, versione PixInsight, PID nativo, sessione e
impronte Owner/ready. Devono provenire dal contesto originale, dai sorgenti
approvati e dall'handle vivo; non da dichiarazioni correnti su disco. Il PID è
una stringa decimale canonica nei limiti Windows. La versione è ASCII stampabile.

Tutti gli stati ammessi richiedono started e log. Started deve dichiarare una
sola esecuzione e corrispondere a operazione, parametri, sigillo e versione. Il
log può essere vuoto; gli altri prodotti dichiarati devono essere non vuoti.
Il validatore riutilizza schema, nomi fissi, limiti e flag del terminale. Rifiuta
UNCERTAIN_RETENTION, viste dichiarate aperte e qualsiasi errore di retention.

Per COMPLETED_CONDITIONAL_COMPUTATION richiede esattamente i dodici prodotti
del wrapper, nessun errore o superamento nativo del termine. L'evidenza V2 deve
essere chiusa, concordare con tutte le impronte/versioni/identità attese e avere
i tre confronti strettamente true: importazione dei valori, conservazione di
tutti i valori e riapertura del checkpoint. Verifica anche formato Float32 BE,
orientamento, natura del checkpoint e assenza di History a monte nel FITS.
Queste sono dichiarazioni controllate, non nuove misure di pixel del genitore.

Per FAILED_RETAINED e CANCELLED_RETAINED richiede errore non vuoto, zero viste
e retention senza errori. Il codice di annullamento deve concordare con lo stato
prodotto dal wrapper approvato. Sono distinti tre rami:

- insieme completo dei dodici prodotti con evidenza valida, per un errore tardivo;
- soli started e log, per errore precedente alle immagini;
- conservazione d'errore della fonte: source-initial, closing-source e
  error-owned-1 obbligatori. Se esiste checkpoint-initial, servono anche
  closing-checkpoint ed error-owned-2; sono rifiutati ruoli checkpoint orfani.

Un checkpoint salvato prima di una riapertura fallita può essere conservato
senza affermarne la riapertura. Prodotti intermedi restano distinti da prove
complete. Se l'evidenza nativa esiste, tutti i dodici prodotti devono esserci,
anche quando sono conservate in aggiunta le immagini d'errore. Evidenza fornita
ma non dichiarata nel terminale viene rifiutata.

Il risultato indica soltanto coerenza dei metadati e ramo dichiarato. Restano
sempre false processClosureAuthorized, newNativeStartAllowed e
measurementAccepted; varianza fisica completa e significatività sono null,
scientificValidation è NOT_VALIDATED e qualifiedControls è zero.

Prima di una chiusura, il supervisore deve ancora provare causalità del ritorno,
conservazione completa dei byte e identità originali, blocchi delle copie native,
codice effettivamente caricato, proprietà del processo, assenza di segnali,
budget e gate di stato. La compatibilità delle API e History reali richiede il
preflight nativo; l'interpretazione osservativa richiede inoltre il modello e
la qualificazione scientifica. Il solo risultato di questa funzione non basta.

Le prove sono metadati sintetici, compresi hash arbitrari e dimensioni fittizie;
non vengono presentati come prodotti nativi esistenti. Nessun processo o I/O.
Rollback tramite revert preservando evidenze e registri precedenti.
