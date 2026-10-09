# Allsky: pannelli informativi esterni alla ripresa

Baseline operativa verificata il **09/10/2026**, in Europe/Rome. Riferimento: [Capitolo 27 — Sistema Allsky](../chapters/27-sistema-allsky.md#2726-pannelli-informativi-esterni-alla-ripresa).

## Disposizione e contenuto

| Posizione | Contenuto |
|---|---|
| Alto sinistra, fuori dalla foto | **La notte a Manciano**: fase del cielo, altezza Sole/Luna, prossima alba in ora locale |
| Basso sinistra, fuori dalla foto | **Acquisizione**: timestamp dello scatto, esposizione, guadagno, temperatura del sensore, percentuale illuminata della Luna |
| Alto destra, fuori dalla foto | **Meteo locale · CloudWatcher**: temperatura ambiente, umidità, punto di rugiada e ora della misura |
| Destra, sotto il meteo | **Cielo ed eventi**: stelle rilevate, fotogrammi/tracce candidate della notte, prossimo passaggio ISS previsto e Aircraft nell’area di Manciano |
| Fascia inferiore, fuori dalla foto | **Raspberry Pi**: temperatura CPU, RAM usata, disco libero e uptime |
| Dentro il fotogramma, basso sinistra | Soltanto logo Digital Stargate e scritta ridotti |

La mappa delle costellazioni resta sovrapposta alla fotografia, limitata al suo rettangolo. La geometria viene ricavata dalle dimensioni visualizzate e dalla calibrazione stellare precedente; i pannelli non introducono una nuova calibrazione ottica. I comandi delle gallerie e della mappa sono disposti in una barra orizzontale sopra il riquadro.

Il JPEG pubblico, gli archivi e le anteprime Home/Status ricevono il solo logo/scritta; i pannelli sono componenti della pagina Allsky e non vengono impressi nelle nuove immagini. Le fotografie storiche conservano le sovraimpressioni presenti al momento della loro acquisizione.

## Sorgenti e significato dei valori

| Dato | Sorgente e limite |
|---|---|
| Acquisizione | `tmp/extra/allsky_camera.json`; timestamp ricavato dal nome del fotogramma e esposizione `AS_EXPOSURE_S`. Gli aggiornamenti del pannello e del JPEG hanno cicli distinti: controllare l’ora dello scatto visualizzata. |
| Luna, Sole e ISS | Modulo `allsky_solarsystem` nella pipeline periodica. Sole, Luna e ISS abilitati; passaggi ISS visibili previsti su cinque giorni. È una previsione orbitale, non un rilevamento fotografico. |
| Prossima alba | Astral nell’ambiente virtuale Allsky, posizione configurata sul Raspberry ed elevazione 100 m; selezione dell’alba futura e conversione Europe/Rome, anche dopo mezzanotte e nelle ore diurne. |
| Meteo locale | CloudWatcher locale tramite CSV su EAGLE e proiezione Observatory Status già esistente. Allsky legge dal relay i soli campi richiesti; non collega direttamente la porta seriale o modifica il dispositivo. |
| Raspberry | Modulo `allsky_pistatus`; dati periodici ogni 60 secondi. Spazio libero espresso in GB decimali. |
| Stelle | Modulo nativo `allsky_starcount`, notturno, metodo Fast, scala 0,5, dimensione minima 6. Conteggio riferito alla porzione di cielo inclusa nella maschera, non a tutto il cielo. |
| Candidati meteore | File `meteors-*.json` nell’archivio locale della notte corrente. Mostra separatamente fotogrammi e tracce; più tracce possono appartenere a un fotogramma. Nessuna conferma automatica. |
| Aircraft | API pubblica [adsb.fi](https://adsb.fi/), area centrata sulla posizione approssimata di Manciano, raggio 27 NM (circa 50 km). Conta mezzi in volo con posizione recente ed espone un identificativo di volo disponibile. Non prova che l’aereo sia visibile nella foto; copertura ADS-B/MLAT incompleta. |

Il CloudWatcher locale resta distinto dalla sorgente SOLO già documentata per SQM. Questa integrazione non pubblica SQM, pressione, velocità del vento o quantità di pioggia non validate nel flusso corrente. La temperatura ambiente è distinta da quelle del sensore fotografico e della CPU.

Le soglie descrittive dell’altezza del Sole sono: giorno ≥0°, crepuscolo civile da −6° a 0°, nautico da −12° a −6°, astronomico da −18° a −12°, notte astronomica sotto −18°. Non modificano la soglia di acquisizione Allsky né costituiscono un criterio di apertura della cupola.

La maschera `config/overlay/images/star-digital-stargate-mask.png` deriva dalla maschera meteore: binarizzazione e ulteriore erosione ellittica di 51 pixel escludono apparati e bordi artificiali. Le immagini restano inalterate e senza cerchi sulle stelle. Luna, riflessi, nuvole ed esposizione influenzano il conteggio; non usarlo come misura calibrata di trasparenza o copertura nuvolosa. Il confronto fra notti richiede condizioni e parametri confrontabili.

L’accesso Aircraft usa la versione v3 documentata, senza credenziali o nuove sottoscrizioni. È una sorgente per uso personale non commerciale; il pannello include il collegamento e l’attribuzione richiesti. [Condizioni e limiti del servizio](https://github.com/adsbfi/opendata/blob/main/README.md). Airplanes.live ha restituito 403 nel tentativo di verifica; non è la sorgente attiva. Sul Raspberry non sono risultati attivi `dump1090` o `readsb`; nessun nuovo ricevitore è stato installato.

## Componenti, frequenza e scadenza

Percorsi relativi a `/home/pi/allsky`, salvo quelli assoluti:

| Componente | Funzione |
|---|---|
| `config/myFiles/live-panels/dsg-live-telemetry.py` | Lettura delle sorgenti e pubblicazione atomica dei soli dati selezionati |
| `html/allsky/dsg-live-data.json` | Proiezione pubblica consumata dal browser; senza credenziali, coordinate precise, seriali o configurazioni complete |
| `html/allsky/js/dsg-live-panels.js` | Aggiornamento del testo dei pannelli, tramite `textContent` |
| `html/allsky/css/dsg-live-panels.css` | Colonne esterne e fascia Raspberry; regole per impilare i pannelli sugli schermi piccoli |
| `html/allsky/index.php` | Struttura dei pannelli e inclusione dei file CSS/JS |
| `html/allsky/js/controller.js` | Mappa confinata al rettangolo della fotografia |
| `/etc/systemd/system/dsg-live-telemetry.service` | Servizio oneshot come utente `pi`, Python dell’ambiente virtuale Allsky; timeout 25 secondi |
| `/etc/systemd/system/dsg-live-telemetry.timer` | Aggiornamento ogni 30 secondi, avvio automatico dopo il boot |
| `/etc/lighttpd/conf-enabled/98-allsky-public-https.conf` | Eccezione pubblica per il solo `/allsky/dsg-live-data.json`; amministrazione e file riservati esclusi |

Il browser interroga la proiezione ogni 15 secondi. Il timer esegue le richieste esterne ogni 30 secondi, indipendentemente dal numero di visitatori; i timeout delle letture HTTP sono di 8 secondi. Il limite pubblico adsb.fi è una richiesta al secondo: la configurazione resta ampiamente al di sotto di tale limite.

Una proiezione complessiva vecchia di oltre 150 secondi produce “Non disponibile”. Camera, Raspberry e stelle sono accettati entro 180 secondi; stelle solo quando il fotogramma di riferimento corrisponde a quello della camera. Le effemeridi periodiche hanno una finestra di 600 secondi. Il meteo richiede qualità `CURRENT`, timestamp non futuro oltre la tolleranza di 30 secondi e scadenza `fresh_until_utc` ancora valida. Il browser ricontrolla tale scadenza. La lettura normalizza le frazioni di secondo prodotte da EAGLE per compatibilità con Python 3.9.

Aircraft richiede una risposta API recente entro 120 secondi e posizioni aggiornate entro 60 secondi. Errori delle sorgenti esterne mostrano indisponibilità, senza riutilizzare misure vecchie come se fossero attuali. Un guasto al collector non interrompe l’acquisizione Allsky.

## Verifica e manutenzione

Controlli effettuati il 09/10/2026: sintassi PHP valida; modulo Sole/Luna/ISS eseguito con esito `OK`; conteggi stelle reali nel log Allsky; dati CloudWatcher recenti; risposta adsb.fi dal Raspberry; servizio e timer operativi; valori presenti nei pannelli pubblici e logo ridotto nella foto. In quel momento il modulo ISS non prevedeva passaggi visibili nei cinque giorni successivi: è un risultato temporaneo, non uno stato fisso.

La verifica visiva è stata svolta nel browser interno desktop, con controllo della separazione dei pannelli dalla ripresa. La prova del viewport mobile non ha modificato le dimensioni effettive della superficie: il collaudo su un telefono reale resta aperto. Non sono stati attesi il cambio di giorno/notte, la prossima alba o un passaggio ISS, né è stata validata l’accuratezza dei conteggi rispetto a una classificazione manuale.

```sh
systemctl is-active dsg-live-telemetry.timer
systemctl status dsg-live-telemetry.service
journalctl -u dsg-live-telemetry.service -n 20 --no-pager
/home/pi/allsky/venv/bin/python /home/pi/allsky/config/myFiles/live-panels/dsg-live-telemetry.py
php -l /home/pi/allsky/html/allsky/index.php
```

Un servizio oneshot può essere `inactive` dopo l’esecuzione riuscita: verificare il risultato dell’ultima esecuzione e che il timer sia attivo. Se il meteo è indisponibile, controllare freschezza della proiezione CloudWatcher/EAGLE prima di attribuire il problema al sensore. Se tutte le voci sono indisponibili, controllare collector, età del JSON e accessibilità HTTP. Dopo modifiche al controller o al CSS/JS, aggiornare il riferimento di versione nella pagina e ricaricare il browser.

La WebUI amministrativa e `myFiles/footer.php` sono stati verificati con risposta pubblica 403 dopo l’aggiunta dell’eccezione JSON. Conservare tale separazione nelle successive modifiche.

## Backup e ripristino

Backup sul Raspberry, fuori dalla directory pubblica:

- `/home/pi/allsky-private-archive/live-panels-20261009-220648`: configurazioni notturna/periodica, overlay, pagina, controller e configurazione HTTPS precedenti ai pannelli;
- `/home/pi/allsky-private-archive/night-panel-20261009-221623`: pagina, CSS/JS, collector e configurazione periodica prima di “La notte a Manciano”.

Per annullare solo il riquadro astronomico ripristinare il secondo gruppo, incluso il precedente collector, e ripristinare l’interprete del servizio solo se necessario. Per annullare tutti i pannelli: disabilitare il timer, ripristinare il primo gruppo e la precedente eccezione HTTPS; validare PHP/lighttpd prima del reload. Conservare i file nuovi finché il ripristino non è verificato. Non cancellare archivi di immagini o candidati.

I sorgenti installati dei pannelli sono conservati anche in `config/myFiles/live-panels`; questa guida ne descrive la baseline ma non sostituisce un backup completo del Raspberry. Le configurazioni e i dati di accesso riservati non devono essere copiati nel repository pubblico.

L’integrazione è informativa e in sola lettura: nessun comando a EAGLE, CloudWatcher, cupola, montatura o router e nessuna modifica alla Safety Authority. Non sono stati aggiunti asset hardware o cambiati i contratti Observatory Status esistenti.
