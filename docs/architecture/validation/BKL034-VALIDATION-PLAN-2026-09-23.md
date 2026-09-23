# BKL-034 — Validation Plan

## Gate

Acceptance of the Scientific Image Gallery as a bounded, descriptive and read-only projection.

## Evidence

1. Contract: `schemas/bkl034-scientific-image-gallery.schema.json`.
2. Bounded fixture: `docs/data/bkl034-scientific-image-gallery-fixture.json`.
3. Deterministic validator: `.github/scripts/verify-bkl034-scientific-image-gallery.mjs`.
4. Local validator result: PASS with 3 items, 3 sessions and 3 targets.
5. Boundary review: image mutation, processing execution, command path, remediation, scheduler decisionale and Safety Authority are excluded.

## Acceptance criteria

- every item is explicitly linked to one session, one target and at least one provenance reference;
- source references remain traceable and do not become source authority;
- current, stale and unknown states remain explicit;
- bounded cardinality is enforced at contract and validator level;
- authority remains `projection`, with `commandAuthority=NONE` and `safetyAuthority=NONE`.

Runtime ingestion and any image write operation remain excluded. The bounded gallery UI consumer is now part of the reopened BKL-034 acceptance gate and must be verified on public GitHub Pages.
