# Capitolo 28 – Gestione dei dati e archiviazione

**Codice documento:** DSG-TM-001-28  
**Revisione:** 0.1 Draft

## 28.1 Scopo

Questo capitolo definisce il ciclo di vita dei dati prodotti da Digital StarGate, dalla creazione dei file FITS fino alla loro classificazione, verifica, copia, elaborazione e conservazione.

Gli obiettivi sono preservare integrità, reperibilità, tracciabilità e coerenza dei dati osservativi.

## 28.2 Tipologie di dati

| Categoria | Esempi |
|---|---|
| dati scientifici grezzi | light, dark, flat, bias, dark-flat |
| metadati | header FITS, profilo, target, filtro, temperatura |
| log applicativi | N.I.N.A., PHD2, CPWI, ASCOM, Windows |
| dati ambientali | meteo, AllSky, sensori |
| configurazioni | profili, sequenze, driver, parametri |
| prodotti elaborati | master, immagini calibrate, integrazioni finali |
| report | riepilogo sessione, incidenti, manutenzione |

## 28.3 Regole di naming

È raccomandato includere almeno:

```text
DATA_TARGET_TELESCOPIO_CAMERA_FILTRO_EXPOSURE_BIN_TEMPERATURA_PROGRESSIVO.fits
```

Esempio:

```text
2026-07-13_M51_C8_QHY695A_L_300s_BIN2_M10C_001.fits
```

Il naming deve essere coerente con i metadati FITS e non contenere caratteri incompatibili con Windows o strumenti di elaborazione.

## 28.4 Struttura delle cartelle

```text
observations/
  YYYY/
    YYYY-MM-DD_TARGET/
      raw/
        light/
        dark/
        flat/
        bias/
      logs/
      reports/
      processed/
      exports/
```

Per progetti pluriennali o mosaici è possibile aggiungere un livello dedicato al progetto.

## 28.5 Procedura DSG-PROC-028-01 – Chiusura dati di sessione

1. Verificare che tutti i file FITS siano leggibili.
2. Contare le immagini attese e quelle effettive.
3. Verificare la presenza dei log applicativi.
4. Generare il report di sessione.
5. Copiare i dati verso la destinazione primaria di conservazione.
6. Eseguire una verifica di integrità mediante dimensioni, hash o confronto file.
7. Applicare la politica di backup.
8. Marcare la sessione come `ARCHIVED` solo dopo la verifica.

## 28.6 Integrità dei dati

I controlli raccomandati comprendono:

- apertura automatica o campionaria dei FITS;
- verifica dimensione file;
- controllo header essenziali;
- confronto del numero di frame con la sequenza;
- hash SHA-256 per archivi o trasferimenti critici;
- controllo SMART dei supporti di memorizzazione.

## 28.7 Librerie di calibrazione

Le librerie devono essere organizzate per:

- camera;
- gain e offset;
- binning;
- temperatura;
- durata;
- data o intervallo di validità;
- configurazione del treno ottico per flat e dark-flat.

I flat non devono essere riutilizzati dopo modifiche a camera, rotazione, filtri, fuoco, polvere o treno ottico senza una verifica.

## 28.8 Politica di conservazione

| Dato | Conservazione raccomandata |
|---|---|
| light grezzi selezionati | lungo termine |
| master di calibrazione | fino a sostituzione e validazione |
| log di sessione | almeno quanto i dati correlati |
| file intermedi voluminosi | secondo spazio e valore del progetto |
| immagini finali | permanente |
| configurazioni e report | permanente e versionato |

La retention effettiva deve essere definita in base a capacità, valore scientifico e costi di conservazione.

## 28.9 Trasferimento remoto

Per evitare di saturare la connettività:

- privilegiare trasferimenti differiti;
- applicare limiti di banda nelle finestre osservative;
- trasferire prima report e anteprime, poi i FITS;
- usare meccanismi di ripresa del trasferimento;
- non eliminare la copia locale prima della verifica della destinazione.

## 28.10 Protezione dei dati

- applicare almeno due copie su supporti differenti;
- mantenere una copia separata dall'osservatorio;
- evitare che ransomware o cancellazioni possano raggiungere tutte le copie;
- cifrare supporti contenenti credenziali o configurazioni sensibili;
- testare periodicamente il ripristino.

## 28.11 Troubleshooting

| Problema | Azione |
|---|---|
| file FITS corrotto | conservare il file, verificare log e storage, non sovrascrivere |
| disco quasi pieno | sospendere acquisizioni non essenziali e liberare spazio in modo controllato |
| trasferimento interrotto | riprendere con verifica hash |
| header incompleto | verificare profilo N.I.N.A. e driver camera |
| duplicati | usare naming univoco e report di inventario |
| calibrazione non compatibile | ricreare la libreria corretta |

## 28.12 KPI

| KPI | Descrizione |
|---|---|
| esposizioni valide | percentuale rispetto alle acquisite |
| sessioni archiviate correttamente | percentuale mensile |
| errori di integrità | numero per trimestre |
| tempo medio di trasferimento | per sessione o GB |
| spazio disponibile | giorni stimati residui |
| ripristini testati | numero e percentuale di successo |

## 28.13 Checklist archiviazione

- [ ] frame conteggiati;
- [ ] FITS leggibili;
- [ ] header verificati;
- [ ] log presenti;
- [ ] report generato;
- [ ] copia primaria completata;
- [ ] copia secondaria completata;
- [ ] integrità verificata;
- [ ] sessione marcata ARCHIVED.

## 28.14 Dati da validare

> **DA VALIDARE:** percorsi reali di salvataggio sull'EAGLE e sui sistemi esterni.

> **DA VALIDARE:** capacità dei dischi, soglie di spazio e politica di retention.

> **DA VALIDARE:** software e protocollo utilizzati per il trasferimento dei FITS.
