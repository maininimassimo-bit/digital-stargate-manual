# Handover — M27 e pilota PixInsight con IA

| Campo | Valore |
|---|---|
| ID | DSG-HO-BKL049-20261005 |
| Versione | 1.2 |
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

La coda remota, un provider IA con API, budget, credenziali e il comando dal portale sono fasi successive non implementate. L’abbonamento alla chat non è una credenziale API per un servizio. L’installazione già presente non costituisce attestazione di licenza per usi multiutente o commerciali.

## Handover operativo e rollback

Conservare privatamente originali, XISF/TIFF/JPEG, export, correlazioni, journal di elaborazione e verifiche. Il repository pubblico contiene documentazione, codice e prove minimizzate: niente percorsi privati, parametri integrali, token o binari scientifici.

Per un errore del pilota fermare il job tra i processi, conservare la ricevuta e ripartire da copie nuove. Non sovrascrivere master, prodotti approvati o revisioni pubblicate. Il pilota non richiede sostituzione della M27 pubblicata. Un eventuale ritiro pubblico segue la procedura autenticata e conserva l’archivio privato; non garantisce il richiamo di copie o cache di terzi.

## Gate e registro revisione

Riconciliazione locale e verifica GET effettuate. CI, ARB, Release Quality, merge e verifica Pages della presente revisione devono risultare dalla PR di consegna; non sono anticipati come completati. Versione 1.0: prima riconciliazione cumulativa al 5 ottobre e consegna al pilota locale.

## Aggiornamento successivo — pilota P1 avviato

Riconciliazione documentale consegnata tramite PR #478, merge `351067822c5b5ac0632c57408fd530ad85614914`, 17 controlli exact-head e 18 workflow post-merge SUCCESS; ARB e RQ AI-assistite sequenziali, zero finding finali. Successivamente effettuato il preflight nativo sul PC Owner: PI 1.9.5 build 1706, quattro master integri e invariati, selezione esplicita nei contenitori multi-image e 12 costruttori di processo disponibili. [Ricevuta minimizzata](evidence/BKL-049-PIAI-P1-2026-10-05.json). Nessuna elaborazione pixel o richiesta provider nel test. Versioni moduli, modelli e licenze non attestati dal preflight. P2 esecutore su copie e P3 elaborazione restano successivi; il pilota è avviato, non completo né di produzione. Versione 1.1: esito P1, nuova consegna CI/review da tracciare sulla PR di implementazione.

## Aggiornamento corrente — P2 locale verificato

P1 consegnata tramite PR #479, merge `76d6186489c78aceb32f34a6b96afbe8f88457a7`, 17 controlli exact-head e 16 workflow post-merge SUCCESS, ARB/RQ sequenziali senza finding finali. P2 ora dispone di coordinatore, prenotazione di un job, snapshot esecutore, handle esclusivo Windows, copie verificate e journal privato delle operazioni native. Il lancio rimane supervisionato in PixInsight; nessuna connessione remota è inclusa.

Prova nativa M27: cinque processi riusciti e cinque checkpoint Float32 4634×2808 lineari, con originali invariati. Quattro estrazioni del fondo sulle copie e composizione RGB; luminanza preparata ma non integrata. Pre-cancel nativo con zero processi; replay rifiutato e 37 file del job concluso invariati. [Ricevuta P2](evidence/BKL-049-PIAI-P2-2026-10-05.json). Il workflow derivato contiene solo le cinque operazioni riuscite, leggibili come dati dall’importer 1.2; non rappresenta tutta la History precedente dei master.

Il prossimo gate è P3: elaborazione non lineare, controlli pixel, colore/astrometria e confronto visivo. Questa prova non sostituisce la M27 pubblicata e non ne certifica qualità scientifica. Annullamento durante un processo reale verificato dopo la correzione ARB del canale di richiesta; guasti nativi coperti da test sintetici; crash/offline e connessione remota restano gate futuri. Per un crash conservare la prenotazione e l’evidenza, confermare PixInsight fermo e quarantinare il root prima di usarne uno nuovo. Procedura dettagliata in `tools/pixinsight/local_pilot/README.md`. Versione 1.2: esito P2; CI/review/merge e post-merge da registrare sulla PR della consegna.

Riesame P2: un Major ARB ha rilevato che il comando cancel tentava di leggere il file tenuto con handle esclusivo. Corretto con identità immutabile del job separata e marker completo pubblicato atomicamente, vincolato al token e verificato dal runtime. Prova Windows con handle reale e prova nativa PixInsight: lettura del lease negata, comando cancel riuscito durante il primo processo; arresto prima del checkpoint successivo, un processo registrato, zero output e originali invariati. Il processo in corso può terminare prima dell’annullamento. Il riesame finale richiede CI e ARB/RQ sul nuovo head.
