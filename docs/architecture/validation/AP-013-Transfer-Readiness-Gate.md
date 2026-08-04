# AP-013 — Transfer Readiness Gate

| Campo | Valore |
|---|---|
| Gate ID | `G-AP013-TR-001` |
| Package | AP-013 — Scientific Image Repository |
| Scope | Abilitazione controllata della modalità `TRANSFER` |
| Baseline discovery | `E-AP013-SD-001` |
| Branch | `architecture/ap-013-package-initiation` |
| Stato iniziale | `NOT READY` |
| Data | 04/08/2026 |
| Decisione | Transfer non autorizzato fino alla chiusura di tutti i criteri obbligatori |

## 1. Scopo del gate

Questo gate definisce le condizioni minime e non derogabili per passare dalla discovery read-only alla copia reale dei file scientifici dalla share EAGLE verso il repository di destinazione.

Il superamento del gate autorizza esclusivamente una copia controllata. Non autorizza automaticamente spostamento, rinomina distruttiva, cancellazione o cleanup della sorgente.

## 2. Principi vincolanti

1. **Copy before delete.** Nessun file sorgente può essere cancellato prima della verifica completa della copia.
2. **Source read-only by default.** L'account di discovery resta separato da qualunque identità eventualmente autorizzata alla manutenzione della sorgente.
3. **No silent overwrite.** Una destinazione esistente non può essere sovrascritta senza una decisione esplicita e tracciata.
4. **Evidence before promotion.** Ogni run reale deve produrre manifest, log, checksum e disposizione finale.
5. **Idempotency.** La riesecuzione dello stesso piano non deve generare duplicazioni o risultati divergenti non segnalati.
6. **Fail closed.** In presenza di errore, ambiguità, instabilità o mismatch hash, il file resta in sorgente e il run viene marcato non completato.
7. **No source cleanup in initial transfer.** La prima fase operativa è copy-only.

## 3. Criteri obbligatori

| ID | Criterio | Evidenza richiesta | Stato |
|---|---|---|---|
| TR-01 | Destinazione disponibile, identificata e con spazio sufficiente | inventory volume, health, filesystem, free space e path root | Open |
| TR-02 | Scrittura limitata alla root governata | ACL/permission evidence e test di path escape negativo | Open |
| TR-03 | Doppia verifica stabilità sorgente | due osservazioni di size e mtime separate da intervallo configurato | Open |
| TR-04 | Hash sorgente pre-copy | SHA-256 calcolato prima della copia | Open |
| TR-05 | Copia atomica o staging | uso di file temporaneo/staging e rename finale solo dopo verifica | Open |
| TR-06 | Hash destinazione post-copy | SHA-256 destinazione uguale alla sorgente | Open |
| TR-07 | Size destinazione post-copy | byte count identico alla sorgente | Open |
| TR-08 | Collision policy completa | classificazione NEW, IDENTICAL, CONFLICT e policy per ciascun caso | Open |
| TR-09 | Resume e retry controllati | test di interruzione, riesecuzione e ripresa senza duplicazioni | Open |
| TR-10 | Rollback tecnico | rimozione sicura del solo file temporaneo/incompleto; nessuna perdita sorgente | Open |
| TR-11 | Manifest immutabile del run | elenco file, azioni, hash, esiti, timestamp e versioni | Open |
| TR-12 | Evidence bundle | checksum del bundle e posizione di conservazione separata | Open |
| TR-13 | Operating window enforcement | test positivo nella finestra e negativo fuori finestra senza bypass | Open |
| TR-14 | Performance baseline | misura throughput, durata stimata e impatto sulla VPN/SMB | Open |
| TR-15 | Test su dataset sintetico | esecuzione completa su fixture non scientifiche | Open |
| TR-16 | Pilot reale limitato | massimo una sessione approvata, copy-only, con verifica manuale finale | Open |
| TR-17 | Four-eyes approval del pilot | approvazione separata tra esecutore e revisore | Open |
| TR-18 | Source cleanup separato | procedura, retention period e autorizzazione specifica; non inclusa nel pilot | Open |

## 4. Collision policy minima

