# Capitolo 8 – Sistema ottico Celestron C8 XLT

**Codice documento:** DSG-TM-001-08  
**Revisione:** 0.3 Draft consolidato  
**Sistema:** Ottica ad alta focale

## 8.1 Scopo

Il capitolo documenta il Celestron C8 XLT impiegato a Digital StarGate, la configurazione ottica con riduttore 0,63×, il fuocheggiatore Pegasus FocusCube, le camere compatibili, le procedure di collimazione, messa a fuoco, verifica del backfocus e manutenzione.

## 8.2 Caratteristiche principali

| Parametro | Valore |
|---|---|
| Schema | Schmidt-Cassegrain |
| Diametro | 203 mm |
| Focale nominale | 2032 mm |
| Rapporto focale nominale | f/10 |
| Riduttore operativo | 0,63× |
| Focale operativa indicativa | circa 1260–1280 mm |
| Fuocheggiatore | Pegasus FocusCube |
| Installazione | Su CGX-L |

> **DA VALIDARE:** anno e numero di serie, modello esatto del riduttore, distanza riduttore-sensore e focale reale misurata dal plate solving.

## 8.3 Impiego previsto

Il C8 è utilizzato principalmente per:

- galassie;
- nebulose planetarie;
- ammassi globulari;
- resti di supernova compatti;
- soggetti con piccola o media dimensione angolare;
- riprese lunari e, con configurazioni dedicate, planetarie.

## 8.4 Architettura del treno ottico

```text
Lastra correttrice
      ↓
Specchio primario mobile
      ↓
Specchio secondario
      ↓
Riduttore 0,63×
      ↓
Adattatori / OAG / ruota filtri
      ↓
Camera
```

Il treno reale deve essere documentato in ordine meccanico, con spessori e filetti di ogni elemento.

## 8.5 Campionamento

La scala d’immagine può essere stimata con:

```text
scala [arcsec/pixel] = 206,265 × pixel [µm] / focale [mm]
```

Per la QHY695A con pixel da circa 4,54 µm e focale di 1260 mm, la scala nativa è indicativamente 0,74 arcsec/pixel. In BIN2 la scala effettiva è circa 1,49 arcsec/pixel.

Questi valori devono essere verificati con la focale effettiva ottenuta dal plate solving.

### Indicazioni operative

- BIN1: solo con seeing molto buono, guida stabile e obiettivi che richiedono massima risoluzione;
- BIN2: configurazione frequentemente preferibile per aumentare rapporto segnale/rumore e coerenza con il seeing tipico;
- la scelta deve basarsi su seeing, FWHM, target e obiettivo scientifico/fotografico.

## 8.6 Riduttore e backfocus

Il riduttore modifica focale, campo, luminosità e curvatura residua. La distanza ottica deve essere misurata dalla superficie di riferimento del riduttore al piano del sensore.

### Sintomi di distanza non corretta

- stelle allungate ai bordi;
- campo non uniformemente corretto;
- riduzione reale diversa da quella attesa;
- difficoltà a ottenere fuoco e ortogonalità.

### Procedura DSG-PROC-008-01 – Verifica del backfocus

1. montare il treno ottico completo;
2. acquisire un campo stellare ricco prossimo allo zenit;
3. verificare fuoco e guida;
4. analizzare centro e quattro angoli;
5. distinguere tilt da errore simmetrico di backfocus;
6. modificare gli spessori con incrementi piccoli e documentati;
7. ripetere l’acquisizione nelle stesse condizioni;
8. registrare configurazione e risultato.

## 8.7 Messa a fuoco con FocusCube

Il FocusCube agisce sul sistema di messa a fuoco del C8. Devono essere definiti:

- posizione zero o riferimento;
- intervallo operativo;
- step size;
- backlash in/out;
- direzione preferenziale di avvicinamento;
- curve di autofocus per filtro e temperatura.

### Procedura DSG-PROC-008-02 – Autofocus

1. attendere un adeguato acclimatamento termico;
2. puntare un campo con numero sufficiente di stelle;
3. selezionare il filtro di riferimento;
4. eseguire la routine di autofocus;
5. verificare forma e simmetria della curva;
6. rifiutare curve influenzate da nuvole, vento o seeing molto variabile;
7. acquisire un frame di verifica;
8. registrare posizione, temperatura e FWHM.

## 8.8 Mirror shift e stabilità

Il movimento dello specchio primario può introdurre spostamenti durante il fuoco o il cambio di orientamento. Per ridurne gli effetti:

