# Capitolo 27 – Sistema AllSky

**Codice documento:** DSG-TM-001-27  
**Revisione:** 1.6 — affiancamento privato del rilevatore temporale, 12/11/2026
**Stato:** acquisizione, sito locale e HTTPS pubblico operativi; limiti della mappa e collaudi residui espliciti

## 27.1 Scopo

Il sistema AllSky fornisce una vista continua del cielo e dell'ambiente circostante, supportando il controllo operativo, la verifica della copertura nuvolosa, la documentazione delle sessioni e l'analisi di eventi astronomici o meteorologici.

Il sistema non sostituisce i sensori di sicurezza certificati o dedicati, ma costituisce una fonte indipendente di supervisione visiva.

## 27.2 Configurazione nota

| Componente | Configurazione |
|---|---|
| computer | Raspberry Pi 4 Model B Rev 1.2, RAM 4 GB |
| camera | ZWO ASI290MC |
| ottica | fisheye 1,8 mm, confermata fisicamente dall'Owner il 09/10/2026 |
| copertura | cupola trasparente protettiva |
| rete | LAN/Wi-Fi dell'osservatorio |
| funzione | immagini, monitoraggio e timelapse |
| sistema operativo | Raspberry Pi OS / Raspbian 11 Bullseye, userland armhf e kernel aarch64 |
| software | AllskyTeam/allsky v2026.10.01_01, aggiornato il 12/11/2026; commit `f1406ea78ba969313abd1ddd14a4272967081a06` |
| fotogramma | 1936 × 1096 pixel |
| directory applicazione | `/home/pi/allsky` |
| sito locale | `/home/pi/allsky/html/allsky`, pagina `/allsky/index.php` |

La baseline hardware deriva dalla verifica del 09/10/2026; la versione software e la conservazione delle personalizzazioni sono state verificate dopo l’aggiornamento del 12/11/2026 (§27.35). Indirizzi LAN, coordinate precise, seriali, credenziali e chiavi private restano nella documentazione operativa riservata e non sono pubblicati nel manuale.

## 27.3 Architettura funzionale

```text
CIELO
  |
OTTICA FISHEYE
  |
ASI290MC
  |
RASPBERRY / SOFTWARE ALLSKY
  |------ immagini correnti
  |------ archivio notturno
  |------ timelapse
  |------ interfaccia web
  |
RETE DIGITAL STARGATE
```

## 27.4 Funzioni operative

- verifica visiva della copertura nuvolosa;
- controllo del cielo prima dell'apertura;
- conferma di eventi meteo o anomalie;
- osservazione della Via Lattea e del transito di nubi;
- produzione di timelapse;
- supporto alla diagnosi di cali di qualità nelle immagini;
- documentazione di meteore, satelliti e fenomeni luminosi.

## 27.5 Procedura DSG-PROC-027-01 – Controllo pre-sessione

1. Verificare la raggiungibilità dell'interfaccia AllSky.
2. Controllare che l'immagine corrente sia recente.
3. Verificare la pulizia apparente della cupola protettiva.
4. Controllare la presenza di condensa o gocce.
5. Valutare visivamente nuvole e trasparenza.
6. Confrontare il risultato con i dati meteo.
7. Registrare eventuali incongruenze.

## 27.6 Acquisizione e archiviazione

Le immagini devono essere organizzate per data osservativa, preferibilmente con struttura:

```text
allsky/
  YYYY/
    YYYY-MM-DD/
      images/
      keograms/
      startrails/
      timelapse/
      logs/
```

La politica di conservazione deve distinguere:

- immagini operative a breve termine;
- timelapse selezionati;
- eventi significativi;
- materiale destinato a divulgazione o analisi.

## 27.7 Riscaldamento anticondensa

Per un sistema con copertura emisferica, il riscaldamento deve:

- ridurre la formazione di condensa;
- non produrre gradienti termici eccessivi;
- essere protetto elettricamente;
- essere controllato in funzione delle condizioni ambientali, se possibile.

> **DA VALIDARE:** presenza, potenza e logica di controllo del riscaldatore.

## 27.8 Manutenzione

### Settimanale

- verificare immagine corrente e timestamp;
- controllare spazio disco;
- verificare generazione del timelapse.

### Mensile

- pulire la cupola protettiva con materiali idonei;
- controllare cavi e alimentazione;
- verificare messa a fuoco e orientamento;
- controllare log e riavvii.

### Semestrale

- ispezionare guarnizioni e contenitore;
- verificare il sistema anticondensa;
- eseguire backup della configurazione.

## 27.9 Troubleshooting

| Sintomo | Possibile causa | Azione |
|---|---|---|
| immagine nera | esposizione, camera o alimentazione | verificare driver e USB |
| immagine non aggiornata | processo bloccato o rete | riavviare servizio e verificare LAN |
| condensa | riscaldatore assente o insufficiente | verificare alimentazione e soglie |
| stelle non a fuoco | ottica spostata | rifocalizzare e bloccare la ghiera |
| timelapse mancante | job di elaborazione fallito | controllare log e spazio disco |
| aloni o macchie | cupola sporca o bagnata | pulizia controllata |

## 27.10 Sicurezza informatica

- mantenere l'interfaccia amministrativa WebUI, SSH, log e configurazioni riservate accessibili soltanto tramite LAN o VPN;
- predisporre l'accesso Internet alla sola pagina pubblica e ai media Allsky tramite HTTPS, con regole dedicate e verifica degli URL consentiti;
- sostituire le credenziali predefinite;
- aggiornare il sistema operativo in finestre controllate;
- mantenere una copia della configurazione e della scheda di memoria.

## 27.11 KPI

| KPI | Descrizione |
|---|---|
| disponibilità AllSky | percentuale di immagini attese prodotte |
| gap di acquisizione | intervalli senza immagini |
| timelapse completati | percentuale per notte |
| eventi di condensa | numero per mese |
| spazio archivio utilizzato | trend mensile |

## 27.12 Dati da validare

Verificata nella configurazione: conservazione immagini originali per 14 giorni e archivi del sito locale senza scadenza automatica (`keeplocalwebsitedays=0`). Frequenza/esposizioni operative e dimensionamento disco nel tempo restano da validare.

> **DA VALIDARE:** adeguatezza della retention e ripristino completo da backup; riscaldatore, alimentatore e supporto di storage non sono stati censiti fisicamente nella sessione.

## 27.13 Aggiornamento e ripristino — 9 ottobre 2026

L'installazione precedente v2023 è stata aggiornata alla release v2026.10.01 del progetto [AllskyTeam/allsky](https://github.com/AllskyTeam/allsky). Le copie di ripristino sono in `/home/pi/allsky-backup-20261009` e `/home/pi/allsky-OLD`.

Durante l'aggiornamento è stata corretta una sovrapposizione di installazioni NumPy incompatibili. L'ambiente risultante usa NumPy 1.24.4; sono state verificate le importazioni di SciPy 1.8.1, OpenCV 4.6.0 e Astropy 6.0.1. Un aggiornamento successivo deve ricontrollare le dipendenze e la produzione di una nuova immagine prima di essere considerato operativo.

Il ripristino va eseguito in una finestra di manutenzione: conservare prima la configurazione corrente e i media nuovi, confrontare i backup, fermare l'acquisizione, ripristinare una configurazione coerente con la versione scelta e verificare camera, timestamp, overlay e sito locale. Il ripristino completo non è stato collaudato nella sessione.

## 27.14 Personalizzazione della ripresa e del sito

- Nel fotogramma rimangono soltanto logo e scritta Digital Stargate ridotti, in basso a sinistra. Le precedenti scritte di acquisizione e Raspberry sono state trasferite nei pannelli del sito, fuori dalla ripresa (§27.26).
- A sinistra: “La notte a Manciano” in alto e acquisizione in basso. A destra: meteo CloudWatcher e cielo/eventi. Temperatura CPU Raspberry, utilizzo RAM, spazio libero e uptime occupano una fascia inferiore separata.
- Overlay personalizzato in `config/overlay/config/overlay-Digital-Stargate.json`; moduli `allsky_pistatus` e `allsky_solarsystem` con aggiornamento periodico ogni 60 secondi. Elevazione impostata a 100 m s.l.m. su indicazione Owner.
- Fotogramma completo mantenendo il rapporto d'aspetto, bordi neri laterali e superiori/inferiori; mappa celeste dimensionata sul cerchio della ripresa e ricollocata secondo i limiti reali dell'immagine visualizzata.
- Orologio della mappa aggiornato al timestamp del fotogramma tramite `Last-Modified`; la regolazione iniziale sul Sole è stata sostituita da una calibrazione sulle stelle, con riscontro su un secondo fotogramma (§27.20). Overlay automatico notturno, pianeti e nomi abilitati (§27.21).
- Sfondo scuro con dettagli stellari e Via Lattea semitrasparente; immagine `digital-stargate-via-lattea.png`, opacità finale 0,23.

File interessati: `allsky.css`, `controller.js`, `configuration.json` e `index.php` nel sito Allsky. Le personalizzazioni vanno confrontate con i nuovi file upstream a ogni aggiornamento.

## 27.15 Accesso pubblico — verifiche concluse e limiti

