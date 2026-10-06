# Planner F9 — correzione precisione GRIB, 6 ottobre 2026

Baseline: `7ee3fe61a519f1a4f67fc5268967f6ee52935188` (PR #493).
Scope autorizzato dall’Owner: diagnosticare e correggere il planner non aggiornato,
prima di riprendere P6. Non modifica soglie, provider, costi o autorità.

I run GitHub `37407187465` e `37449841369` hanno abortito per
`PRECIPITATION_ACCUMULATOR_REGRESSION`. L’ultima projection pubblicata risaliva
al 5 ottobre, 16:08:59 UTC; il consumer l’ha correttamente dichiarata scaduta.
La diagnosi sul run ufficiale ICON-2I `2026100600` riproduce il problema:
calo di 0.00390625 mm entro l’errore combinato dichiarato di 0.005859375 mm.
Il file diagnostico corrente non prova identità di byte con i run falliti;
i loro GRIB non sono stati conservati. Nessuna coordinata è pubblicata.

La [specifica F9](../architecture/scientific-assets/BKL-031-F9-Repeatable-Current-Night-Planner.md)
descrive il limite basato su packingError e la policy 1.2. L’ora dubbia è
indeterminata e non eleggibile; le regressioni maggiori restano bloccanti.
Gli importi positivi conservano la precisione numerica e non diventano zero.
La rappresentazione del cielo non presenta una notte dubbia come serena.

Verifiche locali: 34 test Python, consumer Node (ora indeterminata, ora asciutta,
policy precedente e rappresentazione cielo), smoke ecCodes 2.44.0 su griglia
sintetica. I GRIB diagnostici e sintetici sono stati eliminati.
Il build rigoroso, CI exact-head, ARB e RQ process-separated precedono il merge;
l’acquisizione reale e Pages si verificano dopo il rilascio. Non sono qui
asseriti risultati futuri. Evidenza exact-head, merge e post-merge nella PR
associata e nel rapporto locale di consegna.

Mandato: DSG-AEM-001; eventuale merge usa W-DSG-AEM-RULESET-001.
Rollback: PR governata con ripristino selettivo della riduzione/acquisizione
precedente, mantenendo consumer F9, modulo sky e relativi test compatibili con
`precipitationUncertain` e policy 1.2. Non fare revert integrale del merge:
il consumer precedente sospende ranking ma può mostrare zero e cielo sereno
per una projection 1.2 residua. Il consumer mantenuto mostra l’incertezza anche
con policy 1.1 e sospende le nuove graduatorie incompatibili. Dataset scaduti
restano indisponibili; nessun force push o conservazione GRIB. Il rollback
richiede i propri gate CI/ARB/RQ e verifica Pages, prima di una nuova acquisizione.

ARB iniziale sul head `88e72a47f0bc324a0c3c61087363287ca6902ede`: un Major sulla
procedura di rollback, corretto con conservazione dei lettori compatibili e test
policy legacy + ora indeterminata; necessario nuovo exact-head review.

P6 rimane aperta, con percorsi master indicati dall’Owner per ogni elaborazione.
Il collegamento unico C → F attende sempre la conferma di chiusura PixInsight.

## Verifica reale e correzione dello step zero

PR #494: publication head `4f3ff8f464a182c22e5aff490a406ceef6e929f1`,
merge `44bead238397f3b9697e971403529475486d76e4`; nove workflow exact-head
e nove workflow post-merge PASS, ARB/RQ AI separati PASS, Pages verificata.
Il tentativo manuale governato `37487868127` è fallito prima della pubblicazione
per `PRECIPITATION_ACCUMULATOR_METADATA_INVALID`; nessun rerun del tentativo.

La lettura limitata in memoria del primo messaggio ufficiale del run
`2026100612` (210 byte) ha isolato un errore introdotto dal confronto generico:
ecCodes 2.44.0 restituisce `startStep`/`endStep` come `0m` nel campione iniziale,
pur essendo accumulazione da zero. L’accessore tipizzato `codes_get_long`
legge correttamente zero senza dipendere dal suffisso di unità. Il reader usa
questo accessore per l’origine; gli altri vincoli e la policy 1.2 sono invariati.
Il nuovo test nativo costruisce in memoria un GRIB sintetico a step `0m` e
verifica il reader effettivo, oltre al controllo del formato nel test mock.
Totale: 35 test Python con ecCodes installato; i dati di fuso orario Windows
sono una dipendenza locale del venv diagnostico, non una modifica del runtime
Linux governato. Il secondo incremento richiede nuovi CI/ARB/RQ exact-head
prima del merge e una nuova acquisizione governata dopo la verifica post-merge.
