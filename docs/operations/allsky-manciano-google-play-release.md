---
title: AllSky Manciano · preparazione Google Play
description: Bundle Android, scheda localizzata e requisiti ancora da completare per Google Play.
---

# AllSky Manciano — preparazione Google Play

**Aggiornato:** 17 novembre 2026. **Stato:** materiale di release candidato 0.2.6 predisposto; nessun bundle caricato. L’account personale `maininimassimo@gmail.com` è attivo e la scheda Play Console è stata creata: ID `4974041146086048690`, package `it.digitalstargate.allskypocket`. Testi, icona, banner e quattro screenshot smartphone per ciascuna localizzazione (it-IT ed en-US) risultano salvati come bozza e verificati dopo un nuovo caricamento della pagina. Contatto pubblico confermato: `maininimassimo@gmail.com`. Nella Console sono state anche salvate le dichiarazioni “nessuna parte soggetta a limitazioni” e “nessun annuncio”, la categoria Fotografia e l’email di contatto.

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

`testDebugUnitTest assembleDebug bundleRelease` completano correttamente; i 9 test JUnit passano senza failure. L’AAB è stato validato con bundletool ufficiale 1.18.3; il manifest estratto conferma application ID, versione, minSdk 26 e targetSdk 36. `jarsigner -verify` conferma che il bundle è unsigned. `bundletool build-apks --connected-device` e `install-apks` hanno installato il candidato precedente sul simulatore API 36 firmandolo localmente con la chiave debug; il bundle aggiornato contiene il link privacy ma non è stato reinstallato sul G84 o sul simulatore. Nessuna di queste prove crea una firma Play.

Le schermate sono state acquisite dall’emulatore Android API 36; il Motorola G84 non è stato aggiornato con questo candidato. I set italiano e inglese mostrano contenuti pubblici reali dell’Allsky.

## Materiali della scheda

In `release/play-store/` sono pronti:

- `app-icon-512.png`: icona quadrata 512×512, PNG RGBA con canale alpha (immagine opaca).
- `it-IT/feature-graphic-1024x500.png` e `en-US/feature-graphic-1024x500.png`: banner localizzati 1024×500, PNG RGB.
- `LISTING-DRAFT.md`: titolo, descrizione breve e descrizione completa in italiano e inglese.
- `it-IT/` e `en-US/`: quattro screenshot reali dell’app per ciascuna lingua (1080×2160, PNG, senza alpha): Live, meteo, archivio/keogramma e meteore; ciascuna cartella contiene anche il banner locale. Le schermate tablet non sono incluse: l’emulatore in landscape non ha prodotto un set uniforme e stabile.
- `privacy-policy-draft.md`: riferimento alla pagina bilingue candidata; l’URL previsto non è ancora stato verificato dal deploy.
- `listing-manifest.json`: riepilogo candidato e campi console mancanti.

La scheda è stata creata come **App** (non gioco) e la categoria **Fotografia** è ora salvata in Play Console. Il bundle in questa cartella è solo un candidato unsigned; il file ottenuto dal toolchain locale è stato aggiunto anche a `release/` con checksum per agevolare la successiva firma.

