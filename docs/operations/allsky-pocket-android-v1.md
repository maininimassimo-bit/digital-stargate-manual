---
title: Allsky Pocket · Android nativo v0.2
description: Sorgenti, integrazione, verifiche e limiti della beta Android nativa v0.2.
---

# Allsky Pocket: Android nativo v0.2

**Stato al 16 novembre 2026:** beta 0.2.5 installata via USB sul Motorola G84, Android 15/API 35. Nome “AllSky Manciano”, icona adattiva dettagliata e schermata Info; l’Info mostra Massimo Mainini, breve descrizione dell’attività astrofilo con cupola a Manciano, versione/build e lingua corrente. L’interfaccia segue la lingua configurata in Android: italiano per `it`, inglese come fallback per le altre lingue. Il telefono è attualmente bloccato, quindi la finestra Info non è stata controllata visivamente; pacchetto, nome, versione e build sono stati verificati. APK `release/allsky-pocket-v0.2.5-debug.apk`, package `it.digitalstargate.allskypocket`, versionCode 7/versionName 0.2.5, min SDK 26, target SDK 36, SHA-256 `e64fa3373bc92a08a0459b06a6857fdd16103fdf474ecef012bedf0722d4c061`, dimensione 14,946,527 byte. `testDebugUnitTest assembleDebug` PASS, 9 test. Il fix della mappa è stato verificato sulla versione 0.2.2: costellazioni, griglia e radianti visibili sopra il fotogramma dopo reload. La galleria meteore e l’immagine candidata completa erano già state verificate sul dispositivo; l’Owner ha confermato rotazione generale, rete dati, rete lenta e stato offline (“Connessione non disponibile”). Fix mappa registrato nella PR #641. Toolchain portabile locale in `android/.local-toolchain/`, esclusa da Git.
**Stato al 16 novembre 2026:** beta 0.2.5 installata via USB sul Motorola G84, Android 15/API 35. Nome “AllSky Manciano”, icona adattiva dettagliata e schermata Info; l’Info mostra Massimo Mainini, breve descrizione dell’attività astrofilo con cupola a Manciano, versione/build e lingua corrente. L’interfaccia segue la lingua configurata in Android: italiano per `it`, inglese come fallback per le altre lingue. L’Owner ha verificato positivamente i test finali sul telefono. APK `release/allsky-pocket-v0.2.5-debug.apk`, package `it.digitalstargate.allskypocket`, versionCode 7/versionName 0.2.5, min SDK 26, target SDK 36, SHA-256 `e64fa3373bc92a08a0459b06a6857fdd16103fdf474ecef012bedf0722d4c061`, dimensione 14,946,527 byte. `testDebugUnitTest assembleDebug` PASS, 9 test. Il fix della mappa è stato verificato sulla versione 0.2.2: costellazioni, griglia e radianti visibili sopra il fotogramma dopo reload. La galleria meteore e l’immagine candidata completa erano già state verificate sul dispositivo; l’Owner ha confermato rotazione generale, rete dati, rete lenta e stato offline (“Connessione non disponibile”). Fix mappa registrato nella PR #641. Toolchain portabile locale in `android/.local-toolchain/`, esclusa da Git. La preparazione della release Play 0.2.6 è documentata in [preparazione Google Play](allsky-manciano-google-play-release.md); il bundle generato è unsigned e non caricabile.

## Baseline e fonti

