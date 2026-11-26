---
title: Allsky rilevatore temporale privato
description: Affiancamento asincrono del rilevatore temporale di meteore, con archivio privato e rilevatore ordinario invariato.
---

# Affiancamento privato del rilevatore meteore

Dal **12 novembre 2026 alle 22:03 Europe/Rome** il servizio `dsg-meteor-shadow.service` analizza le nuove immagini notturne già salvate da Allsky. L’Owner ha autorizzato l’affiancamento dopo la valutazione su tre notti complete. Il rilevatore ordinario rimane nel flusso esistente; **il worker non pubblica i candidati temporali**. Dal 24 novembre i soli nuovi risultati possono passare dalla revisione manuale riservata descritta sotto; lo storico precedente resta escluso.

Dopo il riavvio del 16 novembre il servizio non era partito per un ciclo di ordinamento systemd. Corretto e riattivato con autorizzazione Owner alle **15:24:49**; il controllo diurno lo trova attivo in attesa di fotogrammi notturni. [Diagnosi e snapshot aggiornato](allsky-configuration-backup.md#avvio-del-rilevatore-temporale-privato-16-novembre-2026-1524).

Il servizio è esterno alla pipeline di acquisizione: legge i JPEG dopo il salvataggio e lavora a bassa priorità. Non cambia parametri fotografici, maschere della produzione, calibrazione VirtualSky, contatori pubblici o generazione dei prodotti notturni. [Configurazione Allsky e cronologia degli interventi](../chapters/27-sistema-allsky.md#2737-valutazione-e-affiancamento-privato-delle-meteore-12-novembre-2026).

## Risultati della valutazione precedente

La prova offline ha elaborato **2.176 JPEG** delle notti 31/10–01/11, 03–04/11 e 11–12/11, circa 38 ore e 21 minuti. Il confronto considera i **2.170 fotogrammi centrali**, escludendo il primo e l’ultimo di ciascuna sequenza per il confronto temporale con i vicini.

| Notte | Fotogrammi candidati dell’attuale a 100 px | Temporale a 100 px | Temporale a 50 px |
|---|---:|---:|---:|
| 31/10–01/11 | 33 | 11 | 14 |
| 03–04/11 | 42 | 8 | 10 |
| 11–12/11 | 1 | 1 | 4 |
| Totale | 76 | 20 | 28 |

Sono segnalazioni algoritmiche su immagini storiche, **non meteore confermate né conteggi dei file già presenti nella galleria**. A 100 px i metodi condividono 11 fotogrammi; il temporale ne conserva 9 aggiuntivi e ne esclude 65 segnalati dall’attuale. La coincidenza per fotogramma non identifica necessariamente lo stesso oggetto. I 360 conteggi ordinari della precedente prova a blocchi sono stati riprodotti esattamente.

Il contesto dell’intera notte permette di scartare riflessi persistenti e una struttura nuvolosa che nel campione a blocchi era rimasta candidata. Restano tracce compatibili con oggetti in movimento e segnalazioni tratteggiate. Il gate sulle variazioni/nubi esclude 397/2.176 fotogrammi; questo dato non misura la copertura fisica del cielo e non prova che tutti gli eventi esclusi fossero disturbi. La cadenza mediana delle immagini è 62 s, con 38 intervalli oltre 90 s e massimo 141 s: nelle pause un satellite o un aereo può apparire isolato.

Non è disponibile un insieme di meteore confermate indipendentemente con cui misurare sensibilità e perdite. Il calo 76→20 non dimostra da solo una maggiore precisione scientifica. Le immagini sono JPEG già elaborati e non i frame in memoria prima dell’overlay; esposizioni singole, pioggia e traffico storico non sono stati ricostruiti. I risultati dettagliati, i candidati e le schede visive restano nell’archivio privato della valutazione.

## Profilo attivo e percorsi

Il motore è **Meteor Detection temporal v1.0.1**, sorgente [AllskyTeam/allsky-modules](https://github.com/AllskyTeam/allsky-modules/tree/ee0b6567b829e3bf86cd1e2190e4e0c59e5e2b31/allsky_meteordetect), commit `ee0b6567b829e3bf86cd1e2190e4e0c59e5e2b31`. Il file upstream è immutato e verificato con SHA-256 `b6a8993125373aa466257a8831f0fbf683042c170c8d88884a691075cdd83447`.

| Elemento | Configurazione |
|---|---|
| Servizio indipendente | `dsg-meteor-shadow.service`, abilitato all’avvio |
| Codice e profilo sull’impianto | `config/myFiles/meteor-shadow/` sotto Allsky |
| Soglia privata | `min_length=100` px; nessun cambio alla soglia del rilevatore ordinario |
| Maschera privata | Copia fissata della maschera meteore aggiornata, SHA-256 `631fbb2035a829ba9becbed470aa486ff82bfbe08864237dfbf30c66683b6d31` |
| Archivio persistente | `/var/lib/dsg-meteor-shadow/candidates/<notte>/meteors/` |
| Registro e stato operativo | `/var/lib/dsg-meteor-shadow/ledger.sqlite3` e `status.json` |
| Stato temporale in memoria | `/run/dsg-meteor-shadow/` |
| Contatori | Nomi `DSG_SHADOW_*`, soltanto nello stato privato |
| Risorse | Un thread, priorità 15, I/O idle, massimo 50% di un core e 384 MiB |
| Controlli geometrici | Filtri stelle/traiettorie basati su calibrazione fisheye disabilitati; nessuna calibrazione di esempio applicata |
| Pubblicazione | `upload_remote=false`, `save_webui=false`; funzioni di caricamento e copia WebUI bloccate |

I [sorgenti dell’adattatore e della unit](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/main/tools/allsky/meteor-shadow) sono versionati con il manuale. La licenza MIT e la provenienza del modulo upstream sono incluse.

All’avvio il worker usa al massimo gli ultimi due JPEG idonei per inizializzare il confronto. Legge solo immagini con orario entro cinque minuti rispetto al Raspberry, controlla che siano stabili e decodificabili e usa la stessa soglia solare Allsky per la selezione notturna. Non recupera automaticamente l’intero storico dopo una fermata. Un cambio di notte o un intervallo superiore a 180 s azzera lo stato temporale privato. Il registro impedisce di reinserire uno scatto già elaborato; dopo un riavvio è necessario ricostruire il confronto con i nuovi frame.

La conferma è differita al fotogramma successivo, quindi l’archiviazione può ritardare di circa un ciclo di acquisizione. La parola `confirmed` nei risultati del motore indica soltanto il superamento del controllo temporale e non una conferma astronomica. L’eventuale segnale di pioggia non è collegato a questo adattatore: la selezione è basata sui JPEG. Non usare i candidati o il loro numero per decisioni di sicurezza dell’osservatorio.

## Isolamento e conservazione

Il worker importa il motore con un sostituto privato di `allsky_shared`: variabili assenti non ricaricano la configurazione d’ambiente live e non vengono scritti collector o database dell’applicazione. Il servizio ha `PrivateNetwork=yes`, socket limitati ad `AF_UNIX`, filesystem in sola lettura e scritture consentite soltanto alle proprie directory persistenti e temporanee. All’avvio verifica che tre file di produzione non siano apribili in scrittura e che non sia possibile creare un socket IPv4.

Le due directory private sono di proprietà dell’utente del servizio con permessi **0700**; l’utente del server web non può leggere neppure `status.json`. Il sito pubblico non accede a questo archivio. Dal 24 novembre un servizio separato offre alla sola amministrazione autenticata i candidati successivi alla propria attivazione, senza esporre lo storico precedente. Il rilevatore ordinario continua a gestire i propri candidati e contatori con la procedura precedente.

La soglia di conservazione è **2 GiB**, verificata ogni 60 s: se lo spazio privato la supera, l’analisi si mette in pausa senza cancellare candidati. È un controllo applicativo e non una quota rigida del filesystem. Se cambia il checksum della maschera di produzione, il servizio si mette in pausa per evitare di usare silenziosamente una maschera superata. Per riprendere occorre rivedere profilo e copia privata, oppure liberare spazio dopo aver archiviato i risultati. Non viene modificata la configurazione Allsky per risolvere una pausa privata.

## Controllo operativo

Da una sessione autorizzata sul Raspberry:

```bash
systemctl status dsg-meteor-shadow.service --no-pager
cat /var/lib/dsg-meteor-shadow/status.json
journalctl -u dsg-meteor-shadow.service -n 30 --no-pager
```

`waiting-for-night-frame` è normale fra due salvataggi o in orario diurno. Controllare `last_stamp` per l’ultimo JPEG analizzato: `updated` indica soltanto quando è stato scritto lo stato del servizio. `candidate_frames_total` conta i fotogrammi archiviati privatamente, non meteore confermate. Gli stati `paused-mask-changed`, `paused-storage-limit` ed `error` richiedono verifica dell’operatore.

I test del 12 novembre hanno verificato un candidato sintetico archiviato privatamente, sorgenti invariati, idempotenza e riavvio, reset dopo intervallo lungo, blocco di caricamento/WebUI/sottoprocessi e pause per maschera/spazio. Sull’unit reale sono riusciti i tre controlli di scrittura negata, il blocco del socket IPv4 e il diniego di lettura all’utente web. Sono stati elaborati nuovi fotogrammi prima e dopo un riavvio del solo servizio privato. L’acquisizione ordinaria non è stata riavviata e conserva i checksum di settings, flusso notturno, maschera e configurazione/controller della mappa. Il funzionamento immediato non valida ancora la classificazione delle meteore né il riavvio fisico del Raspberry.

## Backup e disattivazione

Snapshot corrente dopo la correzione di avvio del 16 novembre: **15:25:02**, `configuration-backup-20261116-152502`; precedente alla modifica **15:24:06**, `configuration-backup-20261116-152406`. Copie private su Raspberry/PC fuori da Git, solo nuovo export sanificato nel repository. La unit versionata è allineata a quella corretta sul Raspberry: non deve contenere `After=allsky.service`, perché Allsky è a sua volta ordinato dopo `multi-user.target`. Il worker attende autonomamente i nuovi JPEG. Validazione del grafo positiva, riavvio fisico non eseguito.

Backup preliminare **21:53**, `configuration-backup-20261112-215352`; snapshot dopo l’attivazione **22:07**, `configuration-backup-20261112-220710`. [Download sanificato, perimetro e ripristino](allsky-configuration-backup.md). Il privato resta su Raspberry e PC Owner; il repository contiene soltanto l’export sanificato e risultati aggregati. I nuovi candidati non sono inclusi nei file pubblicati.

Lo snapshot di configurazione comprende codice, profilo, maschera e unit. **Non comprende immagini private, registro SQLite o stato in `/var/lib/dsg-meteor-shadow`**: per conservarli fuori dal Raspberry serve una copia privata separata. Il tool di snapshot aggiornato è `config/myFiles/backup/capture-configuration.py`; non esegue il ripristino.

Per annullare l’affiancamento, in manutenzione autorizzata:

```bash
sudo systemctl disable --now dsg-meteor-shadow.service
```

L’archivio privato viene conservato e la pipeline ordinaria continua a funzionare. Non serve ripristinare settings, calibrazione o intero sito per disattivare il servizio. Ogni cambio di soglia/versione, integrazione nella pipeline o abilitazione della pubblicazione richiede una nuova valutazione e autorizzazione dell’Owner.


## Esame privato dei primi sei candidati — 13 novembre 2026

L’Owner ha confermato di continuare l’affiancamento privato dopo l’esame dei sei fotogrammi candidati acquisiti il 13 novembre. Sono stati confrontati originali, coordinate dei segmenti, due immagini precedenti e due successive per candidato (**23 JPEG distinti**) e file/metadati già prodotti dal rilevatore ordinario. Non sono stati rieseguiti i rilevatori nella pipeline. Gli orari della tabella sono locali, Europe/Rome.

| Scatto | Segnalato anche dall’ordinario | Esito dell’esame visivo |
|---|---|---|
| 18:18:45 | No | Traccia sottile reale, isolata nella regione nei frame vicini; origine incerta, satellite o meteora non distinguibili con certezza. |
| 18:20:48 | No | Probabile falso positivo da struttura nuvolosa diffusa alle coordinate selezionate. Un’altra traccia nell’immagine si trova in posizione diversa e non identifica il segmento candidato. |
| 18:34:53 | No | Traccia luminosa vicina al bordo della maschera; plausibilmente collegata alla traccia più a destra nel successivo scatto. |
| 18:35:55 | Sì | Accordo sullo stesso oggetto, con centri distanti circa 5 px. Il quasi allineamento con il candidato precedente dopo 62 s suggerisce un transito artificiale; identità satellite/aereo non dimostrata. |
| 19:11:19 | No | Traccia sottile reale, apparentemente isolata nella regione; classificazione incerta. |
| 19:30:54 | Sì | Accordo sullo stesso oggetto, con centri distanti circa 3 px, vicino al bordo superiore; origine incerta. |

**Due fotogrammi su sei sono condivisi e quattro sono aggiuntivi del temporale. Nessuna meteora è confermata.** Un candidato è probabilmente nuvoloso; due fotogrammi possono appartenere allo stesso passaggio artificiale; tre restano non classificati. Si tratta di valutazioni visive preliminari, non di identificazioni mediante effemeridi. Le diverse lunghezze registrate dai due algoritmi non sono direttamente equivalenti: per lo scatto 18:35:55 sono 244,1 e 314,1 px, per 19:30:54 sono 111,2 e 127,3 px.

Il campione è selezionato fra i candidati del temporale: non comprende tutte le segnalazioni dell’ordinario né una verità di riferimento indipendente, quindi **non misura precisione, sensibilità o superiorità**. La voce `Leonids` nei metadati, con `radiant=null` e senza i filtri geometrici calibrati attivi, non costituisce un’associazione verificata allo sciame.

Il controllo operativo al termine dell’analisi ha trovato entrambi i servizi attivi e `publication_enabled=false`. Configurazione, soglie, maschere e calibrazione restano invariate. Nessuna immagine candidata, ritaglio, miniatura o metadato individuale è aggiunto al repository o alla galleria: qui si pubblica soltanto il resoconto testuale autorizzato. Le prove visive e il confronto dettagliato rimangono nell’archivio privato dell’Owner.

La decisione è **continuare l’affiancamento privato**, raccogliendo altre notti e contesto temporale prima di proporre modifiche o attivazione pubblica. Questa analisi non comporta un nuovo backup di configurazione, perché non modifica l’impianto; a quella data restavano validi gli snapshot del 12 novembre; quelli successivi sono indicati nella sezione backup. L’eventuale aggiornamento di versione o pubblicazione richiede una successiva autorizzazione. La verifica upstream del 13 novembre ha trovato il ramo ufficiale identico al commit v1.0.1 già installato, senza aggiornamenti da applicare.


## Verifica delle notti 16–17 e 17–18 novembre 2026

Riscontro conclusivo **18 novembre 2026, ore 09:07 Europe/Rome**, via SSH in sola lettura. Verificati stato dei servizi, journal dalla riattivazione del 16 novembre, registro SQLite aperto con `mode=ro`, file JPEG salvati e selezione notturna secondo la soglia solare configurata. La copertura indica i JPEG notturni idonei effettivamente salvati, non garantisce assenza di eventi durante l'intervallo fra due scatti.

| Notte locale | JPEG idonei elaborati | Intervallo elaborato | JPEG idonei mancanti | Intervallo massimo fra scatti | Frame esclusi dal gate nuvolosità | Fotogrammi candidati privati / ordinari |
|---|---:|---|---:|---:|---:|---:|
| 16–17 novembre | 756 | 17:22:49–06:34:48 | 0 | 94 s | 27 | 10 / 18 |
| 17–18 novembre | 706 | 17:21:39–06:35:56 | 0 | 171 s | 150 | 0 / 0 |

Gli esclusi dal gate nuvolosità sono compresi nei JPEG elaborati: il motore li ha letti e ha scelto di saltarne il confronto; non sono errori o file mancanti. Nessuno scatto elaborato risulta estraneo alla selezione notturna ricostruita. Entrambi gli intervalli massimi restano sotto la soglia di reset temporale di 180 s.

Al controllo entrambi i servizi risultano **attivi**, con gli stessi PID osservati dopo la riattivazione e `NRestarts=0`. Nel journal esaminato non emergono errori, traceback, arresti forzati o pause applicative. Il registro supera `PRAGMA quick_check` con esito `ok`. Il contatore complessivo privato è passato da 3.342 a 4.048 fotogrammi, coerentemente con i 706 dell'ultima notte. Lo stato è fresco e `waiting-for-night-frame` è normale in orario diurno; l'ultimo JPEG elaborato è quello delle 06:35:56 del 18 novembre. I reset dello stato temporale includono inizializzazione/cambio notte e non vanno confusi con riavvii del processo.

### Confronto privato e limiti

Per la notte 16–17 novembre, i 10 fotogrammi privati e i 18 ordinari condividono **6 fotogrammi**, ma soltanto **5 selezionano la stessa traccia**. Vi sono 4 fotogrammi aggiuntivi privati e 12 esclusivi dell'ordinario. L'esame di originali e immagini vicine dei candidati privati individua **6 fotogrammi con tracce visibili di origine non confermata** e **4 probabili falsi positivi da nuvole o bordi**. Dei quattro aggiuntivi privati, tre sono probabili falsi positivi e uno contiene una traccia reale non classificata.

Nel confronto con i candidati esclusivi dell'ordinario si osservano strutture nuvolose, tracce in movimento fra scatti consecutivi e altre tracce di origine incerta. Questi riscontri non costituiscono una classificazione astronomica indipendente. Alcune tracce segmentate o persistenti possono avere origine artificiale; la cadenza di acquisizione non permette di escludere satelliti o aerei dalle sole immagini vicine. **Nessuna meteora è confermata** e la riduzione del numero di candidati non misura da sola precisione o sensibilità. Nell'ultima notte entrambi gli archivi contengono zero candidati: non vi sono nuovi oggetti da confrontare, e questo non dimostra l'assenza di meteore nel cielo.

### Esito operativo e riservatezza

Il rilevatore ordinario `allsky_meteorarchive.py` resta abilitato; nello stato privato è confermato `publication_enabled=false`, con i controlli di isolamento riusciti e nessun errore corrente. Non emergono anomalie operative che richiedano correzioni. Prosegue l'affiancamento privato; non viene attivato il temporale nella pipeline pubblica.

Il primo tentativo SSH del 18 novembre era scaduto senza risposta; il successivo è riuscito e ha permesso il controllo conclusivo. Il timeout di collegamento non è stato attribuito a un guasto del rilevatore. L'automazione una tantum è stata rimossa dopo il resoconto; il nuovo controllo è stato richiesto dall'Owner.

Questa attività e il relativo aggiornamento documentale **non modificano configurazione Allsky, software, soglie, maschere, calibrazione o servizi** e non richiedono un nuovo snapshot della configurazione. Immagini, ritagli, miniature, coordinate, orari dei singoli candidati e metadati individuali restano privati e non sono aggiunti al repository né alla galleria pubblica. Le sole informazioni pubblicate qui sono risultati aggregati e finestre operative della notte.


## Revisione manuale dei nuovi candidati — 24 novembre 2026

L’Owner ha autorizzato l’integrazione con **nuovi candidati soltanto dopo revisione manuale** e storico privato escluso. Il nuovo servizio `dsg-meteor-review.service` è separato da entrambi i rilevatori: non cambia modulo/versione/soglie, flusso Allsky o `publish=false` dell’adattatore privato.

Il limite iniziale persistente è **24/11/2026 alle 19:19:36 Europe/Rome** (`2026-11-24T18:19:36.165126+00:00`). Un fotogramma deve avere timestamp e file successivi al limite. I **29 fotogrammi storici privati** presenti al collaudo restano esclusi anche se si tenta di richiamarli direttamente. Il limite non viene spostato ai riavvii e un valore diverso dalla copia nello stato privato impedisce l’avvio. Sono ammessi solo percorsi validati sotto l’archivio temporale, senza link simbolici.

### Uso dall’amministrazione

1. Accedere alla normale WebUI locale o tramite VPN.
2. Nella pagina **Meteors**, aprire **Revisione nuovi candidati temporali**; è disponibile anche `/meteor-review.php` nell’amministrazione.
3. Aprire un nuovo fotogramma e controllare l’anteprima. I cerchi sugli estremi delle tracce sono solo privati, non alterano il JPEG pubblicato.
4. Dopo l’esame, selezionare la conferma e **Pubblica candidato esaminato**, oppure **Escludi dalla pubblicazione**. Il rifiuto conserva l’originale privato.

La pubblicazione richiede sessione autenticata, protezione CSRF e coincidenza dell’hash immagine/metadati con l’anteprima esaminata. Se il file cambia, occorre rivederlo. Decisioni ripetute sono idempotenti; una immagine già pubblicata dal rilevatore ordinario non viene sovrascritta. Una diversa decisione dopo approvazione/rifiuto richiede manutenzione esplicita. L’esame autorizza la visibilità, **non conferma scientificamente una meteora**. Il rilevatore ordinario conserva il proprio comportamento e i contatori pubblici attuali; i risultati temporali in attesa non vengono conteggiati nel sito.

Il servizio ascolta soltanto su socket Unix, accessibile soltanto a root e all’utente del server web; richieste dell’utente del worker privato respinte, con rete IP disabilitata e scritture limitate al proprio registro e alla galleria pubblica. La WebUI non riceve accesso filesystem generale allo storico. Richieste senza login e accesso dalla porta pubblica restituiscono **403**; nessuna credenziale viene inclusa nel nuovo componente. [Codice e test](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/main/tools/allsky/meteor-review).

**Collaudo:** dieci test sintetici riusciti: storico e file precedenti esclusi, nessuna pubblicazione da lista/anteprima, approvazione esplicita e ripetibile senza duplicati, rifiuto con conservazione, hash cambiato respinto, immagini ordinarie preservate, percorsi/link simbolici respinti, azione non valida respinta e limite iniziale non retrodatabile al riavvio. Test eseguiti in directory temporanee, mai su candidati reali. Verificati sintassi PHP, socket dall’utente web e diniego per l’utente del worker, accesso autenticato e collegamento dalla pagina Meteors nel browser. Coda vuota al collaudo; **nessun candidato reale approvato o pubblicato durante l’intervento**.

Acquisizione e worker temporale rimangono sugli stessi PID, senza riavvio o modifica di otto hash protetti; il nuovo servizio di revisione è attivo. Il test dopo un riavvio fisico e il percorso umano completo su un nuovo candidato reale restano da osservare: non sono sostituiti dai test sintetici.

Configurazione in `config/myFiles/meteor-review/`, decisioni e limite persistente in `/var/lib/dsg-meteor-review/` (privati), unit systemd dedicata. Il nuovo snapshot comprende configurazione/codice/unit e pagina amministrativa, **non** candidati o registri runtime privati. [Backup e rollback](allsky-configuration-backup.md#seo-e-revisione-manuale-meteore-24-novembre-2026). Per sospendere solo la revisione usare `sudo systemctl disable --now dsg-meteor-review.service`: rilevatore ordinario e worker privato restano attivi. Non abilitare `publish` nel worker e non retrodatare il limite per recuperare lo storico.


## Controllo della notte 24–25 novembre 2026

Controllo programmato eseguito il **25 novembre 2026**, con prima lettura dello stato alle **09:05 Europe/Rome**, esclusivamente in lettura. Allsky, worker temporale e servizio di revisione risultano **attivi**, rispettivamente sui PID 721, 22685 e 31936; `NRestarts=0` per tutti. Il worker conserva `publication_enabled=false`, nessun `last_error` e i controlli di isolamento già previsti (tre scritture alla produzione negate e socket IPv4 negato). Il rilevatore ordinario rimane attivo e invariato.

Il registro privato, aperto in sola lettura e con `PRAGMA quick_check=ok`, contiene **778 fotogrammi** della notte, fra **24/11 alle 17:17:58 e 25/11 alle 06:43:40**, ora locale. **552 fotogrammi** riportano `Cloudy frame skipped`; sono esclusioni del filtro del rilevatore, non errori di esecuzione né una misura fisica della percentuale di cielo coperto. Nessuna riga della notte segnala errori; un solo reset di sequenza è registrato per la notte. Il totale persistente è salito a **9.446 fotogrammi elaborati**. Alle 09:05 lo stato `waiting-for-night-frame` è coerente con la fine del periodo notturno, non prova di inattività.

La API locale di revisione, interrogata come utente del server web con la sola operazione `list`, restituisce il limite persistente autorizzato invariato e **zero nuovi candidati in attesa**. Anche il contatore della notte del worker è zero: **non ci sono anteprime da presentare o candidati da approvare per questa notte**. Eventuali segnalazioni temporanee “pending” durante il confronto non equivalgono a candidati archiviati o meteore confermate. Lo storico precedente resta escluso: i 29 fotogrammi privati preesistenti non sono stati importati nella revisione, mostrati o pubblicati.

Non sono state compiute operazioni di approvazione/rifiuto, copie in galleria, pubblicazioni, riavvii o cambi a codice, configurazione, soglie, maschere, calibrazione o servizi Allsky. Il solo aggiornamento è documentale; non è necessario un nuovo backup della configurazione invariata. Immagini, anteprime, identificativi puntuali, metadati individuali e registri dei candidati non sono aggiunti a Git, allegati o portale.

Il controllo attesta attività e risultati del worker sui fotogrammi registrati; **zero candidati non dimostra assenza di meteore nel cielo**, soprattutto in presenza di numerose esclusioni del filtro. Non viene certificata la sensibilità scientifica del rilevatore. Il percorso umano completo di revisione/pubblicazione di un nuovo candidato reale non è stato esercitato perché la coda è vuota. Non è emersa una correzione da applicare alla configurazione; eventuali future variazioni del filtro richiederanno una valutazione separata e autorizzazione Owner.


## Bonifica reversibile della galleria pubblica del 26 novembre 2026

La bonifica autorizzata riguarda soltanto le copie del rilevatore ordinario già presenti nella galleria pubblica. Le classificazioni di probabile artefatto sono provvisorie: non costituiscono esclusioni scientifiche né esempi etichettati singolarmente dall’Owner.

| Verifica | Esito |
| --- | ---: |
| Immagini pubbliche inventariate | 422 |
| Con metadati storici disponibili | 129 |
| Senza metadati storici disponibili | 293 |
| Immagini trasferite in quarantena privata | 103 |
| File trasferiti, comprese le miniature | 206 |
| Immagini conservate nella galleria | 319 |

Le 319 immagini conservate comprendono 293 casi senza metadati storici e 26 con tracce sottili o valutazione incerta. Gli originali amministrativi delle 103 immagini ritirate restano invariati. Sono rimasti invariati anche gli 11 file protetti di configurazione e codice; acquisizione, calibrazione, soglie e servizi non sono stati modificati o riavviati. Lo storico temporale privato precedente è rimasto escluso e non è stato consultato.

La verifica HTTP ha restituito 200 per la galleria con 319 immagini; le copie quarantinate risultano assenti. Un controllo diretto ha restituito 404 per una copia rimossa e 200 per una conservata. Questi conteggi descrivono l’istante della bonifica: le successive acquisizioni possono incrementare la galleria.

Il backup preventivo dell’intera galleria e i manifesti restano privati sul Raspberry e nell’archivio locale su J:, fuori da Git. Sono stati verificati checksum dell’archivio e hash di tutte le 422 immagini originali. La quarantena è esterna alla radice web, con permessi 0700 sul Raspberry; la copia locale è accessibile al solo account proprietario.

Il report privato successivo comprende soltanto le 319 immagini conservate, con caselle per proporre ulteriori spostamenti. Salvare una selezione non modifica la galleria: un successivo intervento richiede richiesta esplicita e nuova verifica di inventario e hash. Report, selezioni, immagini, anteprime e dettagli individuali non vengono pubblicati nel repository.

La bonifica è una tantum e non introduce filtri nella produzione: il rilevatore ordinario mantiene la pubblicazione automatica esistente. Il controllo delle 08:00 resta in sola lettura e non autorizza quarantene automatiche. Per annullare il trasferimento consultare la [procedura di ripristino della galleria](allsky-configuration-backup.md#ripristino-della-bonifica-della-galleria).


## Selezione manuale e quarantena del 27 novembre 2026

L’Owner ha selezionato 300 delle 319 immagini conservate nel report privato e ha autorizzato il trasferimento delle sole copie pubbliche, senza cancellazione. L’elenco esportato è stato confrontato con l’impronta dell’inventario e con gli identificativi e hash del report prima dell’intervento.

| Verifica | Esito |
| --- | ---: |
| Immagini selezionate manualmente | 300 |
| File trasferiti con le miniature | 600 |
| Immagini pubbliche prima del secondo intervento | 319 |
| Immagini pubbliche dopo il secondo intervento | 19 |
| Immagini complessivamente in quarantena nei due interventi | 403 |
| Copie amministrative esistenti verificate e conservate nel secondo intervento | 23 |
| File protetti di codice e configurazione invariati | 11 |

Per 277 immagini selezionate non era presente una copia amministrativa nel percorso atteso: tutte le 300 immagini a piena risoluzione e le miniature sono state salvate in un nuovo backup privato verificato prima dello spostamento e restano nella quarantena privata. Nessuna immagine è stata cancellata. I file pubblici non selezionati sono stati confrontati con gli hash precedenti e risultano invariati.

I tre servizi Allsky, rilevatore temporale e revisione sono rimasti attivi, con PID e contatori di riavvio invariati. Non sono stati modificati acquisizione, maschere, calibrazione o parametri fotografici; lo storico temporale privato escluso non è stato consultato. Il controllo HTTP di un’immagine e della miniatura ritirate restituisce 404; una conservata restituisce 200. I conteggi restano riferiti all’istante dell’intervento.

Il report privato è stato aggiornato alle sole 19 immagini rimaste e il registro delle quarantene comprende la selezione Owner. La selezione manuale autorizza la segregazione, non costituisce conferma scientifica di artefatti né etichetta automatica di addestramento.

Il controllo quotidiano delle **08:00 Europe/Rome** produce sempre un report privato con caselle, contatore, filtri, ingrandimento e salvataggio dell’elenco su J:, in una sottocartella giornaliera senza sovrascrivere le selezioni precedenti. Un report vuoto distingue l’assenza di nuovi risultati dall’impossibilità di effettuare il controllo. Le immagini già quarantinate e lo storico temporale escluso non sono inclusi; i risultati ordinari e temporali restano distinti. Le caselle esportano proposte e non eseguono spostamenti o pubblicazioni. Ogni successiva operazione richiede richiesta esplicita e nuove verifiche.

Immagini, anteprime, selezioni, nomi e hash individuali rimangono privati. Nel repository sono pubblicati soltanto questi dati aggregati e la [procedura di ripristino](allsky-configuration-backup.md#ripristino-della-selezione-manuale-del-27-novembre-2026).
