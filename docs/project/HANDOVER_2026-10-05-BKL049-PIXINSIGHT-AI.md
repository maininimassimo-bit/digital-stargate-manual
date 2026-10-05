# Handover — M27 e pilota PixInsight con IA

| Campo | Valore |
|---|---|
| ID | DSG-HO-BKL049-20261005 |
| Versione | 1.7 |
| Data | 2026-10-05 |
| Stato | Riconciliazione operativa; estensione pilota autorizzata, non accettata come produzione |
| Pacchetto | BKL-049 archivio chiuso; BKL-049-EXT-PIAI pilota distinto |

## Continuità e autorità

Questo documento e la [baseline corrente](CURRENT_TECHNICAL_BASELINE_2026-10-05.md) sostituiscono gli snapshot del 25 settembre come punto di ingresso. Gli snapshot e la [closure BKL-049](BKL-049-CLOSURE-2026-10-02.md) restano storici. BKL-043 rimane aperta: F4 attende lifecycle e accettazione finale, secondo lo [stato del 1 ottobre](BKL-043-F4-STATUS-2026-10-01.md). Il lavoro PixInsight non ne modifica autorizzazioni o gate.

L’Owner ha richiesto documentazione completa e avvio del pilota sul proprio PC già utilizzato per M27. Questa autorizzazione riguarda file scientifici locali e copie di lavoro; non introduce comandi all’osservatorio, Safety Authority, servizi a pagamento o pubblicazione automatica.

## Lavoro effettuato

| Risultato | Evidenza e limite |
|---|---|
| Archivio e collegamento immagine/versione/workflow | BKL-049 chiusa nel perimetro available-history; PR #471 e closure. La successiva rimozione della scadenza mantiene la pubblicazione fino a ritiro esplicito. |
| Caricamento foto e workflow | Procedura Owner-only autenticata, archivio privato e preview pubblica; PR #474–#476, runbook infrastrutturale. Gli esempi M31/M42/NGC7000 sono stati rimossi. |
| Esportazione History e lettore | Esportatore multi-view 2.0.1 e importer 1.2, PR #477. Importazione dati senza eseguire JavaScript caricato. Correlazioni e lacune esplicite. |
| M27 LRGB con assistenza IA | Elaborazione nativa PixInsight su quattro master calibrati/allineati, 4634×2808, senza modificare i master. ABE, composizione RGB, calibrazione colore stellare, BXT/NXT/SXT, stretch, luminanza, contrasto locale, saturazione e reintegrazione stelle. Non è stata applicata SPCC. |
| Dettaglio interno M27 | Due LHE mascherate sulla nebulosa senza stelle; parametri conservati privatamente; ricomposizione con le stelle conservate. Versione precedente conservata. |
| File finali | XISF Float32 non lineare, TIFF RGB16 sRGB, JPEG piena risoluzione e derivato web. Verifiche native e integrità conservate privatamente. Non si dichiara assenza di clipping o qualità scientifica certificata. |
| History dell’ultima versione | 24 viste selezionate, 80 processi, 147 istanze, export di 452929 byte. Viste invariate dopo esportazione. Completezza delle history disponibili, non ricostruzione universale del progetto o replay garantito. |
| Sostituzione pubblicazione | Il 5 ottobre vecchia versione ritirata e nuova versione pubblicata sulla stessa immagine M27, con il relativo workflow. UI archivio e successiva GET pubblica verificate; evidenze private conservate. |
| Sessioni associate | Tutte le 16 sessioni M27 presenti nel catalogo consultato sono associate per dichiarazione Owner; questa associazione non dimostra il contributo di ogni sessione ai master finali. |

## Identità dell’ultima pubblicazione

- Immagine: `IMG-c82f01a62d69990ecb22693d6caf76d2`.
- Versione ritirata: `VER-66396f1a229a92f53d6d64aa9e225976`.
- Versione pubblicata: `VER-5e5dd49a62f90e349e2931f3d143b941`.
- Workflow: `WF-5e5dd49a62f90e349e2931f3d143b941`.
- Data elaborazione: 2026-10-02; pubblicazione: 2026-10-05.