Google richiede l’icona Play in PNG 32-bit con canale alpha, 512×512 e massimo 1 MB; la feature graphic è 1024×500. Per pubblicare la scheda base occorrono almeno due screenshot; per l’idoneità alle superfici di raccomandazione ne occorrono almeno quattro a 1080 px (verticali 1080×1920 o superiori, oppure orizzontali 1920×1080 o superiori). Entrambe le localizzazioni hanno ora quattro screenshot smartphone 1080×2160 e un banner 1024×500 associato. [Requisiti asset Google Play](https://support.google.com/googleplay/android-developer/answer/9866151?hl=en).

## Dati, privacy e moduli Play

L’app ha il solo permesso `INTERNET`, non include login, pubblicità o SDK di analytics e interroga il server Allsky per immagini, meteo, cataloghi pubblici e mappa. Il titolare ha confermato di gestire direttamente l’hosting e conservare i log di accesso per sei mesi, usandoli solo per gestione tecnica e sicurezza, senza analytics o geolocalizzazione IP. Il server riceve l’IP di connessione e i dati tecnici della richiesta; per Google, i tipi da dichiarare dipendono da come il dato viene effettivamente usato. Il modulo Data Safety deve dichiarare con accuratezza raccolta, finalità, condivisione e cifratura, senza selezionare “nessun dato raccolto” per omissione. La policy candidata è in `docs/operations/allsky-manciano-privacy.md`; URL previsto: `https://maininimassimo-bit.github.io/digital-stargate-manual/operations/allsky-manciano-privacy/`. Va verificato dopo il deploy. Google richiede una policy pubblica e un collegamento in-app oltre che nella scheda. [Policy privacy Play](https://support.google.com/googleplay/android-developer/answer/18265346), [indicazioni Data Safety/IP](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en-en).

Prima di inviare un test o richiedere la pubblicazione, completare:

1. Rivedere la scheda `AllSky Manciano` (italiano, app gratuita, package `it.digitalstargate.allskypocket`): testi, icona condivisa, banner localizzati e quattro screenshot per lingua sono salvati. La categoria Fotografia e l’email pubblica sono impostate. Restano da controllare i dettagli asset nella schermata di revisione e l’associazione Play App Signing. L’Owner ha autorizzato e confermato le dichiarazioni richieste nel modulo di creazione.
2. Il contatto pubblico è `maininimassimo@gmail.com` e il titolare confermato è Massimo Mainini. Pubblicare la pagina privacy con il normale deploy documentale e verificare l’URL dall’esterno.
3. Completare il modulo Data Safety in Play Console, dichiarando i log di accesso (sei mesi) secondo le definizioni e finalità del modulo corrente.
4. Selezionare fascia d’età, completare classificazione contenuti e dichiarazioni Console.
5. Generare la upload key e conservarla in modo sicuro; condividere con il progetto solo il riferimento locale alle credenziali, mai inserirle in Git. Il precedente tentativo locale è stato respinto dalla revisione automatica dell’ambiente; richiedere all’Owner di crearla sul proprio PC tramite il flusso standard Play Console/Android Studio, quindi firmare e verificare il bundle.
6. Caricare il bundle firmato su una traccia di test e completare la verifica da parte di Play Console prima della produzione.

Le dichiarazioni “nessun annuncio”, accesso non limitato, categoria Fotografia e contatto email sono salvate come modifiche in bozza. Il questionario “Pubblico di destinazione e contenuti” è ancora da completare: scegliere le fasce d’età in base al pubblico effettivamente previsto, poi completare la classificazione dei contenuti. Data Safety rimane da compilare dopo la mappatura esatta dei log IP e dei metadati di richiesta ai tipi e alle finalità del modulo corrente. Nessun invio alla revisione è stato effettuato.

Google richiede inoltre la verifica del possesso del dispositivo Android da parte dei nuovi account personali e la registrazione dei nomi dei package secondo le regole entrate in vigore il 30 settembre 2026. Il Motorola G84 Android 15 soddisfa la soglia tecnica; completare la verifica nell’app Play Console quando richiesto. [Verifica dispositivo](https://support.google.com/googleplay/android-developer/answer/14316361?hl=en), [registrazione dei package](https://support.google.com/googleplay/android-developer/answer/16984799?hl=en).

Per gli account personali creati dopo il 13 novembre 2023 Google richiede un test chiuso con almeno 12 tester iscritti continuativamente per 14 giorni prima di consentire la richiesta di accesso alla produzione. Verificare il requisito nella dashboard dell’account e organizzare il gruppo di tester prima di avviare il periodo di prova. [Requisiti di test per account personali](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en).

## Scheda e screenshot

Testi, icona condivisa, banner e quattro screenshot smartphone per ciascuna lingua sono stati salvati come bozza nella scheda Play Console `4974041146086048690`; la persistenza è stata verificata riaprendo la pagina. La categoria Fotografia, il contatto `maininimassimo@gmail.com`, l’assenza di annunci e l’assenza di aree con accesso limitato risultano salvati. Il questionario sul pubblico target è ancora da compilare. Le immagini preparate esprimono la UI dell’emulatore API 36, non mockup. È esclusa la schermata Mappa dalle immagini promozionali, poiché la pagina Allsky incorporata è in italiano anche con la lingua dell’app impostata a inglese.

Non caricare il bundle unsigned, non pubblicare la bozza privacy come informativa definitiva e non dichiarare completata la Data safety finché i punti precedenti non sono stati verificati.
