# Local PixInsight pilot — P1

Trusted PJSR library for an explicit `PREFLIGHT_ONLY` manifest. It opens selected
XISF containers, checks SHA-256 before/after reading, selects an explicit image
index, checks expected monochrome dimensions and instantiates the fixed native
process list without executing any process. Four roles in R/G/B/L order are
required. Master windows remain open for inspection; no save or close occurs.

Manifest fields: `schemaVersion: "1.0"`, safe `jobId`, mode, and four inputs with
`role`, private absolute `path`, `sha256`, `imageIndex`, `width`, `height`.
The local wrapper includes `preflight.jsh`, calls `DSGPilotPreflight(manifest)`
and writes its private receipt to a previously selected local destination.
Never include an imported History export as a library or executable script.

This is P1 only: no remote worker, queue, API model, processing recipe, job lock,
cancellation implementation, automatic upload or publication. Those are P2–P6
requirements; a passed preflight does not grant their execution authority.
Module constructors demonstrate availability, not plugin model/license readiness
or version compatibility; process-instance module versions are explicitly unknown.
Reading a multi-image container can leave its auxiliary masks open too.

Synthetic boundary verification: `node --test tools/pixinsight/local_pilot/preflight.test.mjs`.
These tests stub native objects; the real PixInsight test is reported separately.
Plan: `docs/architecture/assessments/BKL-049-EXT-PIAI-Local-Pilot.md`.
