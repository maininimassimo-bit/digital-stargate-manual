# AP-013 — COPY_ONLY Limited Pilot Evidence

| Campo | Valore |
|---|---|
| Evidence ID | `E-AP013-COPYONLY-PILOT-001` |
| Package | AP-013 — Scientific Image Repository Architecture |
| Scope | Limited real pilot, COPY_ONLY |
| Execution host | PC principale |
| Execution date | 06/08/2026 |
| Run ID | `DSG-TRANSFER-RUN-9c993706-341b-4eb8-9412-89a76d8d0e63` |
| Result | Passed |
| Classification | TR-16 limited real pilot evidence |
| Review status | Independent four-eyes review pending |

## 1. Scopo

Registrare l'esecuzione del pilot reale limitato AP-013 in modalità `COPY_ONLY` su un singolo file scientifico, senza cancellazione della sorgente e senza overwrite della destinazione.

Questa evidenza chiude il criterio tecnico TR-16. Non chiude TR-17, che richiede una revisione indipendente nominativa, e non costituisce ancora autorizzazione alla produzione continuativa o al source cleanup.

## 2. Configurazione e finestra operativa

Il run è stato eseguito con:

- modalità `COPY_ONLY`;
- un solo file richiesto;
- destinazione `F:\Astrofotografia`;
- SHA-256;
- `SourceCleanupAuthorized = false`;
- `OverwriteExisting = false`;
- finestra autorizzata dalle 07:30 alle 08:15 locali.

Il run è iniziato alle 07:30:28 e si è concluso alle 07:32:48 ora locale, all'interno della finestra autorizzata.

## 3. Risultato del run

| Indicatore | Valore |
|---|---:|
| RequestedFileCount | 1 |
| ResultCount | 1 |
| CopiedVerifiedCount | 1 |
| SkippedIdenticalCount | 0 |
| DeferredUnstableCount | 0 |
| FailedCount | 0 |
| WhatIfCount | 0 |
| SourceFilesDeleted | 0 |

Stato finale: `COMPLETED`.

## 4. File verificato

- stato: `COPIED_VERIFIED`;
- dimensione: `23190016` byte;
- SHA-256 sorgente: `7be9d9d843876d5f116ab1c41b2c428fd9e9e3ebf17536aff8ff00ede3ee9337`;
- SHA-256 destinazione: `7be9d9d843876d5f116ab1c41b2c428fd9e9e3ebf17536aff8ff00ede3ee9337`;
- sorgente cancellata: `false`.

Il file destinazione è stato scritto sotto la root governata `F:\Astrofotografia`.

## 5. Evidence bundle

La cartella di evidence contiene:

- `transfer-manifest.json`;
- `transfer-results.csv`;
- `evidence-checksums.txt`.

Checksum del bundle:

```text
82ed558b652c18750991b0f99203b5076d4c678e164aa761f8d042345256ae4f  transfer-manifest.json
f4292a7e91b3095047ac0f22b53bf17d0162c732d6daf97a0feb17ec5ba7a6a8  transfer-results.csv
```

I checksum ricalcolati sugli artefatti forniti coincidono con `evidence-checksums.txt`.

## 6. Safety assertions

- `Mode = COPY_ONLY`;
- esecuzione reale (`WhatIfCount = 0`);
- un solo file pilota;
- copia verificata con hash coincidenti;
- nessun file fallito;
- nessun file sorgente cancellato;
- cleanup non autorizzato;
- overwrite non autorizzato;
- nessun file `.dsg-partial` residuo segnalato.

## 7. Valutazione gate

| Criterio | Esito |
|---|---|
| TR-13 — Operating window enforcement | Evidenza positiva del run nella finestra; il test negativo resta documentato separatamente |
| TR-14 — Performance baseline | Prima misura: 23.190.016 byte in circa 140,7 secondi end-to-end |
| TR-16 — Pilot reale limitato | Passed |
| TR-17 — Four-eyes approval | Open |
| TR-18 — Source cleanup separato | Open / prohibited |

## 8. Disposizione

**Limited real COPY_ONLY pilot: PASSED.**

**TR-16: SATISFIED.**

**TR-17: OPEN — independent reviewer approval required.**

**Production continuous COPY_ONLY: NOT YET AUTHORIZED.**

**Source cleanup: PROHIBITED.**

La promozione alla produzione continuativa richiede almeno la revisione indipendente, la chiusura dei gate tecnici residui, un runbook operativo e una disposizione esplicita di Operational Acceptance.
