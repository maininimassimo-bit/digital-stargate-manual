# BKL-051 S1-R/S4-R — Anteprima locale ADES per MPC

| Campo | Valore |
|---|---|
| Identificativo | BKL-051-S1-MPC-ADES-PREVIEW |
| Versione | 1.0 |
| Data | 2026-10-09 |
| Stato | Proposed — export privato offline; scienza NOT_VALIDATED |
| Dipendenze | ADR-020, piano reporting Owner-approved, registro locale di evidenze |

## Problema e comportamento

Il dossier preliminare esistente seleziona un canale dichiarato ma non produce un formato specifico. `tools/scientific_transients/mpc_export.py` aggiunge un'anteprima XML ADES 2022 per astrometria dichiarata di oggetti numerati, con JSON privato che conserva i gate mancanti. Non implementa invio, credenziali, endpoint, policy autonoma o integrazione cloud/portale. Il dossier generico e il suo contratto restano invariati.

Il registro locale verifica i byte selezionati prima e dopo l'export. Richiesta e manifest sono vincolati a digest indipendentemente forniti dal chiamante locale fidato. L'export usa directory nuova esclusiva; un tentativo parziale viene conservato con `failed.json` e non può essere sovrascritto o ripetuto nella stessa directory. Le ricevute collegano XML, JSON e richiesta esatta; non attestano validità astrometrica delle dichiarazioni.

## Contratto ristretto

Schema chiuso `DSG_MPC_ADES_PREVIEW_V1`, richiesta locale tramite API `export(registry, request_path, expected_sha, output_root)`. Nessun intake di percorsi dal portale. Il parser stretto esistente rifiuta chiavi duplicate; dati materializzati, manifest e percorsi relativi restano soggetti ai limiti del registro.

Il contesto contiene codice osservatorio dichiarato di tre caratteri alfanumerici, nome submitter, osservatori/measurers e telescopio: design, apertura in metri, detector CCD oppure CMO. Il codice non viene assegnato, verificato presso MPC o ricavato dalle immagini. I nomi sono dati privati e non vengono pubblicati; email, indirizzi di contatto e credenziali non sono campi ammessi. L'esempio sintetico usa codice 500 e nomi esplicitamente sintetici, non identità o codice dell'Owner.

Le righe contengono solo `permID` numerico positivo, UTC ISO8601 ordinario con suffisso Z, RA/Dec astrometriche J2000 in gradi, catalogo dichiarato `Gaia3` e percorsi registrati di immagine/riduzione. Si richiedono dichiarazioni esplicite di midpoint UTC, coordinate e convenzione delle incertezze; non si convertono OBSJD/HJD, epoche Gaia TCB, centroidi PixInsight o WCS. Secondi intercalari, altre designazioni/cataloghi/modalità, osservatori mobili, trail-end, fotometria e PSV non sono supportati da questa versione. Sono incrementi futuri del perimetro approvato, non esclusioni dai requisiti di chiusura.

I numeri sono stringhe decimali limitate, senza esponenti, NaN, booleani o arrotondamenti impliciti. Coordinate e precisione devono già appartenere al formato supportato; valori incompatibili sono respinti. Due righe per lo stesso oggetto e lo stesso istante sono rifiutate anche con diversa precisione scritta del timestamp. Oggetti distinti allo stesso istante sono ammessi. Non si inferiscono indipendenza delle esposizioni, associazione, notte osservativa o qualità di un tracklet dal numero di righe.

`rmsRA` è la componente random 1σ di RA × cos(Dec) in arcsec; `rmsDec` in arcsec; `rmsTime` in secondi; `rmsCorr` adimensionale, compreso strettamente tra −1 e 1 secondo lo schema di submission fissato. Nessuna trasformazione di covarianza viene effettuata. Una correlazione nota richiede entrambe le sigma; una correlazione ignota resta null. Errori null vengono omessi dall'XML e conservati in `unknownFieldsByObservation`. Non diventano zero o budget completo; zero sigma e correlazioni singolari non sono rappresentate da questa versione.

Testo viene serializzato con escaping XML; caratteri illegali, controlli e separatore PSV sono respinti. `render` è una routine interna su risultati già ispezionati, non un parser o un boundary d'intake indipendente.

## Validazione di formato indipendente

La fonte ufficiale collegata da MPC distingue validità di schema e accettabilità di una submission. La CI Windows/Linux scarica soltanto `submit.xsd` dal commit IAU-ADES/ADES-Master `f4158f96a049b83dfcf848fa33eaac4391db9460`, verifica SHA256 `2a5d049808e947cffa11a973a2395c1dde09f00207313a496450b0ef1be27026` e applica il motore W3C XSD System.Xml di PowerShell. Il file non è incorporato come codice di terze parti o dipendenza runtime. Questo è un riferimento fissato, non attestazione di aggiornamento perpetuo alle regole del provider.

