# AP-013 — Morning Transfer Scheduler Evidence

| Campo | Valore |
|---|---|
| Evidence ID | `E-AP013-SCHEDULER-001` |
| Package | AP-013 — Scientific Image Repository Architecture |
| Execution host | PC principale |
| Task name | `Digital StarGate - Morning Transfer` |
| Stato task | `Ready` |
| Trigger | Giornaliero alle 07:30 locali |
| Finestra ammessa | 07:30–08:05 locali |
| Completamento previsto | entro le 08:15 locali |
| Ultima esecuzione verificata | 06/08/2026 07:30:01 |
| Ultimo risultato | `0` — success |
| Prossima esecuzione verificata | 07/08/2026 07:30:00 |
| Batch target successivo | 30 file massimi per run |

## 1. Scopo

Registrare la configurazione effettiva della schedulazione automatica AP-013 e distinguere chiaramente:

- l'orario del trigger Windows Task Scheduler;
- la finestra applicativa ammessa dall'orchestratore;
- l'orario massimo previsto per il completamento;
- il batch target pianificato per il run successivo.

## 2. Task Scheduler verificato

La task configurata è:

```text
Digital StarGate - Morning Transfer
```

Configurazione verificata:

- task abilitata;
- stato `Ready`;
- trigger giornaliero alle 07:30;
- launcher `Start-DSGMorningTransfer.ps1`;
- working directory `tools\dsdm\session-importer`;
- `MultipleInstances = IgnoreNew`;
- `ExecutionTimeLimit = PT45M`;
- `RestartCount = 3`;
- `RestartInterval = PT5M`;
- `StartWhenAvailable = true`;
- ultima esecuzione conclusa con `LastTaskResult = 0`;
- nessun run perso.

## 3. Finestra applicativa

Il file locale `session-transfer.local.json` applica:

```json
{
  "notBeforeLocal": "07:30",
  "doNotStartAfterLocal": "08:05",
  "mustFinishBeforeLocal": "08:15"
}
```

La finestra operativa autorevole è quindi:

- trigger automatico: 07:30;
- avvio consentito: dalle 07:30 alle 08:05;
- completamento previsto: entro le 08:15.

La formula generica "07:00–08:15" non rappresenta la configurazione effettiva verificata e deve essere sostituita dalla sequenza temporale sopra indicata.

## 4. Launcher e credenziale

Il launcher:

- importa la credenziale cifrata `EAGLE30154-DSGReadOnly.credential.xml`;
- usa l'account `EAGLE30154\DSGReadOnly`;
- monta `\\192.168.1.144\NINA-Images` come `DSGNINA:`;
- seleziona il discovery run più recente contenente `transfer-plan.csv`;
- richiama l'orchestratore `Invoke-DSGSessionTransfer.ps1`;
- registra il transcript;
- smonta `DSGNINA:` al termine.

## 5. Batch target da 30 file

Per il run del 07/08/2026 il target richiesto è:

```text
maxFilesPerRun = 30
```

Questo valore rappresenta un limite massimo, non una garanzia di 30 copie. Il numero effettivo dipende dal transfer plan più recente e dal numero di righe con:

```text
PlannedAction = COPY_NEW
```

La promozione è valida solo se, prima del trigger delle 07:30:

1. `session-transfer.local.json` contiene `maxFilesPerRun = 30`;
2. il transfer plan più recente contiene almeno 30 elementi `COPY_NEW` eleggibili;
3. restano invariati:
   - `mode = COPY_ONLY`;
   - `sourceCleanupAuthorized = false`;
   - `overwriteExisting = false`;
   - `hashAlgorithm = SHA-256`;
4. la share EAGLE è accessibile tramite `DSGReadOnly`;
5. il volume `F:` è disponibile e con spazio sufficiente.

## 6. Safety boundary

L'aumento del batch non autorizza:

- source cleanup;
- overwrite;
- bypass della operating window;
- esecuzione parallela;
- trasferimento di righe diverse da `COPY_NEW`;
- modifica dei file sorgente.

## 7. Disposizione

**Scheduler giornaliero: VERIFIED.**

**Trigger: 07:30 local time.**

**Allowed start window: 07:30–08:05.**

**Expected completion: by 08:15.**

**Next batch target: 30 files maximum, subject to transfer-plan eligibility.**

**Source cleanup: PROHIBITED.**
