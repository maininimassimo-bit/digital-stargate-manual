# BKL-051 S4 — archivio privato del rapporto conservato

| Campo | Valore |
|---|---|
| Identificativo | BKL-051-S4-RETAINED-REPORT-BUNDLE |
| Versione | 1.0 |
| Data | 2026-10-10 |
| Stato | Candidate; gate exact-head/review/rilascio propri |
| Baseline | PR549 merge `37955d323b36bd107c69acd4abebef9ac272395b` |

## Problema e comportamento

Il [rapporto locale](BKL-051-S4-LOCAL-REPORT-2026-10-08.md) esporta JSON/HTML ma lascia i byte dell'esecuzione in una cartella separata. Il nuovo exporter passivo `tools/scientific_transients/report_bundle.py` aggiunge un archivio privato trasportabile del solo attempt conservato: rapporto leggibile, rapporto JSON, ancora, eventi del journal e tutti i file referenziati di snapshot, operazioni e checkpoint. Nessuna scansione ricorsiva della cartella: file estranei, outbox e credenziali non sono inclusi per inferenza. Il codice non estrae né esegue l'archivio, non avvia PixInsight, non modifica coda/cloud e non effettua richieste esterne.

Il chiamante fidato deve fornire un attempt già COMPLETED, il digest tecnico ottenuto indipendentemente e una root privata esistente e separata. Sigillo, catena e correlazioni vengono verificati con l'inspector esistente. File e percorsi passano i controlli esistenti contro traversal, link e reparse; la root richiede quiescenza e ACL Owner, non costituisce sandbox. Limite di archiviazione 8 GiB, distinto da qualsiasi soglia scientifica; copia streaming con digest e lunghezza attesi prima/durante/dopo. ZIP senza compressione, membro letto integralmente dopo la scrittura per CRC, dimensione e SHA256; manifest confrontato esattamente. Ricontrollo del rapporto/journal dopo la copia prima della ricevuta di successo.

Directory esclusiva per attemptId: archivio e ricevuta non sovrascritti, nessun retry implicito. Un errore conserva ZIP parziale/completo e `failed.json`; senza `bundle-receipt.json` non è un export completato. La ricevuta distingue SHA256 dell'archivio, digest tecnico del rapporto e testa del journal. L'HTML rimane passivo con escaping e CSP del renderer esistente.

## Uso e limiti

La CLI `python -m tools.scientific_transients.report_bundle --help` espone directory attempt, digest tecnico atteso e root di output. Le directory dell'export JSON/HTML precedente e del nuovo bundle devono essere distinte quando usate per lo stesso attempt. Il manifest del bundle ha protocollo `DSG_TRANSIENT_RETAINED_REPORT_BUNDLE_V1`, classificazione PRIVATE e scope `REFERENCED_RETAINED_ATTEMPT_ONLY`.

Il pacchetto comprende i byte referenziati conservati, non il programma PixInsight installato, runtime transitive, archivio genitore completo, acquisizioni o dipendenze scientifiche non registrate. `completeDependencyArchive=false`, `NOT_VALIDATED`, History a monte NOT_ATTESTED, esecuzione CALLER_REPORTED_NOT_ATTESTED e nessuna acceptance Owner per effetto dell'export. Percorsi dichiarati nel rapporto rimangono storici; non sono istruzioni di ripristino. Unknown di varianza/significatività non diventa zero. Questo incremento non integra il download autenticato del rapporto completo nel portale e non attesta un OAT scientifico reale.

## Verifica e residui

Cinque test sintetici Windows locali PASS: archivio riaperto con ogni byte/hash verificato e file estraneo escluso; sigillo/byte/root invalidi; esclusività; limite di dimensione; errore nel ricontrollo con conservazione e assenza della ricevuta di successo. Nessun nuovo nativo/cloud eseguito dai test. Il primo tentativo locale ha rilevato che Windows non permette fsync su un descrittore aperto in sola lettura: corretto usando un descrittore scrivibile del solo ZIP appena creato, senza riscrittura dei byte. CI esplicita Windows/Linux e revisioni ARB poi RQ obbligatorie sull'head esatto; risultati registrati nella PR, non dedotti dalla baseline.

Restano pipeline e rapporto scientifici completi, calibrazione/rumore/covarianze/timing/matching, recuperi ciechi/falsi positivi, cancellazione Owner durante il nativo e recovery prima del terminale, integrazione privata autenticata, oggetti mobili/tracklet, reporting/policy/accessibilità/accettazione S5. BKL-051 OPEN / NOT_VALIDATED; S1/S2 aperte, S3 parziale e S4 incompleta. Il [collaudo cloud isolato](BKL-051-S4-ISOLATED-CLOUD-OAT-EVIDENCE-2026-10-10.md) resta concluso e il servizio spento: nessun nuovo avvio/build/login autorizzato da questo exporter. P6, F4/F5, BKL-050, Safety e C→F invariati.

Rollback: revert del solo exporter, test, collegamenti e CI aggiuntiva; conservare archivi ed evidenze private, nessuna migrazione di coda o ripristino automatico.
