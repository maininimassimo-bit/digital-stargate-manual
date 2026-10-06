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
Rollback: revert del commit di merge e nuovo deployment Pages; nessun force push.
Una projection 1.2 residua è bloccata dal consumer 1.1 fino a nuova acquisizione
coerente; dati scaduti restano indisponibili. Non richiede conservazione GRIB.

P6 rimane aperta, con percorsi master indicati dall’Owner per ogni elaborazione.
Il collegamento unico C → F attende sempre la conferma di chiusura PixInsight.
