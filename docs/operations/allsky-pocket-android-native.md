---
title: Allsky Pocket · progetto Android nativo
description: Prima versione Android nativa con Live, Meteo e Archivio, da provare sul telefono, senza modificare Allsky e con candidati privati esclusi.
---

# Allsky Pocket: prima versione Android nativa

**Aggiornamento:** 16 novembre 2026. **Stato:** beta APK debug v0.1.0 installata su Motorola G84, Android 15/API35; l’Owner conferma avvio, riproduzione timelapse e apertura immagini startrail/keogramma. Il decoder AVC e il dialogo immagini sono stati corretti dopo la prova reale. Restano da completare le prove di resilienza e l’integrazione della PR #638. La pubblicazione Google Play è separata e non compresa. Gestione del progetto: Massimo Mainini. Vedi [rapporto tecnico v0.1](allsky-pocket-android-v1.md) per APK e checksum.

Questo documento prepara una chat Work dedicata alla realizzazione della prima versione installabile sul telefono dell’Owner. La [PWA pubblica esistente](allsky-pocket-pwa.md) resta separata e disponibile: non è la nuova app nativa. Questo aggiornamento del manuale non modifica il Raspberry, l’acquisizione o l’hosting della PWA.

## Obiettivo della prima versione

Client Android in **Kotlin e Jetpack Compose**, con interfaccia nativa e tre schede di sola consultazione. La prima consegna è un **APK di prova locale**, con sorgenti, istruzioni e rapporto dei controlli; la distribuzione Google Play è una fase successiva, senza acquisti o invii allo store in questo perimetro.

| Scheda | Perimetro della prova |
|---|---|
| Live | Ultimo JPEG, ora dello scatto, aggiornamento automatico mentre visibile e manuale, zoom/schermo intero, stato connessione e immagine scaduta |
| Meteo | Temperatura ambiente, umidità, punto di rugiada e vento km/h CloudWatcher; ora della misura, scadenza e indisponibilità |
| Archivio | Timelapse, startrails e keogrammi pubblici, elenco dal più recente, selezione data/notte, immagini complete e video con controlli |

Il live è una successione di fotografie, non un flusso video continuo. Le date archivio rappresentano l’inizio della notte. Nessun controllo dell’osservatorio, login amministrativo, galleria meteore, overlay astronomico nativo, push, analisi scientifica o archivio offline completo è richiesto alla prima versione. L’overlay resta consultabile sul sito Allsky esistente.

## Confini di dati e integrazione

Le sorgenti pubbliche sono state verificate il 16 novembre 2026: i cinque endpoint ammessi hanno risposto correttamente; ciascun catalogo conteneva 605 link validi e i tre media recenti erano scaricabili. Dettagli e campioni sono nel rapporto tecnico.

