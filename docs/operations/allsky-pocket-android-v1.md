---
title: Allsky Pocket · Android nativo v0.1
description: Sorgenti, integrazione, verifiche e limiti del prototipo Android nativo.
---

# Allsky Pocket: Android nativo v0.1

**Stato al 16 novembre 2026:** branch di sviluppo isolato; build, 7 test JUnit e verifica interattiva su emulatore Android 16/API 36 superati. APK debug verificato e pronto per Motorola G84/Android 15; installazione e collaudo Owner ancora da eseguire. Toolchain portabile locale in `android/.local-toolchain/`, esclusa da Git.

## Baseline e fonti

- Manuale upstream: commit `d9a7bdd99bdf7322eea7ac1c12fadb7d3125f670` (PR #637).
- PWA: [contratto e confini](allsky-pocket-pwa.md), sorgente separato Sites non presente localmente nella cartella attesa. Non è stato modificato.
- Capitolo 27: [Allsky](../chapters/27-sistema-allsky.md), in particolare acquisizione fotografica, proiezione telemetrica e pubblicazione.
- Worktree sviluppo: branch `feat/allsky-pocket-android-v1`, directory `C:\Users\MassimoMainini\Documents\Codex\2026-11-16\allsky-pocket-android`.
- Dispositivo Owner dichiarato: Motorola G84, Android 15 (risposta in chat del 16/11/2026); compatibilità installata ancora da provare.

## Contratto pubblico osservato

Data verifica: 16/11/2026, da PowerShell con TLS ordinario e timeout HTTP. Origine fissata `https://digitalstargate.freeddns.it:23232`.

| Risorsa ammessa | Esito osservato |
|---|---|
| `/current/image.jpg` | HTTP 200, `image/jpeg`, 294124 byte nel campione |
| `/allsky/dsg-live-data.json` | HTTP 200, `application/json`, 799 byte nel campione |
| `/allsky/videos/` | HTTP 200, HTML Allsky; 605 link MP4 con prefisso `allsky-YYYYMMDD`, ordinamento HTML crescente |
| `/allsky/startrails/` | HTTP 200, HTML Allsky; 605 link JPEG `startrails-YYYYMMDD` |
| `/allsky/keograms/` | HTTP 200, HTML Allsky; 605 link JPEG `keogram-YYYYMMDD` |
| media recenti `20261115` | MP4 200 `video/mp4` 17417533 byte; JPEG startrail 200 627295 byte; JPEG keogram 200 803903 byte |
| hosting PWA | HTTP 200 HTML. Il manuale documenta un relay server `/api/`; l’hosting non viene assunto come API nativa |

La proiezione campionata comprende `generated_at`, camera, meteo, Raspberry, stelle, meteore, ISS, aeromobili e astronomia. La versione nativa legge soltanto `generated_at`, `camera.AS_CAMERAIMAGE` e i quattro valori/tempi meteo; gli altri nodi sono ignorati e non persistiti. Il nome `image-YYYYMMDDhhmmss.jpg` viene validato come basename e convertito dall’ora parete Europe/Rome, con regole DST, come fa la PWA. Il JPEG viene ricaricato quando cambia quel nome o su aggiornamento manuale. Il badge richiede proiezione entro 150 s e scatto entro 180 s; non certifica che il corpo JPEG corrisponda all’etichetta se l’upstream è incoerente.

I cataloghi sono pagine HTML con singoli link in attributo `href` tra apici singoli, non JSON/API. Il client ammette soltanto tre directory, nome file a prefisso esatto, data di otto cifre `20YYYYMMDD` e suffisso MP4/JPEG atteso. Non richiede né visualizza miniature, che il contratto esclude. Le date sono l’inizio della notte.

## Implementazione

- Kotlin 2.2.20, Jetpack Compose Material 3, AGP 8.13.1, Gradle wrapper 8.13, minSdk 26, target/compile SDK 36, JDK Temurin 17.0.21. Toolchain locale scaricato; JDK e command-line tools verificati con checksum ufficiale, SDK/build-tools installati. Otto licenze Android SDK accettate dall’Owner in chat. Motorola G84/Android 15 supera il minSdk dichiarato; installazione reale ancora da fare.
- Solo permesso Internet; TLS di default Android, cleartext disabilitato, redirect HTTP disabilitati, timeout, limite risposta 2 MB e origine/endpoint codificati. Nessun login, cookie, amministrazione o SSH.
- Live/Meteo: proiezione ogni 30 s soltanto con la relativa scheda selezionata e l’attività RESUMED/STARTED; retry esponenziale dopo errore fino a 5 minuti. Live ha pulsante manuale, immagine JPEG con caricamento/errore esplicito, zoom pinch e modalità espansa. Ora scatto derivata dal nome camera Europe/Rome, ora proiezione separata; badge freschezza 150/180 s.
- Meteo: campi numerici finiti selezionati, proiezione al massimo 150 s, timestamp non futuro oltre 30 s, `fresh_until_utc` successivo all’istante corrente. Valori assenti/invalidi restano trattino; i valori fuori intervalli plausibili sono omessi. Un campo mancante rende la misura complessiva non aggiornata.
- Archivio: parser HTML delimitato, directory/categorie allowlist, media costruiti dall’origine fissa e validazione esatta della data/file prima del fetch. Selettore notte successiva/precedente sull’intero archivio (circa 605 link per categoria); la UI richiede un solo media per volta e cancella i fetch quando si cambia categoria/schermata. Immagini JPEG complete tramite loader bounded (8/12 s, massimo 12 MB, content-type verificato, decode ridotto) e visualizzazione espansa; video on-demand tramite Media3 con timeout e controlli nativi.
- Grafica: palette blu notte, aurora turchese e accento stellare, campo stellato Compose e icone adaptive/monochrome disegnate localmente, senza immagini o font remoti.
- Nessuna galleria meteore, API meteo esterna, campo telemetrico escluso, miniatura/JSON di archivio, cache applicativa o log payload.

Toolchain riportata come effettivamente usata nel primo build. Il wrapper è incluso nel repository; il toolchain scaricato, cache e SDK restano locali e ignorati da Git.

## Stato prove e limiti

**Eseguito:** fetch HTTPS reale dei cinque endpoint ammessi, ispezione JSON/HTML, conteggio cataloghi e HEAD dei tre media del 15/11; `testDebugUnitTest assembleDebug` PASS, 7 test, zero failure. APK `release/allsky-pocket-v0.1.0-debug.apk`, package `it.digitalstargate.allskypocket`, versionCode 1/versionName 0.1.0, min SDK 26, target SDK 36, firma APK v2 verificata, SHA-256 `9a7d00b96e7bb67ad88065a658cfce55185a7d51491c9613efcf7f185b703976`; dimensione 14,302,914 byte. Emulatore Android 16/API36: avvio, fotogramma Live, meteo aggiornato, tre cataloghi e immagini JPEG con navigazione date visivamente verificati. Il player video compare con controlli ma non ha mostrato immagine durante la sessione; logcat non registra errore ExoPlayer/codec, quindi il playback non è attestato. Dopo la verifica è stata corretta la gestione di rilascio del player; il nuovo APK ricompilato mantiene lo stesso hash. Il PC non aveva un telefono ADB collegato; Motorola G84 reale non installato né provato.

La cartella sorgente Sites individuata in `C:\Users\MassimoMainini\Documents\Codex\2026-10-09\ti\work\sites\allsky-pocket` è un progetto Next/Vinext con API server e hosting autonomo. La scheda pubblica PWA documenta che il relay seleziona weather/camera/astronomy e inoltra i media via GET/range; non si introduce dipendenza dell’app dal dominio Sites.

**Ancora non eseguito:** playback video riuscito, rotazione, passaggio Wi-Fi/mobile, rete assente/lenta e collaudo su telefono fisico; PR/review. API effettiva/build del Motorola da confermare durante l’installazione.

I test JUnit coprono freshness meteo/proiezione/fotogramma ai limiti, timestamp camera Europe/Rome, JSON parziale/futuro, zero misurato, campi estranei, allowlist archivio, file/date invalidi e catalogo vuoto. Prima compilazione ha trovato errori Kotlin e `org.json` del framework Android non mockato nei test JVM; corretti e ritestati.

Rete assente/lenta, HTTP error, risposta JSON oltre budget e errore del player non sono ancora stati provati come scenari d’integrazione; gli stati di codice non equivalgono a una prova osservata. Registrare i risultati emulator/device senza estenderli al collaudo fisico.

## Build e installazione

Per ricreare il build nel worktree, impostare `JAVA_HOME` a `android/.local-toolchain/jdk/jdk-17.0.21+9` e `ANDROID_HOME`/`ANDROID_SDK_ROOT` a `android/.local-toolchain/sdk`, poi eseguire:

```powershell
cd android
.\gradlew.bat testDebugUnitTest assembleDebug
Get-FileHash app/build/outputs/apk/debug/app-debug.apk -Algorithm SHA256
```

La firma `debug` è locale e solo per test; non è una release Play. Non salvare chiavi, credenziali o dati privati nel repository, APK o output di log. La toolchain portabile è esclusa da Git; la firma debug è generata localmente.

## APK e installazione Owner

Distribuire `release/allsky-pocket-v0.1.0-debug.apk` al telefono tramite USB o trasferimento file privato. Verificare il checksum con `Get-FileHash allsky-pocket-v0.1.0-debug.apk -Algorithm SHA256`, che deve risultare `9a7d00b96e7bb67ad88065a658cfce55185a7d51491c9613efcf7f185b703976`. Aprire il file, autorizzare temporaneamente l’app sorgente richiesta da Android e completare l’installazione. La firma è di debug e non va usata per Google Play.

## Checklist Owner

Sul simulatore sono già state viste le tre schede, meteo, live, cataloghi timelapse/startrail/keogrammi, immagini e selezione di notti diverse. Queste verifiche non sostituiscono il collaudo Owner.

- [x] Modello dichiarato: Motorola G84; Android 15. API level e build specifica da leggere sul telefono.
- [ ] APK debug installato, schermata app e navigazione tra le tre schede.
- [ ] Live: aggiornamento manuale/automatico, immagine non aggiornata, zoom e ritorno all’app dopo background.
- [ ] Meteo: misura valida, campi assenti e misure scadute/non disponibili; zero vento resta zero solo quando misurato.
- [ ] Archivio: notte selezionata, apertura immagine completa, controlli video, catalogo vuoto/errore.
- [ ] Passaggio Wi-Fi/rete mobile, rete lenta/assente, rotazione e ripresa dopo timeout.

## Vincoli invariati

Nessun cambiamento a Raspberry/Allsky, acquisizione, maschere, calibrazione, router, rilevatori, PWA pubblicata o backup. Nessun nuovo servizio/costo o pubblicazione Play. L’app è una consultazione pubblica e non costituisce funzione di sicurezza.