La [evidenza minimizzata](evidence/BKL-049-M27-PUBLIC-2026-10-05.json) deriva da una nuova GET anonima effettuata il 5 ottobre: una sola riga per M27, versione corretta, 80 passi, 16 sessioni, zero parametri pubblici. La GET non dimostra da sola il ritiro privato della vecchia versione o gli hash dei file privati. La [gallery](../scientific-image-gallery/index.md) conserva `PARTIAL`, `NOT_ESTABLISHED` e `OWNER_DECLARED`: l’importer non certifica l’esecuzione anche quando l’elaborazione assistita è documentata separatamente.

## Ripresa del pilota

Seguire il [piano BKL-049-EXT-PIAI](../architecture/assessments/BKL-049-EXT-PIAI-Local-Pilot.md). Prima verificare ambiente e disponibilità dei master senza modificarli, poi eseguire una ricetta controllata su copie. Un job per volta; journal privato per ogni azione, output e dipendenza. Le history importate restano dati, mai programmi da eseguire.

La coda P4 è implementata e il cloud/credenziale sono stati approvati e attivati; OAT Owner/nativo ancora aperto. Provider IA con API e comando scientifico P5 non sono attivati. L’abbonamento alla chat non è una credenziale API per un servizio. L’installazione già presente non costituisce attestazione di licenza per usi multiutente o commerciali.

## Handover operativo e rollback

Conservare privatamente originali, XISF/TIFF/JPEG, export, correlazioni, journal di elaborazione e verifiche. Il repository pubblico contiene documentazione, codice e prove minimizzate: niente percorsi privati, parametri integrali, token o binari scientifici.

Per un errore del pilota fermare il job tra i processi, conservare la ricevuta e ripartire da copie nuove. Non sovrascrivere master, prodotti approvati o revisioni pubblicate. Il pilota non richiede sostituzione della M27 pubblicata. Un eventuale ritiro pubblico segue la procedura autenticata e conserva l’archivio privato; non garantisce il richiamo di copie o cache di terzi.

## Gate e registro revisione

Riconciliazione locale e verifica GET effettuate. CI, ARB, Release Quality, merge e verifica Pages della presente revisione devono risultare dalla PR di consegna; non sono anticipati come completati. Versione 1.0: prima riconciliazione cumulativa al 5 ottobre e consegna al pilota locale.

## Aggiornamento successivo — pilota P1 avviato

Riconciliazione documentale consegnata tramite PR #478, merge `351067822c5b5ac0632c57408fd530ad85614914`, 17 controlli exact-head e 18 workflow post-merge SUCCESS; ARB e RQ AI-assistite sequenziali, zero finding finali. Successivamente effettuato il preflight nativo sul PC Owner: PI 1.9.5 build 1706, quattro master integri e invariati, selezione esplicita nei contenitori multi-image e 12 costruttori di processo disponibili. [Ricevuta minimizzata](evidence/BKL-049-PIAI-P1-2026-10-05.json). Nessuna elaborazione pixel o richiesta provider nel test. Versioni moduli, modelli e licenze non attestati dal preflight. P2 esecutore su copie e P3 elaborazione restano successivi; il pilota è avviato, non completo né di produzione. Versione 1.1: esito P1, nuova consegna CI/review da tracciare sulla PR di implementazione.

## Aggiornamento storico — P2 locale verificato

P1 consegnata tramite PR #479, merge `76d6186489c78aceb32f34a6b96afbe8f88457a7`, 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ sequenziali senza finding finali. P2 ora dispone di coordinatore, prenotazione di un job, snapshot esecutore, handle esclusivo Windows, copie verificate e journal privato delle operazioni native. Il lancio rimane supervisionato in PixInsight; nessuna connessione remota è inclusa.

