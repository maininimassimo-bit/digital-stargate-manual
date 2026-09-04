# AP-013B — OneDrive Transport Incident / Recovery Evidence — 2026-09-04

| Campo | Valore |
|---|---|
| Tipo | Operational incident / recovery evidence |
| Data | 2026-09-04 |
| Baseline interessata | AP-013B `COPY_ONLY` |
| Safety impact | Nessuna modifica alla Safety Authority |
| Data loss osservata | No |
| Recovery | Completed |

## 1. Contesto

Durante la sessione M 27 `2026-09-03_2026-09-04`, il transport raw Digital StarGate ha mostrato una divergenza tra EAGLE30154 e PC principale dopo l'uso della funzione OneDrive Files On-Demand / libera spazio sul transport EAGLE.

Questo record documenta soltanto evidence osservata e recovery. Non modifica retroattivamente l'acceptance AP-013B e non autorizza cleanup automatico.

## 2. Sintomo

Transport EAGLE:

- XISF: 445;
- READY: 445;
- partial osservati: 0.

Transport PC iniziale:

- XISF: 426;
- READY: 426.

Gap: 19 XISF + 19 READY.

Il range mancante era M 27 `0123–0141`, esattamente 19 frame. I file erano presenti nel transport EAGLE con i rispettivi manifest READY.

## 3. Importer escluso come causa primaria

Il PC Import Agent vedeva soltanto i 426 READY convergenti e non riportava failure/deferred. I file mancanti non erano ancora disponibili nel transport PC, quindi l'importer non poteva richiederli.

Questo ha localizzato il problema nel layer di sincronizzazione/convergenza OneDrive tra producer transport e consumer PC, non nella copia verso `F:\Astrofotografia`.

## 4. Diagnostica OneDrive

Sul lato EAGLE sono stati verificati processo, settings `Business1`, log e `SyncDiagnostics.log`. Un restart semplice di OneDrive non ha prodotto la convergenza dei 19 file.

È stato quindi eseguito un reset controllato del client OneDrive EAGLE. Il processo è ripartito correttamente. Un sync probe creato nel transport EAGLE non è risultato immediatamente visibile sul PC.

Sul PC principale è stato eseguito un reset controllato del client OneDrive. Il registry mapping ha confermato:

- account: `Business1`;
- UserFolder: `C:\Users\MassimoMainini\OneDrive - Massimo Mainini`;
- DisplayName: `Massimo Mainini`;
- account email: `massimo.mainini@mmainini.it`.

Dopo la ricostruzione dello stato di sincronizzazione, il transport PC ha raggiunto 445 XISF / 445 READY e il probe è diventato visibile.

## 5. Verifica recovery raw files

Sul PC principale tutti i 19 XISF `0123–0141` sono risultati presenti. Ogni XISF osservato aveva dimensione 11,897,856 byte.

La successiva evidence `Digital StarGate - OneDrive Import` ha riportato:

```text
ReadyManifestsObserved = 445
AlreadyImportedSkipped = 445
DeferredNoPlan = 0
DeferredPlanAction = 0
DeferredTransportNotReady = 0
Requested = 0
CopiedVerified = 0
SkippedIdentical = 0
Failed = 0
SourceFilesDeleted = 0
TransportFilesDeleted = 0
OverwritesPerformed = 0
```

La verifica diretta della destinazione `F:\Astrofotografia` ha trovato tutti i 19 frame `0123–0141`.

## 6. Esito

Recovery completata senza perdita osservata dei raw file coinvolti.

AP-013B `COPY_ONLY` ha preservato source/transport e ha consentito recovery senza ricostruzione dei dati scientifici. Tuttavia l'incidente dimostra che la sola presenza nel transport locale EAGLE non costituisce prova di convergenza end-to-end.

## 7. Follow-up governato

È approvata la progettazione di AP-013C Verified Transport Cleanup / convergence monitoring. Fino alla sua acceptance:

- AP-013B resta `COPY_ONLY`;
- nessuna cancellazione automatica viene autorizzata da questo record;
- la cleanup eligibility deve essere derivata da evidence end-to-end, non dalla sola export completion;
- failure, timeout o evidence incompleta devono produrre no-delete.
