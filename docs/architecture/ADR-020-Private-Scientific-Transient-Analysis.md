# ADR-020 — Private scientific transient analysis

**Status:** Owner-approved direction, provider-query boundary and concrete private transport; implementation candidate not activated, scientific operating policy not accepted.

**Date:** 2026-10-08

**Scope:** BKL-051, additive private local analysis and governed portal consultation.

## Concrete transport decision — 8 October 2026

The Owner authorized the pending concrete proposal: separate transient-analysis namespace in the existing private HTTPS service, dedicated worker identity, remote opaque references/status/aggregate counts/report digest, detailed images and reports on the Owner PC. No new cloud resources or scientific upload. [Minimized event](../project/evidence/BKL-051-OWNER-TRANSPORT-2026-10-08.json), [reviewable contract and implementation](../project/BKL-051-S4-PRIVATE-QUEUE-2026-10-08.md). Authentication, permissions, leases, cancellation/recovery and complete Owner workflow still require reviewed implementation and real tests before activation. This supersedes earlier direction-only transport-pending wording; earlier evidence remains historical. No scientific policy or final milestone acceptance is granted.

## Decision and evidence

The Owner approved all three questions in the reviewable S1 proposal: computation on the Owner PC with private portal consultation; minimal queries to ESA Gaia, NASA-IPAC IRSA and MAST; recommended pilot selection criteria. No specific field was named. The local selection must retain actual dates, filter response and independent input identities. The decision is recorded in [the minimized event](../project/evidence/BKL-051-OWNER-DIRECTION-2026-10-08.json). It does not accept S1 or quantitative scientific operating thresholds.

Images, local paths, terrestrial site coordinates, instrument serials and full scientific reports stay private on the Owner PC. Only celestial region, necessary angular extent, pinned provider product/release, filter and necessary epoch restrictions may be sent to the approved providers. The provider can observe network-origin and request timing as already described in S1. No new paid service, credentials, cloud resource or publication is implied.

## Boundary

Use a dedicated local component for explicit allowlisted provider requests and native scientific processing. It must retain request/response hashes, timestamps, catalog release, units, pagination/limits and negative receipts. Do not accept arbitrary URLs, SQL or executable text from portal payloads. Redirects and provider/schema changes require fail-closed treatment in the future adapter. Self-declared consent in an intake payload never grants access.

The portal consults private results through a dedicated adapter governed by SDE. Existing SDE catalog/cache consumption is not a private analysis broker. No frontend filesystem access or direct scientific-provider fetch is introduced here. The private transport, authentication, expiry, replay protection, cancellation and crash semantics require a concrete reviewed contract and operational tests before activation. Existing PIAI SESSION_ASSISTED jobs do not silently acquire a new scientific job type.

AP-013 remains asset/lineage authority, AP-014 context/catalog and admission authority, and ADR-019 retrospective PARTIAL/UNKNOWN semantics remain intact. An admitted asset is not scientifically accepted. Derived private measurements must anchor exact image bytes, image index, parent lineage, algorithm/version and parameters; incomplete history stays explicit.

## Scientific boundary

Single-band linear calibrated data and disjoint dated exposures are preferred. SHO/HOO presentation products, denoise, deconvolution and stretch are not interchangeable photometric measurements. WCS, centroid/PSF uncertainty, catalog epoch/proper motion/covariance, depth, saturation, variance and filter compatibility must be verified. A bounded successful query is not complete field coverage. Gaia Julian-year TCB and acquisition UTC remain distinct.

No numeric association radius, S/N cutoff, magnitude-change threshold, ranking or discovery claim is accepted by this ADR. Native solver defaults may be recorded for exploratory baseline experiments but are not an operational candidate policy. An unavailable/truncated/incompatible reference or unverified astrometry produces explicit incomplete status, never a negative scientific finding. Photometry/difference images require their own validation and uncertainty evidence. Scientific reports and astronomy-organization submissions require separate explicit publication authority.

## Verification and rollout

Current evidence is private input inspection, History export, one bounded authorized Gaia access sample and three completed native local-Gaia DR3 solutions on new copies with identical pixels and unchanged originals. Failed initialization/alignment branches are retained. Solver fitting residuals are in-sample evidence, not independent scientific validation. Full astrometric validation, proper-motion known-answer tests, independent matching, photometry/recovery/false-positive baseline, private transport tests and Owner operating acceptance remain outstanding. P6 tests do not count as tests of this new module.

No runtime is deployed by this document. New dependencies or materially different transport alternatives remain decisions before implementation. S1/S2 remain open, F4 lifecycle pending, F5 after F4, BKL-050 final, S10 unavailable and device/Safety authority unchanged.

Rollback removes additive analysis components and portal adapters when implemented, retaining immutable private inputs, histories and receipts. This direction-only delivery requires no migration and changes no registry or infrastructure.
