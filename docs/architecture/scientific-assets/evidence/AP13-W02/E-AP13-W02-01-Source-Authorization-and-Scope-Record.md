# E-AP13-W02-01 — Source Authorization and Scope Record

| Campo | Valore |
|---|---|
| Architecture Package | AP-013 — Scientific Image Repository Architecture |
| Work item | AP13-W02 — Current-State Scientific Asset Inventory |
| Evidence ID | E-AP13-W02-01 |
| Titolo | Source Authorization and Scope Record |
| Data | 04/08/2026 |
| Owner / approver | Massimo Mainini |
| Stato | Approved for discovery design and P0/P1 preparation; connectivity verification pending |
| Modalità autorizzata | Read-only discovery and metadata inventory only |

## 1. Decisione

È approvata la preparazione dell'inventario scientifico corrente e dell'automazione di trasferimento per le sorgenti e destinazioni descritte in questo record.

L'approvazione consente esclusivamente:

- discovery P0 delle sorgenti e dei volumi;
- inventario P1 dei metadata di filesystem;
- progettazione e dry-run degli script;
- verifica di raggiungibilità e accesso SMB;
- creazione di manifest e report senza modifica degli asset.

Non sono ancora autorizzati:

- cancellazione o spostamento automatico dei file dall'EAGLE;
- hashing completo P4;
- modifica dei RAW o dei metadata FITS/XISF;
- deduplication o consolidamento automatico;
- riorganizzazione dell'archivio storico D:;
- migrazione dei file già presenti;
- accesso a dispositivi fisici dell'osservatorio;
- credenziali privilegiate in script NINA, PixInsight o PowerShell.

## 2. Sorgente di acquisizione EAGLE

| Campo | Valore verificato |
|---|---|
| Source ID | `SRC-EAGLE30154-NINA-001` |
| Nome logico | EAGLE NINA Acquisition Source |
| Host | `EAGLE30154` |
| Hardware | Intel NUC7CJYH |
| Sistema operativo | Microsoft Windows 10 Enterprise LTSC, build 17763 |
| Root sorgente | `D:\Images NINA\Target` |
| Path esistente | Sì |
| Filesystem | NTFS |
| Tipo volume | Fixed |
| Capacità rilevata | 735304478720 byte |
| Spazio libero rilevato | 358237487104 byte |
| Collection profile iniziale | `P0 + P1` |
| Access mode | `READ_ONLY` per discovery e inventory |
| Owner | Massimo Mainini |

### 2.1 Rete osservata

| Interfaccia | IPv4 | Uso candidato |
|---|---|---|
| Ethernet 2 | `192.168.1.144/24` | percorso preferito per il trasferimento, da verificare |
| Wi-Fi 2 | `192.168.1.184/24` | percorso alternativo, non preferito |
| Local Area Connection* 11 | `192.168.137.1/24` | non incluso nel percorso di trasferimento iniziale |

La raggiungibilità del nome host, dell'indirizzo Ethernet e della porta SMB TCP 445 deve essere ancora verificata dal PC principale.

### 2.2 Modello dei file NINA osservato

I campioni reali nella root sorgente seguono il pattern operativo:

```text
IMAGETYPE_BINNING_EXPOSURETIMEs_GAIN_OFFSET_TARGETNAME_TELESCOPE__SENSORTEMPC_FILTER_FRAMENR_DATETIME_FWHM_FWHM_Fok_FOCUSERPOSITION.xisf
```

Esempio osservato:

```text
LIGHT_1x1_600.00s_910_99_LDN 1320_Skywatcher quattro 200p__-10.00C_LPRO_0163_2026-07-17_04-16-06_FWHM_5.77_Fok_116189.xisf
```

Il parser dovrà gestire target e telescopio con spazi, temperature negative, esposizioni decimali, filtri, date che attraversano la mezzanotte e sessioni distribuite su più notti.

## 3. Finestra operativa autorizzata

| Campo | Valore |
|---|---|
| EAGLE acceso dopo la sessione | Sì |
| Spegnimento normale | circa 08:30 ora locale |
| NINA in acquisizione durante la copia | No |
| Finestra preferita | 07:30–08:30 ora locale |
| Avvio operativo raccomandato | non prima delle 07:35 |
| Ultimo avvio raccomandato di un nuovo trasferimento | 08:10 |
| Termine massimo raccomandato | 08:25 |

Lo script dovrà rifiutare l'avvio quando:

- NINA risulta ancora in acquisizione;
- uno o più file sono ancora aperti o aumentano di dimensione;
- l'ultimo file non è stabile da almeno 10 minuti, salvo diversa configurazione approvata;
- la destinazione non è disponibile;
- lo spazio libero è insufficiente;
- il tempo residuo non è sufficiente a completare in sicurezza l'operazione.

## 4. PC principale

| Campo | Valore verificato |
|---|---|
| Host | `WIN-QOOF3903TQS` |
| Sistema operativo | Microsoft Windows 11 Pro, build 26200 |
| PowerShell | 5.1.26100.8972 |
| Rete candidata verso EAGLE | `vEthernet (DSG-Internet)` — `192.168.1.145/24` |
| Owner | Massimo Mainini |

Il PC principale è il nodo designato per prelevare i file dall'EAGLE e scrivere sugli storage locali. L'EAGLE non riceverà accesso di scrittura generale all'archivio.

## 5. Storage autorizzati e ruoli approvati

### 5.1 Volume D — archivio storico