Prova nativa M27: cinque processi riusciti e cinque checkpoint Float32 4634×2808 lineari, con originali invariati. Quattro estrazioni del fondo sulle copie e composizione RGB; luminanza preparata ma non integrata. Pre-cancel nativo con zero processi; replay rifiutato e 37 file del job concluso invariati. [Ricevuta P2](evidence/BKL-049-PIAI-P2-2026-10-05.json). Il workflow derivato contiene solo le cinque operazioni riuscite, leggibili come dati dall’importer 1.2; non rappresenta tutta la History precedente dei master.

Il prossimo gate è P3: elaborazione non lineare, controlli pixel, colore/astrometria e confronto visivo. Questa prova non sostituisce la M27 pubblicata e non ne certifica qualità scientifica. Annullamento durante un processo reale verificato dopo la correzione ARB del canale di richiesta; guasti nativi coperti da test sintetici; crash/offline e connessione remota restano gate futuri. Per un crash conservare la prenotazione e l’evidenza, confermare PixInsight fermo e quarantinare il root prima di usarne uno nuovo. Procedura dettagliata in `tools/pixinsight/local_pilot/README.md`. Versione 1.2: esito P2; CI/review/merge e post-merge da registrare sulla PR della consegna.

Riesame P2: un Major ARB ha rilevato che il comando cancel tentava di leggere il file tenuto con handle esclusivo. Corretto con identità immutabile del job separata e marker completo pubblicato atomicamente, vincolato al token e verificato dal runtime. Prova Windows con handle reale e prova nativa PixInsight: lettura del lease negata, comando cancel riuscito durante il primo processo; arresto prima del checkpoint successivo, un processo registrato, zero output e originali invariati. Il processo in corso può terminare prima dell’annullamento. Il riesame finale richiede CI e ARB/RQ sul nuovo head.

Consegna P2 completata: PR #480, head `1a9e90142ec969d23540ff344eb983af6dde1564`, merge `f8ec8a066b56095db430f1c50d4b8dad9f812ce4`; 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate. Questo esito supera le indicazioni di consegna ancora pendente nelle sezioni storiche.

## Aggiornamento corrente — P3 non lineare

Implementata la ricetta M27 separata: 29 processi nativi e 15 checkpoint, incluso il finale Float32 RGB non lineare. Il journal registra anche maschere e output stelle; l’export delle istanze è dati, non replay o completezza della History a monte. La raccolta legge tutti i pixel finali e conta clipping/canali. La valutazione cromatica è empirica, non SPCC; l’acceptance scientifica rimane Owner review required.

Prova nativa definitiva e confronto visivo completati; evidenza minimizzata riportata di seguito. Consegna CI/review riferita allo stesso head sulla PR. P4 protocollo/provider/diritti e P5–P6 portale/acceptance sono successivi. Nessuna nuova pubblicazione, chiamata provider o authority sui dispositivi. Conservare privatamente XISF, derivati, workflow, correlazioni, manifest e ricevute. [Procedura](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/main/tools/pixinsight/local_pilot).

Prova definitiva nativa 2026-10-05: 29 azioni, 15 checkpoint, finale RGB Float32 4634×2808 non lineare, originali invariati e snapshot verificato. Tutti i pixel finali finiti e in [0,1]; clipping presente e misurato, senza dichiarazione di assenza. Astrometria nativa conservata, TIFF RGB16 e JPEG sRGB verificati. Confrontati campo intero e ritaglio 100% con la versione pubblicata: strutture/stelle/colore coerenti, ma la precedente conserva maggior contrasto interno. Nessuna sostituzione né acceptance scientifica automatica.

History disponibili esportate: 13 viste, 47 passi, 82 istanze, 427862 byte; immagini invariate durante la lettura, importer 1.2 `PARSED_SUBSET`. `executionEvidence=NOT_ESTABLISHED` e `workflowCompleteness=UNAVAILABLE` restano le classificazioni del file importato; non sono convertite dalla prova nativa del pilota. Il journal nuovo conserva separatamente 29 azioni e relazioni con maschere/stelle/copie.