DTD, resolver XML e riferimenti esterni dello schema sono disabilitati; nessun endpoint MPC riceve fixture. Due output sintetici CCD/CMO validano; tre controlli con versione, range RA e tag/ordine invalidi sono rifiutati. Tredici test di contratto controllano precisione, unknown, duplicati temporali, convenzioni, scope, testo ostile, raw JSON duplicato, digest obsoleto, byte alterati, overlap, non sovrascrittura e mutazione durante export. Il motore XSD è distinto dal serializer; il controllo non è solo un confronto dell'output con se stesso.

L'esportatore conserva `schemaValidation: NOT_EXECUTED_BY_EXPORTER`; le ricevute di test XSD sono separate e non vengono trasferite come validazione automatica di futuri output. Stato sempre `PRIVATE_PREVIEW`, `scienceValidation: NOT_VALIDATED`, `declarationsAttested: false`, `submissionAuthorized: false`, `externalSubmission: NONE`. Nessuna ricezione, scoperta, classificazione o accettazione MPC viene dedotta dalla sintassi.

## Riconciliazione scientifica e comunicazioni private

PR #530 è conclusa sul merge `39d6e39977caaae2a68b56f493ec172417e6da4b`, con ARB/RQ e verifiche finali conservate. Le prove precedenti non vengono rilanciate per questa consegna. Gaia TOP100 con velocità radiale resta campione incompleto; i tempi dei tre science frame restano condizionali; i controlli AT2018cow restano scelti su evento noto, non ciechi.

Tre differenze ZTF e PSF effettive sono conservate privatamente. Una nuova acquisizione del riferimento completo rafforza la provenienza: MD5 calcolato uguale al checksum del registro di generazione, ID e parametri coerenti con il log di sottrazione. Non attesta il digest effettivamente letto dal processo di sottrazione. L'orario CREATED è dichiarato Pacific Time: non confrontarlo direttamente con UTC. Il rumore completo resta ignoto, inclusi prodotti interni e correlazioni del ricampionamento; non applicare due volte la correzione già presente nei prodotti pubblici. READ NOISE configurato dal fondo non è calibrazione elettronica indipendente.

Conservate sei richieste dirette, ricevute, timeout/404/cap superato e hash, senza retry automatico. Il 404 vale solo per l'URL esplorato; il cap non prova che refunc sia assente. L'Owner ha autorizzato una sola nuova comunicazione IRSA su rumore/provenienza: connettore invio completato e ricevuta privata conservata. Distinta dal ticket IRSASD-21929 di calibrazione; nessuna risposta tecnica attestata dalla ricerca mirata di ripresa. Non reinviare o trasformare una presa in carico in soluzione scientifica.

## Consegna, rollback e residui

Gate di questo incremento: controlli locali, CI exact-head, ARB poi RQ, merge protetto e post-merge/Pages. Il dossier non anticipa gate pendenti. Nessun deploy scientifico/cloud o sessione OAT implicita. Rollback mediante revert coerente di modulo/test/CI/documenti e rigenerazione delle projection; conservare export, richieste, registri ed evidenze private. Nessuna migrazione, account, nuova dipendenza scientifica o modifica di immagini/History.

BKL-051 resta OPEN / NOT_VALIDATED: S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. Restano astrometria/timing/covarianze indipendenti, budget fotometrico completo, misure PSF native e sottrazione giustificate, validazioni cieche reali di recupero/falsi positivi, oggetti mobili/tracklet adeguati, formati e procedure degli altri canali, approvazione payload immutabile, revoca/duplicati/ricevute, percorso Owner completo, residui del servizio distribuito, policy quantitativa, accessibilità e accettazione finale. I tre dati Atami su due notti non diventano un tracklet MPC. Invio reale e prove provider/sandbox restano da autorizzare concretamente. P6 Accepted nei limiti; F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva; Safety e collegamento C→F invariati.

## Fonti primarie

- [MPC — ADES e validazione submission](https://docs.minorplanetcenter.net/mpc-ops-docs/observations/ades-format/).
- [MPC — valori ammessi](https://docs.minorplanetcenter.net/mpc-ops-docs/observations/valid-ades-values/).
- [IAU-ADES — schema esatto](https://github.com/IAU-ADES/ADES-Master/blob/f4158f96a049b83dfcf848fa33eaac4391db9460/xsd/submit.xsd) e [convenzioni dei campi](https://github.com/IAU-ADES/ADES-Master/blob/f4158f96a049b83dfcf848fa33eaac4391db9460/xml/adesmaster.xml).
- [Piano reporting](BKL-051-SCIENTIFIC-REPORTING-PLAN-2026-10-08.md), [ADR-020](../architecture/ADR-020-Private-Scientific-Transient-Analysis.md), [dossier preliminare](BKL-051-S4-REPORTING-DRAFT-2026-10-09.md), [handover](HANDOVER_2026-10-09-BKL051-MPC-ADES.md).
