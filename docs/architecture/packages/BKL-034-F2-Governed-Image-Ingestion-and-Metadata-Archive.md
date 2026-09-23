# BKL-034-F2 — Governed Image Ingestion and Metadata Archive

| Campo | Valore |
|---|---|
| Identificativo | `BKL-034-F2` |
| Stato | ACTIVE / CONTRACT AND ARCHIVE GATE |
| Versione | 1.0 |
| Data | 23/09/2026 |
| Dipendenze | BKL-034, AP-013, AP-014, BKL-044, BKL-045; BKL-049 for native capture |
| Owner | Massimo Mainini |

## Obiettivo

Definire il caricamento governato e l’archiviazione dei metadati immagine senza confondere il consumer GitHub Pages con uno storage scrivibile. Il contract descrive asset, checksum, object reference, metadata, sessione, target, preview/derivative e relazioni verso workflow PixInsight.

Il contract è `schemas/bkl034-f2-image-archive-ingestion.schema.json`; la fixture bounded è `docs/data/bkl034-f2-image-archive-fixture.json`.

## Stati

- `CATALOGED`: asset validato e riferibile nel catalogo;
- `QUARANTINED`: asset ricevuto ma non pubblicabile finché MIME, sicurezza, metadata e provenance non sono validati;
- `UNAVAILABLE`: riferimento conosciuto ma bytes o metadata non disponibili;
- `COMPLETE`, `PARTIAL`, `UNAVAILABLE` qualificano la completezza dei metadata e della relazione workflow.

## Relazione PixInsight

La relazione è `ImageAsset -> processingRun/workflowRef -> PixInsight evidence`. BKL-034-F2 non cattura né esegue workflow: consuma sidecar/provenance già governati da BKL-045 e, per la cattura nativa futura, da BKL-049. `PARTIAL` e `UNAVAILABLE` restano visibili e non vengono trasformati in assenza di processing.

## Step successivo: storage boundary preflight

`docs/architecture/packages/BKL-034-F2-Storage-Boundary-Preflight.md` definisce il dry-run eseguibile per validare una richiesta senza trasferire bytes o tentare scritture. Il preflight è il prerequisito per un futuro storage runtime.

## Gate storage reale

Lo storage runtime deve essere un gate separato con quarantine, validazione MIME/magic bytes, limite dimensionale, checksum SHA-256, deduplicazione, antivirus, sanitizzazione EXIF, retention, ACL, audit e object immutability. GitHub Pages resta un consumer read-only e non riceve credenziali di scrittura.

Sono esclusi image mutation, processing execution, provider/AI apply, command, remediation, scheduler decisionale e Safety Authority.
