# BKL-051 S4 — Registro locale dei byte e ricevute di verifica

| Campo | Valore |
|---|---|
| Identificativo | BKL-051-S4-LOCAL-EVIDENCE-REGISTRY |
| Versione | 1.0 |
| Data | 2026-10-08 |
| Stato | Library candidate, private derivative proof; native worker/UI/OAT incomplete |
| Baseline | PR #507 merge `0a61c113ef07ec8e5cee196a1a118d3164caa063`, 15 workflow post-merge e Pages verificati |

## Problema e risultato

La [coda privata](BKL-051-S4-PRIVATE-QUEUE-2026-10-08.md) conosce riferimenti opachi; non prova a quali byte corrispondono. `tools/scientific_transients/local_registry.py` aggiunge un registro privato in sola lettura sugli artifact, con scritture esclusive dei manifest e ricevute locali. Non è ancora un worker, journal di operazioni native, parser di immagine, adapter HTTP o modulo UI. Nessuna route, credenziale, IAM, processo, dipendenza o invio aggiunto.

Il chiamante locale fidato sceglie due directory esistenti e disgiunte: artifact e registro. Manifest raw JSON limitato a 1 MiB, chiavi duplicate/extra rifiutate; schema chiuso con protocollo e cinque riferimenti uguali al contratto della coda. Da sei a 128 file, percorsi relativi canonici, ruolo dichiarato, SHA256 e dimensione. Tutti i ruoli INPUT/REFERENCE/ALGORITHM/CONTRACT/PARAMETERS/PROVENANCE devono essere rappresentati. Più artifact dello stesso ruolo sono ammessi. Ruoli e riferimenti restano dichiarazioni: non attestano qualità, approvazione del contratto, indipendenza, completezza della History o replay autonomo.

La verifica legge file regolari, rifiuta link/reparse anche negli antenati, controlla identità/dimensione/timestamp prima e dopo l'hash e confronta SHA256/dimensione dichiarati. Il confronto `ctime` resta fra chiamate fstat della stessa API; il raccordo path/descriptor usa device/file-id, dimensione e mtime. Su Windows `stat` e `fstat` possono differire in ctime: [issue CPython #157671](https://github.com/python/cpython/issues/157671). Identità nulla è rifiutata. Non è una protezione completa da un processo ostile concorrente, né uno snapshot per un'esecuzione futura: artifact quiescenti sotto controllo Owner sono prerequisito; l'adapter dovrà reverificare/snapshot al boundary di uso. File ID/hash non provano l'autore del dato.

Registrazione: manifest canonico scritto con creazione esclusiva, flush/fsync. Retry esatto reverifica i parent e conserva il manifest; stesso binding con contenuto diverso rifiutato. Scrittura parziale resta conservata e impedisce la sostituzione: nessuna autoriparazione o eliminazione. Verifica successiva richiede il digest esatto del manifest oltre al binding, così modifiche del registro non sono assorbite automaticamente. Ogni verifica ammessa conserva una ricevuta autonoma PASS/FAILED con codice limitato; errore di persistenza non restituisce successo. Nessuna garanzia di transazione multipla o durabilità completa contro perdita di alimentazione, firma o ACL attestata. La library non ruota/recupera file e non elimina evidenze per liberare spazio.

I manifest/receipt rimangono sul PC: percorsi, riferimenti e hash privati non vanno alle projection. Non memorizzare bearer o credenziali negli artifact; la library non è un filtro di segreti o classificatore di dati. Nessuna pubblicazione del registro. La coda resta disabilitata: nessun binding di prova registrato nel cloud. `BYTES_VERIFIED` è integrità puntuale, sempre `NOT_VALIDATED` scientificamente; non consente COMPLETED remoto o rilancio nativo da solo.

## Budget delle aperture riconciliato

Sono verificate 13.884 formule diagnostiche sky-only sulle aperture corrette salvate e 965 budget parziali dei cinque confronti sulle stesse 193 identità. I cinque confronti condividono esposizioni: non sono 965 prove indipendenti. La formula storica tratta approssimativamente la varianza del fondo come media, mentre il fondo usato è mediano; resta diagnostica. Nessuna varianza completa viene dedotta dal quadrato di quella sigma. Varianze/covarianze complete sono null, così l'inspector conserva sigma condizionale e significatività null. Segnale vero/Poisson, dark/flat condivisi, cosmetica, fondo/correlazioni, PSF/centro, normalizzazione e banda restano aperti. Non sommare di nuovo il read noise al cielo empirico.

Il trasferimento di unità già verificato, le soluzioni/detection, immagini e aperture non vengono rieseguiti. Parent invariati; misure, History, tentativi e risultati precedenti conservati. Prova del registro su derivate private esistenti, con otto artifact nel binding raccordato al contratto d'incertezza. Prima prova con contratto delle coordinate conservata separatamente, poi binding additivo corretto; nessuna sovrascrittura o nuova esecuzione dei budget. Non è la catena completa per un'analisi nuova. [Ricevuta minimizzata](evidence/BKL-051-S4-LOCAL-REGISTRY-2026-10-08.json).

## Validazione, residui e rollback

Dodici test sintetici di hashing/scritture reali coprono restart/retry, modifica dei byte/manifest, conflitti, parziali, schema/path/ruoli, scrittura fallita e rilevamento di mutazione durante lettura. Suite Python coda+registro: 26 test locali, 25 pass e un test symlink saltato perché il PC non concede la creazione di link. CI Windows/Linux deve registrare il proprio esito; prova reale reparse/ACL e crash/power-loss rimane OAT futura. I 55 test Node precedenti non sono nuova validazione scientifica.

Gate della PR: CI exact-head → ARB → RQ → expected-head merge → post-merge/Pages. Non attestati prima della loro esecuzione. Rollback del solo incremento con revert e rigenerazione projection, mantenendo archivi/registri; nessuna migrazione, cancellazione o riuso implicito di vecchi binding. Seguono adapter nativo con snapshot/parametri/versioni, journal per tentativo e checkpoint, sealing del rapporto correlato, cancel/recovery reali, UI e OAT. Restano S2/S3 scientifiche e invii nei canali approvati, senza attivazione. BKL-051 aperta; soglie/policy e acceptance finale Owner non dedotte dal registro. P6/F4/F5/BKL-050/S10/Safety invariati.
