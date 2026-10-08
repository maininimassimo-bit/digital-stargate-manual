# BKL-051 S4 — Driver locale e riconciliazione dopo riavvio

| Campo | Valore |
|---|---|
| Versione | 1.0 |
| Stato | Candidate; exact-head CI, ARB/RQ e release pending |
| Baseline | PR #515 merge `46e8e9e75d9549f50b4473eed9182dd9cb3799dc`: 16 check exact-head, ARB/RQ e 15 workflow post-merge SUCCESS; cinque endpoint Pages verificati |

## Confine del driver

`local_driver.py` prepara e coordina un solo tentativo già prenotato. Il chiamante locale fidato fornisce
identità indipendentemente verificata, binding e manifest pinned, run PJSR già preparato, registro locale,
root journal/outbox esistenti e disgiunte, trasporto dedicato e lease soltanto in memoria.
Il driver legge la ricevuta worker e richiede identità esatta, RESERVED, sequenza zero e nessuna ricevuta.
Queste condizioni non provano la freschezza di una prenotazione: la coda può restituire un attempt già
esistente. Il driver **non chiama claim**, non legge credenziali, non registra binding remoti, non acquisisce
un altro job e non carica percorsi/script dal portale. Claim sicuro, attivazione e driver completo restano gate.

Directory attempt nuove ed esclusive; anche PREPARED non viene riutilizzato. Un marker esclusivo nel run locale
impedisce di riusare lo stesso run tramite altre root journal/outbox. Snapshot/registry/supervisor mantengono
i controlli esistenti; failure e directory parziali restano conservate. Il marker non è un lock globale contro
copie dello stesso run, altri processi o caller che non usano il driver: quiescenza e ownership sul PC restano
prerequisiti. Parametri, runtime e processo sono forniti dal chiamante fidato, mai da payload eseguibile remoto.

`start()` esegue una volta il supervisore; `step()` controlla un solo tick esplicito quando dovuto.
Intervallo locale predefinito due secondi, ammesso 1–30 s: limite operativo, non scientifico. Clock monotono,
valori finiti; nessun sleep, loop, daemon o heartbeat. Il chiamante deve programmare realmente le chiamate;
il limite minimo non garantisce una frequenza massima effettiva e i timeout HTTP possono allungare il ciclo.
Terminato o incerto il tentativo, niente secondo start/tick. Avvio, cancel al punto sicuro, timeout e
chiusura dell'handle corrente restano responsabilità del supervisore già rilasciato. Nessun PID persistito
concede ownership e nessuna istanza PixInsight Owner viene terminata da questo incremento.
Eccezioni inattese durante start/tick e clock invalido dopo start congelano il driver; non autorizzano
un secondo avvio, ulteriori tick o una terminazione del processo. La riconciliazione resta esplicita.

## Riconciliazione esplicita

`reconcile_retained()` richiede una outbox riaperta e lo stesso journal. Verifica snapshot, eventi e byte degli
artefatti; esegue una GET worker autenticata tramite il trasporto già governato. Identità remota correlata,
riconciliazione della sola ultima ricevuta: ACK quando i byte/stadio coincidono, oppure evidenza di recovery
come previsto dalla outbox. Nessuna POST, lease renewal, riscrittura del journal o avvio nativo.
La GET può materializzare la scadenza del lease sul server secondo il contratto esistente; non è una promessa
di lettura senza effetti sullo stato remoto. I file ACK/recovery locali sono nuove evidenze esclusive.

Un ACK storico può restare ACKNOWLEDGED mentre il job remoto è RECOVERY_REQUIRED: entrambi sono restituiti,
con `currentRemoteMatchesLastReceipt` separato. Nessuna conclusione di successo dalla sola ricevuta storica.
Outbox senza messaggi produce NO_RETAINED_RECEIPT. File corrotti, identità diversa o trasporto non verificato
non producono una riconciliazione positiva. La funzione non cancella recovery server, non riassegna job,
non ricrea lease/ownership e non rende validi i dati scientifici. La risoluzione operativa server resta aperta.

## Verifica e limiti

Dodici prove nuove con mock di processo e MemoryStore: percorso COMPLETED, cadence/no replay, cancel prima
di start, ACK perso e riconciliazione senza POST, ACK storico/stato remoto divergente, PREPARED e root alternative,
clock invalido/regressione, byte corrotti, preparazione parziale conservata, timeout senza process kill,
identità remota conflittuale, outbox live rifiutata ed eccezione inattesa durante start senza replay.
Non sono native/cloud OAT; nessuna nuova elaborazione,
solve, detection o aperture eseguita. CI Windows/Linux e revisioni exact-head restano gate della PR.
CALLER_REPORTED_NOT_ATTESTED, History a monte NOT_ATTESTED, NORMALIZED_SAMPLE_SUM e science NOT_VALIDATED
restano invariati. Nessuna unità, variance, significatività, soglia o classificazione nuova.
Suite locale complessiva: 108 prove Python, 107 PASS e un symlink skip per privilegi Windows;
104 prove Node PASS. MkDocs strict, fixture portale e coerenza/generator roadmap/projection PASS.
Questi risultati locali non sostituiscono CI e review sul commit esatto.

BKL-051 OPEN: claim completo, recovery server, workflow scientifico, noise/covariance/passband, validation,
policy, accessi/PC/cloud OAT e reporting CBAT/TNS/VSX/MPC ancora aperti. Runtime e invii disattivati.
P6 Accepted, F4 lifecycle pending, F5 dopo F4, BKL-050 finale; gallery, root C→F, S10 e Safety invariati.
Rollback: revert del modulo/test/docs e rigenerazione projection; conservare journal, marker, History e ricevute,
senza cleanup o riuso implicito dei run. Gate CI → ARB → RQ → expected-head merge → post-merge/Pages.
