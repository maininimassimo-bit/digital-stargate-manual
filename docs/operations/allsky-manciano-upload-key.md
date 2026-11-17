---
title: AllSky Manciano · chiave di caricamento Play
description: Procedura locale per predisporre la chiave di caricamento senza inserirla nel repository.
---

# Chiave di caricamento Google Play — AllSky Manciano

La chiave di caricamento firma l’Android App Bundle inviato a Play Console. Play App Signing conserva la chiave che firma le app distribuite agli utenti; la chiave privata di caricamento va custodita con cura e non deve essere committata, inviata via email o incollata in chat.

## Creazione

Da Android Studio, usare **Build → Generate Signed Bundle / APK → Android App Bundle → Create new**. Selezionare una cartella privata fuori dal repository, impostare un alias e password robuste, usare RSA da 2048 bit e una validità lunga (per esempio 10.000 giorni). Annotare percorso e alias. Fare una copia di sicurezza cifrata del keystore in un archivio controllato dal titolare.

In alternativa, usare `keytool` dal JDK installato. L’esempio crea il keystore nella cartella utente, non nel repository; sostituire `AllSkyMancianoUpload` con un alias scelto. `keytool` chiede le password in modo interattivo:

```powershell
$keystorePath = Join-Path $env:USERPROFILE 'AllSkyMancianoUpload.jks'
keytool -genkeypair -v -keystore $keystorePath -alias AllSkyMancianoUpload -keyalg RSA -keysize 2048 -validity 10000
```

Non condividere il file `.jks` o le password. Per la registrazione su Play Console può essere necessario esportare e caricare soltanto il certificato pubblico. Il certificato non contiene la chiave privata.

## Collegamento alla build locale

Nel file locale `android/gradle.properties` (già presente su questa macchina; non sovrascriverlo), impostare le seguenti proprietà. Usare un percorso assoluto al file `.jks` e l’alias scelto. Le password restano in questo file locale, escluso dal controllo Git; non inserirle in `local.properties`, nei file versionati o nei log condivisi.

```properties
playUploadStoreFile=C:/Users/<utente>/AllSkyMancianoUpload.jks
playUploadStorePassword=<password-del-keystore>
playUploadKeyAlias=AllSkyMancianoUpload
playUploadKeyPassword=<password-della-chiave>
```

Le proprietà sono lette dalla configurazione `playUpload` in `android/app/build.gradle.kts`. Una volta configurate, il bundle si genera con:

```powershell
cd android
.\gradlew.bat bundleRelease
```

Prima del caricamento verificare la firma con `jarsigner -verify -verbose -certs` e confrontare SHA-256 e certificato con i dati richiesti dalla Console. Non caricare l’AAB se `jarsigner` lo segnala unsigned o se la Console indica che il certificato non corrisponde.

## Cosa serve per continuare qui

Quando il keystore è pronto, comunicare solo:

- percorso locale assoluto del keystore;
- alias della chiave.

Non inviare password, il file `.jks` o codici di recupero. Le password vanno inserite direttamente nel file locale sul PC. Dopo averle configurate, si può firmare l’AAB e verificarlo senza esporle in Git o nella conversazione.
