# Capitolo 10 – Camere astronomiche, filtri e treno ottico

**Codice documento:** DSG-TM-001-10  
**Revisione:** 0.3 Draft consolidato  
**Sistema:** Acquisizione scientifica e fotografica

## 10.1 Scopo

Il capitolo descrive le camere principali QHY695A e ToupTek 294MC Pro, le camere di guida, i filtri, la ruota portafiltri, l’OAG, i fuocheggiatori, i flat panel Wanderer Cover V4 e le configurazioni standard del treno ottico.

L’obiettivo è rendere ogni configurazione riproducibile e verificabile nel tempo.

## 10.2 Inventario delle camere

### 10.2.1 QHY695A

| Parametro | Dato |
|---|---|
| Tecnologia | CCD monocromatica |
| Sensore | Sony ICX695 |
| Dimensione pixel | circa 4,54 µm |
| Raffreddamento | Termoelettrico |
| Uso principale | LRGB e SHO |
| Configurazioni | C8 e Quattro |

> **DA VALIDARE:** risoluzione esatta, firmware, driver, numero di serie, setpoint operativo e modalità di binning effettivamente utilizzate.

### 10.2.2 ToupTek 294MC Pro

| Parametro | Dato |
|---|---|
| Tecnologia | CMOS a colori raffreddata |
| Sensore | Famiglia IMX294 |
| Raffreddamento | Termoelettrico |
| Uso principale | OSC broadband e dual narrowband |
| Filtri | L-Pro, L-Extreme |
| Configurazioni | C8 e Quattro |

> **DA VALIDARE:** modello commerciale esatto, dimensione pixel, modalità readout, gain/offset, numero di serie e driver.

### 10.2.3 Camere di guida

Nel sistema risultano utilizzate o disponibili camere quali QHY8IIM, ASI120Mini e ASI290MC. L’associazione effettiva ai profili PHD2 deve essere censita.

| Camera | Uso previsto | Configurazione | Stato |
|---|---|---|---|
| QHY8IIM | Guida/OAG | DA VALIDARE | DA VALIDARE |
| ASI120Mini | Guida/OAG | DA VALIDARE | DA VALIDARE |
| ASI290MC | AllSky o guida | AllSky dichiarato | Da separare per ruolo |

## 10.3 Filtri

### Monocromatico

- Luminanza;
- Rosso;
- Verde;
- Blu;
- Hα;
- OIII;
- SII.

### One Shot Color

- L-Pro;
- L-Extreme.

Per ogni filtro devono essere registrati produttore, diametro/formato, posizione nella ruota, offset di fuoco e data di installazione.

| Posizione | Filtro | Tipo | Offset fuoco | Note |
|---|---|---|---:|---|
| 1 | L | Broadband | DA VALIDARE | QHY695A |
| 2 | R | Broadband | DA VALIDARE | QHY695A |
| 3 | G | Broadband | DA VALIDARE | QHY695A |
| 4 | B | Broadband | DA VALIDARE | QHY695A |
| 5 | Hα | Narrowband | DA VALIDARE | QHY695A |
| 6 | OIII | Narrowband | DA VALIDARE | QHY695A |
| 7 | SII | Narrowband | DA VALIDARE | QHY695A |

## 10.4 Componenti del treno ottico

- telescopio;
- riduttore o correttore;
- adattatori filettati;
- fuocheggiatore;
- rotatore, se presente;
- OAG o guida separata;
- ruota portafiltri;
- distanziali;
- tilt plate;
- camera principale;
- cablaggi dati e alimentazione.

Ogni configurazione deve essere documentata con una distinta base e un diagramma quotato.

## 10.5 Configurazioni standard

### DSG-CONF-001 – C8 / QHY695A / LRGB

- C8 XLT;
- riduttore 0,63×;
- Pegasus FocusCube;
- OAG o sistema guida da validare;
- ruota LRGB;
- QHY695A;
- BIN2 preferenziale.

### DSG-CONF-002 – C8 / QHY695A / SHO

- configurazione meccanica analoga;
- filtri Hα, OIII, SII;
- esposizioni lunghe;
- offset di fuoco per filtro;
- librerie dark dedicate.

