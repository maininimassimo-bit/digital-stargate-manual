---
title: AllSky Manciano · preparazione Google Play
description: Stato del bundle Android, scheda localizzata e preparazione alla pubblicazione su Google Play.
---

# AllSky Manciano — preparazione Google Play

**Aggiornato:** 17 novembre 2026. **Stato:** materiale di release candidato 0.2.6 predisposto; bundle Play firmato non ancora disponibile. L’account personale `maininimassimo@gmail.com` è attivo e la scheda Play Console è stata creata: ID `4974041146086048690`, package `it.digitalstargate.allskypocket`. Testi, icona, banner e quattro screenshot smartphone per ciascuna localizzazione (it-IT ed en-US) sono salvati; la scheda predefinita risulta pronta per la revisione, ma non è stata inviata. L’Owner ha dichiarato come creati o modificati con AI l’icona app e i due banner localizzati. Sono state salvate le dichiarazioni “nessuna parte soggetta a limitazioni”, “nessun annuncio”, “nessuna funzionalità finanziaria”, “nessuna funzionalità relativa alla salute”, l’assenza di app governativa, la categoria Fotografia, il pubblico 13–17 anni, la classificazione IARC e la dichiarazione Data Safety. Le modifiche restano in attesa nella panoramica della pubblicazione.

## Configurazione del candidato

| Campo | Valore |
|---|---|
| Nome pubblico | AllSky Manciano |
| Application ID | `it.digitalstargate.allskypocket` |
| Versione candidata | `0.2.6` (versionCode `8`) |
| minSdk / targetSdk / compileSdk | 26 / 36 / 36 |
| Tipo | Android App Bundle release |
| Firma | **non firmato**; non caricabile in Play Console |