Prove native negative: pre-cancel con zero processi/output; selezione della maschera ausiliaria invece del master rifiutata prima delle operazioni; replay rifiutato con tutti i 117 file del job concluso identici. Le prove di errore plugin restano sintetiche. Test locali: 13 preflight, 20 esecutore, 25 coordinatore e 5 pixel. [Ricevuta minimizzata P3](evidence/BKL-049-PIAI-P3-2026-10-05.json). CI/review e post-merge tracciati sulla PR dello stesso head. P4–P6 e acceptance Owner restano successivi.

Consegna P3 completata: PR #481, head `ce819ea192a30522f2c168631a0c1b05f77adfd9`, merge `342a169dbc87433da971f1660a239e6dc5a6b343`; 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate. Supera le indicazioni storiche di consegna P3 ancora pendente; acceptance scientifica Owner aperta.

## Snapshot precedente — P4 candidato prima dell’approvazione

L’Owner sceglie `SESSION_ASSISTED`: assistente di questa sessione, zero nuove chiamate API IA a pagamento. Implementati coda privata con CAS/backup, identità persistente senza scadenza o riassegnazione offline, autenticazione distinta Google Owner/credenziale worker e adapter PC HTTPS in uscita con allowlist locale. Preparazione una sola volta, retry di messaggi identici, cancellazione P2, raccolta solo dopo conferma di arresto nativo, recupero conservativo. Nessun avvio automatico PixInsight o modello cloud autonomo.

[Pacchetto operativo e proposta concreta](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/main/infrastructure/pixinsight-pilot): servizio Cloud Run separato, identità/registry e due bucket privati per soli stati, min=0/max=1, 1 CPU/512 MiB. Nuova infrastruttura potenzialmente a pagamento e credenziale dedicata richiedono approvazione prima di creazione/attivazione. Nessuna risorsa o credenziale creata, nessun OAT cloud/Google/TLS nativo dichiarato. Test persistenti sintetici e HTTP loopback reali restano distinti da runtime operativo. P4 resta aperta per attivazione; P5/P6 e acceptance Owner restano successivi. Archivio/M27 pubblicata e autorità dispositivi/Safety invariati.

Verifica candidato P4: 33 test Node e 62 Python Windows, inclusi 32 casi trasporto. [Ricevuta minimizzata](evidence/BKL-049-PIAI-P4-2026-10-05.json). CI/review dello stesso head e post-merge da registrare sulla PR; nessuna attivazione cloud anticipata.

Riesame P4: un Major ARB ha riprodotto una seconda preparazione su root nuovo privo di binding. Corretto con identità locale persistente fissata dalla prima claim e transizione PREPARING confermata prima delle copie; claim avanzata senza binding rifiutata. Cinque regressioni coprono nuovo root, stati avanzati, perdita della risposta iniziale e preparazione interrotta. CI e riesame finale dello stesso head richiesti sulla PR.

## Aggiornamento corrente — P4 cloud autorizzato e attivato

L’Owner ha approvato le risorse e la credenziale dedicate il 5 ottobre. PR #482 consegnata: head `875cc375a130268b4be98b28ad11a7c8c11e4552`, merge `e000a3b96c980c22d47967e26fb5e79633c3d249`; 16 CI exact-head e 16 workflow post-merge SUCCESS, ARB/RQ AI-assistite separate e sequenziali senza finding finali, Pages effettive verificate.

Il nuovo servizio Cloud Run è attivo su immagine verificata per digest, con identità/registry e due bucket privati versionati separati. Credenziale PC generata e protetta con Windows User DPAPI, solo digest al server. Collegamento PC HTTPS reale e dieci controlli HTTP PASS; nessuna nuova API IA, porta PC in ingresso, esecuzione nativa automatica o pubblicazione. La [ricevuta di attivazione](evidence/BKL-049-PIAI-P4-ACTIVATION-2026-10-05.json) e il [runbook](PIAI-P4-CLOUD-ACTIVATION-2026-10-05.md) distinguono prove reali e gate ancora aperti.

