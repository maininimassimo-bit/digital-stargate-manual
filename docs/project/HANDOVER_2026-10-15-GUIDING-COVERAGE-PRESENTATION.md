# Guiding coverage: assenza del denominatore e visualizzazione — 15 ottobre 2026

## Diagnosi e audit

Richiesta Owner: verificare GUIDING_STABILITY 1,34 arcsec / coverage 0% e tutte
le sessioni. Baseline `549a46d06d08be7fa856a1d4979a13556345429b`.
[Evidenza delle 24 sessioni](evidence/guiding-coverage-audit-2026-10-15.json):
21 espongono RMS e campioni di guida eleggibili; tutte hanno coverage F4 zero.
Le altre tre (26–27 agosto, 7–8 settembre, 22–23 settembre) non hanno evidence
GUIDING_STABILITY eleggibile. Nessuna diventa una misura zero o una sessione
validata dall'assenza di dati.

Il mapping `scientific-data-quality-projection.mjs` imposta intenzionalmente
zero perché il catalogo non espone un denominatore temporale governato. È il
limite accettato in ARB F4 O-02; non equivale a nessun dato PHD2. La notte
14–15 ottobre ha RMS 1,34 arcsec e 14.974 campioni validi. Il rapporto fra
campioni validi e totali non misura la frazione di notte coperta dalla guida.

## Correzione di presentazione

Il consumer distingue il sentinel F4 dal vero valore misurato zero usando la
limitation esistente GUIDING_TEMPORAL_COVERAGE_NOT_REPRESENTED_IN_SOURCE_CATALOG.
Per GUIDING_STABILITY con quel limite e coverage zero mostra «copertura
temporale non disponibile» e spiega il limite vicino alle evidenze. L'RMS resta
visibile. Null/coverage assente non vengono trasformati in 0%; gli zeri numerici
senza quel limite e le coverage rappresentate delle altre dimensioni restano
zero/percentuali. Il testo può andare a capo anche nelle viste strette.

Il modello sperimentale conserva il valore prudenziale e quindi score,
confidence, coverage aggregata, profilo, digests e readiness F5 non cambiano.
Non vengono imputati dati o rinormalizzati pesi. Una futura percentuale temporale
richiede metodo e denominatore scientifici versionati nella source e relativa
review, come già previsto dalla governance F4; non viene introdotta da questa
correzione. Non è una modifica al parser PHD2 o ai dati originali.

## Verifiche e rilascio

Regressioni: sentinel distinto da zero, null/assente/invalidi non mostrati come
zero, numeri delle altre dimensioni conservati, projection immutata, scansione
completa delle evidenze persistite. Browser sui viewport desktop e mobile:
righe di guida senza falso 0%, nota esplicita visibile, nessun overflow.
Freshness SHA-256, consumer fail-closed, scoring e F5 invariati. CI exact-head,
ARB poi RQ, gate post-merge e riscontro pubblico da attestare nella ricevuta PR.

Rollback: revert del consumer/presentazione e documentazione; source, profilo,
proiezioni scientifiche, report e RAW non richiedono migrazione. Nessuna
modifica a EAGLE, schedulatore, Safety, autorità o comando dispositivi.
