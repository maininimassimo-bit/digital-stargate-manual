---
title: Allsky rilevatore temporale privato
description: Affiancamento asincrono del rilevatore temporale di meteore, con archivio privato e rilevatore ordinario invariato.
---

# Affiancamento privato del rilevatore meteore

Dal **12 novembre 2026 alle 22:03 Europe/Rome** il servizio `dsg-meteor-shadow.service` analizza le nuove immagini notturne già salvate da Allsky. L’Owner ha autorizzato l’affiancamento dopo la valutazione su tre notti complete. Il rilevatore ordinario rimane nel flusso esistente; **i nuovi candidati temporali non vengono pubblicati** né nella galleria pubblica né nella pagina amministrativa Meteors.

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

Le due directory private sono di proprietà dell’utente del servizio con permessi **0700**; l’utente del server web non può leggere neppure `status.json`. Non esiste un collegamento dal sito a questo archivio. Il rilevatore ordinario continua a gestire i propri candidati e contatori con la procedura precedente.

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

La decisione è **continuare l’affiancamento privato**, raccogliendo altre notti e contesto temporale prima di proporre modifiche o attivazione pubblica. Questa analisi non comporta un nuovo backup di configurazione, perché non modifica l’impianto; restano validi gli snapshot del 12 novembre descritti sotto. L’eventuale aggiornamento di versione o pubblicazione richiede una successiva autorizzazione. La verifica upstream del 13 novembre ha trovato il ramo ufficiale identico al commit v1.0.1 già installato, senza aggiornamenti da applicare.