- mantenere una direzione finale costante del fuoco;
- applicare correttamente il backlash;
- evitare grandi movimenti non necessari durante la sequenza;
- eseguire plate solving dopo eventi che possono modificare il centraggio;
- verificare periodicamente il serraggio del FocusCube.

## 8.9 Collimazione

La collimazione deve essere verificata con l’intero sistema termicamente stabilizzato.

### Procedura DSG-PROC-008-03 – Controllo della collimazione

1. scegliere una stella luminosa ma non saturata, prossima allo zenit;
2. centrarla accuratamente;
3. verificare l’immagine intra ed extra focale;
4. regolare il secondario con movimenti minimi;
5. ricentrare dopo ogni regolazione;
6. concludere con verifica a fuoco e, se possibile, valutazione della figura di diffrazione;
7. registrare data, condizioni e interventi.

> **ATTENZIONE:** non eseguire regolazioni importanti da remoto senza controllo visivo e senza la possibilità di ripristinare la configurazione precedente.

## 8.10 Gestione termica

Il C8 richiede tempo per ridurre le differenze tra temperatura interna ed esterna. Una mancata stabilizzazione può produrre:

- stelle meno incise;
- FWHM elevato;
- plume termici;
- autofocus variabile;
- falsa diagnosi di collimazione errata.

Aprire la copertura con anticipo sufficiente quando le condizioni lo consentono e monitorare l’andamento del fuoco durante la notte.

## 8.11 Configurazioni operative

| ID | Camera | Filtri | Binning | Utilizzo |
|---|---|---|---|---|
| DSG-CONF-C8-01 | QHY695A | LRGB | BIN2 preferenziale | Galassie e ammassi |
| DSG-CONF-C8-02 | QHY695A | SHO | BIN2 | Nebulose compatte |
| DSG-CONF-C8-03 | ToupTek 294MC Pro | L-Pro/L-Extreme | DA VALIDARE | OSC |

## 8.12 KPI ottici

| KPI | Metodo | Valore di riferimento |
|---|---|---|
| FWHM mediano | Analisi subframe | DA VALIDARE per stagione |
| Eccentricità | Analisi subframe | DA VALIDARE |
| Focale effettiva | Plate solving | DA VALIDARE |
| Drift del fuoco | Posizione/temperatura | DA VALIDARE |
| Campo corretto | Analisi bordi | Nessuna deformazione sistematica evidente |

## 8.13 Troubleshooting

### Stelle allungate in tutto il campo

- verificare guida e tracking;
- controllare vento e vibrazioni;
- verificare flessioni e serraggi;
- controllare tempo di posa rispetto alle prestazioni di guida.

### Stelle deformate solo ai bordi

- verificare backfocus;
- distinguere errore simmetrico da tilt;
- controllare riduttore e adattatori;
- verificare ortogonalità della camera.

### FWHM elevato

- controllare seeing e quota target;
- attendere acclimatamento;
- eseguire autofocus;
- verificare collimazione;
- verificare condensa o trasparenza del cielo.

### Autofocus irregolare

- controllare backlash e serraggi;
- aumentare il numero di stelle o l’esposizione autofocus;
- evitare campi poveri;
- verificare il FocusCube e la connessione USB.

## 8.14 FMEA sintetica

| Modo di guasto | Effetto | Rilevazione | Mitigazione |
|---|---|---|---|
| Collimazione degradata | Perdita risoluzione | Star test, FWHM | Controllo periodico |
| Backfocus errato | Stelle deformate ai bordi | Analisi angoli | Spessori documentati |
| Mirror shift | Spostamento e fuoco variabile | Plate solve e log focus | Direzione finale costante |
| Condensa | Perdita segnale | Ispezione e immagini | Fascia anticondensa da validare |
| FocusCube allentato | Autofocus fallito | Curva anomala | Controllo meccanico |

## 8.15 Manutenzione

### Prima delle campagne importanti

- verifica collimazione;
- controllo riduttore e adattatori;
- test autofocus;
- verifica cavi e bilanciamento.

### Semestrale

- ispezione superfici esterne;
- controllo serraggi;
- verifica del treno ottico e del backfocus;
- aggiornamento delle curve di fuoco se necessario.

### Annuale

- verifica completa delle prestazioni;
- confronto FWHM con storico;
- ispezione della lastra e pulizia solo se necessaria;
- revisione configurazione e inventario.

## 8.16 Dati da validare

- numero di serie e anno del C8;
- modello riduttore;
- backfocus nominale e reale;
- focale effettiva misurata;
- configurazione FocusCube, step e backlash;
- presenza e gestione anticondensa;
- FWHM ed eccentricità tipici.