| Campo | Valore |
|---|---|
| Drive letter osservata | `D:` |
| Volume label | `Elements` |
| Disco fisico | WD Elements 2621 |
| Bus | USB |
| Filesystem | NTFS |
| Capacità | 2000363188224 byte |
| Spazio libero rilevato | 54798868480 byte |
| Ruolo approvato | Archivio storico |
| Modifiche automatiche | Proibite nella fase iniziale |

Il volume contiene numerosi target storici già organizzati. Non sarà usato come destinazione primaria delle nuove sessioni e non sarà riorganizzato automaticamente.

### 5.2 Volume F — archivio attivo

| Campo | Valore |
|---|---|
| Drive letter osservata | `F:` |
| Volume label | `Elements` |
| Disco fisico | WD Elements 2620 |
| Bus | USB |
| Filesystem | NTFS |
| Capacità | 2000363188224 byte |
| Spazio libero rilevato | 1742603403264 byte |
| Ruolo approvato | Archivio attivo per le nuove sessioni |
| Selezione iniziale | Destinazione primaria |

La prima implementazione userà F: come destinazione candidata, ma dovrà verificare l'identità del volume tramite label e, quando possibile, seriale del disco; non dovrà affidarsi esclusivamente alla lettera assegnata da Windows.

### 5.3 Volume E — calibration library

| Campo | Valore |
|---|---|
| Drive letter osservata | `E:` |
| Filesystem | NTFS |
| Capacità | 320067334144 byte |
| Spazio libero rilevato | 80801910784 byte |
| Contenuti osservati | `Dark_695A`, `Dark_atr294c`, `Light archiviati` |
| Ruolo approvato | Calibration Library |

La struttura target della libreria sarà progettata per camera, temperatura, gain, offset, binning e tipo di calibrazione. La migrazione delle librerie esistenti non è autorizzata in questa fase.

## 6. Struttura target approvata per le nuove sessioni

La struttura iniziale conserva il modello corrente basato sul target:

```text
<ArchiveRoot>\<Target>\
├── Light\
├── Dark\
├── Flat\
├── Bias\
├── DarkFlat\
├── 12_Processing\
└── _Inventory\
```

Per sessioni distribuite su più notti, la baseline progettuale prevede una suddivisione opzionale per data sotto le cartelle di frame:

```text
<Target>\Light\YYYY-MM-DD\
```

La scelta definitiva della root fisica su F: e la regola completa per le sessioni multi-night saranno validate nel dry-run.

## 7. Libreria di calibrazione approvata come target design

Struttura candidata:

```text
<CalibrationRoot>\
└── <Camera>\
    └── <Temperature>\
        └── Gain_<Gain>_Offset_<Offset>\
            └── Bin_<Binning>\
                ├── Dark\
                ├── Flat\
                ├── DarkFlat\
                └── Bias\
```

Durante il pilot:

- i file di calibrazione non saranno rimossi dalla sessione sorgente;
- nessun file esistente su E: sarà spostato;
- la classificazione sarà prima verificata in dry-run;
- eventuali collisioni o duplicati saranno soltanto segnalati.

## 8. Componenti software approvati per la progettazione

| Componente | Responsabilità | Stato |
|---|---|---|
| `DSG-SessionImporter.ps1` | parsing nomi NINA, creazione struttura target, manifest e copia controllata | Design approved; not implemented |
| `DSG-CalibrationOrganizer.ps1` | classificazione e proposta di organizzazione delle calibrazioni | Design approved; not implemented |
| `DSG-Inventory.ps1` | inventario, manifest, statistiche, duplicate report e evidence | Design approved; not implemented |
| Digital StarGate Scientific Data Manager | catalogo futuro interrogabile di sessioni, target, strumenti, processing e pubblicazioni | Architecture concept approved; not implemented |

## 9. Regole di sicurezza del pilot

1. Prima esecuzione esclusivamente in `-WhatIf` / dry-run.
2. Nessuna cancellazione dalla sorgente EAGLE.
3. Nessuna sovrascrittura silenziosa.
4. Ogni collisione produce stato `CONFLICT` o `DUPLICATE_CANDIDATE`.
5. La copia reale, quando autorizzata, avverrà prima in una directory di staging.
6. Numero file e byte saranno verificati prima della pubblicazione nella destinazione finale.
7. Gli hash completi non saranno obbligatori nel primo pilot; potranno essere abilitati su un campione.
8. Ogni run produrrà manifest, log, summary ed evidence checksums.
9. Il failure di rete, storage o tempo residuo non comporterà cancellazioni o cleanup.
10. La sorgente EAGLE resterà autorevole fino alla verifica completata della copia.

## 10. Elementi ancora pendenti

- test DNS/hostname `EAGLE30154` dal PC principale;
- test ping verso hostname e `192.168.1.144`;
- test TCP 445 SMB;
- definizione della share read-only dell'EAGLE;
- identificazione della root definitiva su F:;
- decisione finale sul mantenimento o uso delle sottocartelle per data;
- regola definitiva per i file dopo copia verificata;
- scelta sulla sanitizzazione dei path nelle evidence GitHub;
- creazione e test degli script;
- esecuzione del dry-run su una sessione campione;
- review indipendente dei risultati.

## 11. Disposizione

Il source scope e i ruoli degli storage sono approvati per la progettazione e per le verifiche P0/P1.

La raccolta reale, la copia dei file e la creazione automatica delle cartelle non sono ancora autorizzate. Il prossimo step è verificare la connettività PC principale → EAGLE e predisporre una share controllata in sola lettura per il pilot.
