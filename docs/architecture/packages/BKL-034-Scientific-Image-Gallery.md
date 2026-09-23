# BKL-034 — Scientific Image Gallery evoluta

| Campo | Valore |
|---|---|
| Identificativo | `BKL-034` |
| Stato | ACTIVE / BOUNDED READ-ONLY CONTRACT |
| Versione | 1.0 |
| Data | 23/09/2026 |
| Predecessore | BKL-033 Observatory Digital Twin |
| Owner | Massimo Mainini |

## Scopo

Definire una projection navigabile di immagini scientifiche collegata a sessione, target e processing provenance. La gallery descrive asset già osservati o catalogati; non diventa un repository mutabile, un processing engine o un sistema di controllo.

Il contract è `schemas/bkl034-scientific-image-gallery.schema.json`; la fixture bounded è `docs/data/bkl034-scientific-image-gallery-fixture.json`.

## Boundary

- `GalleryItem` identifica un'immagine scientifica e conserva stato e freshness espliciti;
- `sessionRef` e `targetRef` collegano l'asset a contesto già governato;
- `provenanceRefs` e `sourceRefs` conservano la tracciabilità senza assumere autorità sul dato sorgente;
- authority = `projection`, `commandAuthority=NONE`, `safetyAuthority=NONE`;
- stati `observed`, `stale`, `unknown` e `unavailable` non vengono trasformati in qualità, readiness o idoneità.

Sono esclusi image mutation, upload/delete, processing execution, provider/AI apply, command path, remediation, scheduler decisionale e Safety Authority. La gallery non autorizza né seleziona automaticamente un target.

## Acceptance

`.github/scripts/verify-bkl034-scientific-image-gallery.mjs` valida schema identity, cardinalità bounded, riferimenti session/target/provenance, provenance/source refs e boundary fail-closed. L'eventuale UI o ingestione runtime è successiva e separatamente gated.
