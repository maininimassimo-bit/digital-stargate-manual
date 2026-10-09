# BKL-051 — anteprima CBAT locale per nova dichiarata

| Campo | Valore |
|---|---|
| Identificativo | BKL-051-S1-CBAT-NOVA-PREVIEW |
| Versione | 1.0 |
| Stato | Proposed private preview; scientific acceptance pending |
| Data | 2026-10-09 |
| Authority | Reporting scope Owner-approved; ADR-020; nessuna authority di invio |

## Scopo e continuità

PR #534 è rilasciata sul merge `719b455b9bb2b45d55ed7998c127a55b3bba951a`: ARB poi RQ AI-assistite APPROVED, 15 workflow post-merge e sette risorse Pages verificati. L'anteprima MPC rimane limitata a oggetti numerati; nessuna accettazione astrometrica o tracklet. I PENDING del suo dossier sono snapshot precedenti alle ricevute finali.

`cbat_preview.py` aggiunge un'anteprima ASCII privata per `GALACTIC_NOVA_CANDIDATE`, nello [scope reporting approvato](BKL-051-SCIENTIFIC-REPORTING-PLAN-2026-10-08.md). Non assegna classificazioni: categoria, autore, sito, strumenti, coordinate, fotometria e controlli sono dichiarazioni. Il destinatario previsto è quello CBAT verificato nelle istruzioni primarie; non viene contattato. Non sono introdotti API esterna, email inviata o salvata nel mailbox, account, soglie scientifiche, credenziali o dipendenze runtime. L'API locale affidabile segue il registro già esistente; CLI e collegamento al portale restano successivi.

## Contratto e output

Richiesta `DSG_CBAT_NOVA_PREVIEW_V1`, con digest fornito separatamente dal chiamante fidato, export/candidate/binding reference opache e manifest fissato. Campi chiusi, JSON senza chiavi duplicate, file selezionati registrati e tutti i byte del binding verificati prima/dopo l'export. Il registro possiede i boundary; non si attesta che i file contengano misure corrette. Garanzie point-in-time, su file Owner quiescenti, senza promessa di isolamento da modifiche ostili concorrenti illimitate.

L'anteprima include autore e recapito dichiarati, sito, metodo CCD/CMOS/fotografico, descrizione dello strumento, apertura in metri e rapporto focale; coordinate in gradi con equinozio J2000 dichiarato; osservazioni con midpoint UTC, esposizione in secondi, magnitudine/banda dichiarate e componente random 1σ in magnitudini. Le componenti random di posizione sono RA × cos(Dec) e Dec in arcsec. Non vengono trasformati frame, coordinate, tempi, bande o magnitudini; nessuna covarianza o calibrazione viene dedotta. ISO UTC ordinario con fino a sei decimali, senza leap second: istanti non supportati sono rifiutati. Decimali come stringhe con fino a nove cifre frazionarie restano identici; esponenti/nonfinite/booleani e precisione eccedente sono rifiutati, mai arrotondati. Bounds di lunghezza/count e magnitudine ±1.000.000 sono limiti tecnici del parser, non criteri scientifici o provider.

Misure, contatti, apertura, limiti, banda e note mancanti sono null in JSON e `UNKNOWN` nel testo, mai zero. Errore senza magnitudine e sigma di posizione senza coordinate sono rifiutati. Coordinate mancanti sono ammesse soltanto come coppia, mantenendo tutti i gate aperti. Il limite di un riferimento non implica non-detection; presenza dichiarata distinta (`NOT_ASSESSED`, `NON_DETECTION_DECLARED`, `DETECTION_DECLARED`). Date, bandpass, limite e immagine/riduzione sono conservati con provenienza. Zero riferimenti o controlli non produce completezza.

Controlli dichiarati di variabili, oggetti mobili e precedenti report: catalogo nominato, UTC e file registrato quando dichiarati eseguiti. `NOT_CHECKED` richiede data/evidenza null. `NO_MATCH_DECLARED` non è un'associazione negativa verificata, una nova o una scoperta. Un'immagine ripetuta o riusata come riferimento viene rifiutata; percorsi diversi con stessi byte o epoche vicine non attestano indipendenza osservativa. Non si adotta automaticamente un intervallo temporale o un numero sufficiente di immagini.

Testo solo ASCII stampabile su una riga per campo: controlli, CR/LF, Unicode e recapiti multipli sono rifiutati senza traslitterazione. Il testo non contiene percorsi locali di evidenza, ma il JSON privato li conserva. `preview.txt` reca in testa PRIVATE PREVIEW / NOT A DISCOVERY REPORT / NOT SENT e origine dichiarata; nessun `.eml`, HTML generato, allegato o upload. URL eventualmente dichiarati nelle note restano testo privato, senza fetch o pubblicazione. `render` è interno a valori già ispezionati e non un secondo intake.

