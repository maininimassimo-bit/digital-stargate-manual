# Capitolo 27 – Sistema AllSky

**Codice documento:** DSG-TM-001-27  
**Revisione:** 0.4 — integrazione nel portale 09/10/2026
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

- Logo e titolo Digital Stargate; overlay superiore sinistro con data/ora, esposizione, guadagno, temperatura camera e fase lunare.
- Overlay inferiore sinistro con temperatura CPU Raspberry, utilizzo RAM, spazio libero e uptime, senza sostituire quello superiore.
- Overlay personalizzato in `config/overlay/config/overlay-Digital-Stargate.json`; moduli `allsky_pistatus` e `allsky_solarsystem` con aggiornamento periodico ogni 60 secondi. Elevazione impostata a 100 m s.l.m. su indicazione Owner.
- Fotogramma completo mantenendo il rapporto d'aspetto, bordi neri laterali e superiori/inferiori; mappa celeste dimensionata sul cerchio della ripresa e ricollocata secondo i limiti reali dell'immagine visualizzata.
- Orologio della mappa aggiornato al timestamp del fotogramma tramite `Last-Modified`; orientamento regolato sul riferimento solare visibile. Questa regolazione è preliminare e non costituisce calibrazione astrometrica: resta da verificare con stelle riconoscibili.
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
| 0.4 | 09/10/2026 | Documentate anteprime Home/Status, allineamento ai badge, refresh e modalità essenziale; nessuna variazione hardware |
| 0.3 | 09/10/2026 | Retention verificata; tunnel, certificato e HTTPS pubblici collaudati; mappa aggiornata con anteprima non disponibile, residui fisici conservati |

Inventario correlato: [Capitolo 22](22-inventario-asset-management.md).

## 27.18 Anteprime nel portale Digital StarGate

La [Home del portale](../index.md) mostra l’immagine live Allsky nella hero originale. La pagina [Stato osservatorio](../status/index.md) affianca ai badge operativi due riquadri di uguale larghezza: cupola sopra e anteprima Allsky sotto, con bordi superiore e inferiore allineati al gruppo badge. Sugli schermi piccoli i riquadri si dispongono sotto i badge.

L’anteprima usa il JPEG pubblico HTTPS, contiene l’intero fotogramma senza ritagli e richiede una nuova immagine ogni 30 secondi. Il tasto **Allsky** apre il sito completo. **Vista essenziale** sospende gli aggiornamenti e **Attiva il live** li riprende; la preferenza è condivisa con i controlli visuali del portale. L’ora di ultima ricezione è distinta dall’ora di acquisizione mostrata nel fotogramma. Collegamento indisponibile e riprova sono segnalati esplicitamente.

Si tratta di un’anteprima fotografica aggiornata, non di uno stream video continuo o di una fonte Safety Authority. Non modifica l’acquisizione sul Raspberry Pi, le immagini archiviate o i contratti di telemetria. [Dettagli tecnici e manutenzione](../ui/immersive-portal-implementation.md#anteprime-allsky-nella-home-e-in-observatory-status-9-ottobre-2026); [PR e verifiche di pubblicazione](../releases/immersive-portal.md#incremento-anteprime-live-allsky-home-e-status-09102026).
