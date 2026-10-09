# Capitolo 27 – Sistema AllSky

**Codice documento:** DSG-TM-001-27  
**Revisione:** 0.7 — pannelli esterni, meteo locale e informazioni astronomiche 09/10/2026
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
| software | AllskyTeam/allsky v2026.10.01, aggiornato il 09/10/2026 |
| fotogramma | 1936 × 1096 pixel |
| directory applicazione | `/home/pi/allsky` |
| sito locale | `/home/pi/allsky/html/allsky`, pagina `/allsky/index.php` |

I dati derivano dalla verifica del sistema e della configurazione effettuata il 09/10/2026. Indirizzi LAN, coordinate precise, seriali, credenziali e chiavi private restano nella documentazione operativa riservata e non sono pubblicati nel manuale.

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
