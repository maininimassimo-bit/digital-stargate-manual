---
title: Allsky · backup della configurazione
description: Snapshot privato della configurazione Allsky e copia pubblica sanificata, con integrità e procedura di ripristino controllato.
---

# Allsky: backup della configurazione

Snapshot corrente acquisito il **24/11/2026 alle 19:36 Europe/Rome**, dopo le correzioni SEO e l’integrazione della revisione manuale dei nuovi candidati temporali, senza fermare acquisizione o rilevatori. Conserva personalizzazioni, calibrazione, collegamenti Pocket e correzione di avvio del worker privato. Baseline **Allsky v2026.10.01_01**, Git `f1406ea78ba969313abd1ddd14a4272967081a06`, con le personalizzazioni descritte nel [Capitolo 27](../chapters/27-sistema-allsky.md) e nella [guida ai pannelli](allsky-live-panels.md).

## Due copie con finalità diverse

| Copia | Destinazione | Uso |
|---|---|---|
| Privata completa per il perimetro descritto sotto | Archivio privato Raspberry e copia locale consegnata all'owner | Ripristino mirato di configurazione e personalizzazioni, comprese informazioni riservate |
| Pubblica sanificata | Questo repository e portale | Documentazione versionata; richiede reinserimento dei valori privati e dipendenze prima dell'uso |

La copia privata **non è pubblicata su GitHub**. Include autenticazione, database e configurazione HTTPS: va conservata con accesso limitato. È un archivio compresso non cifrato; i permessi di accesso non equivalgono alla cifratura. Sul Raspberry la directory è privata; la copia consegnata su Windows ha accesso limitato all'utente corrente, SYSTEM e amministratori. Per trasferimenti o conservazione su supporti condivisi usare uno spazio privato cifrato.

## Download pubblico e integrità

