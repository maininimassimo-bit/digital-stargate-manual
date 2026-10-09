# Capitolo 22 – Inventario tecnico e Asset Management

**Codice documento:** DSG-TM-001-22  
**Revisione:** 0.2 — aggiornamento Allsky 09/10/2026

## 22.1 Scopo

Questo capitolo definisce l'inventario ufficiale dei componenti dell'osservatorio e le regole per la gestione del loro ciclo di vita.

## 22.2 Categorie di asset

- struttura e cupola;
- alimentazione e rete;
- computer e storage;
- montatura;
- ottiche;
- camere;
- filtri e ruote portafiltri;
- fuocheggiatori;
- sensori e accessori;
- software, licenze e firmware.

## 22.3 Codifica asset

Formato:

```text
DSG-<CATEGORIA>-<NUMERO>
```

Esempi:

```text
DSG-NET-001
DSG-PC-001
DSG-MNT-001
DSG-OTA-001
DSG-CAM-001
```

## 22.4 Scheda asset minima

| Campo | Descrizione |
|---|---|
| Asset ID | identificativo univoco |
| Produttore | marca |
| Modello | modello commerciale |
| Numero di serie | seriale |
| Data installazione | data messa in servizio |
| Posizione | ubicazione fisica |
| Firmware | versione |
| Driver | versione |
| Stato | operativo, riserva, guasto, dismesso |
| Ultima manutenzione | data |
| Prossima manutenzione | data |

## 22.5 Inventario iniziale

| Asset ID | Componente | Modello | Stato |
|---|---|---|---|
| DSG-NET-001 | Connettività/router primario | Starlink, servizio residenziale con IP condiviso | Operativo; ingresso Internet Allsky tramite servizio separato in preparazione |
| DSG-NET-002 | Router failover/VPN | Teltonika RUT955, firmware RUT9XX_R_00.06.09.5 | Operativo; nuovo tunnel Allsky da collaudare end-to-end |
| DSG-PC-001 | Computer di controllo | PrimaLuceLab EAGLE3 | Operativo |
| DSG-PC-002 | Computer Allsky | Raspberry Pi 4 Model B Rev 1.2, RAM 4 GB | Acquisizione e sito locale operativi, verificati 09/10/2026 |
| DSG-MNT-001 | Montatura | Celestron CGX-L | Operativo |
| DSG-OTA-001 | Telescopio | Celestron C8 XLT | Operativo |
| DSG-OTA-002 | Telescopio | Sky-Watcher Quattro 200P | Operativo |
| DSG-CAM-001 | Camera mono | QHY695A | Operativo |
| DSG-CAM-002 | Camera OSC | ToupTek 294MC Pro | Operativo |
| DSG-CAM-003 | Camera Allsky | ZWO ASI290MC, fotogramma 1936 × 1096 pixel | Operativa, verificata 09/10/2026 |
| DSG-OPT-001 | Ottica Allsky | Fisheye 1,8 mm | Confermata fisicamente dall'Owner il 09/10/2026 |
| DSG-FOC-001 | Fuocheggiatore | Pegasus FocusCube | Operativo |
| DSG-FOC-002 | Fuocheggiatore | ESATTO 2" | Operativo |

### 22.5.1 Baseline Allsky e servizi associati

Gli identificativi Allsky sono assegnati in questo aggiornamento documentale. Seriali e date originali di installazione non sono stati acquisiti; la data di verifica non equivale alla data di acquisto o messa in servizio. L'indicazione precedente di ottica Allsky da 8 mm è sostituita da 1,8 mm, riscontrata nella configurazione e confermata fisicamente dall'Owner.

| Categoria | Configurazione / stato al 09/10/2026 |
|---|---|
| Sistema operativo DSG-PC-002 | Raspberry Pi OS / Raspbian 11 Bullseye, userland armhf e kernel aarch64 |
| Applicazione Allsky | AllskyTeam/allsky v2026.10.01, aggiornata il 09/10/2026 |
| Dipendenza corretta | NumPy 1.24.4; importazioni SciPy/OpenCV/Astropy verificate |
| Rete RUT955 | Nuovo profilo OpenVPN `allskyip`; tunnel RMS esistente conservato |
| Ingresso Internet | IPStatico PRO condiviso; regole di pubblicazione e verifica esterna ancora da completare |
| Nome pubblico | dynDNS.it, hostname corrente dell'osservatorio; dettagli di accesso riservati |
| Certificato | RapidSSL, copertura acquistata per un anno; CSR inviato, emissione ancora pendente all'ultima verifica |
| Componenti fisici non censiti | Alimentatore, scheda/storage, contenitore e riscaldatore: modello, capacità, potenza e seriale da verificare |

I servizi di rete e il certificato sono dipendenze operative, non nuovi asset hardware. Nessuna chiave privata, credenziale, indirizzo LAN, coordinata precisa o numero di serie è incluso in questa scheda pubblica. Procedura, backup e attività residue: [Capitolo 27 — Sistema Allsky](27-sistema-allsky.md).

## 22.6 Procedura DSG-PROC-022-01 – Inserimento nuovo asset

1. Assegnare Asset ID.
2. Registrare dati tecnici e seriale.
3. Fotografare il componente e l'etichetta.
4. Registrare firmware e driver.
5. Associare manuali e file di configurazione.
6. Pianificare manutenzione.
7. Aggiornare il repository.

## 22.7 Ciclo di vita

Stati previsti:

```text
ACQUISTATO -> IN TEST -> OPERATIVO -> IN MANUTENZIONE -> RISERVA -> DISMESSO
```

## 22.8 Ricambi critici

Devono essere identificati i ricambi con elevato impatto sulla continuità operativa:

- alimentatori 12 V;
- cavi USB e di rete;
- fusibili e protezioni;
- adattatori meccanici;
- supporti di archiviazione;
- SIM di backup;
- sensori di finecorsa.

## 22.9 KPI

| KPI | Descrizione |
|---|---|
| Asset censiti | % sul totale |
| Asset con seriale registrato | % |
| Asset con firmware noto | % |
| Asset oltre manutenzione | Numero |
| Ricambi critici disponibili | % |

## 22.10 Dati da validare

> **DA VALIDARE:** numeri di serie e date di installazione.

> **DA VALIDARE:** disponibilità e posizione dei ricambi critici.

## 22.11 Registro revisioni

| Revisione | Data | Modifica |
|---|---|---|
| 0.1 | Baseline precedente | Inventario iniziale |
| 0.2 | 09/10/2026 | Raspberry, camera e ottica Allsky censiti; firmware router e dipendenze software/rete aggiornati con limiti di verifica |