Stato sempre `PRIVATE_PREVIEW`, `NOT_VALIDATED`, `declarationsAttested: false`, `submissionAuthorized: false`, `externalSubmission: NONE`, `providerAcknowledgement: NONE`, `providerReadiness: NOT_EVALUATED`. `preview.json`, `preview.txt`, ricevuta dei rispettivi digest creati in directory esclusiva; riuso bloccato, partial/failed conservati, nessun overwrite o retry automatico. Root separate dal registro/artifacts e richiesta non contenuta nell'output. Non si produce un archivio completo di dipendenze o payload autorizzato.

## Verifica e rilascio

Quindici controlli sintetici verificano contenuti/precisione e socket vietato, unknown, campo/categoria chiusi, null coerenti, injection e ASCII, calendari/convenzioni, bound di evidenze, controlli non verificati, duplicati, hash obsoleti/JSON duplicato, root e non overwrite, mutazione durante export e partial conservato. Fixture finte, indirizzo autore nel dominio `.invalid`: nessun invio reale o prova provider. Le istruzioni CBAT descrivono contenuti e testo semplice, ma non forniscono uno schema di submission equivalente a XSD; questi test non certificano accettazione CBAT. La CI aggiunge la suite su Windows/Linux; l'export MPC e i suoi controlli indipendenti restano invariati.

Gate di questo package: controlli locali, CI exact-head, ARB poi RQ sullo stesso SHA, merge protetto e post-merge/Pages. Questa nota non anticipa gate pendenti. Pubblicazione solo di software/documentazione governati; dossier e immagini restano privati. Rollback: revert coerente di modulo/test/CI/documenti, rigenerazione delle projection, conservazione degli export/evidenze. Nessun invio da ritirare o migrazione.

## Riconciliazione del rumore e residui

Nuovo `refunc` pubblico completo acquisito con una sola richiesta controllata HTTP200, senza retry: SHA256 `9c42ca794f088bb414e941ba0bcc8f25c15e992098363e21bd16303a9c653619`, 40.968.000 byte. Header FITS/shape 3200² e griglia WCS/descriptors selezionati coincidono con il riferimento pubblico già conservato. Il refunc non contiene DBRFID; non attesta i byte dell'input effettivo della sottrazione 2026. 9.535.247 pixel finiti positivi e 704.753 non finiti conservati. La finestra diagnostica nativa 25² attorno alla posizione già usata per AT2018cow ha 625 valori finiti positivi; TAN lineare locale non è astrometria indipendente, maschera completa o misura PSF con errore verificato. Nuova evidenza privata separata; originali e archivi precedenti invariati. La precedente richiesta di cutout respinta resta conservata.

Il prodotto corrente non sostituisce `resamprefunc`/`diffimgunc` interni, né attesta propagazione kernel/ricampionamento, correlazioni, equivalenza corretto/nocorr o calibrazione completa. IRSASD-21929 e IRSASD-21930 risultano sole prese in carico nella ricerca di consegna precedente; nessuna risposta tecnica attestata, nessun reinvio. Le prove native già concluse non vengono ripetute. AT2018cow resta evento noto non cieco; Gaia TOP100 incompleto e timing condizionale.

BKL-051 OPEN / NOT_VALIDATED: S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. Restano pipeline/rapporto scientifico e servizio completi, PSF native con errore verificato, calibrazione/astrometria/tempi/covarianze indipendenti, recuperi/falsi positivi ciechi reali, moving objects/tracklet adeguati, TNS/VSX e estensioni MPC, dossier completo CBAT e requisiti correnti, conferma Owner del payload immutabile/destinatario, ledger e revoca/duplicati/esiti, prove provider quando autorizzate, policy quantitativa/accessibilità/accettazione S5. Nessun requisito cancellato. Cloud/OAT precedenti conclusi, nessuna nuova sessione o credenziale; P6 Accepted nei limiti, F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva. Safety e collegamento C→F invariati.

## Fonti e revisione

- [CBAT — modalità di report e testo ASCII](https://tamkin3.eps.harvard.edu/HowToReportDiscovery.html), verificato il 9 ottobre 2026.
- [CBAT — informazioni richieste e sezione Novae](https://tamkin3.eps.harvard.edu/iau/DiscoveryInfo.html), verificato il 9 ottobre 2026; le parti storiche sulle supernovae non sono routing TNS.
- [ADR-020](../architecture/ADR-020-Private-Scientific-Transient-Analysis.md), [dossier preliminare](BKL-051-S4-REPORTING-DRAFT-2026-10-09.md), [anteprima MPC](BKL-051-S1-MPC-ADES-PREVIEW-2026-10-09.md).
- Revisione 1.0, 2026-10-09: contratto locale e conservazione dei gate, nessuna attivazione.