`targetSdk 36` rispetta il requisito corrente per nuove app: dal 31 agosto 2026 Google Play richiede Android 16 / API 36 o superiore. [Fonte Google Play](https://support.google.com/googleplay/android-developer/answer/11926878?hl=en-EN).

Il bundle `release/allsky-manciano-v0.2.6-unsigned.aab` è stato creato con `bundleRelease` dopo l’aggiunta del collegamento privacy in-app. `jarsigner -verify` ha confermato che è unsigned; bundletool 1.18.3 lo valida. SHA-256: `d994c6de6c6e6c9fad0fbd2cd87ddf4391937d3c35504b6177820a13d845178d`. Il file `.sha256` è associato al bundle. Non caricare questo artefatto come release Play: va firmato con la upload key.

La configurazione Gradle supporta una signing config `playUpload` alimentata da proprietà locali `playUploadStoreFile`, `playUploadStorePassword`, `playUploadKeyAlias` e `playUploadKeyPassword`; non contiene credenziali o chiavi. Senza tutte e quattro le proprietà, il bundle rimane unsigned. Non riusare la firma debug dell’APK installato sul G84. Nel flusso di creazione della scheda l’Owner ha accettato i termini di Play App Signing; prima del caricamento verificare l’associazione della chiave di caricamento e del certificato. Google conserva la chiave di firma dell’app. [Concetti e configurazione Play App Signing](https://support.google.com/googleplay/android-developer/answer/9842756?hl=en).

## Build e verifiche eseguite

Comandi eseguiti con JDK 17, Gradle 8.13, Android Gradle Plugin 8.13.1 e SDK 36:

```powershell
cd android
.\gradlew.bat testDebugUnitTest assembleDebug
.\gradlew.bat testDebugUnitTest bundleRelease
```

`testDebugUnitTest assembleDebug bundleRelease` completano correttamente; i 9 test JUnit passano senza failure. L’AAB è stato validato con bundletool ufficiale 1.18.3; il manifest estratto conferma application ID, versione, minSdk 26 e targetSdk 36. Nell’ambiente corrente `bundleRelease` è riuscito il 17 novembre 2026 con Temurin 17.0.21 e Android SDK 36; `jarsigner -verify` conferma che `android/app/build/outputs/bundle/release/app-release.aab` è unsigned e ha SHA-256 `d994c6de6c6e6c9fadf0bd2cd87ddf4391937d3c35504b6177820a13d845178d`, uguale al candidato già in `release/`. `bundletool build-apks --connected-device` e `install-apks` hanno installato il candidato precedente sul simulatore API 36 firmandolo localmente con la chiave debug; il bundle aggiornato contiene il link privacy ma non è stato reinstallato sul G84 o sul simulatore. Nessuna di queste prove crea una firma Play.

Le schermate sono state acquisite dall’emulatore Android API 36; il Motorola G84 non è stato aggiornato con questo candidato. I set italiano e inglese mostrano contenuti pubblici reali dell’Allsky.

## Materiali della scheda

In `release/play-store/` sono pronti:

- `app-icon-512.png`: icona quadrata 512×512, PNG RGBA con canale alpha (immagine opaca).
- `it-IT/feature-graphic-1024x500.png` e `en-US/feature-graphic-1024x500.png`: banner localizzati 1024×500, PNG RGB.
- `LISTING-DRAFT.md`: titolo, descrizione breve e descrizione completa in italiano e inglese.
- `it-IT/` e `en-US/`: quattro screenshot reali dell’app per ciascuna lingua (1080×2160, PNG, senza alpha): Live, meteo, archivio/keogramma e meteore; ciascuna cartella contiene anche il banner locale. Le schermate tablet non sono incluse: l’emulatore in landscape non ha prodotto un set uniforme e stabile.
- `privacy-policy-draft.md`: riferimento alla pagina bilingue pubblicata e verificata.
- `listing-manifest.json`: riepilogo candidato e campi console mancanti.
- Procedura locale per predisporre la chiave di caricamento: [chiave di caricamento Play](allsky-manciano-upload-key.md).

La scheda è stata creata come **App** (non gioco) e la categoria **Fotografia** è ora salvata in Play Console. Il bundle in questa cartella è solo un candidato unsigned; il file ottenuto dal toolchain locale è stato aggiunto anche a `release/` con checksum per agevolare la successiva firma.

Google richiede l’icona Play in PNG 32-bit con canale alpha, 512×512 e massimo 1 MB; la feature graphic è 1024×500. Per pubblicare la scheda base occorrono almeno due screenshot; per l’idoneità alle superfici di raccomandazione ne occorrono almeno quattro a 1080 px (verticali 1080×1920 o superiori, oppure orizzontali 1920×1080 o superiori). Entrambe le localizzazioni hanno ora quattro screenshot smartphone 1080×2160 e un banner 1024×500 associato. [Requisiti asset Google Play](https://support.google.com/googleplay/android-developer/answer/9866151?hl=en).

## Dati, privacy e moduli Play

L’app ha il solo permesso `INTERNET`, non include login, pubblicità o SDK di analytics e interroga il server Allsky per immagini, meteo, cataloghi pubblici e mappa. Il titolare gestisce direttamente l’hosting e conserva i log di accesso per sei mesi per gestione tecnica e sicurezza, senza analytics o inferenza della posizione tramite IP. In Play Console è stata salvata come bozza la raccolta obbligatoria di “ID dispositivo o altri ID”, non condivisa, non trattata temporaneamente e cifrata in transito, con finalità di sicurezza e prevenzione frodi. La mappatura segue l’uso dell’IP nei log come identificatore tecnico per sicurezza; Google indica che il tipo dipende dall’uso effettivo dell’IP. La [policy privacy](https://maininimassimo-bit.github.io/digital-stargate-manual/operations/allsky-manciano-privacy/) è pubblicata, verificata con risposta HTTP 200 il 17 novembre 2026 e salvata nella scheda Play Console; l’app contiene già il collegamento in Info. Le modifiche non sono state inviate per la revisione. [Policy privacy Play](https://support.google.com/googleplay/android-developer/answer/18265346), [indicazioni Data Safety/IP](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en-en).

### Mappatura Data Safety salvata in bozza

La guida Play dice di classificare gli IP secondo l’uso effettivo: per esempio come posizione se usati per inferire la posizione o come identificatori se usati per identificare. Nel modulo è stato selezionato **ID dispositivo o altri ID**, raccolto obbligatoriamente, non condiviso e non trattato temporaneamente; la finalità selezionata è **Prevenzione di attività fraudolente, sicurezza e conformità**. La cifratura in transito è stata dichiarata sì in base alle richieste HTTPS. Conservazione dei log: sei mesi. L’anteprima conferma che Play mostrerà dati raccolti di tipo “ID dispositivo o altri ID”, nessun dato condiviso e trasferimento tramite connessione sicura. La WebView della mappa ammette solo risorse HTTPS dallo stesso host Allsky; richieste verso host terzi vengono bloccate. La dichiarazione è stata salvata, non inviata per la revisione.

Fonti: [tipi, finalità e criterio IP nella guida Data Safety](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en-en), [definizioni mostrate nella scheda Google Play](https://support.google.com/googleplay/answer/11416267?hl=en-001).

Prima di inviare un test o richiedere la pubblicazione, completare:

1. Rivedere la scheda `AllSky Manciano` (italiano, app gratuita, package `it.digitalstargate.allskypocket`): testi, icona condivisa, banner localizzati e quattro screenshot per lingua sono salvati. Categoria Fotografia, contatto pubblico e gli altri campi sono impostati. Restano da controllare i dettagli asset nella schermata di revisione e l’associazione Play App Signing.
2. La pagina privacy è pubblicata, verificata e salvata come bozza nella scheda Play Console. Il contatto pubblico è `maininimassimo@gmail.com` e il titolare confermato è Massimo Mainini.
3. Pubblico target 13–17 anni e classificazione IARC sono stati salvati; il riepilogo IARC indica PEGI 3 e rating generico 3 anni. La scheda target resta quella scelta dall’Owner.
4. Le dichiarazioni Data Safety, finanziaria, salute e app governative sono salvate come modifiche in bozza. Verificare la corrispondenza della Data Safety con il comportamento effettivo del server prima di inviare la revisione.
5. Generare la upload key seguendo [la procedura locale](allsky-manciano-upload-key.md), conservarla in modo sicuro e configurare le proprietà nel `android/gradle.properties` locale. Condividere con il progetto solo percorso e alias, mai la chiave o le password; quindi firmare e verificare il bundle.
6. Caricare il bundle firmato su una traccia di test e completare la verifica da parte di Play Console prima della produzione.

Le dichiarazioni “nessun annuncio”, accesso non limitato, categoria Fotografia e contatto email sono salvate come modifiche in bozza. Il pubblico 13–17, la classificazione contenuti, le dichiarazioni governativa/finanziaria/salute, il modulo Data Safety e la scheda dello Store risultano compilati e salvati; nella dashboard Play Console il flusso di configurazione è completato, mentre la scheda è pronta per essere inviata alla revisione. Nessun invio alla revisione è stato effettuato.

Google richiede inoltre la verifica del possesso del dispositivo Android da parte dei nuovi account personali e la registrazione dei nomi dei package secondo le regole entrate in vigore il 30 settembre 2026. Il Motorola G84 Android 15 soddisfa la soglia tecnica; completare la verifica nell’app Play Console quando richiesto. [Verifica dispositivo](https://support.google.com/googleplay/android-developer/answer/14316361?hl=en), [registrazione dei package](https://support.google.com/googleplay/android-developer/answer/16984799?hl=en).

Per gli account personali creati dopo il 13 novembre 2023 Google richiede un test chiuso con almeno 12 tester iscritti continuativamente per 14 giorni prima di consentire la richiesta di accesso alla produzione. Verificare il requisito nella dashboard dell’account e organizzare il gruppo di tester prima di avviare il periodo di prova. [Requisiti di test per account personali](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en).

## Scheda e screenshot

Testi, icona condivisa, banner e quattro screenshot smartphone per ciascuna lingua sono stati salvati come bozza nella scheda Play Console `4974041146086048690`; la persistenza è stata verificata riaprendo la pagina. La categoria Fotografia, il contatto `maininimassimo@gmail.com`, l’assenza di annunci e di aree con accesso limitato, il pubblico 13–17 e le dichiarazioni di contenuto risultano salvati. Le immagini preparate esprimono la UI dell’emulatore API 36, non mockup. È esclusa la schermata Mappa dalle immagini promozionali, poiché la pagina Allsky incorporata è in italiano anche con la lingua dell’app impostata a inglese.

Non caricare il bundle unsigned e non pubblicare la bozza privacy come informativa definitiva. Data Safety e gli altri questionari risultano salvati in Console, ma le modifiche sono ancora in attesa di revisione e non autorizzano il caricamento del bundle privo di firma.
