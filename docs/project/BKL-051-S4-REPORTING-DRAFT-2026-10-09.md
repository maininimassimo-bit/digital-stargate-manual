# BKL-051 S4-R — dossier preliminare privato

Stato: Candidate; exact-head CI, ARB/RQ e rilascio pending. BKL-051 OPEN. Estensione reporting già approvata dall’Owner; questo incremento prepara evidenze, senza invii.

## Comportamento

`python -m tools.scientific_transients.reporting_draft` riceve root artifacts/registry, request locale, SHA256 indipendentemente verificato e output-root privata disgiunta. Protocollo chiuso `DSG_TRANSIENT_REPORTING_DRAFT_V1`: dossierRef/bindingRef opachi, manifestSha256, categoryDeclared/channelDeclared/dataOriginDeclared, note e evidencePaths. Origine dichiarata REAL/SYNTHETIC/NOT_ATTESTED non viene attestata. Categoria e canale sono dichiarazioni esplicite, non classificazioni automatiche: GALACTIC_NOVA_CANDIDATE/CBAT, EXTRAGALACTIC_TRANSIENT_CANDIDATE/TNS, VARIABLE_STAR_CANDIDATE/VSX, MOVING_OBJECT_CANDIDATE/MPC. Sorgente sconosciuta non instradata; nova galattica/TNS respinta.

Parser stretto, hash raw pinned, binding registrato e tutti i byte del manifest verificati. Selezione evidenze soltanto fra percorsi registrati unici, senza traversal/link/reparse. Hash attesta integrità puntuale, non verità, origine, calibrazione, priorità o novità scientifica. Il binding non deve necessariamente essere un run completato: il dossier può contenere materiale preparatorio e non ne deriva alcuna attestazione nativa. Note private possono contenere osservazioni libere; non sono interpretate o promosse a misure.

Stato sempre DRAFT; scienceValidation NOT_VALIDATED, scientificClassification NOT_EVALUATED, submissionAuthorized false, externalSubmission NONE. Nessun campo di input può concedere READY/AUTHORIZED/SENT/ACCEPTED. Nessuna lettura di credenziali, rete, payload produttivo o destinatario automatico. I gate dichiarati mancanti comprendono validazione indipendente, calibrazione/uncertainty, timing/passband, requisiti correnti del provider e autorizzazione Owner. Non sono un elenco esaustivo né una policy che abilita invii.

## Esportazione e conservazione

JSON privato completo con manifest genitore, HTML italiano passivo escapato e CSP default-src/base-uri/form-action none; nessun link o risorsa remota. Directory esclusiva per dossierRef, digest di entrambi gli output nel manifest export.json, seconda verifica dei sorgenti prima del completamento. File parziali e failed.json conservati; stesso riferimento non riutilizzabile e nessun overwrite/retry. Radici disgiunte dal registro/dati, richiesta esterna all’output; archivi non autosufficienti (completeDependencyArchive false): conservare radice dati e registro genitore. Nessun export automatico nel portale pubblico.

Non dedurre magnitudini, ADU, banda, coordinate, sigma o tempo dalla somma normalizzata o dalla data di elaborazione. Un’eventuale richiesta di futura segnalazione produttiva richiede workflow scientifico validato, policy quantitativa accettata e authority Owner separata.

## Fonti e limiti degli adattatori

[CBAT](https://tamkin3.eps.harvard.edu/HowToReportDiscovery.html) descrive la segnalazione di possibili scoperte; API produttiva non verificata. [VSX](https://vsx.aavso.org/index.php?view=about.notice) ha un percorso di revisione. TNS richiede verifica completa del formato ufficiale e delle restrizioni: accesso a parti della documentazione è stato negato, nessun payload inventato. [MPC ADES](https://docs.minorplanetcenter.net/mpc-ops-docs/observations/ades-format/) distingue lo schema di invio dai requisiti ulteriori: ricerca privata pinned IAU-ADES `f4158f96a049b83dfcf848fa33eaac4391db9460`, fixture 2022 valida e vecchia fixture non valida. Non viene aggiunta una dipendenza XML né implementato un esportatore produttivo. Validità XML non attesta misura o accettazione provider.

## Verifica e residui

Dodici prove locali sintetiche verificano i quattro canali, assenza rete, schema/authority extra e duplicate keys respinti, hash/dati alterati, percorsi sconosciuti/duplicati/traversal, root overlap, HTML ostile, riuso e alterazione durante export con conservazione dei fallimenti. Nessun OAT nativo/cloud o evento recuperato. CI Linux/Windows include il modulo.

Restano S2/S3 scientifiche, PC/cloud OAT, moving objects con tempi/astrometria/calibrazione validati, adattatori produttivi, sandbox e policy/invii accettati. Runtime e invii disattivati. P6, F4/F5/BKL-050 e S10/Safety invariati. Rollback del codice conserva integralmente tutti gli archivi; non cambia vecchi job o evidenze.
