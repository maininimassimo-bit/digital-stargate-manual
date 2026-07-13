# Capitolo 44 — Allegati tecnici e piano di completamento

**Codice documento:** DSG-TM-001-44  
**Revisione:** 1.0 Draft

## 44.1 Scopo

Il capitolo definisce l'elenco degli allegati tecnici necessari per trasformare il manuale da documentazione descrittiva a fascicolo completo dell'impianto reale.

## 44.2 Allegati obbligatori

| Codice | Allegato | Stato |
|---|---|---|
| DSG-ATT-001 | Inventario hardware completo | Da completare |
| DSG-ATT-002 | Schema elettrico as-built | Da produrre |
| DSG-ATT-003 | Schema di rete as-built | Bozza disponibile |
| DSG-ATT-004 | Mappa porte USB e alimentazioni EAGLE | Da rilevare |
| DSG-ATT-005 | Configurazione RUT955 esportata | Da archiviare in area protetta |
| DSG-ATT-006 | Profili N.I.N.A. | Da esportare |
| DSG-ATT-007 | Profili PHD2 | Da esportare |
| DSG-ATT-008 | Configurazione CPWI e Park | Da documentare |
| DSG-ATT-009 | Treni ottici e backfocus | Da misurare |
| DSG-ATT-010 | Librerie di calibrazione | Da censire |
| DSG-ATT-011 | Fotografie annotate | Da acquisire |
| DSG-ATT-012 | Log incidenti significativi | Da selezionare |
| DSG-ATT-013 | Piano manutenzione firmato | Da approvare |
| DSG-ATT-014 | Matrice requisiti/test | Da completare |

## 44.3 Struttura delle cartelle

```text
docs/assets/
├── images/
│   ├── observatory/
│   ├── dome/
│   ├── network/
│   ├── eagle/
│   ├── cgxl/
│   ├── c8/
│   ├── quattro/
│   ├── cameras/
│   └── allsky/
├── diagrams/
├── screenshots/
└── protected-index/
```

Le credenziali, le chiavi VPN e gli export sensibili non devono essere pubblicati nel repository documentale ordinario.

## 44.4 Piano fotografico

Per ogni asset acquisire:

- vista generale;
- etichetta modello e seriale;
- connettori;
- cablaggio;
- posizione installata;
- dettaglio utile alla manutenzione;
- fotografia della condizione di Park o Safe.

Formato consigliato:

`DSG-ASSET-<ID>_<descrizione>_<YYYYMMDD>.jpg`

## 44.5 Screenshot software

Screenshot minimi:

- profili N.I.N.A.;
- Advanced Sequencer;
- autofocus;
- meridian flip;
- PHD2 equipment profile;
- grafico guida e calibrazione;
- CPWI Park e limiti;
- Device Manager Windows;
- EAGLE Manager;
- RUT955 failover e VPN;
- AllSky configuration.

Oscurare sempre:

- password;
- chiavi;
- indirizzi pubblici;
- certificati;
- token;
- dati personali.

## 44.6 Dati tecnici da rilevare

| Area | Dato |
|---|---|
| Cupola | tempi apertura/chiusura, motore, finecorsa |
| Elettrico | tensioni, assorbimenti, protezioni, UPS |
| Rete | IP, subnet, gateway, DHCP, failover |
| EAGLE | modello, seriale, porte, SSD, Windows |
| CGX-L | firmware, Park, limiti, PEC |
| C8 | seriale, riduttore, backfocus, collimazione |
| Quattro | correttore, focale reale, backfocus, tilt |
| Camere | seriali, driver, gain, offset, setpoint |
| Guida | camera, focale, scala, profili PHD2 |
| AllSky | camera, lente, riscaldatore, retention |

## 44.7 Priorità di completamento

### Priorità 1 — Sicurezza

- schema copertura e interlock;
- posizione Park;
- procedure emergenza;
- alimentazione e chiusura in blackout;
- contatti locali.

### Priorità 2 — Ripristino

- backup configurazioni;
- export RUT955;
- immagini sistema EAGLE;
- installer driver;
- inventario ricambi.

### Priorità 3 — Qualità osservativa

- backfocus;
- profili autofocus;
- campionamento;
- guida;
- librerie calibrazione.

### Priorità 4 — Pubblicazione

- fotografie;
- diagrammi finali;
- revisione editoriale;
- PDF e sito web.

## 44.8 Piano di raccolta

| Fase | Attività | Output |
|---|---|---|
| A | Rilievo fisico | Foto, seriali, cablaggi |
| B | Export software | Profili e configurazioni |
| C | Misure | Assorbimenti, backfocus, tempi |
| D | Validazione | Test e verbali |
| E | Impaginazione | Figure e didascalie |
| F | Release | Word, PDF, sito, sorgenti |

## 44.9 Checklist DSG-CHK-044-001

- [ ] Tutti gli asset hanno almeno una foto.
- [ ] Tutti i seriali sono censiti.
- [ ] Gli schemi as-built corrispondono all'impianto.
- [ ] Le configurazioni sono esportate.
- [ ] I segreti sono esclusi dal repository.
- [ ] Le procedure critiche sono validate.
- [ ] I campi “DA VALIDARE” sono riesaminati.
- [ ] Gli allegati sono versionati.

## 44.10 Chiusura della fase editoriale

Il Master Source può essere considerato completo quando:

- tutti i capitoli sono presenti;
- gli allegati critici sono disponibili;
- la matrice requisiti è coperta;
- la FMEA è approvata;
- il collaudo è superato;
- il manuale viene generato senza errori;
- la release è formalmente approvata.

## 44.11 Evoluzione successiva

Dopo la release 1.0, il repository deve essere mantenuto come fonte unica. Ogni modifica all'impianto deve produrre, nello stesso change:

- modifica della configurazione;
- aggiornamento del capitolo interessato;
- revisione del test;
- aggiornamento del registro;
- nuova release documentale quando necessaria.
