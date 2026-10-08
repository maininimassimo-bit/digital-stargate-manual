# BKL-051 S1 — proposed intake inspection

Offline, dependency-free preparation of a **proposed** private measurement intake contract. Not an image reader, astrometric solver, photometry pipeline, catalog client or operational portal integration. It neither establishes the truth of metadata nor manufactures consent from an actor/status field.

Run `node --test tools/scientific_transients/contract.test.mjs tools/scientific_transients/reference.test.mjs tools/scientific_transients/measurement.test.mjs`.

`parseIntake` rejects unknown/duplicate keys, nonfinite values, oversized/deep input, invalid dates and reused master digests as independent evidence. `inspectIntake` always returns `NO_ANALYSIS_EXECUTED` and `OWNER_CONTRACT_DECISIONS_PENDING`; even an apparently complete input receives no candidate/discovery classification. No I/O, credentials, owner paths, coordinates, scientific thresholds or external requests are present.

The limited fixture is synthetic. This tool does not change AP-013/AP-014 or ADR-019 registration/admission/quality semantics. Existing original source text, exact revisions, registry authority and byte-verification remain external prerequisites. Unknown acquisition dates and upstream History remain unknown. Input filter hashes do not establish band compatibility, and disjoint declarations do not independently prove frame independence.

See the [S1 proposal](../../docs/project/BKL-051-S1-FEASIBILITY-AND-CONTRACT-2026-10-07.md). Operational use, provider queries for an Owner field, new infrastructure/dependencies and numerical scientific thresholds remain pending the documented decisions and validation.

`reference.mjs` inspects bounded public CSV samples offline: exact string IDs, PS1 unavailable-magnitude sentinels and Gaia TCB epochs/proper-motion convention. It does not infer catalog completeness, quality, match absence or variability. Six negative/known-answer tests are synthetic and have no external I/O; the raw sample responses are retained separately in the private preparation dossier.

`measurement.mjs` inspects a proposed, closed-schema **already materialized object**, not raw JSON or transport requests. It records local-quality rejection or exploratory limitations from declarations; never grants measurement validity, band compatibility, matching, a nondetection limit, a transient classification or operating acceptance. Hash references do not independently verify bytes or truth. Nine tests cover saturation, defective apertures, crowding, negative/missing flux and unsafe declarations. A caller must separately reject duplicate JSON keys and preserve original evidence. See [reconciled evidence and residual gates](../../docs/project/BKL-051-S1-MEASUREMENT-EVIDENCE-2026-10-08.md). This module adds no I/O, dependency or operational integration.
