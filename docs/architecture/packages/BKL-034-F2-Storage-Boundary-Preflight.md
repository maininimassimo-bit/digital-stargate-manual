# BKL-034-F2 — Storage Boundary Preflight

## Scopo

Rendere eseguibile in modo bounded il preflight di una richiesta di image ingestion prima di autorizzare qualsiasi storage runtime. Il preflight produce una decisione descrittiva `CATALOGED` o `QUARANTINED`; non trasferisce bytes, non scrive su storage e non pubblica immagini.

Il contract è `schemas/bkl034-f2-ingestion-request.schema.json`; la fixture è `docs/data/bkl034-f2-ingestion-request-fixture.json`; l’adapter è `.github/scripts/verify-bkl034-f2-ingestion-preflight.mjs`.

## Regole

- `mode` deve essere `DRY_RUN_PREFLIGHT`;
- filename, media type, byte size e SHA-256 sono obbligatori;
- MIME e magic bytes devono essere verificati;
- malware scan `PENDING` o `UNAVAILABLE` mantiene l’asset in `QUARANTINED`;
- metadata `PARTIAL` o `UNAVAILABLE` impediscono la pubblicazione `CATALOGED`;
- EXIF deve essere sanitizzato prima della pubblicazione;
- `writeAttempted` deve restare `false`;
- workflow PixInsight è un riferimento evidence-only e non viene eseguito.

## Non autorizzato

Il preflight non implementa upload, object storage, delete, overwrite, processing execution, Cloud Run write path, command, remediation, scheduler decisionale o Safety Authority. Lo storage produttivo richiederà un gate successivo con security, ACL, retention, audit e recovery evidence.
