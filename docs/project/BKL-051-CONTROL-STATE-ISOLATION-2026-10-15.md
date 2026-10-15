# BKL-051 — isolamento esplicito del registro di controllo

Stato: correzione locale candidata, non distribuita. BKL-051 resta **OPEN /
NOT_VALIDATED**, stima prudenziale 37%, zero controlli qualificati.

La prova operativa reale autorizzata il 15 ottobre ha creato una sola revisione
temporanea sulla stessa immagine del servizio esistente. La prima registrazione
worker è stata rifiutata con HTTP 400: il registro di controllo preesistente del
9 ottobre appartiene a un'altra identità. La sua generazione e data di aggiornamento
sono rimaste invariate. Il confronto ha letto soltanto l'identificativo opaco finale,
senza richiedere campi segreti o l'intero registro. Nessun nuovo job, avvio nativo
o evento del piano. Traffico precedente al 100% e rimozione dell'aggiunta IAM
temporanea verificati; originali ed evidenze del tentativo conservati privatamente.

## Correzione candidata

`TransientQueue` accetta un riferimento di registro opzionale, scelto esplicitamente
nella configurazione attendibile del servizio con `DSG_TRANSIENT_STATE_REF`.
Il riferimento contiene esattamente 32 caratteri esadecimali minuscoli e seleziona
un oggetto sotto il prefisso fisso `control/transient-analysis/`. Nessun percorso
arbitrario o parametro proveniente dal portale. L'assenza della configurazione
mantiene il registro storico e tutti i controlli esistenti; un valore vuoto è
invalido. Non si sceglie automaticamente un registro vuoto dopo un errore.

La nuova campagna conserva separatamente stato, worker, root, richieste idempotenti
e copie di recupero. Il riavvio usa lo stesso riferimento; un worker diverso sullo
stesso registro continua a essere rifiutato. Nessuna migrazione o cancellazione
del registro storico, nessun nuovo endpoint o permesso implicito. Il ruolo IAM
necessario resta limitato al solo oggetto esatto approvato dall'Owner.

## Prove e limiti

La regressione parte da un registro storico con job prenotato e prova che la nuova
campagna può registrare e accodare senza alterarne byte, generazione o backup.
Verifica inoltre riavvio/idempotenza, rifiuto di identità incompatibili e riferimenti
non validi, configurazione esplicita e compatibilità del percorso storico.
Le prove sono locali e sintetiche: non attestano GCS, OAuth, PixInsight o scienza.

La correzione non rimuove i limiti della coda: 32 binding, 32 job e 1 MiB. Occorre
ancora completare la capacità/archiviazione che conservi tutte le evidenze per i
177 job individuali delle 59 triplette candidate. I candidati non diventano
controlli nulli indipendenti qualificati. Calibrazione, incertezze, associazioni,
recuperi, reporting produttivo e acceptance restano aperti; IRSA resta pendente.

Prima di un nuovo collaudo servono gate sul commit esatto, review indipendenti
applicabili e una proposta operativa aggiornata: nuova immagine/revisione,
riferimento opaco congelato, condizione IAM esatta, costi e ripristino. Il consenso
alla precedente prova sulla stessa immagine non autorizza questo nuovo deployment.
Rollback del codice tramite revert; nessuna cancellazione dei registri o delle
ricevute e nessuna adozione dell'identità worker storica.