- [Snapshot pubblico sanificato, TAR.GZ](../assets/backups/allsky-public-20261124-193619.tar.gz).
- [Checksum SHA-256 dell'archivio](../assets/backups/allsky-public-20261124-193619.tar.gz.sha256).

SHA-256 pubblico: `3bb38df504e70b6b3354d997cf1080f9d9292c176753d2ad3ed75f39dd77d587` (5.503.153 byte).

L'archivio pubblico corrente contiene **163 file verificati**, oltre al proprio `SHA256SUMS`. Quello privato contiene **378 file verificati**, oltre al proprio manifest. I checksum verificano identità e integrità dei byte; non attestano un ripristino riuscito e non costituiscono una firma del produttore.

## Snapshot precedenti conservati

La copia delle **15:49:34 del 16 novembre**, dopo la presentazione SEO iniziale, resta immutata: [archivio pubblico](../assets/backups/allsky-public-20261116-154934.tar.gz), [checksum](../assets/backups/allsky-public-20261116-154934.tar.gz.sha256).

La copia delle **15:25 del 16 novembre** con avvio privato corretto resta immutata: [archivio pubblico](../assets/backups/allsky-public-20261116-152502.tar.gz), [checksum](../assets/backups/allsky-public-20261116-152502.tar.gz.sha256). Prima della presentazione SEO è stato acquisito lo snapshot delle **15:47:45**, `configuration-backup-20261116-154745`, conservato su Raspberry/PC; il suo export intermedio non è aggiunto al repository.

La copia Pocket delle **14:57 del 16/11/2026** resta immutata: [archivio pubblico](../assets/backups/allsky-public-20261116-145705.tar.gz), [checksum](../assets/backups/allsky-public-20261116-145705.tar.gz.sha256). Prima della correzione di avvio è stato acquisito anche lo snapshot delle **15:24**, `configuration-backup-20261116-152406`, conservato separatamente su Raspberry/PC; il suo export intermedio non viene aggiunto al repository. Entrambi contengono 367 file privati e 148 pubblici oltre ai manifest.

La copia delle **22:07 del 12/11/2026** rimane immutata: [archivio pubblico](../assets/backups/allsky-public-20261112-220710.tar.gz), [checksum](../assets/backups/allsky-public-20261112-220710.tar.gz.sha256). Precede i collegamenti Pocket e contiene 366 file privati e 147 pubblici oltre ai manifest.

Prima dell’affiancamento è stato creato alle **21:53 del 12/11/2026** `configuration-backup-20261112-215352`: 358 file privati e 140 pubblici oltre ai manifest, conservati separatamente su Raspberry/PC. L’export intermedio non è aggiunto al repository.

La copia delle **19:25 del 12/11/2026** rimane immutata: [archivio pubblico](../assets/backups/allsky-public-20261112-192507.tar.gz), [checksum](../assets/backups/allsky-public-20261112-192507.tar.gz.sha256), SHA-256 `c154b198ec380527d950f14421549119fcff9819a9579008f0e29698d1c7fa53`. Include maschere/flag camera, ma precede il nuovo servizio privato.

Prima delle modifiche a maschere/flag è stato creato lo snapshot delle **19:16 del 12/11/2026**, `configuration-backup-20261112-191658`: 357 file privati e 140 pubblici oltre ai manifest, conservato separatamente sul Raspberry/PC Owner; il relativo export intermedio non è aggiunto al repository. Il backup mirato `masks-autoflags-20261112` conserva settings e PNG originali. [Intervento, verifiche e rollback mirato](../chapters/27-sistema-allsky.md#2736-maschere-aggiornate-e-flag-camera-coerenti-con-snapshot-12-novembre-2026).

La copia del **12/11/2026 alle 18:31**, dopo il solo aggiornamento di versione, resta immutata: [archivio pubblico](../assets/backups/allsky-public-20261112-183125.tar.gz), [checksum](../assets/backups/allsky-public-20261112-183125.tar.gz.sha256). Contiene 357 file privati e 140 pubblici; SHA-256 pubblico `e6f8d26b7971140265d316f331f86d786f4a969e951a0bad8ff0577e495ef73c`. Precede le nuove maschere e la disabilitazione dei quattro automatismi camera.

Prima dell’aggiornamento del 12 novembre è stato acquisito alle **18:15** lo snapshot privato `configuration-backup-20261112-181517`, 356 file oltre al manifest, e un archivio privato aggiuntivo per il ripristino di programma/binari/configurazioni precedenti. Sono conservati separatamente su Raspberry e PC Owner; non vengono pubblicati. Il dettaglio dell’intervento e del ripristino predisposto è nel [§27.35](../chapters/27-sistema-allsky.md#2735-aggiornamento-allsky-v20261001_01-12-novembre-2026).

La copia del **31/10/2026 alle 18:50** resta immutata: [archivio pubblico](../assets/backups/allsky-public-20261031-185033.tar.gz), [checksum](../assets/backups/allsky-public-20261031-185033.tar.gz.sha256). Contiene 356 file privati e 140 pubblici; SHA-256 pubblico `031b57fdd948ca77a728b30462d3d502125002c971e636c0dbc76e5c9523b87b`. Include vento e ricalibrazione, ma precede l’aggiornamento Allsky del 12 novembre.

La copia del **31/10/2026 alle 18:21** resta immutata: [archivio pubblico](../assets/backups/allsky-public-20261031-182122.tar.gz), [checksum](../assets/backups/allsky-public-20261031-182122.tar.gz.sha256). Contiene 356 file privati e 140 pubblici; SHA-256 pubblico `c125bd2226d2e7f0a6da58844cbe3e6e59734a548208708cfce7c1b73107593e`. Include la ricalibrazione, ma precede l’integrazione vento. Lo snapshot storico delle 18:50 include entrambe.

La copia del 27/10/2026 alle 08:01 resta immutata: [archivio pubblico](../assets/backups/allsky-public-20261027-080114.tar.gz), [checksum](../assets/backups/allsky-public-20261027-080114.tar.gz.sha256). Conteneva 140 file pubblici e 355 privati; SHA-256 pubblico `50516b2eeb7653678f43fc1a7b02b6b357f47d0476fd2bb417abfec1cf3809d9`. Include il retry live, ma la geometria overlay precede lo spostamento della camera del 31 ottobre.

La copia dell’11/10/2026 alle 10:49 resta immutata: [archivio pubblico](../assets/backups/allsky-public-20261011-104905.tar.gz), [checksum](../assets/backups/allsky-public-20261011-104905.tar.gz.sha256). Conteneva 140 file pubblici e 351 privati; SHA-256 pubblico `d9546a8a0f8768123d262bf659b04fde539c457a8d0541293bf7ca1dbc57b94e`. Include le anteprime Messier e la soglia startrail ripristinata, ma non il retry del caricamento live introdotto il 27 ottobre.

La copia del 10/10/2026 alle 01:48 resta immutata: [archivio pubblico precedente](../assets/backups/allsky-public-20261010-014844.tar.gz), [checksum](../assets/backups/allsky-public-20261010-014844.tar.gz.sha256). Conteneva 27 file pubblici e 236 privati; SHA-256 pubblico `1cf4884e5f71923c022963db8b879ae66d14eae09bde356f47a026ff302ded50`. La soglia startrail 0,10 presente in quel backup è superata dal ripristino a 0,30 dell’11 ottobre.

## Contenuto privato

- `allsky/config`: impostazioni, pipeline moduli, overlay, logo, maschere, moduli personalizzati, calibrazione e dati di configurazione presenti. Esclusi cache `tmp`, log, bytecode Python e file di lock.
- Moduli `scripts/modules/allsky_pistatus.py` e `allsky_shared.py` inclusi nella sola copia privata: seguono ora la release v2026.10.01_01; la prova locale non risolutiva del 27 ottobre resta annullata.
- Ricetta geometrica delle maschere in `config/myFiles/masks/analysis-masks-20261112.json`, senza fotografie di prova; i progetti del Mask Editor nativo non sono stati generati.
- Collegamento fisico fra i due file settings della camera preservato nella copia privata quando presente nell’installazione; verificato anche nel TAR.
- Database SQLite acquisiti attraverso l'API di backup SQLite, invece di affidarsi alla sola copia del file in uso.
- File del sito selezionati: Home, configurazione del sito, controller, CSS originali modificati e pannelli aggiunti, footer, immagini grafiche, favicon, sitemap, robots.txt e pagina meteore. Incluse le personalizzazioni amministrative `html/includes/meteors.php` e `html/js/jquery-allskysensor/jquery-allskysensor.js`.
- Renderer `virtualsky/virtualsky.js`, catalogo Messier arricchito, 110 miniature DSS2 e relativi crediti: inclusi nelle copie privata e pubblica.
- Configurazione lighttpd, directory HTTPS compresa; servizi `allsky`, `allskyperiodic`, `allskyserver` e servizio/timer `dsg-live-telemetry` e unit `dsg-meteor-shadow`.
- Configurazione `systemd-timesyncd`, eventuali drop-in, fuso e lista dei pacchetti Python del virtual environment.
- Metadati con istante di acquisizione e commit Allsky, manifest dei file e checksum dell'archivio.

**Non è un'immagine completa della scheda SD.** Non include sistema operativo, intero sorgente Allsky, virtual environment eseguibile, librerie native/SDK camera, immagini e video scientifici, storico delle gallerie, configurazione del router, chiavi SSH dell'operatore o snapshot completi di EAGLE/CloudWatcher. Queste componenti richiedono installazione o backup separati. Eventuali cartelle di supporto esterne al perimetro elencato non sono implicitamente incluse.

Sono inclusi codice, profilo e maschera fissata di `config/myFiles/meteor-shadow`, insieme al tool `config/myFiles/backup/capture-configuration.py` nella copia privata. **Archivio candidati, registro SQLite e stato del servizio in `/var/lib/dsg-meteor-shadow` non sono inclusi**: occorre una copia privata separata per recuperarli fuori dal Raspberry. [Perimetro del servizio e disattivazione](allsky-meteor-shadow.md).

## Contenuto pubblico e sanificazione

L'esportazione pubblica è una lista esplicita di file: impostazioni camera sanificate, pipeline principali giorno/notte/periodica, configurazione overlay Digital Stargate, logo e maschere, configurazione del sito, Home/controller/CSS/footer, modulo archivio meteore, collector dei pannelli e relativi servizi systemd. L’export conserva worker/profilo/maschera, modulo upstream, licenza/provenienza e unit del rilevatore temporale privato, senza risultati o candidati. Il nuovo snapshot include la pagina `html/allsky/index.php` con i due collegamenti e il CSS dedicato `html/allsky/css/dsg-pocket-links.css`. Il sorgente e l’hosting della PWA restano separati: il backup Allsky ne conserva i collegamenti, non l’applicazione distribuita su Sites.

Valori riservati sono sostituiti da `__PRIVATE_VALUE__`, `__PRIVATE_IP__`, `__PRIVATE_EMAIL__` o `__PRIVATE_RELAY_HOST__`. Coordinate precise, localizzazione configurata, credenziali e impostazioni di trasferimento sono rimosse; il riferimento pubblico Aircraft all'area approssimata di Manciano resta quello già documentato. Non sono inclusi database, token di sessione, password iniziali, certificati, chiavi, configurazione lighttpd privata, dati live o font di sistema. Il modulo Solar System e le dipendenze si ripristinano dalla copia privata o dal rispettivo progetto, non da questo export ridotto.

Sono incluse le miniature di riferimento Messier, non i media scientifici acquisiti. Coordinate equatoriali degli oggetti celesti sono dati del catalogo pubblico e non coordinate geografiche del sito. Provenienza e crediti delle immagini DSS2 restano nel catalogo e in `CREDITS.txt`; si applicano i diritti indicati dalla sorgente.

La licenza MIT Allsky è mantenuta nel file `ALLSKY-LICENSE`; i file derivati conservano le intestazioni presenti. La pubblicazione dell'export non trasferisce la titolarità delle dipendenze escluse.

**La copia pubblica non va applicata direttamente all'impianto:** alcuni valori hanno intenzionalmente un tipo o un contenuto diverso dall'originale. Serve come riferimento versionato e base di ricostruzione manuale. Anche la copia privata richiede confronto con versione, sistema e host di destinazione.

## Verifiche effettuate e limiti

Lo snapshot v2026.10.01_01 conserva codice/profilo/unit dell’affiancamento privato (§27.37) e aggiunge il richiamo Pocket descritto nel §27.40. Mantiene le maschere del §27.36 e i quattro flag Auto-Gain/Auto White Balance disabilitati, la soglia startrail 0,30, `mouse=false`, catalogo completo di 110 anteprime e retry singolo del caricamento live del 27 ottobre. La prova locale PiStatus del 27 ottobre non è inclusa; i moduli nativi nel privato sono quelli della release aggiornata. Sono inclusi anche pannello vento, JavaScript e collector con fallback diagnostico CloudWatcher in km/h, come descritto nella [guida pannelli](allsky-live-panels.md). Il controller include l’integrazione della release e il riferimento di cache finale `dsg-upgrade-20261112-v2`; i metadati del sito sono a ConfigVersion 6. La geometria overlay corrente è quella ricalibrata il 31 ottobre (§27.33), con evidenza completa inclusa nel privato. Gli snapshot precedenti alla ricalibrazione del 31 ottobre descrivono l’orientamento anteriore allo spostamento; non usarli come calibrazione corrente. Le opzioni fotografiche e la decisione di mantenere la modalità USB corrente restano quelle documentate nei §§27.30–27.31 del Capitolo 27. I due database hanno superato `quick_check`; l’hardlink settings è conservato nell’archivio privato. Sono stati verificati checksum dei due archivi, hash di tutti i file nei manifest, percorsi interni senza attraversamenti `..`, JSON del pacchetto pubblico, parsing degli script Python, sintassi JavaScript e PHP della Home/footer sanificati. La revisione del pacchetto pubblico ha controllato assenza di database, chiavi/certificati, indirizzi privati ed email e sostituzione dei campi riservati. Il servizio di acquisizione e il timer dei pannelli risultavano attivi dopo la copia.

Lo snapshot dei file è stato acquisito con applicazione in funzione: non è una transazione atomica dell'intera installazione. Per i database è stata usata una copia consistente SQLite, ma non è attestata una transazione comune fra database differenti e file JSON. **Non è stato eseguito un ripristino**, né su Raspberry di prova né sull'impianto. Il collaudo di recupero su supporto separato resta da effettuare prima di considerare il pacchetto una soluzione di disaster recovery validata.

## DSG-PROC-027-04 — Ripristino controllato

1. Procurarsi l'archivio privato e il suo checksum dalla copia consegnata all'owner o dalla directory privata `configuration-backup-20261116-154934` del Raspberry. Conservarne una copia fuori dal Raspberry per coprire un guasto della scheda.
2. Controllare SHA-256 dell'archivio; estrarlo in una directory di lavoro privata, senza sovrascrivere direttamente percorsi di sistema. Verificare `SHA256SUMS` dalla directory `private` estratta.
3. Preparare Allsky compatibile con la baseline indicata, sistema/SDK camera e dipendenze Python. La lista dei pacchetti è un inventario, non un installer da eseguire alla cieca. Conservare una nuova copia della configurazione di destinazione per il rollback.
4. In una finestra di manutenzione fermare acquisizione, servizi periodici/sensor server pertinenti e timer dei pannelli. Confrontare e ripristinare soltanto i file necessari di `config` e del sito, con proprietà e permessi corretti. Non sovrascrivere indiscriminatamente autenticazione o database su un host diverso. Su questa installazione `settings.json` e `settings_ZWO_ASI290MC.json` condividono lo stesso inode: dopo un ripristino conservare o ricreare il collegamento fisico verificato; una copia dei soli contenuti non garantisce il mantenimento degli hardlink.
5. Rivedere separatamente certificati, chiavi, regole lighttpd, servizi e NTP. Su un nuovo host adattare percorsi e impostazioni; non cambiare esposizione di rete o amministrazione come effetto implicito del ripristino. Validare configurazione PHP/lighttpd e ricaricare systemd se sono stati cambiati i servizi.
6. Riavviare le componenti necessarie. Controllare camera, fotogramma e timestamp nuovi, NTP, overlay, maschere, pipeline notturna, archivio candidati e pannelli. Verificare sito pubblico e isolamento della WebUI amministrativa; dati scaduti devono restare indisponibili.
7. Se il controllo fallisce, fermare le componenti interessate e ripristinare la copia precedente del punto 3. Documentare esito, versione e file effettivamente ripristinati.

La procedura non interviene su cupola, montatura, interlock o Safety Authority. Non comporta cancellazione o ripubblicazione dei candidati meteore esclusi dall'owner.

## Aggiornamenti futuri

Dopo una modifica verificata a moduli, maschere, overlay, calibrazione o pubblicazione, creare un nuovo snapshot con data, checksum e perimetro. Conservare separatamente il privato; produrre e rivedere una nuova esportazione sanificata prima di qualunque commit. Non copiare mai l'archivio privato nel working tree Git, nemmeno temporaneamente: rimuoverlo in un commit successivo non lo eliminerebbe dalla cronologia.

Per i nuovi snapshot di questo perimetro usare il tool aggiornato `config/myFiles/backup/capture-configuration.py`, che comprende la unit privata e, dal 16 novembre, il CSS dedicato ai collegamenti Pocket in entrambe le copie. L’arresto o il ripristino del solo affiancamento non richiede di fermare Allsky.


## Collaudo successivo dello snapshot — 14 novembre 2026

Il [collaudo dei prodotti della notte 12–13 novembre](../chapters/27-sistema-allsky.md#2738-collaudo-prodotti-della-notte-1213-novembre-concluso-14-novembre-2026) verifica generazione e visualizzazione pubblica di startrails, keogram e timelapse, inclusa riproduzione effettiva nel browser. Registra separatamente una riga statistica storica assente e quattro scarti diurni durante la rampa all’alba, con proposte non applicate e soggette ad autorizzazione. È una diagnosi senza modifiche: non ha sostituito il backup allora corrente del 12 novembre alle 22:07 e non attesta un ripristino integrale della scheda SD.


## Collegamenti Pocket e snapshot del 16 novembre 2026

Sulla pagina Allsky è presente un richiamo fuori dalla ripresa, sotto l’intestazione, con **Apri Allsky Pocket** e **Installa su Android**. Il backup mirato prima della modifica è `pocket-links-20261116-145155`: conserva la pagina precedente; il CSS dedicato era assente. Per annullare soltanto il richiamo, in intervento autorizzato ripristinare quella `index.php` e rimuovere il solo CSS aggiunto, senza ripristinare settings, mappa o intero sito. Nessun riavvio dell’acquisizione è necessario per i due file web.

Lo snapshot completo aggiornato è **`configuration-backup-20261116-145705`**. Il tool canonico è stato esteso nelle due allowlist per includere `dsg-pocket-links.css`; la sua versione precedente è nel backup mirato privato. Manifest e checksum delle due copie sono stati verificati sul Raspberry e dopo il trasferimento al PC; i due database SQLite superano `quick_check` e l’hardlink camera è presente anche nel TAR. Nell’export pubblico sono stati verificati JSON, Python, JavaScript e PHP, esclusione di database/chiavi/certificati e redazione dei campi riservati. I due URL pubblici Pocket/guida e il CSS sono presenti.

I checksum di settings, flusso notturno, maschere, configurazione e controller della mappa coincidono con il controllo precedente all’aggiunta del richiamo. Allsky mantiene lo stesso processo **721**, avviato alle **08:17:29** del 16 novembre, senza riavvio per modifica o backup. Il servizio temporale privato era già **inattivo** al controllo precedente e resta tale; non è stato riattivato né modificato. La presenza della sua unit nel pacchetto non attesta che sia in esecuzione. Il suo archivio immagini e registro privato restano esclusi dal backup di configurazione e dal repository.

La copia privata è conservata separatamente sul Raspberry e, fuori dai checkout Git, nella directory locale `outputs/allsky-backup-20261116-pocket/private`, con ACL per Owner, SYSTEM e amministratori. Nel repository entra esclusivamente il TAR pubblico con il suo checksum. I candidati privati non sono pubblicati; non sono stati eseguiti ripristini o prove distruttive.


## Avvio del rilevatore temporale privato — 16 novembre 2026, 15:24

Il controllo dei log di boot ha individuato un ciclo di ordinamento: il servizio privato era collegato a `multi-user.target` tramite `WantedBy`, aspettava `allsky.service`, e Allsky aspettava `multi-user.target`. Il log riporta `Job dsg-meteor-shadow.service/start deleted to break ordering cycle`. Non era un crash del rilevatore; il suo ultimo stato su disco era precedente al riavvio e non attestava un processo attivo.

Dopo autorizzazione Owner e backup **15:24:06**, è stata rimossa soltanto la riga `After=allsky.service` da `/etc/systemd/system/dsg-meteor-shadow.service`, ricaricata la definizione e avviato il solo servizio privato alle **15:24:49**. Il worker può attendere autonomamente i JPEG notturni, senza dipendere dall’avvio dell’acquisizione. Le protezioni, i limiti di risorse e `publish:false` sono invariati. La validazione della unit e di `multi-user.target` termina senza errori. Non è stato eseguito un riavvio del Raspberry: il prossimo avvio reale resta da verificare.

Collaudo diurno: servizio attivo, nessun riavvio automatico o errore, stato aggiornato `waiting-for-night-frame`. I controlli negano tre accessi in scrittura alla produzione e la creazione di socket IPv4. Registro privato integro; modulo e maschere corrispondono agli hash fissati. Rilevatore attuale `allsky_meteorarchive.py` ancora abilitato; acquisizione sempre sul PID 721. Undici file protetti, inclusi profilo/worker, flusso notturno, settings, maschere, mappa/controller e pagina/CSS Pocket, sono identici al backup precedente. Nessun candidato privato pubblicato o copiato nel repository. L’elaborazione di nuovi fotogrammi notturni non è attestata da questa prova diurna.

Snapshot corrente **15:25:02**, `configuration-backup-20261116-152502`: 367 file privati e 148 pubblici oltre ai manifest. Verificati entrambi gli archivi, manifest, database SQLite, hardlink settings e sanificazione. La copia privata è separata su Raspberry e PC (`outputs/allsky-shadow-fixed-20261116/private` fuori da Git, ACL limitate); il repository contiene solo il nuovo export sanificato con checksum. Candidati e registro privato restano fuori dal perimetro del backup di configurazione.

Rollback mirato, se necessario: fermare soltanto `dsg-meteor-shadow`, ripristinare la unit da `configuration-backup-20261116-152406/private/etc/systemd/system/dsg-meteor-shadow.service` e ricaricare le definizioni. Non toccare Allsky o il rilevatore attuale. La vecchia unit reintroduce il conflitto al boot e va conservata come evidenza, non usata come soluzione definitiva.


## Presentazione HTML e Google — 16 novembre 2026, 15:49

Lo snapshot corrente `configuration-backup-20261116-154934` include la presentazione visibile sotto la ripresa e il CSS dedicato, insieme ai collegamenti Pocket e alla unit privata corretta. [Diagnosi Search Console e richiesta accettata](allsky-search-indexing.md#verifica-e-migliorie-del-16-novembre-2026). Nessuna modifica all’acquisizione o pubblicazione di candidati privati.

Le copie pre/post hanno checksum e manifest verificati, database SQLite `quick_check` positivo, hardlink settings conservato e export pubblico sanificato. Copia privata su Raspberry e PC (`outputs/allsky-seo-post-20261116/private`, fuori da Git con accesso limitato); solo TAR pubblico e checksum pubblicati. Il backup preventivo è `configuration-backup-20261116-154745`; per annullare la presentazione ripristinare soltanto pagina e CSS da quel privato. Non è stato collaudato un ripristino integrale e la conferma di richiesta Google non equivale a indicizzazione.


## SEO e revisione manuale meteore — 24 novembre 2026

Snapshot preventivo **19:01:58**, `configuration-backup-20261124-190158`, 367 file privati e 148 pubblici oltre ai manifest, verificato su Raspberry e PC. Ulteriori originali mirati sono in `seo-rollback` e `meteor-review-rollback` sotto quella directory privata. Il suo export pubblico intermedio non è aggiunto al repository.

Snapshot successivo **19:36:19**, `configuration-backup-20261124-193619`: **378 file privati e 163 pubblici**, oltre ai manifest. Acquisito senza fermare i servizi; SQLite tramite API di backup coerente, hardlink settings preservato. SHA-256 degli archivi e tutti i file dei due manifest verificati sulle copie locali. Il privato è conservato sul Raspberry e in una directory del PC Owner fuori da Git, con accesso limitato all’utente corrente. Pubblico sanificato con allowlist esplicita nel repository, non una copia indiscriminata del privato.

Comprende ora i due WebP decorativi versionati, robots, sitemap, template e ingressi delle quattro gallerie, codice/configurazione/unit della revisione manuale e pagina amministrativa con collegamento Meteors. Nel privato sono presenti anche le regole lighttpd aggiornate; non sono aggiunte all’export pubblico con credenziali o materiale TLS. I sorgenti della revisione pubblicati nel repository non contengono credenziali.

**Esclusioni:** JPEG candidati temporali e ordinari, dati in `/var/lib/dsg-meteor-shadow`, registro decisioni e limite persistente in `/var/lib/dsg-meteor-review`, stato temporaneo, media storici e hosting PWA. Questo è uno snapshot di configurazione, non un backup dello storico o un’immagine SD. Per conservare decisioni e candidati in un ripristino completo serve un backup privato aggiuntivo e coerente di quegli stati; non ricrearli da una copia pubblica e non retrodatare `new_after`.

Per annullare la sola revisione: disabilitare `dsg-meteor-review.service` e ripristinare `html/includes/meteors.php` dall’originale mirato. Conservare lo stato privato per audit; il worker temporale e il rilevatore ordinario restano attivi. Per la sola SEO: ripristinare i file in `seo-rollback`, validare lighttpd e ricaricarlo, senza toccare settings, maschere o calibrazione. Le richieste Google già inviate non sono annullate dal rollback. Nessun ripristino integrale o riavvio fisico è stato eseguito.

[Verifica Google e correzioni](allsky-search-indexing.md#correzioni-seo-e-rendering-google-24-novembre-2026) · [Revisione manuale e collaudo](allsky-meteor-shadow.md#revisione-manuale-dei-nuovi-candidati-24-novembre-2026).


## Ripristino della bonifica della galleria

Il backup media del 26 novembre 2026 è separato dal backup di configurazione: la configurazione non è stata modificata dalla bonifica. L’archivio privato preventivo contiene l’intera galleria prima dell’intervento, misura 259.184.043 byte ed è stato verificato insieme agli hash delle 422 immagini originali. Archivio, miniature, manifesti e report rimangono fuori dal repository, sul Raspberry e nell’archivio privato su J:.

La procedura predisposta ripristina l’intero lotto di 103 immagini e relative 103 miniature descritto nel piano privato. **Il ripristino non è stato eseguito in produzione**: sono state verificate integrità dei backup, segregazione della quarantena ed esito della bonifica.

1. Rivedere privatamente il piano e autorizzare la nuova esposizione delle immagini. Il ripristino non conferma la natura astronomica delle tracce.
2. Sul Raspberry, verificare directory, spazio disponibile e piano originale. Evitare scritture concorrenti sugli stessi nomi durante l’operazione; non è previsto un arresto automatico dell’acquisizione.
3. Nella directory privata dell’intervento, verificare il checksum ed eseguire lo script soltanto dopo le verifiche precedenti:

```bash
cd '<directory_privata_della_bonifica>'
sha256sum -c public-gallery-before.tar.gz.sha256
python3 restore.py
```

Lo script usa i percorsi del Raspberry contenuti in `move-plan.json`: non va eseguito su Windows. Prima della copia verifica tutti gli asset. Salta le destinazioni già presenti e identiche; si interrompe se trova una destinazione diversa o un file di quarantena mancante o con hash inatteso. Copia i file assenti dalla quarantena, verificandone l’hash e conservando le copie private. In caso di conflitto non forzare la sovrascrittura.

Per un ripristino parziale predisporre e rivedere separatamente un piano derivato, mantenendo intatto quello originale. Non estrarre indiscriminatamente l’intero archivio sulla galleria corrente: potrebbero esserci immagini pubblicate dopo la bonifica. Non occorre ripristinare impostazioni, maschere o calibrazione per annullare un trasferimento di soli media.

Al termine verificare coppie immagine/miniatura, hash, risposta HTTP della galleria e di immagini rappresentative, stato dei servizi Allsky e dei due servizi meteore. Confrontare i conteggi tenendo conto delle nuove acquisizioni. Il revert della documentazione su GitHub non ripristina i media: il ripristino operativo è distinto.

La copia pubblica sanificata della configurazione resta separata: il backup media e i suoi dettagli individuali non devono essere aggiunti a Git, allegati alle PR o pubblicati sul portale.


## Ripristino della selezione manuale del 27 novembre 2026

Il secondo intervento ha un proprio backup e un proprio piano privato, separati dal lotto del 26 novembre. Il backup preventivo `selected-public-before.tar.gz` contiene le 300 immagini selezionate a piena risoluzione e 300 miniature, misura **187.835.335 byte** e ha superato la verifica degli hash di tutti i 600 asset prima del trasferimento. Non contiene configurazioni da ripristinare.

Le 23 copie amministrative ancora esistenti sono rimaste invariate; per le altre 277 immagini la conservazione è assicurata dalle copie a piena risoluzione in quarantena e nel backup. Quarantena, backup e manifesti sono esterni alla radice web e restano privati. Il precedente backup completo della galleria rimane separato e disponibile.

Per annullare il solo secondo intervento usare la directory privata del **lotto del 27 novembre**, verificare il checksum e rivedere il relativo piano prima di eseguire sul Raspberry:

```bash
cd '<directory_privata_del_lotto_del_27_novembre>'
sha256sum -c selected-public-before.tar.gz.sha256
python3 restore.py
```

Lo script ripristina l’intero piano di quel lotto: 300 immagini e 300 miniature. Non ripristina automaticamente il primo lotto di 103 immagini. Restano validi i controlli del paragrafo precedente: nessuna sovrascrittura di file diversi, coordinamento contro scritture concorrenti sugli stessi nomi, conservazione della quarantena e verifica finale di hash, coppie immagine/miniatura, HTTP e servizi. Un ripristino parziale richiede un piano derivato separatamente verificato.

**Nessun ripristino è stato eseguito.** L’operazione rende nuovamente pubbliche le copie interessate e richiede autorizzazione; la selezione non certifica la natura delle tracce. Il backup di configurazione e la copia pubblica sanificata restano separati dai backup media e non vengono sostituiti da questi archivi.
