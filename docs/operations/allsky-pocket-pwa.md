---
title: Allsky Pocket · PWA Android
description: Prototipo pubblico per consultare Live, Meteo e Archivio Allsky su Android, senza login e senza accesso ai candidati privati.
---

# Allsky Pocket: Live, Meteo e Archivio su Android

**Baseline:** prototipo pubblicato il **16 novembre 2026**, accesso successivamente reso pubblico su richiesta dell’Owner. **Non richiede un account o un login ChatGPT.**

[Apri Allsky Pocket](https://digital-stargate-allsky-pocket.vibrantbadge.chatgpt.site/){ .md-button .md-button--primary }

La PWA è un sito installabile, distinto dall’[Allsky completa](https://digitalstargate.freeddns.it:23232/allsky/) e dal portale del manuale. Offre consultazione: non configura camera, Raspberry, router o rilevatori. Il passaggio da accesso privato a pubblico riguarda solo l’hosting della PWA e non modifica la configurazione Allsky.

## Installazione e prova su Android

1. Aprire **Chrome sul telefono Android**.
2. Visitare [il link pubblico di Allsky Pocket](https://digital-stargate-allsky-pocket.vibrantbadge.chatgpt.site/). Non è necessario accedere con ChatGPT.
3. Toccare **Installa app**. Se il browser propone l’installazione, confermare la propria scelta.
4. In alternativa aprire il menu **⋮ → Aggiungi a schermata Home → Installa**, secondo le voci disponibili nella versione di Chrome.
5. Avviare **Allsky Pocket** dall’icona aggiunta al telefono e provare le tre schede **Live**, **Meteo** e **Archivio**.

Se Chrome propone soltanto un collegamento alla schermata Home, usarlo per la prova: non equivale alla conferma dell’installazione standalone. Per aggiornare una pagina rimasta sul precedente accesso privato, riaprire il link pubblico; non occorre cambiare impostazioni dell’impianto. Le istruzioni qui riportate descrivono l’accesso pubblico corrente e sostituiscono quelle della prima anteprima privata.

La PWA non è un APK e non è distribuita sul Play Store. L’installazione e il comportamento su un **telefono Android fisico restano da collaudare dall’Owner**: la prova nel browser a larghezza mobile non li sostituisce. I prerequisiti e i diversi comportamenti di installazione sono descritti nella [documentazione PWA di web.dev](https://web.dev/learn/pwa/installation).

## Funzioni del prototipo

| Scheda | Funzioni e limiti |
|---|---|
| Live | Ultimo JPEG, ora dello scatto Europe/Rome, ingrandimento, aggiornamento manuale e dati di esposizione/guadagno/temperatura sensore. Il live è una sequenza di fotografie, non un flusso video continuo. |
| Meteo | Temperatura ambiente, umidità relativa, punto di rugiada e vento in km/h da CloudWatcher tramite la proiezione pubblica esistente. Misure scadute o assenti non sono presentate come attuali. |
| Archivio | Timelapse, startrails e keogram già pubblici, ordinamento dal più recente, filtro per data della notte, caricamento progressivo, apertura delle immagini complete e lettore video con controlli. La data è quella d’inizio della notte. |

Costellazioni e pianeti si consultano tramite il collegamento all’Allsky completa: il prototipo non replica né modifica la calibrazione VirtualSky. La PWA non comprende comandi amministrativi, notifiche push, storico meteo dedicato o strumenti di validazione delle meteore.

## Architettura e percorsi ammessi

Il client usa **React/TypeScript con Vinext/Vite**; un servizio server ospitato separatamente dalla camera legge le sorgenti pubbliche per evitare di cambiare la politica CORS del Raspberry. Manifest, icone e service worker rendono disponibile l’esperienza PWA. Baseline sorgente della prima versione: commit `88e007d4532432a4a70fbf0bee59599f9481b1da` nel repository sorgente del sito Sites, distinto da questo manuale. Il successivo cambio di accesso pubblico è una modifica della policy di hosting, non del commit applicativo.

| Componente PWA | Funzione |
|---|---|
| `app/page.tsx`, `app/globals.css` | Tre schede responsive, stato di aggiornamento, filtri, anteprime e istruzioni di installazione |
| `app/api/[action]/route.ts` | Sole operazioni GET, timeout sulle letture, gestione indisponibilità e streaming/range HTTP dei video |
| `lib/public-allsky.mjs` | Origine fissata, tipi di archivio ammessi, parser del catalogo e selezione dei campi telemetrici |
| `public/manifest.webmanifest` | Nome Allsky Pocket, avvio `/`, ambito `/`, modalità standalone e icone 192/512 px, inclusa maskable |
| `public/sw.js`, `public/offline.html` | Pagina offline e cache limitata alle risorse di fallback |

L’unica origine upstream è `https://digitalstargate.freeddns.it:23232`. I percorsi ammessi sono:

- `/current/image.jpg` per il JPEG live;
- `/allsky/dsg-live-data.json` per camera, meteo e astronomia;
- `/allsky/videos/`, `/allsky/startrails/`, `/allsky/keograms/` per i cataloghi pubblici;
- file e miniature con prefissi e date validati, esclusivamente nelle tre gallerie precedenti.

Il servizio non accetta un URL arbitrario, non segue redirect upstream e non inoltra cookie o credenziali del visitatore al Raspberry. La telemetria restituita contiene soltanto **camera, weather e astronomy**, oltre all’ora di generazione; i campi Raspberry, Aircraft, stelle e meteore non sono inoltrati. L’app non introduce un collegamento SSH, seriale o amministrativo verso l’impianto. La verifica TLS resta ordinaria, senza eccezioni ai certificati.

## Esclusione dei candidati privati

**I candidati del rilevatore temporale privato restano esclusi.** Non sono letti, copiati, indicizzati o pubblicati dalla PWA; il servizio `dsg-meteor-shadow.service` e il suo archivio privato restano separati e invariati.

La PWA non include neppure una galleria meteore: i soli tipi media consentiti sono `videos`, `startrails` e `keograms`. Non espone JSON individuali, immagini, miniature, contatori o registri del rilevatore privato. Rendere pubblico l’accesso alla PWA non concede accesso alla WebUI Allsky né modifica i permessi dei file sul Raspberry. [Confini dell’affiancamento privato](allsky-meteor-shadow.md).

## Aggiornamento, freschezza e offline

La proiezione è richiesta ogni **30 secondi** quando la pagina è visibile; gli aggiornamenti periodici sono sospesi quando è nascosta. Il JPEG viene richiesto nuovamente quando cambia il nome dello scatto. Non è una garanzia di cadenza esatta, che dipende anche da camera, rete e browser.

La proiezione è accettata entro **150 s** e lo scatto entro **180 s**, con controllo degli orari futuri. Il meteo richiede una scadenza `fresh_until_utc` valida e una misura non futura oltre **30 s**. In caso di errore o scadenza, l’interfaccia segnala indisponibilità; un’immagine già caricata può restare come **ultimo fotogramma**, senza essere etichettata come live aggiornato.

Il service worker non intercetta le richieste `/api/` e non salva foto/video live. Conserva la pagina offline e le relative risorse minime. Senza rete, una navigazione può quindi mostrare la pagina di indisponibilità; non è previsto un archivio completo offline. Le normali risposte HTTP possono mantenere per breve tempo i cataloghi pubblici e più a lungo i media storici: questo non rende disponibili dati attuali senza connessione.

## Verifiche e stato di collaudo

Il 16 novembre sono stati verificati:

- test del parser archivio, ordine/deduplicazione, allowlist dei campi e rifiuto di tipi privati o percorsi non validi;
- TypeScript senza errori e build del sito;
- browser locale desktop e viewport **390 × 844**, JPEG live **1936 × 1096**, stato meteo corrente/scaduto, filtro data, miniature e immagini complete;
- timelapse avviato con i controlli del lettore, con tempo osservato da **0,025 a 13,131 s** e fotogrammi visibili;
- pubblicazione del prototipo e successiva policy di accesso **public**; nel browser apertura senza schermata di login, live aggiornato, navigazione Meteo e Archivio con miniature caricate.

L’accesso anonimo è stato verificato nel browser. Una richiesta diagnostica automatica con il client Python ha ricevuto 403 dal filtro Cloudflare: non è stata usata come prova dell’accesso del visitatore e non sono state modificate le protezioni per aggirarla. Restano da verificare installazione Android fisica, riapertura dall’icona, rotazione del telefono, riproduzione sulla rete mobile e fallback offline sul dispositivo. Le informazioni meteo non costituiscono readiness o autorizzazione di sicurezza dell’osservatorio.

## Manutenzione e ripristino

Il sorgente e le versioni della PWA sono gestiti separatamente nel progetto Sites. Il manuale documenta l’integrazione: **i backup della configurazione Allsky non includono automaticamente il sorgente o l’hosting PWA**. Nessuna configurazione o immagine privata del Raspberry è stata trasferita nel progetto.

Per annullare un aggiornamento della PWA si ridistribuisce una sua versione precedente. Un eventuale ritorno all’accesso riservato è una modifica distinta della policy di hosting da autorizzare; non è necessario ripristinare Allsky o intervenire sull’acquisizione. Aggiornamenti al solo manuale non modificano app, server o permessi del sito.


## Accessi dalla Home del portale e dal sito Allsky

Dal 16 novembre la [Home del portale](../index.md) offre **Apri Allsky Pocket** e **Come installarla su Android**. La [pagina Allsky](https://digitalstargate.freeddns.it:23232/allsky/index.php) dispone di un richiamo equivalente sotto l’intestazione, fuori dalla ripresa. Il nuovo [snapshot Allsky delle 14:57](allsky-configuration-backup.md) include la pagina e il CSS di questi collegamenti: non include il sorgente o l’hosting della PWA esterna. Configurazione fotografica e calibrazione restano invariate; candidati privati esclusi.


## Evoluzione Android nativa proposta

Il 16 novembre 2026 è stato definito il [progetto della prima versione Android nativa](allsky-pocket-android-native.md), con Live, Meteo e Archivio e consegna iniziale di un APK locale per il telefono dell’Owner. Sviluppo e collaudo nativi sono ancora da eseguire. La PWA rimane separata e invariata; l’app non legge candidati privati e non richiede modifiche alla configurazione Allsky. La guida contiene piano, stime, confini e prompt per la chat Work dedicata.
