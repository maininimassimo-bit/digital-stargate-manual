# BKL-034-F2 — Validation Plan

## Acceptance criteria

- bounded fixture con `CATALOGED`, `QUARANTINED` e `UNAVAILABLE`;
- SHA-256, media type, byte size e object reference obbligatori;
- sessione, target e metadata refs obbligatori;
- workflow PixInsight opzionale ma tracciabile tramite `workflowRefs`;
- metadata completeness `COMPLETE/PARTIAL/UNAVAILABLE` esplicita;
- `writeAuthority=NONE`, `commandAuthority=NONE`, `safetyAuthority=NONE`;
- nessuna inferenza da filename, preview o risultato visivo;
- validator fail-closed e build documentale strict.

La fixture non rappresenta upload reale né storage runtime: è evidence bounded per chiudere il contract e preparare il futuro gate di implementazione dello storage.