| Stato destinazione | Condizione | Azione consentita |
|---|---|---|
| NEW | path non presente | copia in staging, verifica hash, promozione finale |
| IDENTICAL | path presente, size e SHA-256 uguali | skip idempotente con evidenza |
| CONFLICT | path presente, size o SHA-256 diversi | blocco, nessun overwrite, escalation manuale |
| INCOMPLETE | file temporaneo presente | resume o cleanup del solo temporaneo secondo policy |
| INVALID_PATH | path non conforme alla root o segmenti non validi | blocco e quarantena del piano |

## 5. Modello di esecuzione autorizzabile

La prima modalità reale ammessa dopo il superamento del gate deve rispettare tutti i vincoli seguenti:

- `TRANSFER_MODE = COPY_ONLY`;
- `SOURCE_CLEANUP_AUTHORIZED = false`;
- `OVERWRITE_EXISTING = false`;
- `HASH_ALGORITHM = SHA-256`;
- una singola sessione pilota;
- destinazione esplicitamente approvata;
- finestra operativa 07:35–08:25;
- evidenza completa prima della chiusura del run;
- review manuale del manifest e di almeno un campione dei file copiati.

## 6. Scenari di test richiesti

### 6.1 Happy path

- file stabile;
- destinazione assente;
- copia in staging;
- size e hash coincidenti;
- promozione finale;
- manifest `COMPLETED`.

### 6.2 File instabile

- size o mtime cambia tra le due osservazioni;
- azione `DEFER_UNSTABLE`;
- nessuna scrittura destinazione.

### 6.3 Collisione identica

- destinazione presente;
- size e hash uguali;
- azione `SKIP_IDENTICAL`;
- nessuna riscrittura.

### 6.4 Collisione differente

- destinazione presente;
- size o hash differenti;
- azione `BLOCK_CONFLICT`;
- nessun overwrite.

### 6.5 Interruzione durante copia

- copia interrotta prima del completamento;
- sorgente intatta;
- file temporaneo riconoscibile;
- retry idempotente o cleanup controllato.

### 6.6 Destinazione piena o non disponibile

- preflight fallisce;
- run non avviato o terminato `BLOCKED`;
- nessuna copia parziale non governata.

### 6.7 Path traversal e root escape

- target o nome file produce segmenti non validi;
- percorso normalizzato resta sotto la root autorizzata;
- qualunque escape viene bloccato.

## 7. Evidenze minime per il pilot

- identificativo univoco del run;
- commit e configurazione applicata;
- inventario preflight sorgente/destinazione;
- transfer plan approvato;
- log di ogni fase;
- hash sorgente e destinazione;
- collision classification;
- manifest finale;
- checksum dell'evidence bundle;
- dichiarazione esplicita `source files deleted = 0`;
- firma/approvazione di esecutore e revisore.

## 8. Criteri di stop immediato

Il run deve interrompersi senza proseguire sugli altri file quando si verifica uno dei seguenti eventi:

- impossibilità di leggere la sorgente;
- perdita della destinazione;
- spazio insufficiente;
- mismatch hash;
- tentativo di overwrite non autorizzato;
- path fuori root;
- errore di manifest o evidence write;
- modifica inattesa dei flag di sicurezza;
- richiesta di cleanup sorgente non autorizzata.

## 9. Responsabilità

| Ruolo | Responsabilità |
|---|---|
| Implementer | sviluppa e prova la modalità copy-only |
| Operator | esegue il pilot nella finestra autorizzata |
| Independent Reviewer | verifica piano, output, checksum e assenza di cleanup |
| Data Owner | approva destinazione, naming e collision policy |
| Release/Quality Governor | emette la disposizione finale del gate |

Una singola persona non deve approvare autonomamente implementazione, esecuzione e chiusura del pilot.

## 10. Disposizione corrente

**Discovery readiness: PASSED.**

**Transfer readiness: NOT READY.**

**Source cleanup: PROHIBITED.**

Il gate potrà passare a `READY FOR LIMITED PILOT` solo quando TR-01…TR-17 risultano chiusi con evidenze verificabili. TR-18 resta un gate successivo e separato, necessario per qualunque futura cancellazione dalla sorgente.