- Manuale upstream: commit `d9a7bdd99bdf7322eea7ac1c12fadb7d3125f670` (PR #637).
- PWA: [contratto e confini](allsky-pocket-pwa.md), sorgente separato Sites non presente localmente nella cartella attesa. Non è stato modificato.
- Capitolo 27: [Allsky](../chapters/27-sistema-allsky.md), in particolare acquisizione fotografica, proiezione telemetrica e pubblicazione.
- Worktree sviluppo: branch `feat/allsky-pocket-android-v1`, directory `C:\Users\MassimoMainini\Documents\Codex\2026-11-16\allsky-pocket-android`.
- Dispositivo Owner: Motorola G84, Android 15/API 35 (`getprop` via ADB il 16/11/2026); APK v0.1.0 installata e avviata sul dispositivo.

## Contratto pubblico osservato

Data verifica: 16/11/2026, da PowerShell con TLS ordinario e timeout HTTP. Origine fissata `https://digitalstargate.freeddns.it:23232`.

| Risorsa ammessa | Esito osservato |
|---|---|
| `/current/image.jpg` | HTTP 200, `image/jpeg`, 294124 byte nel campione |
| `/allsky/dsg-live-data.json` | HTTP 200, `application/json`, 799 byte nel campione |
| `/allsky/videos/` | HTTP 200, HTML Allsky; 605 link MP4 con prefisso `allsky-YYYYMMDD`, ordinamento HTML crescente |
| `/allsky/startrails/` | HTTP 200, HTML Allsky; 605 link JPEG `startrails-YYYYMMDD` |
| `/allsky/keograms/` | HTTP 200, HTML Allsky; 605 link JPEG `keogram-YYYYMMDD` |
| `/allsky/meteors/` | HTTP 200, HTML pubblico “Meteore candidate - da verificare”; 324 immagini JPEG e miniature nel campione del 16/11 |
| mappa `/allsky/` | HTTP 200, pagina live con VirtualSky, controller, calibrazione corrente e pulsante overlay |
| media recenti `20261115` | MP4 200 `video/mp4` 17417533 byte; JPEG startrail 200 627295 byte; JPEG keogram 200 803903 byte |
| hosting PWA | HTTP 200 HTML. Il manuale documenta un relay server `/api/`; l’hosting non viene assunto come API nativa |

La proiezione campionata comprende `generated_at`, camera, meteo, Raspberry, stelle, conteggi meteore, ISS, aeromobili e astronomia. La versione nativa legge soltanto `generated_at`, `camera.AS_CAMERAIMAGE` e i quattro valori/tempi meteo; conteggi e nodi esclusi sono ignorati e non persistiti. Le meteore sono consultate solo tramite la galleria pubblica di immagini candidate; l’app non legge JSON individuali, contatori o archivi/metadati privati. Il nome `image-YYYYMMDDhhmmss.jpg` viene validato come basename e convertito dall’ora parete Europe/Rome, con regole DST, come fa la PWA. Il JPEG viene ricaricato quando cambia quel nome o su aggiornamento manuale. Il badge richiede proiezione entro 150 s e scatto entro 180 s; non certifica che il corpo JPEG corrisponda all’etichetta se l’upstream è incoerente.

I cataloghi sono pagine HTML con singoli link in attributo `href` tra apici singoli, non JSON/API. Il client ammette soltanto tre directory, nome file a prefisso esatto, data di otto cifre `20YYYYMMDD` e suffisso MP4/JPEG atteso. Non richiede né visualizza miniature, che il contratto esclude. Le date sono l’inizio della notte.

## Implementazione

- Kotlin 2.2.20, Jetpack Compose Material 3, AGP 8.13.1, Gradle wrapper 8.13, minSdk 26, target/compile SDK 36, JDK Temurin 17.0.21. Toolchain locale scaricato; JDK e command-line tools verificati con checksum ufficiale, SDK/build-tools installati. Otto licenze Android SDK accettate dall’Owner in chat. Installata sul Motorola G84/Android 15/API35.
- Solo permesso Internet; TLS di default Android, cleartext disabilitato, redirect HTTP disabilitati, timeout, limite risposta 2 MB e origine/endpoint codificati. Nessun login, cookie, amministrazione o SSH.
- Live/Meteo: proiezione ogni 30 s soltanto con la relativa scheda selezionata e l’attività RESUMED/STARTED; retry esponenziale dopo errore fino a 5 minuti. Live ha pulsante manuale, immagine JPEG con caricamento/errore esplicito, zoom pinch e modalità espansa. Ora scatto derivata dal nome camera Europe/Rome, ora proiezione separata; badge freschezza 150/180 s.
- Meteo: campi numerici finiti selezionati, proiezione al massimo 150 s, timestamp non futuro oltre 30 s, `fresh_until_utc` successivo all’istante corrente. Valori assenti/invalidi restano trattino; i valori fuori intervalli plausibili sono omessi. Un campo mancante rende la misura complessiva non aggiornata.
- Archivio: parser HTML delimitato, directory/categorie allowlist, media costruiti dall’origine fissa e validazione esatta della data/file prima del fetch. Selettore notte successiva/precedente sull’intero archivio (circa 605 link per categoria); la UI richiede un solo media per volta e cancella i fetch quando si cambia categoria/schermata. Immagini JPEG complete tramite loader bounded (8/12 s, massimo 12 MB, content-type verificato, decode ridotto) e visualizzazione espansa su fondo opaco; chiusura esplicita. Video on-demand tramite Media3 con timeout e controlli nativi; per i filmati H.264 il decoder software viene preferito al decoder hardware Qualcomm che sul G84 ha rifiutato il profilo/dimensione osservati, con fallback MediaCodec attivo.
- Meteore candidate: scheda dedicata che legge esclusivamente `/allsky/meteors/`, filtra i link con nome e timestamp esatti, mostra le miniature pubbliche dalla più recente e apre l’immagine JPEG completa. Limite 1 MB per miniatura e 12 MB per originale. L’interfaccia le chiama sempre “candidate da verificare”; non mostra un punteggio come probabilità o come conferma. JSON, contatori e archivi privati esclusi.
- Mappa celeste: scheda che carica la pagina live HTTPS Allsky nello WebView Android e attiva l’overlay esistente. VirtualSky usa la configurazione corrente del server (proiezione/calibrazione, etichette e radianti) e lo stesso clock/fotogramma del controller originale. WebView limitato a HTTPS e host/porta Allsky, risorse file/content e mixed content disabilitati, terze parti rifiutate, nessun bridge JavaScript nativo. La pagina Allsky resta autorevole per overlay e calibrazione; non è stata duplicata né modificata.
- Grafica: palette blu notte, aurora turchese e accento stellare, campo stellato Compose e icone adaptive/monochrome disegnate localmente, senza immagini o font remoti.
- Nessuna lettura di candidati, miniature o JSON privati, API meteo esterna, campi telemetrici esclusi, cache applicativa o log payload.

Toolchain riportata come effettivamente usata nel primo build. Il wrapper è incluso nel repository; il toolchain scaricato, cache e SDK restano locali e ignorati da Git.

## Stato prove e limiti

**Eseguito:** fetch HTTPS della galleria meteore con 324 link e miniature, pagina live Allsky 200 con VirtualSky/configurazione corrente, risposta 200 per l’immagine candidata più recente e relativa miniatura. `testDebugUnitTest assembleDebug` PASS, 9 test, zero failure. APK `release/allsky-pocket-v0.2.2-debug.apk`, package `it.digitalstargate.allskypocket`, versionCode 4/versionName 0.2.2, min SDK 26, target SDK 36, SHA-256 `67a329b9d24d00fa2fb84e46650793424e10092bb7d5d2df4fc308ec05fd03c7`, dimensione 14,558,718 byte. **Motorola G84 reale, Android 15/API35:** con beta 0.2.1 il fotogramma caricava ma il riquadro sottostante restava bianco. La beta 0.2.2 attende Angular e attiva l’overlay tramite il pulsante originale Allsky; il reload carica un nuovo URL documento e fornisce stato di caricamento visibile. Sul G84 costellazioni, griglia e radianti compaiono sulla ripresa; dopo aver premuto “Ricarica mappa e fotogramma” il fotogramma si aggiorna e l’overlay torna visibile. La galleria meteore e immagine candidata completa erano già state verificate sul dispositivo.

La cartella sorgente Sites individuata in `C:\Users\MassimoMainini\Documents\Codex\2026-10-09\ti\work\sites\allsky-pocket` è un progetto Next/Vinext con API server e hosting autonomo. La scheda pubblica PWA documenta che il relay seleziona weather/camera/astronomy e inoltra i media via GET/range; non si introduce dipendenza dell’app dal dominio Sites.

**Ancora non eseguito:** risposta al cambio di orientamento della specifica vista Mappa WebView, ritorno dal background e catalogo meteore vuoto/errore. Rotazione generale, rete dati, rete lenta e messaggio offline sono stati confermati dall’Owner per l’app.

I test JUnit coprono freshness meteo/proiezione/fotogramma ai limiti, timestamp camera Europe/Rome, JSON parziale/futuro, zero misurato, campi estranei, allowlist archivio, file/date invalidi e catalogo vuoto. Prima compilazione ha trovato errori Kotlin e `org.json` del framework Android non mockato nei test JVM; corretti e ritestati.

La galleria pubblica contiene soltanto immagini JPEG e miniature; questa integrazione non interpreta i metadati riservati del rilevatore, né afferma l’identità astronomica di una traccia. L’overlay è renderizzato dalla pagina Allsky, quindi la sua disponibilità dipende dal sito HTTPS e da WebView Android; non è una cache offline. Non estendere i test video del G84 ad altri dispositivi/codec.

## Build e installazione

Per ricreare il build nel worktree, impostare `JAVA_HOME` a `android/.local-toolchain/jdk/jdk-17.0.21+9` e `ANDROID_HOME`/`ANDROID_SDK_ROOT` a `android/.local-toolchain/sdk`, poi eseguire:

```powershell
cd android
.\gradlew.bat testDebugUnitTest assembleDebug
Get-FileHash app/build/outputs/apk/debug/app-debug.apk -Algorithm SHA256
```

La firma `debug` è locale e solo per test; non è una release Play. Non salvare chiavi, credenziali o dati privati nel repository, APK o output di log. La toolchain portabile è esclusa da Git; la firma debug è generata localmente.

## APK e installazione Owner

Distribuire `release/allsky-pocket-v0.2.2-debug.apk` al telefono tramite USB o trasferimento file privato. Verificare il checksum con `Get-FileHash allsky-pocket-v0.2.2-debug.apk -Algorithm SHA256` e confrontarlo con il sidecar `release/allsky-pocket-v0.2.2-debug.apk.sha256`. Aprire il file, autorizzare temporaneamente l’app sorgente richiesta da Android e completare l’installazione. La firma è di debug e non va usata per Google Play.

## Checklist Owner

Sul simulatore sono già state viste le tre schede, meteo, live, cataloghi timelapse/startrail/keogrammi, immagini e selezione di notti diverse. Il collaudo Owner ha inoltre confermato l’avvio sul G84, la riproduzione del timelapse e l’apertura ingrandita di startrail e keogramma.

- [x] Modello/API osservati: Motorola G84, Android 15/API35; build ID non raccolto.
- [x] APK debug installato, schermata app avviata sul Motorola G84/Android 15/API35.
- [ ] Live: aggiornamento manuale/automatico, immagine non aggiornata, zoom e ritorno all’app dopo background.
- [ ] Meteo: misura valida, campi assenti e misure scadute/non disponibili; zero vento resta zero solo quando misurato.
- [x] Archivio sul telefono: timelapse riprodotto; startrail e keogramma aperti correttamente a schermo ingrandito.
- [ ] Archivio: catalogo vuoto/errore.
- [x] Passaggio orientamento, rete dati, rete lenta e modalità offline: Owner riferisce esito positivo; offline appare “Connessione non disponibile”.
- [x] Beta 0.2 sul G84: caricare galleria Meteore e immagine originale; aprire Mappa con overlay visibile sul fotogramma live.
- [x] Beta 0.2.2 sul G84: overlay celeste visibile e stabile dopo “Ricarica mappa e fotogramma”.
- [ ] Rotazione specifica con WebView Mappa visibile; confermare che immagine/overlay restino allineati.
- [ ] Ritorno dal background, catalogo meteore vuoto/errore e ripresa dopo timeout.

## Vincoli invariati

Nessun cambiamento a Raspberry/Allsky, acquisizione, maschere, calibrazione, router, rilevatori, PWA pubblicata o backup. Le nuove schede leggono solo la galleria meteore pubblica e la pagina Allsky HTTPS esistente. Nessun nuovo servizio/costo o pubblicazione Play. L’app è una consultazione pubblica e non costituisce funzione di sicurezza.