Baseline da verificare nella chat di sviluppo: [contratto della PWA](allsky-pocket-pwa.md#architettura-e-percorsi-ammessi), codice PWA se disponibile e comportamento delle sorgenti pubbliche. Origine Allsky: `https://digitalstargate.freeddns.it:23232`.

| Sorgente pubblica già documentata | Utilizzo ammesso |
|---|---|
| `/current/image.jpg` | Immagine corrente |
| `/allsky/dsg-live-data.json` | Selezione dei soli campi camera, weather e astronomy necessari; non riversare il JSON completo nell’app |
| `/allsky/videos/`, `/allsky/startrails/`, `/allsky/keograms/` | Cataloghi e relativi file/miniature, con nomi e percorsi validati |

L’accessibilità reale e la stabilità del formato vanno provate prima di fissare l’architettura. Il client nativo può leggere le sorgenti HTTPS pubbliche direttamente; un eventuale servizio intermedio va motivato e proposto separatamente, senza introdurre implicitamente canoni o modificare l’impianto. Non assumere che l’hosting PWA sia utilizzabile come API stabile senza verificarlo. I percorsi sono una allowlist, non un invito a esplorare altre risorse.

Sono esclusi candidati meteore privati, immagini/ritagli/miniature, metadati individuali, contatori e registro del rilevatore temporale. Non leggere `/var/lib/dsg-meteor-shadow`, non accedere alla WebUI e non usare SSH per collegare l’app. Anche la galleria meteore già pubblica resta fuori dal prototipo, così da limitare il contratto alle tre categorie concordate. Non copiare backup privati o chiavi nel progetto, nell’APK o nei log.

TLS ordinario, origine fissata, nessuna disabilitazione dei certificati e nessun URL arbitrario. Ridurre le letture al necessario, sospendere il polling quando l’app non è visibile, introdurre timeout e attesa crescente dopo gli errori. La baseline PWA aggiorna ogni 30 s, accetta proiezione entro 150 s e scatto entro 180 s, con controlli sugli orari futuri e scadenza meteo: riusare queste regole dove applicabili e documentare eventuali differenze. Dati mancanti/scaduti non devono diventare zero o condizioni meteo attuali. Un’immagine conservata è etichettata come ultimo fotogramma.

## Piano e stima iniziale

| Traguardo | Stima di lavoro cumulativa | Condizione |
|---|---:|---|
| APK essenziale da provare | 30–50 ore | Tre schede, sorgenti esistenti utilizzabili, strumenti disponibili |
| Beta rifinita | 80–120 ore | Prove aggiuntive su dispositivi e correzioni |
| Preparazione e pubblicazione Play | 120–180 ore | Fase successiva, soggetta a test, account e revisione Google |

Sono stime di pianificazione, non tempi misurati o garanzie. La prima versione può richiedere indicativamente 1–2 settimane di lavoro regolare; non è una scadenza promessa. Le stime successive includono le precedenti. Per l’Owner prevedere indicativamente 4–8 ore distribuite di prove e decisioni nell’intero progetto, oltre alla disponibilità degli eventuali tester.

Android Studio e librerie gratuite sono la scelta iniziale. Nessun nuovo hosting o API AI è previsto se si riusano le sorgenti esistenti. Utilizzo Codex ed eventuali crediti dipendono dal piano dell’Owner e non sono quantificati qui. L’account Google Play costa **25 USD una tantum** se non già presente; non serve acquistarlo per definire il progetto e predisporre l’APK locale. Per nuovi account personali soggetti ai requisiti Google sono richiesti almeno **12 tester iscritti continuativamente per 14 giorni** prima della richiesta di accesso alla produzione. Costi e policy vanno ricontrollati prima della pubblicazione, distinta dalla prova locale.

Fonti: [account Google Play](https://support.google.com/googleplay/android-developer/answer/6112435?hl=en), [test per account personali](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en), [utilizzo Codex](https://chatgpt.com/codex/pricing/).

## Criteri di consegna e verifica

1. Build ripetibile con versioni documentate e APK di prova installabile, identificativo/versione e checksum SHA-256. Chiavi di firma e dati locali fuori da Git; chiarire che la firma di debug è per la prova e non è una release Play.
2. Tre schede funzionanti con dati reali, gestione di rete assente/lenta, JSON parziale, misure scadute, errori JPEG/video e archivio vuoto. Fotogrammi e misure con orari distinti; nessuna condizione meteo inventata.
3. Test mirati dei parser, della selezione dei campi e delle regole di freschezza, più prova di navigazione, rotazione e passaggio Wi-Fi/rete mobile. Verificare che richieste, modello dati e log escludano meteore e percorsi privati.
4. Installazione e avvio, riproduzione timelapse e apertura immagini startrail/keogramma verificati su telefono reale; Live e Meteo sono stati verificati su emulatore. Il riscontro dell’Owner sul Motorola è registrato nel rapporto tecnico. Restano rotazione, cambio Wi-Fi/mobile, background e condizioni di errore/rete.
5. Documentare esiti reali, limiti e problemi aperti nel repository, mantenendo invariata la configurazione Allsky. La rimozione dell’app dal telefono è il rollback del client; non ripristinare il Raspberry.

Il toolchain portabile usato per la build resta sotto `android/.local-toolchain/` e non è incluso in Git. Per installare l’APK, trasferirlo sul telefono, consentire temporaneamente l’installazione da quella sorgente e aprire il file; i passaggi dettagliati e il checksum sono nel rapporto tecnico. La firma debug è destinata alla prova.

## Prompt iniziale per la chat Work (archiviato)

Avvia lo sviluppo della prima versione Android nativa di **Allsky Pocket – Digital Stargate**, da installare e provare sul mio telefono. Usa Kotlin e Jetpack Compose, con schede Live, Meteo e Archivio. Leggi prima questa guida, la guida PWA, il Capitolo 27 e le istruzioni del repository `maininimassimo-bit/digital-stargate-manual`. Usa un branch/worktree isolato, preserva il lavoro esistente e verifica gli strumenti Android disponibili.

Realizza un client di sola consultazione delle sorgenti pubbliche già documentate: JPEG live, selezione dei dati camera/meteo necessari e archivio timelapse/startrails/keogrammi. Verifica i contratti reali prima di implementarli. Mantieni invariata la configurazione Allsky, acquisizione, maschere, calibrazione, router, rilevatori e PWA pubblicata. Nessun accesso amministrativo o SSH dall’app. Nessuna lettura, copia o pubblicazione di candidati temporali privati, metadati, contatori o registri; nessuna galleria meteore nel prototipo.

Live deve avere ora dello scatto, aggiornamento manuale e periodico solo quando visibile, zoom e stato connessione/freschezza. Meteo deve mostrare temperatura ambiente, umidità, rugiada e vento km/h con ora della misura e scadenza. Archivio deve consentire di scegliere notte e prodotto, aprire immagini e riprodurre i filmati pubblici. Non inventare dati e non presentare un dato scaduto come attuale. Usa HTTPS con verifica certificati, timeout, carico limitato e percorsi ammessi; niente URL arbitrari o segreti nei sorgenti/log.

Procedi autonomamente con verifica delle sorgenti, progetto, implementazione, test mirati e build. Consegna sorgenti, APK di prova con checksum, istruzioni semplici di installazione e checklist per il mio telefono. Chiedi modello/versione Android solo se non ricavabili e utili alle prove, continuando il lavoro indipendente. Distingui test automatici/emulatore da collaudo fisico Owner e non dichiarare risultati non osservati.

Prima consegna prevista: APK essenziale, stima iniziale 30–50 ore da affinare dopo l’analisi. Non acquistare servizi, creare account a pagamento o pubblicare su Google Play; eventuali servizi intermedi/costi nuovi vanno proposti prima. La fase Play verrà autorizzata separatamente. Documenta decisioni, versioni, prove e limiti nel repository e completa il normale percorso di PR/controlli/pubblicazione documentale previsto dalle istruzioni applicabili. Se emerge un blocco, spiega il fatto concreto senza modificare l’impianto per aggirarlo.