Il sito pubblico è operativo all’indirizzo [Digital Stargate Allsky](https://digitalstargate.freeddns.it:23232/allsky/). Starlink residenziale resta su IP condiviso; l’ingresso IPStatico PRO condiviso avviene tramite client OpenVPN sul Teltonika. Il visitatore non necessita di VPN.

Il 09/10/2026 sono stati verificati tunnel, inoltro TCP sulla porta assegnata 23232, homepage, immagine corrente e gallerie dall’esterno. La configurazione HTTPS dedicata esclude WebUI amministrativa, comandi, overlay riservati e log (risposte 403 sui percorsi provati); amministrazione locale preservata. Chiavi private e profili VPN completi sono custoditi fuori dal repository.

RapidSSL è stato emesso e installato: hostname, corrispondenza con la chiave e catena verificati. Scadenza effettiva **25/04/2027 23:59:59 UTC**, distinta dalla durata commerciale annuale del servizio. Il controllo periodico dell’emissione è stato disattivato dopo la conferma.

Il piano condiviso assegna le porte 23232–23263 e non include 443. L’Owner ha scelto di mantenere il servizio attuale, senza attivare un IP dedicato. Configurazione failover verificata nel [Capitolo 5](05-infrastruttura-rete.md); commutazione fisica e continuità del sito durante il cambio WAN ancora da provare sul posto.

## 27.16 Allsky Map

Registrazione aggiornata il 09/10/2026 con lo script ufficiale `postToMap.sh`; risposta del servizio di aggiornamento confermata e segnaposto **Astrocampo Manciano / Observatory Digital Stargate** osservato sulla [mappa pubblica](https://www.thomasjacquin.com/allsky-map/). Camera ASI290MC, lente 1,8 mm e Raspberry Pi 4 riconciliati con l’inventario. URL del sito e dell’immagine corrente configurati con HTTPS e porta 23232.

**Limite aperto:** il server della mappa restituisce connessione rifiutata verso l’immagine sulla porta 23232, mentre il download diretto funziona e una prova del proxy verso un’immagine HTTPS su 443 riesce. Restrizione delle connessioni in uscita del server della mappa come causa probabile, non verificata accedendo al suo firewall. Segnaposto e link restano disponibili; anteprima immagine non disponibile. Nessun passaggio alla porta 443 acquistato o configurato.

## 27.17 Registro revisioni

| Revisione | Data | Modifica |
|---|---|---|
| 0.1 | Baseline precedente | Prima descrizione del sistema e dati da validare |
| 0.2 | 09/10/2026 | Hardware verificato e ottica confermata Owner; aggiornamento software, overlay, sito, backup e pubblicazione in preparazione |
| 0.3 | 09/10/2026 | Retention verificata; tunnel, certificato e HTTPS pubblici collaudati; mappa aggiornata con anteprima non disponibile, residui fisici conservati |
| 0.4 | 09/10/2026 | Documentate anteprime Home/Status, allineamento ai badge, refresh e modalità essenziale; nessuna variazione hardware |
| 0.5 | 09/10/2026 | Integrati progetto tecnico, NTP, calibrazione stellare, overlay notturno e pianeti, archivio meteore, verifiche e procedure di ripristino |
| 0.6 | 09/10/2026 | Nomi delle stelle e radianti indicativi; pagina divulgativa Allsky, metadati SEO, sitemap, robots.txt e gestione Search Console |
| 0.7 | 09/10/2026 | Pannelli fuori dalla ripresa; CloudWatcher locale, stelle rilevate, candidati della notte, previsioni ISS, Aircraft adsb.fi e informazioni Sole/Luna/alba |
| 0.8 | 10/10/2026 | Backup configurazione privato, copia pubblica sanificata, manifest SHA-256 e procedura di ripristino controllato |
| 0.9 | 11/10/2026 | Ripristino soglia startrail 0,30, blocco trascinamento overlay, 110 anteprime Messier DSS2 e nuovo snapshot verificato |
| 1.0 | 27/10/2026 | Analisi log e risorse, retry immagine live, prova telemetria annullata e correlazione reset USB/esposizioni; configurazione fotografica confermata |
| 1.1 | 27/10/2026 | Snapshot aggiornato delle 08:01, backup privato 355 file e pubblico 140 file, hardlink settings preservato, checksum e guida aggiornati |
| 1.2 | 31/10/2026 | Camera spostata circa 14:30: nuova geometria overlay, verifica su secondo fotogramma e snapshot 18:21 separato privato/pubblico |
| 1.3 | 31/10/2026 | Vento dal relay diagnostico CloudWatcher, unità km/h confermata, controlli validità/freschezza e nuovo snapshot 18:50 |

Inventario correlato: [Capitolo 22](22-inventario-asset-management.md).

## 27.18 Anteprime nel portale Digital StarGate

La [Home del portale](../index.md) mostra l’immagine live Allsky nella hero originale. La pagina [Stato osservatorio](../status/index.md) affianca ai badge operativi due riquadri di uguale larghezza: cupola sopra e anteprima Allsky sotto, con bordi superiore e inferiore allineati al gruppo badge. Sugli schermi piccoli i riquadri si dispongono sotto i badge.

L’anteprima usa il JPEG pubblico HTTPS, contiene l’intero fotogramma senza ritagli e richiede una nuova immagine ogni 30 secondi. Il tasto **Allsky** apre il sito completo. **Vista essenziale** sospende gli aggiornamenti e **Attiva il live** li riprende; la preferenza è condivisa con i controlli visuali del portale. L’ora di ultima ricezione è distinta dall’ora di acquisizione mostrata nel fotogramma. Collegamento indisponibile e riprova sono segnalati esplicitamente.

Si tratta di un’anteprima fotografica aggiornata, non di uno stream video continuo o di una fonte Safety Authority. Non modifica l’acquisizione sul Raspberry Pi, le immagini archiviate o i contratti di telemetria. [Dettagli tecnici e manutenzione](../ui/immersive-portal-implementation.md#anteprime-allsky-nella-home-e-in-observatory-status-9-ottobre-2026); [PR e verifiche di pubblicazione](../releases/immersive-portal.md#incremento-anteprime-live-allsky-home-e-status-09102026).

## 27.19 Progetto tecnico: componenti e flussi

Il progetto comprende acquisizione Allsky sul Raspberry, personalizzazioni della ripresa, sito pubblico, mappa VirtualSky, ricerca di tracce candidate e anteprime nel portale. La WebUI amministrativa resta distinta dal sito divulgativo. L’inventario hardware verificato è quello del §27.2 e del Capitolo 22; questa revisione non aggiunge apparati né risolve i censimenti fisici ancora aperti.

| Flusso | Implementazione e destinazione |
|---|---|
| Acquisizione | Servizio `allsky`, camera USB ASI290MC, fotogramma 1936 × 1096 |
| Immagine corrente | `/home/pi/allsky/tmp/current_images/image.jpg`; URL pubblico `/current/image.jpg` |
| Originali osservativi | `/home/pi/allsky/images/<data>/image-<YYYYMMDDhhmmss>.jpg`; retention configurata `daystokeep=14` |
| Elaborazione notturna | Pipeline `config/modules/postprocessing_night.json`, con archivio meteore personalizzato |
| Sito | `/home/pi/allsky/html/allsky`; homepage, timelapse, keogrammi, startrail e galleria meteore |
| Mappa celeste | `virtualsky/virtualsky.js` e `js/controller.js`, disegnata nel browser sopra il JPEG |
| Distribuzione Internet | HTTPS pubblico sulla porta 23232 attraverso tunnel e inoltro dedicati (§27.15) |
| Portale | Home e Status consumano il JPEG pubblico; non inviano comandi al Raspberry (§27.18) |

La struttura per anno e sessione descritta nel §27.6 è un criterio organizzativo generale; i percorsi della tabella rappresentano l’installazione corrente. Il fotogramma non è un video continuo: sito Allsky e anteprima del portale hanno cicli di aggiornamento distinti. La mappa è una superficie del sito Allsky e non viene incorporata nel JPEG mostrato nell’anteprima del portale.

### File di configurazione e responsabilità

Percorsi relativi a `/home/pi/allsky`, salvo diversa indicazione:

| File | Responsabilità |
|---|---|
| `config/settings.json` | Camera, acquisizione e conservazione degli originali |
| `config/overlay/config/overlay-Digital-Stargate.json` | Solo logo e scritta ridotti impressi nel fotogramma; dati testuali nei pannelli web |
| `html/allsky/configuration.json` | Opzioni sito, mappa, calibrazione, pianeti e default notturno |
| `html/allsky/data.json` | Orari di alba/tramonto e stato dell’acquisizione diurna/notturna |
| `html/allsky/js/controller.js` | Caricamento immagini, clock del fotogramma, geometria e default della mappa |
| `html/allsky/virtualsky/virtualsky.js` | Proiezione celeste e correzione dell’inclinazione della camera |
| `config/myFiles/modules/allsky_meteorarchive.py` | Rilevazione e archiviazione automatica dei candidati |
| `config/modules/postprocessing_night.json` | Archivio meteore e conteggio stelle prima dell’overlay e del salvataggio |
| `/etc/systemd/timesyncd.conf` | Impostazioni di sincronizzazione dell’orologio di sistema |

Le configurazioni complete possono contenere informazioni riservate: conservarle nel backup operativo protetto. Il repository pubblica descrizione e parametri tecnici selezionati, non copie integrali delle configurazioni, chiavi o profili di accesso.

## 27.20 Calibrazione stellare della mappa

### Metodo e risultati del 09/10/2026

La correzione iniziale sul Sole non era sufficiente a registrare tutta la mappa sul cielo fotografato. È stato analizzato un fotogramma delle **19:56:41 Europe/Rome** con il riconoscimento stellare [tetra3 dell’ESA](https://github.com/esa/tetra3), usando una porzione di cielo libera da ostacoli. Il solver ha identificato 15 stelle; le coordinate di catalogo sono state proiettate attraverso la stessa geometria fisheye e correzione d’inclinazione usate da VirtualSky. L’adattamento ha stimato centro, raggio, orientamento e inclinazione della camera.

| Riscontro | Risultato sul fotogramma originale |
|---|---|
| Prima della correzione, 15 stelle identificate | Errore RMS 133,91 pixel |
| Adattamento sulle stesse 15 stelle | Errore RMS 0,47 pixel |
| Verifica successiva alle 20:08:55, 18 stelle | Errore RMS 1,28 pixel; massimo 4,67 pixel |
| Stelle aggiuntive fuori dalla porzione iniziale | Altair, Albireo e Sadr incluse nella verifica successiva |

La misura sulle 15 stelle è un risultato di adattamento, non una verifica indipendente. Il secondo fotogramma verifica l’evoluzione temporale senza ricalibrazione; tre stelle aggiuntive ampliano il riscontro spaziale. Non certifica l’accuratezza su tutto l’orizzonte, nelle zone coperte dagli apparati o durante nuvole e riflessi. La mappa resta divulgativa e non è un sistema di puntamento scientifico.

### Parametri installati

Valori arrotondati in questa tabella; il file operativo conserva la precisione del calcolo. Centro e raggio sono espressi nei pixel del fotogramma di riferimento; gli angoli seguono le convenzioni interne di VirtualSky.

| Proprietà | Valore |
|---|---|
| `overlayCalibration.referenceWidth` / `referenceHeight` | 1936 / 1096 |
| `overlayCalibration.centerX` / `centerY` | 1081,686 / 500,829 |
| `overlayCalibration.horizonRadius` | 764,867 |
| `az` | 183,918° |
| `overlayLean` | 5,371° |
| `overlayLeanAz` | 283,487° |
| `overlayCalibration.calibratedAt` | `2026-10-09T17:56:41Z` |

Il controller ridimensiona il diametro della mappa e ricolloca il centro usando il rapporto fra immagine visualizzata e riferimento; la bordatura nera non cambia la calibrazione. `overlayCalibration` prevale sul precedente adattamento del cerchio a una percentuale della larghezza. La geometria viene ricalcolata al caricamento delle immagini e al ridimensionamento della finestra.

### Orologio del fotogramma

Per ogni immagine corrente il controller legge `Last-Modified` con una richiesta HEAD e passa la data a `setClock(..., "camera-frame")`. Immagine e mappa espongono lo stesso `data-frame-time`; il controllo della sequenza evita che una risposta precedente sostituisca quella più recente. `live=false` impedisce al timer autonomo di VirtualSky di riportare la mappa all’ora corrente del browser.

`Last-Modified` è l’ora di modifica del file servito, non una misura certificata dell’istante di metà esposizione. Esposizioni, elaborazione e rinnovo del JPEG possono introdurre ritardo; il confronto dei timestamp verifica la coerenza usata dalla pagina, non l’assenza di ritardo nell’acquisizione.

Evidence operative conservate sul Raspberry:

- `config/myFiles/starmap-calibration-20261009.json`: parametri e stelle dell’adattamento;
- `config/myFiles/starmap-calibration-validation-20261009.json`: posizioni ed errori del fotogramma successivo;
- copia precedente dei file in `/home/pi/allsky-private-archive/starmap-calibration-20261009-200803`.

Ricalibrare dopo spostamento della camera, sostituzione della lente, modifica di crop, binning o rapporto d’aspetto. Un semplice ridimensionamento della pagina non richiede una nuova calibrazione.

## 27.21 Default notturno e pianeti

| Proprietà di `configuration.json` | Configurazione verificata |
|---|---|
| `overlayAutoNight` | `true` — personalizzazione Digital Stargate |
| `showOverlayAtStartup` | `false` — attesa della classificazione giorno/notte |
| `showplanets` / `showplanetlabels` | `true` / `true` |
| `showstarlabels` | `true` — nomi delle stelle principali |
| `meteorshowers` | `true` — radianti indicativi del catalogo VirtualSky |
| `planets` | `virtualsky/virtualsky-planets.js` |
| `live` | `false` — clock comandato dal fotogramma |

Il controller usa la classificazione giorno/notte esistente in Allsky, derivata dagli orari di alba e tramonto di `data.json`. Al primo caricamento e al cambio di periodo applica il default: mappa accesa di notte, spenta di giorno. Questa logica usa alba/tramonto della pagina, non la soglia solare del rilevatore meteore.

Il visitatore può cambiare manualmente la visibilità: la scelta resta valida nel periodo corrente. Un nuovo caricamento o il successivo cambio giorno/notte riapplica il default. La transizione rimuove lo stile di visualizzazione lasciato dall’animazione manuale, così che `ng-show` possa mostrare o nascondere la mappa. Il passaggio avviene al successivo ciclo del controller, non mediante un timer separato al secondo esatto del tramonto.

I pianeti e i nomi sono abilitati esplicitamente; il plugin calcola le effemeridi anziché usare il vecchio JSON statico del sito. Le posizioni condividono clock e proiezione della mappa. Non tutti i pianeti sono necessariamente sopra l’orizzonte o dentro la porzione del fotogramma; un simbolo non garantisce che l’oggetto sia distinguibile nella ripresa.

Dal 09/10/2026 sono abilitati anche i nomi delle stelle principali e i radianti degli sciami. I radianti sono riferimenti del catalogo fornito da VirtualSky, non rilevamenti della camera né conferme di meteore. Il file `virtualsky/showers.json` richiama un calendario IMO 2012: non va presentato come previsione verificata per il 2026. Le griglie equatoriale, azimutale e galattica restano disabilitate. Backup della modifica: `/home/pi/allsky-private-archive/stars-showers-20261009-204402`.

Verifiche effettuate: caricamento serale con overlay attivo senza clic, opzioni dei pianeti presenti nella pagina pubblicata, assenza di errori nel log browser e test della logica per avvio notturno/diurno, scelta manuale e cambio di periodo. Il passaggio reale all’alba non è stato atteso durante il collaudo; la prova browser è stata svolta in Europe/Rome. Comportamento dei confini orari con browser in altri fusi da verificare.

Backup delle modifiche: `/home/pi/allsky-private-archive/night-overlay-20261009-201318` e `/home/pi/allsky-private-archive/overlay-planets-20261009-201537`. Il primo contiene controller, configurazione e pagina precedenti; il secondo la configurazione precedente all’abilitazione esplicita dei pianeti.

## 27.22 Sincronizzazione NTP del Raspberry

Il 09/10/2026 alle 20:14 Europe/Rome sono stati verificati `systemd-timesyncd` attivo, abilitazione al riavvio e `System clock synchronized: yes`. Il server esterno osservato è `2.debian.pool.ntp.org`, stratum 2, con offset +7,637 ms e jitter 12,067 ms. Sono misure del controllo, non soglie garantite nel tempo. Il fuso del sistema è `Europe/Rome`; UTC è usato per confrontare gli istanti della mappa e del fotogramma.

Non è stata necessaria una modifica: il servizio usa la configurazione di sistema esistente e i pool di fallback Debian predefiniti. La sincronizzazione viene mantenuta periodicamente quando la rete consente il traffico NTP. L’intervallo osservato era 34 minuti e 8 secondi. Durante un’interruzione Internet l’orologio può continuare localmente, ma non è possibile garantire correzioni NTP esterne; non è stato rilevato un RTC disponibile da `timedatectl`.

Controlli di sola lettura, dalla sessione amministrativa autorizzata:

```bash
timedatectl status
timedatectl timesync-status
systemctl is-active systemd-timesyncd
systemctl is-enabled systemd-timesyncd
journalctl -u systemd-timesyncd --since today
```

Verificare servizio attivo, sincronizzazione confermata e server raggiungibile. Uno stato iniziale non sincronizzato dopo il riavvio richiede di attendere il primo scambio riuscito e controllare rete/DNS/NTP; l’avvio reale dopo riavvio non è stato collaudato nella sessione. Non correggere manualmente l’ora durante l’acquisizione senza una finestra di manutenzione. NTP mantiene l’orologio del Raspberry; non elimina il ritardo di esposizione o trasferimento dell’immagine.

## 27.23 Rilevazione e storico automatico delle meteore candidate

### Acquisizione corrente

Il modulo personalizzato `allsky_meteorarchive.py`, versione `v1.0.0-digitalstargate`, estende il rilevatore nativo Allsky e conserva lo storico dei candidati. È abilitato nella voce `meteor` di `postprocessing_night.json`. Parametri verificati: maschera `meteor-digital-stargate-mask.png`, lunghezza minima 100 pixel, `annotatemain=false`, `enabledebug=false`, `useclearsky=false`.

Il modulo evita l’elaborazione fuori dal flusso notturno. La maschera esclude ostacoli; una contrazione del bordo di 31 × 31 pixel elimina i contorni che toccano aree escluse o bordi artificiali. I candidati restano tracce da valutare: aerei, satelliti, riflessi e artefatti possono produrre falsi positivi. Non è stata misurata l’efficienza scientifica del rilevatore né una probabilità di conferma.

| Prodotto | Percorso nella cartella osservativa `<data>` |
|---|---|
| Copia senza marcatura | `images/<data>/meteors/meteors-<YYYYMMDDhhmmss>.jpg` |
| Copia con rilevazioni disegnate | `images/<data>/meteors/meteors-<YYYYMMDDhhmmss>-marked.jpg` |
| Miniature | `images/<data>/meteorsthumbnails/`, versioni normale e marcata |
| Metadati | `images/<data>/meteors/meteors-<YYYYMMDDhhmmss>.json` |
| Copie divulgative indipendenti | `html/allsky/meteors/` e relativa `thumbnails/` |

I metadati includono `candidate=true`, `confirmed=false`, identificativo del rilevatore, lunghezza, angolo, score, bounding box, centro e rapporto d’aspetto. Lo score non rappresenta una probabilità certificata che la traccia sia una meteora. Immagini e JSON vengono sostituiti atomicamente dopo la scrittura temporanea; un errore di archiviazione viene registrato e propagato.

Le copie pubbliche sono indipendenti dalla finestra di conservazione degli originali; i prodotti nella cartella notturna restano soggetti alla pulizia di quella cartella. Lo storico pubblico richiede quindi controllo dello spazio e una politica di selezione: non è un archivio perpetuo garantito.

### Analisi delle immagini storiche

Analisi conclusa il 09/10/2026: **9.221 immagini notturne elaborate**, **94 fotogrammi candidati**, **105 tracce candidate**, **0 errori registrati**. La selezione delle immagini ha usato l’altitudine solare e la soglia di acquisizione configurata, −6°, con timestamp dei nomi file interpretati in Europe/Rome. La maschera è adattata alla risoluzione; rapporti d’aspetto differenti oltre la tolleranza dello script richiedono una maschera separata.

Lo stato è in `config/myFiles/meteor-historical-scan.json`, comprensivo dei file completati. Questi conteggi descrivono l’analisi originale, non il numero corrente nella galleria: revisione umana e nuove acquisizioni modificano la raccolta pubblica. Non sono stati riconosciuti automaticamente eventi confermati.

La galleria pubblica [Meteore candidate](https://digitalstargate.freeddns.it:23232/allsky/meteors/) usa il sito Allsky, non il repository GitHub dei documenti. I candidati marcati dall’Owner come indesiderati sono stati rimossi dalla pubblicazione dopo copia privata e verifica SHA-256 di immagini e miniature; originali osservativi, versioni marcate e metadati amministrativi sono stati preservati. I tre lotti hanno rimosso 39, 29 e 16 candidati. Manifest e copie recuperabili sono in `/home/pi/allsky-private-archive/user-rejected-meteors-20261009`, con varianti `-batch2` e `-batch3`.

Una nuova analisi può ripubblicare copie precedentemente rimosse: non è stato introdotto un catalogo permanente di esclusione. Prima di rilanciare una scansione completa, confrontare i manifest dei candidati respinti e pianificare la revisione della galleria. Non confondere la depubblicazione con la cancellazione irreversibile delle osservazioni.

## 27.24 Procedure di verifica, manutenzione e ripristino

### DSG-PROC-027-02 — Verifica dopo un aggiornamento

1. Salvare configurazioni, moduli personalizzati, sorgenti web ed evidence in un’area protetta; non sovrascrivere le copie precedenti.
2. Confrontare l’aggiornamento upstream con le personalizzazioni del §27.19. In particolare, conservare geometria/clock della mappa e archiviazione meteore.
3. Verificare dipendenze Python, servizio `allsky`, nuova immagine, timestamp, sovraimpressioni e spazio disponibile.
4. Verificare NTP con i controlli del §27.22.
5. Aprire il sito pubblico: fotogramma intero, default giorno/notte, controllo manuale e nomi dei pianeti. Aggiornare il riferimento di versione del controller quando cambia il codice, per evitare asset precedenti in cache.
6. Su un’immagine stellata confrontare più stelle distribuite nel campo e i `data-frame-time` di immagine e mappa; ricalibrare se cambia la geometria ottica.
7. Verificare il modulo meteore nel flusso notturno e, quando un candidato è rilevato, la coerenza di immagine, marcatura, JSON, miniatura e copia pubblica.
8. Ricontrollare i percorsi pubblici consentiti e l’esclusione della WebUI; confermare il caricamento delle anteprime Home/Status.
9. Registrare versione, esito, difetti e limiti; non dichiarare riuscito il ripristino completo senza una prova effettiva.

### DSG-PROC-027-03 — Ripristino mirato del sito e della mappa

Conservare prima lo stato corrente e i media acquisiti. Per annullare i soli pianeti, ripristinare la configurazione del relativo backup; per annullare il default notturno, ripristinare insieme i tre file del backup notturno. Il backup della calibrazione ripristina configurazione, controller e pagina anteriori alla nuova geometria. Operare nell’ordine inverso delle modifiche per evitare combinazioni incoerenti; una configurazione di un backup precedente può anche annullare personalizzazioni successive.

Dopo il ripristino, aggiornare il riferimento di versione del controller e ricaricare il sito; verificare immagine, mappa e clock. Questa operazione riguarda la presentazione e non richiede di cancellare gli archivi. Il ripristino dell’intera installazione segue il §27.13 e richiede una finestra controllata.

### Diagnosi delle personalizzazioni

| Sintomo | Controllo prioritario |
|---|---|
| Mappa spostata rispetto alle stelle | Geometria ottica/crop, parametri `overlayCalibration`, cache del controller e confronto con più stelle |
| Mappa corretta ma immagine apparentemente vecchia | Timestamp nel JPEG, `Last-Modified`, clock NTP e stato del processo di acquisizione |
| Overlay non compare la sera | `data.json`, classificazione giorno/notte, `overlayAutoNight`, ora/fuso browser e scelta manuale corrente |
| Pianeta non visibile nella mappa | Opzioni e caricamento plugin; posizione rispetto a orizzonte e campo visualizzato |
| Candidato presente nell’admin ma assente sul sito | Depubblicazione intenzionale, manifest privati o errore della copia divulgativa |
| Nessun candidato archiviato | Pipeline notturna, maschera, soglia, accesso in scrittura, log; zero rilevazioni può essere un esito normale |
| Immagine assente nella mappa globale | Limite della porta 23232 del §27.16, distinto dal funzionamento del sito pubblico |

Restano aperti i collaudi fisici elencati nel §27.12, la prova di failover sul posto, l’accuratezza della calibrazione nelle zone non verificate, il primo aggancio NTP dopo riavvio, la transizione reale all’alba e i fusi browser diversi. Nessuna funzione Allsky autorizza automaticamente apertura della cupola o sostituisce gli interlock locali.

## 27.25 Pubblicazione e indicizzazione Google

La [pagina divulgativa Allsky](../allsky/index.md) integra anteprima live, descrizione del cielo di Manciano e collegamenti a timelapse, startrail, keogrammi e meteore candidate. I dettagli di metadati SEO, sitemap, robots.txt, proprietà Google, segnalazione iniziale di sicurezza e ripristino sono nella [procedura di indicizzazione](../operations/allsky-search-indexing.md). Disponibilità del sito e richiesta di scansione non equivalgono a indicizzazione effettiva.

## 27.26 Pannelli informativi esterni alla ripresa

Dal 09/10/2026 acquisizione, meteo e conteggi sono presentati fuori dalla fotografia. In alto a sinistra “La notte a Manciano” mostra fase del cielo, altezza del Sole, altezza della Luna e prossima alba; sotto resta l’acquisizione. A destra compaiono meteo CloudWatcher e cielo/eventi; i dati Raspberry sono nella fascia inferiore. Nella ripresa rimangono soltanto logo e scritta ridotti in basso a sinistra. La mappa celeste è confinata al rettangolo della foto, mantenendo la calibrazione precedente.

Il collector legge le sorgenti locali Allsky e le proiezioni esterne autorizzate, pubblicando solo i campi selezionati ogni 30 secondi. CloudWatcher proviene dal flusso locale già raccolto su EAGLE; Aircraft usa adsb.fi nell’area approssimata di Manciano. Le stelle sono conteggiate con una maschera dedicata; i candidati della notte sono fotogrammi e tracce archiviati, senza conferma automatica. ISS indica passaggi visibili previsti, non eventi riconosciuti nella foto. Dati scaduti o sorgenti non disponibili sono esplicitamente segnalati.

I pannelli non sono incorporati nel JPEG o nelle anteprime Home/Status. Nessun nuovo hardware, contratto Observatory Status o comando di sicurezza è introdotto. [Sorgenti, frequenze, limiti, verifiche e ripristino](../operations/allsky-live-panels.md).

## 27.27 Backup della configurazione

Il 10/10/2026 è stato acquisito un primo snapshot privato della configurazione e delle personalizzazioni, con copia locale per l'owner. Il nuovo snapshot dell’11/10/2026 alle 10:49 Europe/Rome conserva anche il ripristino startrail e il catalogo delle anteprime Messier; il precedente resta disponibile come riferimento storico. Una copia ridotta e sanificata è conservata nel repository; non contiene credenziali, database, certificati o coordinate precise. La [procedura di backup e ripristino](../operations/allsky-configuration-backup.md) elenca inclusioni, esclusioni, checksum e limiti del collaudo. È un backup della configurazione, non un'immagine della scheda SD; il ripristino su supporto separato resta da collaudare.


## 27.28 Ripristino della generazione startrail — 11 ottobre 2026

Nel vecchio `allsky-OLD/config/config.sh` la soglia `BRIGHTNESS_THRESHOLD` era **0,30**. Dopo l’aggiornamento `startrailsbrightnessthreshold` era **0,10**: nelle due generazioni del 10 e 11 ottobre la selezione aveva accettato rispettivamente zero e un fotogramma. I JPEG esistevano, ma non potevano mostrare scie stellari composte.

È stata ripristinata soltanto la soglia a **0,30**; gli altri parametri startrail risultavano equivalenti. La selezione usa la luminosità media del fotogramma, non una soglia di magnitudine delle stelle. Esposizione, guadagno e calibrazione non sono stati modificati. Il collegamento fisico fra `settings.json` e `settings_ZWO_ASI290MC.json` è stato conservato.

La prova sulla notte osservativa `20261010` ha accettato **624 immagini su 663**, escludendone 39. Sono stati rigenerati e ripubblicati i prodotti delle notti `20261009` e `20261010`, con miniature aggiornate. SHA-256 dei JPEG amministrativi e pubblici, e delle rispettive miniature, coincidenti. La camera è rimasta attiva. Gli avvisi e le statistiche delle elaborazioni precedenti possono restare nello storico: non descrivono necessariamente i file rigenerati manualmente.

Backup mirato precedente alla correzione: `/home/pi/allsky-private-archive/startrails-restore-20261011`. Comprende impostazioni e prodotti sostituiti. Prima di nuovi aggiornamenti confrontare il valore nel vecchio `config.sh` con il campo della nuova configurazione; non ripristinare indiscriminatamente l’intera configurazione precedente.

## 27.29 Overlay bloccato e anteprime Messier — 11 ottobre 2026

`config.mouse=false` disabilita rotazione/trascinamento manuale della mappa, mantenendo il passaggio del mouse sui marcatori. La sincronizzazione continua a usare `Last-Modified` del fotogramma e `setClock(..., "camera-frame")`; nel controllo browser i due `data-frame-time` erano identici. Parametri `overlayCalibration`, coordinate del sito, dimensioni e controller della sincronizzazione sono rimasti invariati. Il pulsante della mappa conserva il controllo della visibilità.

Il catalogo `virtualsky/messier.json` conserva i **110 oggetti** e tutte le coordinate originali; aggiunge per ciascuno una proprietà `preview` con immagine locale, URL della sorgente, credito e campo angolare. Le miniature JPEG 192 × 192 sono in `virtualsky/messier-preview/`; la scheda le mostra a 160 × 160 con nome, dicitura **Immagine di archivio** e credito. Non rappresentano osservazioni o rilevazioni della camera Allsky. Le miniature sono ritagli DSS2 color ottenuti dal servizio [CDS HiPS2FITS](https://alasky.cds.unistra.fr/hips-image-services/hips2fits); crediti STScI/NASA/CDS, provenienza individuale nel catalogo e attribuzioni in `CREDITS.txt`, con riferimento ai [diritti DSS](https://archive.stsci.edu/dss/copyright.html).

Il loader `virtualsky/virtualsky.js` costruisce le schede usando nodi DOM e percorsi locali limitati al catalogo. Il rilevamento converte i pixel dello schermo nei pixel del canvas; la zona del marcatore è di circa 8 pixel visualizzati. La scheda resta entro il canvas. Questo adattamento riguarda l’interazione, non la proiezione celeste. Il riferimento versionato nella Home e la richiesta versionata del catalogo evitano copie precedenti nella cache.

Controlli: sintassi JavaScript, 110 JPEG e integrità del catalogo, coordinate originali invariate, accesso HTTPS pubblico al catalogo e alle immagini, prova browser con M1 e miniatura caricata, clock immagine/mappa coincidente e nessun errore console nel controllo. La presenza dei singoli oggetti dipende dall’orizzonte e dal campo; non è stato collaudato manualmente il passaggio del mouse su tutti i 110 oggetti o su tutti i browser. La funzionalità riguarda gli oggetti Messier, non miniature di stelle, pianeti o figure di costellazioni.

Backup mirati: `/home/pi/allsky-private-archive/overlay-mouse-lock-20261011` e `/home/pi/allsky-private-archive/messier-previews-20261011`. Il secondo conserva renderer, catalogo e Home precedenti. Per annullare l’integrazione ripristinare soltanto quei file e aggiornare il riferimento di cache, mantenendo `mouse=false` se si vuole conservare il blocco. Non toccare la calibrazione o il controller del clock.


## 27.30 Analisi dei log e ottimizzazione del caricamento live — 27 ottobre 2026

L’analisi è stata eseguita via SSH nelle prime ore del 27/10/2026, fuso Europe/Rome, dopo il ripristino della raggiungibilità VPN. I risultati seguenti sono osservazioni della finestra esaminata, non garanzie di disponibilità futura.

| Controllo | Esito osservato |
|---|---|
| Acquisizione, servizi periodici e lighttpd | Attivi; camera non riavviata durante l’analisi |
| Temperatura CPU | Circa 37–39 °C |
| Alimentazione e limitazioni termiche | `get_throttled=0x0` al controllo |
| Disco | Circa 92 GB liberi, 19% occupato |
| Memoria | Circa 3,4 GB disponibili; swap non utilizzato |
| Orario | NTP sincronizzato |
| Log acquisizione delle 24 ore precedenti | Nessuna corrispondenza ai filtri `error`, `traceback`, `failed`; non è una certificazione di assenza di ogni difetto |
| Immagini scartate | 30 fotogrammi sotto soglia media 0,10, concentrati all’alba e al tramonto |
| Prodotti dell’ultima notte completata | Keogramma, startrail e timelapse riusciti; startrail con 560 fotogrammi usati e 212 esclusi, soglia 0,30 |

### Avviso «immagine mancante o corrotta»

Lo screenshot del 26 ottobre mostrava l’avviso insieme a un fotogramma già ricevuto. Nei controlli successivi l’URL pubblico dell’immagine ha restituito JPEG validi e aggiornati; sei richieste consecutive erano riuscite. Il controller precedente generava l’avviso generico già al primo evento `error`, mantenendo nella pagina l’ultimo fotogramma caricato. Non sono disponibili log browser/accesso sufficienti per ricostruire la causa del singolo episodio: non è stata dimostrata né una corruzione del JPEG né una relazione causale con i reset USB.

**Modifica mantenuta:** in `html/allsky/js/controller.js` un caricamento fallito viene ritentato una sola volta dopo due secondi, con URL aggiornato. Se fallisce ancora e nella pagina esiste un’immagine `current`, compare un avviso esplicito: l’aggiornamento non è riuscito e resta visibile l’ultimo fotogramma ricevuto. In assenza di un precedente fotogramma resta l’avviso di errore originario. Il successivo caricamento riuscito cancella il messaggio. Non viene attestata la freschezza dell’immagine sulla sola base della sua presenza nel riquadro.

La Home usa il riferimento `js/controller.js?v=dsg-live-retry-20261027` per aggiornare la cache. Sono passati il controllo di sintassi JavaScript e una prova isolata del gestore con: singolo retry, avviso con vecchio fotogramma e errore persistente senza fotogramma. Sono stati verificati anche il controller pubblicato e un JPEG valido via HTTPS. Non è stato simulato un guasto della camera o della rete sull’impianto per collaudare il browser in condizioni di interruzione reale.

### Telemetria: prova non mantenuta

Il servizio periodico registra `PinFactoryFallback: Falling back from lgpio: No module named 'lgpio'`, pur aggiornando correttamente i dati. È stata provata la lettura CPU da `/sys/class/thermal/thermal_zone0/temp` nel modulo `allsky_pistatus.py`. La prova non eliminava l’avviso: anche il helper condiviso inizializza `gpiozero` per le informazioni della scheda. Il modulo originale è stato quindi ripristinato e i suoi SHA-256 confrontati con il backup. Nessun pacchetto o dipendenza è stato installato; l’avviso resta visibile e non bloccante nel controllo effettuato. È stato ricaricato solo `allskyperiodic`, senza riavviare `allsky`.

### Conservazione e ripristino mirato

Prima delle prove sono stati conservati controller, Home e modulo PiStatus in `/home/pi/allsky-private-archive/log-audit-20261027`, insieme ai log acquisiti. I log completi rimangono privati; questo capitolo ne riporta solo il riepilogo tecnico. Il rollback del retry consiste nel ripristino dei soli controller e Home precedenti, verificando le modifiche successive e aggiornando il riferimento di cache. Non sovrascrivere configurazioni fotografiche o calibrazione per annullare una modifica alla gestione del caricamento.

Gli snapshot completi del 10 e 11 ottobre del §27.27 restano immutati e **non includono il retry del 27 ottobre**. Il backup mirato non equivale a un nuovo snapshot completo o a un ripristino integrale collaudato. Il successivo snapshot delle 08:01 del 27 ottobre, descritto sotto e nella guida backup, include invece il controller aggiornato e preserva le copie storiche. Esposizione, guadagno, soglie, geometria, dimensioni e sincronizzazione della mappa non sono stati modificati.

## 27.31 Verifica dei reset USB della camera — 27 ottobre 2026

L’ASI290MC era collegata direttamente sul bus USB3 a 5000 Mbit/s e gestita dal processo `capture_ZWO` rimasto attivo. La camera aveva risparmio energetico USB già disabilitato (`power/control=on`), stato runtime `active` e tempo di sospensione runtime pari a zero: il valore di autosuspend configurato non comportava sospensioni osservate del dispositivo.

Nella finestra precedente di 24 ore erano presenti **2.809 messaggi** `reset SuperSpeed USB device ... using xhci_hcd`. Per approfondire è stata confrontata una finestra di **30 minuti** dei log kernel e acquisizione: **30 avvii di esposizione, 30 reset, tutti entro 0,138 secondi dall’avvio più vicino e zero errori di acquisizione riconosciuti dai filtri**. Nei controlli non sono emerse disconnessioni, timeout o errori di descrittore. Questi conteggi valgono per le finestre osservate e non per tutte le acquisizioni future.

La configurazione `zwoexposuretype=0` corrisponde nel sorgente Allsky a `ZWOsnap`, modalità singolo scatto che usa `ASIStartExposure` e `ASIGetDataAfterExp`. L’SDK è incorporato staticamente nel binario; i simboli e il codice ispezionati confermano la presenza di funzioni di gestione/reset USB. Questa ispezione, da sola, non costituisce una traccia delle chiamate eseguite in tempo reale.

Una risposta del supporto ZWO nel [forum tecnico del produttore](https://bbs.zwoastro.com/d/9937-linux-sdk-asi120mm-mini-usb-reset-on-each-frame) descrive reset del collegamento USB eseguiti dall’SDK per ogni esposizione singola. La discussione riguarda ASI120MM Mini e versioni SDK specifiche, non una certificazione della ASI290MC installata. **L’interpretazione più coerente con i dati locali è un comportamento dell’SDK nella modalità corrente**, non una disconnessione casuale dimostrata. Non è stata provata in modo assoluto l’assenza di problemi hardware o firmware.

**Decisione Owner:** mantenere la configurazione attuale. Non è stato individuato un metodo verificato per eliminare questi reset a caldo senza interrompere l’acquisizione o cambiare la modalità. Non sono stati modificati esposizione, guadagno, banda USB, modalità, SDK, driver, firmware, alimentazione o collegamenti. Non sono stati introdotti filtri per nascondere i messaggi kernel.

Un eventuale confronto con un’altra modalità/SDK richiede una finestra di manutenzione separata, backup e collaudo; non è autorizzato implicitamente dalla diagnosi. Riaprire l’indagine se compaiono timeout, errori di trasferimento, disconnessioni/rinumerazioni, JPEG invalidi o interruzioni dei nuovi fotogrammi. Un reset isolato correlato allo scatto, con acquisizione riuscita, non basta da solo a concludere un guasto.


## 27.32 Snapshot aggiornato dopo l’analisi — 27 ottobre 2026

Alle **08:01 Europe/Rome** è stato acquisito lo snapshot `configuration-backup-20261027-080114`, con camera e servizi attivi. La copia privata comprende **355 file verificati** oltre al manifest, quella pubblica **140 file verificati** oltre al manifest. Rispetto al perimetro precedente il privato include anche PiStatus originale e helper condiviso; il collegamento fisico settings è preservato nel TAR. I due database SQLite sono stati acquisiti tramite backup API e hanno superato `quick_check`.

L’export pubblico include il controller con retry e la Home con riferimento cache aggiornato; non contiene la prova PiStatus annullata, log grezzi, database, certificati, credenziali o coordinate geografiche precise. La copia completa privata è conservata nella directory riservata del Raspberry e consegnata separatamente all’Owner, fuori dal repository, con permessi limitati. Gli archivi del 10 e 11 ottobre restano immutati. Nessun servizio è stato fermato e nessun parametro fotografico o USB è stato modificato durante il backup.

[Download sanificato, SHA-256, perimetro ed istruzioni di ripristino](../operations/allsky-configuration-backup.md). Integrità degli archivi e dei manifest, sintassi e sanificazione verificate; questo non attesta un ripristino integrale. È uno snapshot live del perimetro configurazione, non una transazione atomica dell’intera installazione o un’immagine SD.


## 27.33 Ricalibrazione dopo spostamento camera — 31 ottobre 2026

L’Owner ha dichiarato lo spostamento della camera alle **14:30 circa Europe/Rome**. La calibrazione del 9 ottobre è quindi storica e non va usata per l’orientamento corrente. I fotogrammi usati per la nuova soluzione sono successivi allo spostamento. Il primo controllo, ancora troppo chiaro, non è stato usato per applicare una correzione approssimativa.

### Metodo e verifica

È stato analizzato il fotogramma con `Last-Modified` **17:10:21 UTC / 18:10:21 Europe/Rome**, a risoluzione 1936 × 1096. Le coordinate stellari sono state inizialmente riconosciute con il solver locale tetra3 e catalogo Hipparcos su un riquadro: 16 corrispondenze, probabilità di associazione casuale riportata dal solver circa 6,65×10⁻¹⁹ nel proprio modello. Questo valore non è una probabilità certificata della correttezza dell’intera calibrazione.

La soluzione iniziale è stata confrontata con punti stellari distribuiti nel campo: **72 corrispondenze entro 4 pixel**, quindi ottimizzazione robusta della proiezione equisolidale usata dalla mappa. Una suddivisione interna di 24 riferimenti tenuti fuori dal fit iniziale ha dato RMS **0,74 pixel**, massimo 1,27 pixel. Il fit finale sui 72 riferimenti dà RMS **1,04 pixel**. La selezione mediante vicinanza alla proiezione è condizionata dalla soluzione iniziale; non equivale a 72 identificazioni cieche indipendenti.

Un **secondo fotogramma**, `Last-Modified` **17:19:10 UTC / 18:19:10 Europe/Rome**, è stato verificato senza rifare il fit: **71 dei 72 riferimenti entro 4 pixel**, RMS 1,10 pixel sulle 71 corrispondenze e massimo 2,87 pixel; RMS 1,23 pixel su tutti i 72 punti più vicini. Il clock impiegato nel modello è quello del `Last-Modified`, coerente con la sincronizzazione web esistente, non una misura dell’inizio esposizione. La differenza temporale di elaborazione resta un limite. Il conteggio automatico del pannello, 15 al primo controllo, dipende dalla propria maschera/soglia ed è distinto dai riferimenti usati dalla calibrazione.

### Geometria applicata

| Parametro | Nuovo valore |
|---|---|
| Riferimento immagine | 1936 × 1096 pixel |
| Centro X / Y | 1048,433 / 510,933 pixel |
| Raggio orizzonte | 764,885 pixel |
| `az` | 323,298707° |
| `overlayLean` | 1,249056° |
| `overlayLeanAz` | 164,934848° |
| `overlayCalibration.calibratedAt` | `2026-10-31T17:10:21Z`, istante del fotogramma di fit |

Sono cambiati **soltanto** `az`, `overlayLean`, `overlayLeanAz` e `overlayCalibration` in `html/allsky/configuration.json`. Centro e raggio seguono la nuova geometria misurata; il layout responsive e la dimensione del riquadro web non sono stati riscritti. Controller, sincronizzazione del clock, catalogo/miniature, retry live e `mouse=false` sono stati conservati. Esposizione, guadagno, acquisizione e parametri USB non sono stati modificati; la camera è rimasta attiva.

Il nuovo JSON è stato verificato anche dal sito HTTPS pubblico. L’errore misurato riguarda i riferimenti visibili selezionati, non ogni punto dell’orizzonte o le aree coperte dagli apparati. Non è stato effettuato un audit di tutte le etichette/pianeti tramite browser o una nuova calibrazione fotometrica. Dopo ogni ulteriore spostamento ripetere il confronto su più stelle e fotogrammi. Le maschere di stelle/meteore non sono state modificate in questo intervento: dopo lo spostamento richiedono una verifica separata rispetto agli ostacoli nella nuova ripresa.

### Backup e ripristino

Backup prima dell’applicazione: `/home/pi/allsky-private-archive/starmap-recalibration-20261031-182056`, con configurazione, controller e Home precedenti. Evidenza completa di fit, verifica e soli campi modificati in `config/myFiles/starmap-calibration-20261031.json`, inclusa nella copia privata. La precedente copia di precauzione `pre-recalibration-20261031` è mantenuta.

Per annullare questa sola calibrazione confrontare lo stato corrente e ripristinare i quattro campi geometrici dal JSON precedente, conservando le personalizzazioni successive. Ricaricare la pagina per ricreare la mappa e verificare clock/geometria; non ripristinare indiscriminatamente un intero sito storico.

Alle **18:21 Europe/Rome** è stato creato lo snapshot `configuration-backup-20261031-182122`, con **356 file privati e 140 pubblici** oltre ai manifest; include la nuova configurazione e, nel privato, l’evidenza di calibrazione. SHA-256, manifest, JSON/Python/JavaScript, PHP Home/footer, due database SQLite (`quick_check`) e hardlink settings verificati; servizi di acquisizione/periodici/telemetria attivi. Privato conservato separatamente su Raspberry e PC Owner con permessi limitati; repository contenente solo export sanificato. Tutti gli snapshot precedenti restano immutati. [Archivio pubblico, checksum e limiti del ripristino](../operations/allsky-configuration-backup.md). Non è un’immagine SD e non è stato eseguito un ripristino completo.


## 27.34 Vento locale e nuovo snapshot — 31 ottobre 2026

Il pannello **Meteo locale · CloudWatcher** include la velocità del vento in km/h. L’unità dell’app è stata confermata dall’Owner. Il CSV contiene misure valide in `Wind Value`; il produttore già attivo le inoltra come `diagnostics.wind_value_raw`, mentre il campo canonico resta nullo. Il collector Allsky usa quella sola misura come fallback per la sorgente CloudWatcher esplicitamente riconosciuta, con gli stessi controlli di freschezza del meteo e accettando soltanto numeri finiti non negativi. Dati assenti/scaduti restano indisponibili; zero misurato resta zero. Nessuna raffica è derivata. [Dettagli, limiti, test e rollback](../operations/allsky-live-panels.md#vento-cloudwatcher-in-kmh-31-ottobre-2026).

Home, `js/dsg-live-panels.js` e collector sono i soli componenti runtime interessati; esportatore e clone EAGLE non sono stati modificati. Nessun parametro fotografico, geometria overlay, USB, soglia meteo o Safety Authority è cambiato. Misure aggiornate sono state verificate nel JSON pubblico HTTPS; non è stata eseguita una calibrazione metrologica del vento.

Lo snapshot `configuration-backup-20261031-185033`, acquisito alle **18:50 Europe/Rome** senza fermare la camera, comprende la configurazione corrente con vento e ricalibrazione. **356 file privati e 140 pubblici** oltre ai manifest, SHA-256 verificati, due database SQLite `quick_check` OK, hardlink settings preservato e sintassi verificata. Il privato è separato su Raspberry/PC Owner con accesso limitato; nel repository è pubblicata soltanto la copia sanificata. Gli snapshot delle 18:21 e precedenti restano immutati. [Download, checksum e perimetro](../operations/allsky-configuration-backup.md). Il backup non è un’immagine SD; ripristino integrale non collaudato.


## 27.35 Aggiornamento Allsky v2026.10.01_01 — 12 novembre 2026

### Baseline, confronto e migrazione

Installata la [release ufficiale v2026.10.01_01](https://github.com/AllskyTeam/allsky/releases/tag/v2026.10.01_01), pubblicata il 1° novembre, passando dal commit `2b2c7b1347d076a489df5e614acf27de450738fb` al commit `f1406ea78ba969313abd1ddd14a4272967081a06`. Sistema operativo Bullseye e SDK ZWO sono rimasti invariati.

Il confronto ha individuato **319 percorsi modificati** dalla release, inclusa la documentazione generata. Un solo file modificato sia localmente sia a monte richiedeva integrazione: `html/allsky/js/controller.js`. Il confronto a tre vie, dopo normalizzazione dei ritorni a capo, ha mantenuto il retry singolo del §27.30, il messaggio sul fotogramma precedente, la sincronizzazione al `Last-Modified`, l’avvio notturno della mappa e il dimensionamento calibrato. Sono state integrate le altre correzioni ufficiali, incluso l’uso di `imageName` dallo scope. Nel sito finale 315 file presenti coincidevano con la release, tre percorsi erano stati eliminati dalla release e il controller era la sola integrazione locale fra i file aggiornati a monte. Le altre personalizzazioni locali sono rimaste nei rispettivi file.

`capture_ZWO`, `capture_RPi`, `keogram` e `startrails` sono stati compilati nell’area privata di prova mentre l’acquisizione continuava, con percorsi di produzione nell’header generato. Dopo backup e controlli è stato eseguito il fast-forward al tag verificato; sono stati installati i binari già compilati e usata la rigenerazione ufficiale dei file Allsky. La lista per la rigenerazione escludeva la compilazione già conclusa e la sostituzione del Lighttpd personalizzato. Gli header generati sono stati confrontati identici. Non è stata eseguita una reinstallazione indiscriminata del sito.

Sono stati aggiornati gli elenchi nativi dei formati dell’editor, `ConfigVersion` a 6 e `config.AllskyVersion`. Il nuovo collegamento keolapse è presente ma **disabilitato**; nessun nuovo modulo è stato installato o abilitato. Il modulo meteore precedente è conservato: il sorgente di questa release ne aggiunge il metadato di deprecazione dalla versione `v2026.10.01_02`, senza rimuoverlo in quella installata. Non è stata migrata automaticamente l’analisi verso un rilevatore diverso.

### Conservazione e controlli

| Elemento | Esito del controllo del 12 novembre |
|---|---|
| Parametri fotografici | Settings identici byte per byte; collegamento fisico tra i due settings camera preservato |
| Mappa | Geometria del §27.33 invariata, `mouse=false`, catalogo con 110 anteprime conservato; stesso `data-frame-time` per JPEG e mappa nel browser |
| Sito e pannelli | Logo, sfondo, layout, collegamento al portale e pannelli conservati; CloudWatcher con vento, scatto e Raspberry aggiornati nel browser |
| Meteore | Flussi e modulo archivio personalizzato conservati; 293 immagini candidate pubbliche prima e dopo |
| Startrails | Soglia di luminosità 0,30 conservata |
| Accesso e orario | Lighttpd/TLS e sudoers identici alla situazione precedente; NTP sincronizzato |
| Dati e servizi | Due database SQLite con `quick_check` OK; acquisizione, periodic, server Allsky, Lighttpd e timer pannelli attivi |
| Pubblicazione | HTTPS con verifica ordinaria del certificato: Home, JPEG e galleria meteore HTTP 200; amministrazione `/index.php` HTTP 403 dall’esterno |

Il controllo preliminare comprendeva compilazione dei quattro programmi, sintassi di 27 script shell, 17 file PHP, 28 file Python e 15 file JavaScript aggiornati, import dei moduli comuni/meteore/archivio personalizzato/condizioni overlay e test isolato del retry. La finestra registrata va dall’arresto delle **18:27:45** al riavvio dei servizi delle **18:27:49 Europe/Rome**; i log confermano la prima acquisizione effettiva alle **18:28:04** e altre immagini fino alle **18:32:04**, senza errori di acquisizione riconosciuti nella finestra. Non è una garanzia di assenza di ogni difetto o disponibilità futura.

Durante la verifica, la maschera di permessi restrittiva usata per gli archivi privati aveva inizialmente reso illeggibili al web server alcuni sorgenti pubblici appena riscritti da Git. Sono stati corretti i soli sorgenti tracciati ufficiali e schemi pubblici: file 0644, eseguibili e directory 0755. Permessi degli archivi privati e dati sensibili conservati. Il riferimento finale `js/controller.js?v=dsg-upgrade-20261112-v2` evita il riuso della risposta precedente. La pagina è stata quindi verificata completa, senza espressioni Angular irrisolte, con JPEG 1936 × 1096 e clock mappa/fotogramma coincidente. Questa correzione non modifica calibrazione o parametri fotografici.

### Backup, ripristino e limiti

Prima del passaggio è stato acquisito lo snapshot delle **18:15**, `configuration-backup-20261112-181517`, con 356 file privati verificati oltre al manifest. Un ulteriore archivio privato conserva i file sostituiti del programma, binari, configurazione e controlli di accesso precedenti; il processo di aggiornamento aveva predisposto il ripristino su errore, che non è stato attivato né collaudato con un guasto deliberato. Questi archivi e i log grezzi rimangono fuori dal repository.

Dopo l’esito positivo è stato acquisito lo snapshot delle **18:31**, `configuration-backup-20261112-183125`: **357 file privati e 140 pubblici verificati**, oltre ai manifest. Repository e portale ospitano soltanto il TAR pubblico sanificato e il suo SHA-256; il privato è conservato separatamente sul Raspberry e sul PC Owner con accesso limitato. [Download aggiornato, checksum, perimetro e procedura di ripristino](../operations/allsky-configuration-backup.md). Tutti gli archivi pubblici precedenti restano immutati e rappresentano le rispettive baseline storiche.

La generazione completa di startrails, keogram e timelapse alla successiva chiusura della notte **non è stata eseguita nella finestra di verifica**; resta un controllo operativo residuo, senza promessa di un monitoraggio automatico aggiuntivo. Le [limitazioni ufficiali della release](https://github.com/AllskyTeam/allsky/blob/v2026.10.01_01/docs/source/allsky_guide/known_issues.md) segnalano inoltre l’indisponibilità dei grafici nativi su Bullseye; non è stato aggiornato il sistema operativo per risolverla. Nel solo aggiornamento di versione non erano state ricalibrate la mappa o le maschere, né modificati modalità e parametri USB. Il successivo aggiornamento delle sole maschere e dei flag camera è nel §27.36. Il backup non è un’immagine SD e il ripristino integrale resta da collaudare su supporto separato.


## 27.36 Maschere aggiornate e flag camera coerenti con Snapshot — 12 novembre 2026

L’Owner ha autorizzato il rifacimento delle maschere di analisi e la disabilitazione di Auto-Gain e Auto White Balance giorno/notte, con backup preliminare e **calibrazione della mappa invariata**. La migrazione del rilevatore meteore e quella del sistema operativo restano proposte separate non applicate.

### Maschere e perimetro

Le maschere del 9 ottobre precedevano lo spostamento della camera. Sono state confrontate riprese successive allo spostamento: il riferimento stellato del 31 ottobre usato dalla calibrazione, una ripresa dell’11 novembre e due del 12 novembre. Le nuove PNG conservano 1936 × 1096 pixel, escludono apparati a sinistra, logo e bordo, con margini prudenti. Sono usate soltanto per l’analisi: **non oscurano il JPEG pubblico e non cambiano la mappa**.

La regione base è un cerchio di analisi di raggio **700 pixel**, centro immagine X **1048,433** / Y **510,933**, meno un poligono di esclusione degli apparati. Questi parametri descrivono la maschera, non sostituiscono il raggio/orientamento della calibrazione VirtualSky. La maschera meteore ha sfumatura di **16 pixel verso l’interno**, senza valori non nulli fuori dalla regione consentita; quella stelle è binaria e usa un margine interno aggiuntivo di **20 pixel**. Resta il filtro preesistente del modulo archivio meteore, che esclude contorni a contatto con il bordo tramite erosione 31 × 31.

| PNG di analisi | Area precedente | Area aggiornata |
|---|---:|---:|
| Stelle, pixel non nulli | 14,49% del fotogramma | 51,68% del fotogramma |
| Meteore, intensità maggiore di 127/255 | 18,74% del fotogramma | 53,43% del fotogramma |

Il nucleo meteore sopra 250/255 è il 52,28%; il filtro di sicurezza applica poi altre esclusioni. Le percentuali sono riferite ai pixel del fotogramma, **non alla superficie celeste, al campo angolare o all’area effettiva dopo tutti i filtri dell’algoritmo**. Il conteggio stelle Fast esclude inoltre parte del bordo inferiore e applica i propri criteri. Non confrontare direttamente i conteggi precedenti e successivi senza annotare il cambio di maschera.

La ricetta geometrica, il poligono e i riferimenti sono conservati in `config/myFiles/masks/analysis-masks-20261112.json`, incluso nel backup privato. È una generazione da dati geometrici, non un progetto modificabile nativamente dal nuovo Mask Editor: le PNG sono operative e ripristinabili, ma per modificarne le forme occorre usare la ricetta o ricreare il progetto nell’editor. La copia pubblica ridotta include le due PNG, non le fotografie di prova o la ricetta privata. [Indicazioni ufficiali sulle maschere](https://github.com/AllskyTeam/allsky/blob/v2026.10.01_01/docs/source/allsky_guide/overlays/interface.md#the-mask-editor).

### Automatismi camera

La [documentazione della release](https://github.com/AllskyTeam/allsky/blob/v2026.10.01_01/docs/source/allsky_guide/known_issues.md) segnala che Auto-Gain e Auto White Balance non operano nella modalità ZWO Snapshot. Sono stati modificati solo i quattro flag e il metadato `lastchanged` del settings, mantenendo il collegamento fisico fra i due file settings della camera.

| Impostazione | Prima | Dopo |
|---|---|---|
| `dayautogain`, `nightautogain` | `true` | `false` |
| `dayawb`, `nightawb` | `true` | `false` |
| Guadagno giorno / notte | 0 / 300 | 0 / 300 |
| Bilanciamento rosso / blu, giorno e notte | 52 / 95 | 52 / 95 |
| Auto-esposizione, massimo notte, ritardi | Abilitata, 30 s, 30 s | Invariati |
| Modalità ZWO | Snapshot | Snapshot |

Il valore `gaintransitiontime=5` minuti è rimasto invariato. Con entrambi i flag Auto-Gain disabilitati, il sorgente ZWO torna a consentire la transizione graduale fra i guadagni diurni e notturni; prima era inibita da Auto-Gain. È un effetto della configurazione richiesta, non un ulteriore cambio di parametro: va considerato nel controllo del passaggio all’alba.

`configuration.json` del sito e `js/controller.js` hanno SHA-256 identici prima e dopo: geometria, calibrazione del §27.33, dimensionamento, clock, `mouse=false` e avvio notturno conservati. Nessuna modifica a SDK, parametri USB, soglia startrails 0,30, detector, flussi o formati video.

### Prove e applicazione

Il test offline ha richiamato gli stessi algoritmi configurati (Star Count Fast, scala 0,5, minimo 6 pixel; rilevatore meteore con minimo 100 pixel e filtro di bordo), su copie delle quattro immagini e con entrambe le versioni delle maschere. Sul fotogramma stellato del 31 ottobre i rilevamenti passano da **13 a 40**; sugli altri tre, nuvolosi/crepuscolari, sono rispettivamente **1→1, 0→0 e 0→0**. Nessuna traccia candidata meteore è stata restituita nei quattro test. Originali, database e galleria non sono stati modificati dal test. Sono risultati del rilevatore, non identificazioni stellari confermate, misure di magnitudine o una stima validata di sensibilità/falsi positivi.

Backup preliminare alle **19:16 Europe/Rome**, `configuration-backup-20261112-191658`: 357 file privati e 140 pubblici oltre ai manifest, integrità verificata; il privato è copiato separatamente sul PC Owner. Backup mirato precedente in `/home/pi/allsky-private-archive/masks-autoflags-20261112`, con settings e due PNG originali.

Acquisizione e servizio periodico sono stati fermati per il passaggio e avviati alle **19:23:47**; il nuovo processo camera è partito alle **19:23:51**. Il primo scatto iniziale è nei log alle 19:24:02 e un nuovo fotogramma scientifico salvato alle **19:24:34**, con elaborazione stelle riuscita. I log mostrano Auto: No per guadagno e bilanciamento, con i valori numerici conservati. Nel browser il JPEG 1936 × 1096 e la mappa avevano lo stesso timestamp, **18:25:41 UTC**, con pannelli aggiornati. HTTPS pubblico per pagina, JPEG e galleria meteore HTTP 200; amministrazione esterna HTTP 403.

Il backup successivo delle **19:25**, `configuration-backup-20261112-192507`, comprende **358 file privati e 140 pubblici** oltre ai manifest; nel privato si aggiunge la ricetta delle maschere. Le due copie hanno manifest/checksum verificati, database SQLite `quick_check` OK e hardlink settings conservato. Nel repository entra soltanto il nuovo export sanificato con checksum; precedenti immutati. [Download e ripristino controllato](../operations/allsky-configuration-backup.md).

### Limiti e ripristino

Le prove coprono quattro riferimenti e il funzionamento immediato notturno, non un intero ciclo stagionale, tutte le posizioni degli apparati o un confronto fotometrico diurno/notturno. I flag diurni sono caricati correttamente nei log, ma il comportamento in luce diurna va verificato al successivo passaggio. Il controllo programmato dall’Owner per il **13 novembre alle 09:00** comprende i prodotti completi della notte e la visualizzazione pubblica; la notte contiene fotogrammi prima e dopo questi interventi. Non attribuire ogni differenza di luminosità alla sola disabilitazione degli automatismi: esposizione, nuvole e condizioni cambiano.

Per annullare l’intervento, in manutenzione autorizzata confrontare le modifiche successive e ripristinare le sole due maschere e i quattro flag precedenti dal backup mirato, aggiornando `lastchanged` e preservando l’hardlink; riavviare le componenti pertinenti e controllare nuovi fotogrammi. Non ripristinare l’intero sito o la calibrazione per annullare maschere/flag. Ripristino integrale non collaudato. Eventuali correzioni successive alle anomalie del collaudo richiedono la proposta e l’autorizzazione Owner già richieste.


## 27.37 Valutazione e affiancamento privato delle meteore 12 novembre 2026

Dopo la prova su tre notti complete l’Owner ha autorizzato l’affiancamento privato, mantenendo il rilevatore ordinario e vietando la pubblicazione dei nuovi candidati. Dal **12/11/2026 alle 22:03 Europe/Rome** `dsg-meteor-shadow.service` legge i JPEG notturni già salvati, con soglia privata 100 px, stato/registro/contatori separati e rete disabilitata. Non è stato aggiunto un modulo al flusso di acquisizione. [Guida operativa, isolamento e disattivazione](../operations/allsky-meteor-shadow.md).

Il confronto offline copre **2.176 immagini**, circa 38 ore e 21 minuti, con **2.170 fotogrammi confrontabili**. Il rilevatore attuale, riprodotto sulle stesse immagini e con la maschera aggiornata, segnala 76 fotogrammi candidati; il temporale ne conserva 20 a 100 px e 28 a 50 px. Sono candidati non confermati, non conteggi della galleria né una misura di sensibilità. La notte completa aiuta a scartare riflessi e nubi ricorrenti, ma restano tracce compatibili con aerei/satelliti e non è disponibile un campione indipendente di meteore confermate. Il profilo da 50 px non è stato attivato.

Il modulo upstream è v1.0.1, commit `ee0b6567b829e3bf86cd1e2190e4e0c59e5e2b31`; sorgente immutato, checksum verificato e licenza MIT conservata. L’adattatore privato impedisce l’uso delle variabili, del database e delle funzioni di pubblicazione dell’applicazione. Risultati in `/var/lib/dsg-meteor-shadow`, permessi 0700 e nessun accesso dal sito. Il limite applicativo di 2 GiB mette in pausa l’analisi senza cancellare immagini; una modifica alla maschera ordinaria richiede una revisione esplicita della copia privata.

Backup prima dell’intervento alle **21:53**, 358 file privati e 140 pubblici oltre ai manifest; snapshot successivo alle **22:07**, 366 privati e 147 pubblici. Le copie private sono conservate separatamente su Raspberry/PC e soltanto l’export sanificato entra nel repository. Lo snapshot comprende codice/profilo/unit del servizio, ma non il suo archivio di candidati o il registro persistente. [Backup aggiornato e limiti di recupero](../operations/allsky-configuration-backup.md).

Le prove isolate hanno verificato un candidato sintetico, assenza di modifica ai JPEG sorgenti, riavvio senza duplicati, reset per divario temporale e blocco degli effetti esterni. L’unit reale ha verificato tre scritture negate ai file di produzione, socket IPv4 bloccato e stato non leggibile dall’utente web; sono stati elaborati nuovi fotogrammi prima e dopo un riavvio del solo servizio privato. Il servizio ordinario conserva l’avvio delle **19:23:47** del §27.36, senza interruzione per questo intervento; checksum di settings, flusso notturno, maschera e mappa/controller invariati. La classificazione scientifica e il comportamento su un riavvio fisico restano da validare. La galleria pubblica e i contatori precedenti continuano a dipendere dal rilevatore ordinario.