Autenticazione Google Owner reale PASS sulla pagina diagnostica: creazione sintetica, ripetizione idempotente, annullamento e lettura CANCELLED/NONE. Google valido non-Owner negato e stale-create CAS reale negato senza mutazione. Riavvio del servizio sullo stesso digest e perdita deliberata dell’ack PREPARING dopo commit remoto: stessa richiesta recuperata, una preparazione; ciclo ripetuto con otto file identici.

Trasporto nativo sul PC verificato con due fixture amministrative isolate: pre-cancel con zero processi/output; M27 non lineare COMPLETED con 29 azioni, 15 checkpoint e 29 istanze workflow, originali invariati, finale Float32 RGB 4634×2808 e tutti i pixel finiti in [0,1]. Clipping misurato, non certificato assente. Raccolta dopo arresto PixInsight, prenotazioni chiuse e report remoto verificato. Questa prova usa Broker/BackedUpStore tramite CLI Owner amministrativa: non attesta ancora la creazione di un job scientifico dal comando HTTP/UI Owner. La prova HTTP Owner separata è sintetica; executionEvidence resta WORKER_REPORTED_NOT_ATTESTED, publication=NONE.

P4 ha ora una prova tecnica nativa circoscritta; CAS GCS concorrente reale PASS tramite CLI Owner amministrativa: due scritture degli stessi bytes di coda terminale, una accettata e una rifiutata per generazione obsoleta, backup verificato e stato logico invariato. Concorrenza sulle route Owner HTTP soltanto sintetica; acceptance operativa più ampia resta aperta. P5 comando scientifico/sessioni/preview/provenance, P6 e acceptance scientifica Owner sono successivi. SESSION_ASSISTED, zero nuove chiamate API IA; M27 pubblicata e autorità dispositivi/Safety invariate. Evidenza privata conservata; ricevuta pubblica minimizzata e runbook collegati sopra. CI/review/merge e Pages di questa riconciliazione sono da verificare sulla PR di consegna.

Osservazione reale dopo oltre 120 secondi senza contatto: OFFLINE diagnostico, stesso job/root ancora RUNNING, nessuna scadenza o riassegnazione osservata. Non è una prova di crash recovery del desktop.

Derivati locali TIFF RGB16/JPEG sRGB verificati; soluzione astrometrica conservata e checkpoint invariato dopo export. History disponibile: 13 viste, 47 passi, 82 istanze, 429679 byte; importer 1.2 PARSED_SUBSET. La History conservata non prova completezza a monte: executionEvidence=NOT_ESTABLISHED e workflowCompleteness=UNAVAILABLE del file importato restano invariati. Journal e correlazioni runtime delle 29 azioni conservati separatamente. Campo intero/dettaglio coerenti con la ricetta P3; nessuna superiorità scientifica o sostituzione pubblica dichiarata.


## Aggiornamento P5 — portale scientifico privato (2026-10-05)

Implementato il candidato P5: pagina Owner, selezione di master M27 registrati, sessioni/catalogo e versione di riferimento esatti; job con contesto immutabile e verifica sul PC prima delle copie; stato/cancel espliciti, preview privata, workflow delle 29 azioni, correlazioni runtime e revisione Owner vincolata alla ricevuta. Originale e journal completo restano sul PC. Le identità IMG/VER/WF del pilota sono private e distinte dall’archivio di pubblicazione; nessun caricamento o pubblicazione automatica. SESSION_ASSISTED senza nuove API IA; classificazioni WORKER_REPORTED_NOT_ATTESTED, OWNER_DECLARED e History a monte NOT_ESTABLISHED preservate. Deployment/release e prova scientifica reale HTTP/UI → PixInsight → consegna/revisione sono ancora gate P5 aperti, non simulati dai test. P6 e acceptance scientifica Owner restano successivi. [Procedura P5](PIAI-P5-PORTAL-2026-10-05.md).