### DSG-CONF-003 – Quattro / ToupTek 294MC Pro

- Quattro 200P;
- ESATTO 2";
- correttore/riduttore;
- filtro L-Pro o L-Extreme;
- camera OSC;
- guida da censire.

### DSG-CONF-004 – Quattro / QHY695A / SHO

- Quattro 200P;
- ESATTO 2";
- correttore/riduttore;
- OAG/ruota filtri;
- QHY695A;
- filtri SHO.

## 10.6 Gestione meccanica

Principi:

- preferire connessioni filettate rispetto a innesti a compressione;
- evitare leve eccessive sul fuocheggiatore;
- mantenere il baricentro vicino all’asse;
- serrare senza deformare;
- gestire i cavi per evitare trazione durante slew e flip;
- marcare l’orientamento della camera quando richiesto dai mosaici.

## 10.7 Backfocus

Per ogni configurazione compilare:

| Configurazione | Backfocus nominale | Spessori | Backfocus reale | Esito |
|---|---:|---:|---:|---|
| DSG-CONF-001 | DA VALIDARE | DA VALIDARE | DA VALIDARE | DA VALIDARE |
| DSG-CONF-002 | DA VALIDARE | DA VALIDARE | DA VALIDARE | DA VALIDARE |
| DSG-CONF-003 | DA VALIDARE | DA VALIDARE | DA VALIDARE | DA VALIDARE |
| DSG-CONF-004 | DA VALIDARE | DA VALIDARE | DA VALIDARE | DA VALIDARE |

La misura deve includere la distanza interna degli adattatori e la posizione del piano sensore dichiarata dal costruttore.

## 10.8 Raffreddamento delle camere

### Procedura DSG-PROC-010-01 – Cool-down

1. connettere la camera;
2. verificare che la ventola funzioni;
3. impostare il setpoint approvato;
4. applicare una rampa graduale se disponibile;
5. attendere stabilizzazione della temperatura e della potenza del cooler;
6. verificare assenza di condensa;
7. iniziare l’acquisizione solo dopo stabilità.

### Procedura DSG-PROC-010-02 – Warm-up

1. terminare esposizioni e salvataggi;
2. avviare il riscaldamento graduale;
3. attendere l’avvicinamento alla temperatura ambiente;
4. spegnere il cooler;
5. disconnettere il software;
6. togliere alimentazione solo al termine.

## 10.9 Gain, offset e binning

Ogni profilo deve indicare:

- gain;
- offset;
- modalità readout;
- binning;
- bit depth;
- temperatura;
- durata esposizione;
- filtro.

Non modificare questi parametri senza aggiornare le librerie di calibrazione compatibili.

## 10.10 Librerie di calibrazione

La struttura consigliata:

```text
Calibration/
  Camera/
    Temperature/
      Binning/
        Gain-Offset/
          Exposure/
```

### Dark

Devono corrispondere a camera, temperatura, gain/offset, binning e durata.

### Flat

Devono essere acquisiti senza modificare orientamento, fuoco, filtri o presenza di polvere rispetto ai light.

### Bias / Dark flat

La scelta dipende dalla camera e dal workflow. La compatibilità deve essere verificata sperimentalmente e documentata.

## 10.11 Flat panel Wanderer Cover V4

Sono presenti due unità Wanderer Cover V4. Per ciascuna devono essere censiti:

- telescopio associato;
- porta USB e alimentazione;
- posizione di apertura/chiusura;
- luminosità per filtro;
- tempi di esposizione flat;
- comportamento in caso di disconnessione;
- interazione con la sicurezza della copertura.

### Procedura DSG-PROC-010-03 – Acquisizione flat

1. parcheggiare la montatura nella posizione definita;
2. verificare assenza di interferenze meccaniche;
3. chiudere il flat panel;
4. impostare luminosità per il filtro;
5. eseguire esposizioni di test;
6. verificare istogramma e uniformità;
7. acquisire la serie completa;
8. riaprire il pannello e confermare la posizione.

## 10.12 Metadati e nomenclatura

Ogni FITS deve contenere, per quanto disponibile:

- target;
- data e ora UTC;
- filtro;
- esposizione;
- gain/offset;
- binning;
- temperatura sensore;
- telescopio e focale;
- camera;
- coordinate;
- sessione e configurazione.

Nomenclatura consigliata:

```text
TARGET_DATE_CONFIG_FILTER_EXPOSURE_BIN_TEMP_SEQUENCE.fits
```

## 10.13 Procedura DSG-PROC-010-04 – Cambio configurazione

1. mettere montatura e copertura in sicurezza;
2. disalimentare le periferiche interessate;
3. fotografare la configurazione esistente;
4. etichettare e scollegare cavi/adattatori;
5. montare il nuovo treno secondo distinta base;
6. verificare backfocus e orientamento;
7. aggiornare bilanciamento;
8. aggiornare profilo N.I.N.A. e PHD2;
9. eseguire test di connessione, autofocus, plate solving e guida;
10. aggiornare registro configurazioni.

## 10.14 KPI

| KPI | Descrizione | Obiettivo |
|---|---|---|
| Stabilità temperatura | Scostamento dal setpoint | DA VALIDARE |
| Frame persi | Errori download | 0 |
| Ripetibilità flat | Media ADU e forma istogramma | DA VALIDARE |
| Tilt | Differenza angoli | Minima |
| Backfocus | Qualità stelle ai bordi | Validato |
| Autofocus riusciti | Percentuale | ≥ 98% |

## 10.15 Troubleshooting

### Camera non connessa

- verificare alimentazione e USB;
- controllare driver e presenza in Gestione dispositivi;
- chiudere software che mantiene la camera occupata;
- provare il software nativo del produttore;
- non cambiare contemporaneamente porta, cavo e driver.

### Condensa o ghiaccio

- interrompere il raffreddamento;
- eseguire warm-up graduale;
- verificare essiccante e tenuta secondo manuale del produttore;
- controllare umidità e setpoint;
- non aprire la camera senza procedura approvata.

### Download lento o frame corrotti

- verificare cavo USB e banda condivisa;
- controllare hub e porte;
- ridurre USB traffic se supportato;
- controllare spazio e prestazioni SSD;
- esaminare log del driver.

### Flat non correggono

- verificare che la configurazione non sia cambiata;
- controllare orientamento e polvere;
- verificare saturazione e linearità;
- controllare filtro e luminosità del pannello;
- verificare il corretto master e workflow.

## 10.16 FMEA sintetica

| Modo di guasto | Effetto | Rilevazione | Mitigazione |
|---|---|---|---|
| Camera disconnessa | Interruzione acquisizione | Driver/log | Cavi stabili e recovery |
| Condensa | Frame inutilizzabili/danno | Ispezione immagini | Setpoint e warm-up controllati |
| Backfocus errato | Bordi degradati | Analisi stelle | Distinta spessori |
| Ruota filtri fuori posizione | Filtro errato | Header/immagine | Homing e verifica posizione |
| Flat panel bloccato | Collisione o flat errati | Sensore/stato | Test e interlock |
| Libreria calibrazione errata | Artefatti | Analisi preprocessing | Nomenclatura e metadati |

## 10.17 Manutenzione

### Mensile

- controllo cavi, ventole e connettori;
- verifica raffreddamento;
- test ruota filtri e flat panel;
- verifica librerie di calibrazione.

### Trimestrale

- controllo essiccante secondo necessità e indicazioni del produttore;
- revisione dark library;
- test completo delle configurazioni;
- verifica backfocus/tilt con campo stellare.

### Annuale

- aggiornamento inventario e seriali;
- revisione driver e firmware;
- pulizia esterna e ispezione sensore/finestra senza apertura non autorizzata;
- collaudo di tutte le configurazioni standard.

## 10.18 Dati da validare

- modelli e seriali delle camere;
- dimensioni pixel e modalità readout effettive;
- gain, offset, setpoint e binning standard;
- associazione delle camere di guida;
- modello e posizioni della ruota filtri;
- backfocus e distinta spessori;
- luminosità flat per filtro;
- nomenclatura e percorsi definitivi dei dati.
