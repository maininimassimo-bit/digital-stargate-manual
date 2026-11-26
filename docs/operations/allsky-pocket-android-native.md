---
title: AllSky Manciano · progetto Android nativo
description: App Android nativa Allsky Pocket con Live, Meteo, Archivio, galleria meteore candidate pubblica e mappa VirtualSky calibrata.
---

# AllSky Manciano: progetto Android nativo

## Beta 0.2.12 (build 14)

- **Meteo:** mostra lo stato della copertura del cielo rilevato dal CloudWatcher di Manciano (Sereno, Nuvoloso o Coperto).
- **Archivio:** la scheda **Meteo della notte** compare sotto il timelapse, lo startrail o il keogramma selezionato. La data del prodotto identifica la sera di inizio notte. Il riepilogo riporta la condizione prevalente, le percentuali sul tempo classificato, la temperatura minima e massima, l’umidità e il vento medi. Le notti con copertura incompleta dei dati sono indicate come parziali.
- **Acquisizione e pubblicazione:** un’attività giornaliera sull’EAGLE di Manciano legge il CSV del CloudWatcher con lo [script di pubblicazione](https://github.com/maininimassimo-bit/digital-stargate-manual/blob/main/scripts/telemetry/Publish-AllSkyNightWeather.ps1). La finestra va dalle 19:00 alle 06:00 locali del giorno successivo. Gli intervalli di almeno 60 secondi tra misure consecutive sono esclusi dal calcolo della copertura e rendono il riepilogo parziale. L’attività pubblica i riepiloghi aggregati nel repository e GitHub Pages genera il [catalogo JSON](https://maininimassimo-bit.github.io/digital-stargate-manual/data/realtime/allsky-night-weather.json) che l’app scarica automaticamente.
- **Importazione storica del 26 novembre 2026:** lo [script di importazione](https://github.com/maininimassimo-bit/digital-stargate-manual/blob/main/scripts/telemetry/Import-AllSkyNightWeather.ps1) ha incrociato il CSV storico con le date dei tre cataloghi AllSky e aggiunto 226 riepiloghi, conservando i 34 già pubblicati. Il catalogo verificato dopo la pubblicazione conteneva 260 notti (150 complete e 110 parziali), dal 29–30 aprile 2025 al 25–26 novembre 2026. [Commit dell’importazione](https://github.com/maininimassimo-bit/digital-stargate-manual/commit/e497d197deba71ea30e51fa9994e8a54a1c25710).
- **Verifica sul Motorola G84 (Android 15):** testata la build 14 in Timelapse, Startrail e Keogrammi. In tutte e tre le sezioni, passando dalla notte del 24–25 novembre a quella del 23–24 novembre, il riepilogo è passato da 25% sereno e 49% coperto a 100% sereno e 0% coperto. In Startrail e Keogrammi è cambiata anche l’immagine associata alla data.

## Beta 0.2.11 (build 13)

- **Sfondo:** paesaggio illustrativo ispirato alla Maremma, con la Via Lattea sul bordo destro e la cupola all'orizzonte. La risorsa locale `drawable-nodpi/manciano_night.png` è condivisa dalle schermate principali. Compose la adatta al contenitore e applica un velo scuro per mantenere il contrasto dei testi. Il fotogramma Live resta separato.
- **Accessibilità:** include le modifiche della build 12. Le categorie e i comandi dell'Archivio vanno su più righe quando serve. Se le etichette della barra inferiore non hanno spazio sufficiente, le cinque destinazioni sono disponibili nel menu **Sezioni**. La dimensione dei caratteri segue Android. Il layout della build 12 è stato verificato sul Motorola g84 al 200%.

## Beta 0.2.9 (build 11)

- **Archivio:** le anteprime Startrail e Keogrammi hanno un'altezza di 200 dp e mantengono le proporzioni. Toccando l'anteprima si apre l'immagine completa, con il pulsante **Chiudi** per tornare all'Archivio.
- **Timelapse:** il pulsante **Schermo intero** apre il lettore in orizzontale. Il video mantiene le proporzioni. I comandi si nascondono durante la riproduzione e ricompaiono con un tocco. **Esci da schermo intero** torna al lettore nell'Archivio mantenendo la posizione del video. **Archivio** chiude il lettore e torna al catalogo.
- **Verifica su Motorola g84:** apertura e chiusura di entrambe le immagini, riproduzione a tutto schermo, comandi inferiori interamente visibili e ritorno al lettore con la posizione conservata.
- **Distribuzione:** bundle firmato inviato al test chiuso Alpha. All'ultima verifica su Play Console, la 0.2.9 era in revisione e la 0.2.8 era disponibile ai tester.

## Stato iniziale del progetto

**Aggiornamento storico:** 17 novembre 2026. **Stato:** beta APK debug v0.2.5 installata via USB sul Motorola G84. Nome “AllSky Manciano”, icona adattiva dettagliata e schermata Info. Il codice candidato 0.2.6 aggiunge in Info un link alla policy privacy bilingue, verificato sull’emulatore API 36; la pagina non è ancora pubblicata sul sito. L’interfaccia segue la lingua configurata in Android: italiano per `it`, inglese come fallback per le altre lingue. Build e 9 test JUnit passati. L’Owner ha confermato che i test finali sul telefono hanno esito positivo. Rotazione generale, rete dati/lenta e messaggio offline sono già stati verificati dall’Owner; il reload della mappa è stato verificato nella 0.2.2. È stato predisposto il candidato Play 0.2.6: AAB locale unsigned, scheda store it-IT/en-US, icona, feature graphic, screenshot e policy privacy candidata. Account Play Console creato dall’Owner ma con verifica identità/telefono ancora pendente; la Console disabilita “Crea app”. Vedi [rapporto tecnico](allsky-pocket-android-v1.md), [preparazione Google Play](allsky-manciano-google-play-release.md) e [informativa privacy](allsky-manciano-privacy.md).

Questo documento prepara una chat Work dedicata alla realizzazione della prima versione installabile sul telefono dell’Owner. La [PWA pubblica esistente](allsky-pocket-pwa.md) resta separata e disponibile: non è la nuova app nativa. Questo aggiornamento del manuale non modifica il Raspberry, l’acquisizione o l’hosting della PWA.

## Obiettivo della prima versione

Client Android in **Kotlin e Jetpack Compose**, con cinque schede di sola consultazione: Live, Meteo, Archivio, Meteore e Mappa. La prima consegna è stata un **APK di prova locale**; il progetto è poi passato al test chiuso su Google Play. Il candidato AAB e i materiali della scheda sono descritti nel [rapporto di preparazione Google Play](allsky-manciano-google-play-release.md).

| Scheda | Perimetro della prova |
|---|---|
| Live | Ultimo JPEG, ora dello scatto, aggiornamento automatico mentre visibile e manuale, zoom/schermo intero, stato connessione e immagine scaduta |
| Meteo | Temperatura ambiente, umidità, punto di rugiada e vento km/h CloudWatcher; ora della misura, scadenza e indisponibilità |
| Archivio | Timelapse, startrails e keogrammi pubblici, elenco dal più recente, selezione data/notte, anteprime compatte, immagini complete e timelapse con lettore a tutto schermo |
| Meteore | Consultazione delle immagini e miniature candidate già pubbliche; sempre etichettate da verificare, mai come conferme |
| Mappa | Pagina Allsky originale con overlay VirtualSky, calibrazione e clock sincronizzato sul fotogramma corrente |

Il live è una successione di fotografie, non un flusso video continuo. Le date archivio rappresentano l’inizio della notte. Nessun controllo dell’osservatorio, login amministrativo, push, analisi scientifica o archivio offline completo. La mappa è visualizzata dal sito Allsky esistente dentro WebView; la calibrazione resta gestita dalla pagina originale.

## Confini di dati e integrazione

Le sorgenti pubbliche sono state verificate il 16 novembre 2026: i cinque endpoint ammessi hanno risposto correttamente; ciascun catalogo conteneva 605 link validi e i tre media recenti erano scaricabili. Dettagli e campioni sono nel rapporto tecnico.

Baseline da verificare nella chat di sviluppo: [contratto della PWA](allsky-pocket-pwa.md#architettura-e-percorsi-ammessi), codice PWA se disponibile e comportamento delle sorgenti pubbliche. Origine Allsky: `https://digitalstargate.freeddns.it:23232`.

| Sorgente pubblica già documentata | Utilizzo ammesso |
|---|---|
| `/current/image.jpg` | Immagine corrente |
| `/allsky/dsg-live-data.json` | Selezione dei soli campi camera, weather e astronomy necessari; non riversare il JSON completo nell’app |
| `/allsky/videos/`, `/allsky/startrails/`, `/allsky/keograms/` | Cataloghi e relativi file/miniature, con nomi e percorsi validati |
| `/allsky/meteors/` | Catalogo HTML e JPEG pubblici con timestamp validati; esclusi JSON, metadati e contatori riservati |
| `/allsky/` | Pagina live per mappa e overlay calibrato, caricata in WebView con limite host/porta HTTPS |

L’accessibilità reale e la stabilità del formato vanno provate prima di fissare l’architettura. Il client nativo può leggere le sorgenti HTTPS pubbliche direttamente; un eventuale servizio intermedio va motivato e proposto separatamente, senza introdurre implicitamente canoni o modificare l’impianto. Non assumere che l’hosting PWA sia utilizzabile come API stabile senza verificarlo. I percorsi sono una allowlist, non un invito a esplorare altre risorse.

Sono esclusi candidati meteore privati, metadati individuali, contatori e registro del rilevatore temporale. La galleria inclusa nell’app è soltanto quella pubblica; non leggere `/var/lib/dsg-meteor-shadow`, non accedere alla WebUI e non usare SSH per collegare l’app. Non copiare backup privati o chiavi nel progetto, nell’APK o nei log.

TLS ordinario, origine fissata, nessuna disabilitazione dei certificati e nessun URL arbitrario. Ridurre le letture al necessario, sospendere il polling quando l’app non è visibile, introdurre timeout e attesa crescente dopo gli errori. La baseline PWA aggiorna ogni 30 s, accetta proiezione entro 150 s e scatto entro 180 s, con controlli sugli orari futuri e scadenza meteo: riusare queste regole dove applicabili e documentare eventuali differenze. Dati mancanti/scaduti non devono diventare zero o condizioni meteo attuali. Un’immagine conservata è etichettata come ultimo fotogramma.

## Piano e stima iniziale

| Traguardo | Stima di lavoro cumulativa | Condizione |
|---|---:|---|
| APK essenziale da provare | 30–50 ore | Tre schede, sorgenti esistenti utilizzabili, strumenti disponibili |
| Beta rifinita | 80–120 ore | Prove aggiuntive su dispositivi e correzioni |
| Preparazione e pubblicazione Play | 120–180 ore | Fase successiva, soggetta a test, account e revisione Google |

Sono stime di pianificazione, non tempi misurati o garanzie. La prima versione può richiedere indicativamente 1–2 settimane di lavoro regolare; non è una scadenza promessa. Le stime successive includono le precedenti. Per l’Owner prevedere indicativamente 4–8 ore distribuite di prove e decisioni nell’intero progetto, oltre alla disponibilità degli eventuali tester.

Android Studio e librerie gratuite sono la scelta iniziale. Nessun nuovo hosting o API AI è previsto se si riusano le sorgenti esistenti. Utilizzo Codex ed eventuali crediti dipendono dal piano dell’Owner e non sono quantificati qui. Google indica una registrazione Play Console di **25 USD una tantum**; l’Owner ha dichiarato di non avere ancora un account e nessun acquisto è stato effettuato. Per i nuovi account personali creati dopo il 13 novembre 2023, Google richiede un test chiuso con almeno **12 tester iscritti continuativamente per 14 giorni**, oltre alla verifica del dispositivo Android reale, prima di richiedere l’accesso alla produzione. [Account e registrazione](https://support.google.com/googleplay/android-developer/answer/6112435?hl=en), [test personali](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en), [verifica dispositivo](https://support.google.com/googleplay/android-developer/answer/14316361?hl=en).

Fonti: [account Google Play](https://support.google.com/googleplay/android-developer/answer/6112435?hl=en), [test per account personali](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en), [utilizzo Codex](https://chatgpt.com/codex/pricing/).

## Criteri di consegna e verifica

1. Build ripetibile con versioni documentate e APK di prova installabile, identificativo/versione e checksum SHA-256. Chiavi di firma e dati locali fuori da Git; chiarire che la firma di debug è per la prova e non è una release Play. Per il candidato Play, vedi la checklist del bundle e della upload key nel rapporto dedicato.
2. Cinque schede funzionanti con dati reali, gestione di rete assente/lenta, JSON parziale, misure scadute, errori JPEG/video e archivio vuoto. Fotogrammi e misure con orari distinti; nessuna condizione meteo inventata.
3. Test mirati dei parser, della selezione dei campi e delle regole di freschezza, più prova di navigazione, rotazione e passaggio Wi-Fi/rete mobile. Verificare che richieste, modello dati e log escludano meteore e percorsi privati.
4. Installazione e avvio, riproduzione timelapse e apertura immagini startrail/keogramma verificati su telefono reale; Live e Meteo sono stati verificati su emulatore. Il riscontro dell’Owner sul Motorola è registrato nel rapporto tecnico. Restano rotazione, cambio Wi-Fi/mobile, background e condizioni di errore/rete.
5. Documentare esiti reali, limiti e problemi aperti nel repository, mantenendo invariata la configurazione Allsky. La rimozione dell’app dal telefono è il rollback del client; non ripristinare il Raspberry.

Il toolchain portabile usato per la build resta sotto `android/.local-toolchain/` e non è incluso in Git. Per installare l’APK, trasferirlo sul telefono, consentire temporaneamente l’installazione da quella sorgente e aprire il file; i passaggi dettagliati e il checksum sono nel rapporto tecnico. La firma debug è destinata alla prova.

## Prompt iniziale per la chat Work (archiviato)

Avvia lo sviluppo della prima versione Android nativa di **Allsky Pocket – Digital Stargate**, da installare e provare sul mio telefono. Usa Kotlin e Jetpack Compose, con schede Live, Meteo e Archivio. Leggi prima questa guida, la guida PWA, il Capitolo 27 e le istruzioni del repository `maininimassimo-bit/digital-stargate-manual`. Usa un branch/worktree isolato, preserva il lavoro esistente e verifica gli strumenti Android disponibili.

Realizza un client di sola consultazione delle sorgenti pubbliche già documentate: JPEG live, selezione dei dati camera/meteo necessari e archivio timelapse/startrails/keogrammi. Verifica i contratti reali prima di implementarli. Mantieni invariata la configurazione Allsky, acquisizione, maschere, calibrazione, router, rilevatori e PWA pubblicata. Nessun accesso amministrativo o SSH dall’app. Nessuna lettura, copia o pubblicazione di candidati temporali privati, metadati, contatori o registri; nessuna galleria meteore nel prototipo.

Live deve avere ora dello scatto, aggiornamento manuale e periodico solo quando visibile, zoom e stato connessione/freschezza. Meteo deve mostrare temperatura ambiente, umidità, rugiada e vento km/h con ora della misura e scadenza. Archivio deve consentire di scegliere notte e prodotto, aprire immagini e riprodurre i filmati pubblici. Non inventare dati e non presentare un dato scaduto come attuale. Usa HTTPS con verifica certificati, timeout, carico limitato e percorsi ammessi; niente URL arbitrari o segreti nei sorgenti/log.

Procedi autonomamente con verifica delle sorgenti, progetto, implementazione, test mirati e build. Consegna sorgenti, APK di prova con checksum, istruzioni semplici di installazione e checklist per il mio telefono. Chiedi modello/versione Android solo se non ricavabili e utili alle prove, continuando il lavoro indipendente. Distingui test automatici/emulatore da collaudo fisico Owner e non dichiarare risultati non osservati.

Nota storica del perimetro iniziale: APK essenziale, stima 30–50 ore. L’Owner ha poi richiesto la preparazione alla pubblicazione Play: questa comprende bundle e scheda store, ma non autorizza l’acquisto dell’account da 25 USD o la pubblicazione pubblica. Nessun servizio aggiuntivo è stato acquistato. Documenta decisioni, versioni, prove e limiti nel repository e completa il normale percorso di PR/controlli/pubblicazione documentale previsto dalle istruzioni applicabili. Se emerge un blocco, spiega il fatto concreto senza modificare l’impianto per aggirarlo.
