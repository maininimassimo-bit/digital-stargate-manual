# BKL-031 F3-C — Bounded Adapter, Sanitized Projection and Portal

| Field | Value |
|---|---|
| Identifier | `BKL-031-F3-C-INTEGRATION-001` |
| Status | **ACCEPTED — POST-MERGE VERIFIED** |
| Date | 2026-09-17 |
| Predecessor | F3-B Accepted / Post-Merge Verified |
| Environment / authority | `TEST` / `NONE` |
| Runtime effect | None; S10 remains `UNAVAILABLE` |
| Safety effect | None |

## Scope

F3-C implements a deterministic repository adapter over the accepted F3-B synthetic evidence, a closed sanitized projection, browser-side integrity validation and a read-only portal page. The adapter validates the complete F3-B fixture before deriving output. It never repairs invalid input, changes facts, selects a fallback method or reads protected authority records.

This increment deliberately uses the accepted synthetic evidence. It does not run Astropy, Skyfield or Cloud Run, download a kernel, resolve a protected site, contact an external reference or activate a runtime publisher. The result proves the integration and privacy boundary while S10 remains unavailable for production.

## Governed artifacts

| Artifact | Purpose |
|---|---|
| `.github/scripts/observation-planner-ephemeris-lunar-f3c-adapter.mjs` | deterministic adapter and fail-closed projection validator |
| `.github/scripts/generate-observation-planner-ephemeris-lunar-f3c.mjs` | reproducible generated-projection writer/checker |
| `schemas/observation-planner-ephemeris-lunar-projection-f3c.schema.json` | closed JSON Schema for the public projection |
| `docs/data/observation-planner-ephemeris-lunar-f3c-projection.json` | bounded `TEST` / `NONE` projection |
| `docs/javascripts/observation-planner-core.mjs` | browser-side identity, boundary and SHA-256 verification |
| `docs/javascripts/observation-planner.js` | read-only fail-closed renderer |
| `docs/observation-planner/index.md` | portal entry point |
| `.github/scripts/test-observation-planner-ephemeris-lunar-f3c.mjs` | 35-case adapter/projection/browser suite |

## Adapter contract

`BKL031-F3C-BOUNDED-ADAPTER@1.0` accepts only the complete F3-B fixture after its existing validator succeeds. Output identity is derived from the exact sanitized source projection and adapter identity. The projection digest covers every published field using canonical JSON and SHA-256.

The adapter preserves:

- exact context, evidence, fixture and method-profile references;
- exact method version, output frame and airless refraction semantics;
- exact normalized fact values and order;
- half-open validity and availability states;
- repository-resolvable citations and synthetic provenance;
- explicit `TEST_ONLY`, runtime `UNAVAILABLE`, zero external calls and no protected-site use.

## Sanitization and authority

The projection has a closed property set. It excludes coordinates, elevation, protected site/setup identities, internal input/output/data/contract digests, raw locators, paths, credentials and secrets. The validator also rejects forecast, weights, score, ranking, target order, readiness, go/no-go, scheduler and command fields.

The public page labels the result as synthetic integration evidence. It does not present it as a real observing plan. Browser validation recomputes the projection SHA-256 before rendering and fails closed without last-known-good substitution.

## Validation and OAT boundary

The 35-case suite covers deterministic generation, invalid upstream rejection, exact identities, availability, method/output semantics, validity, fact preservation, Citation/Provenance, privacy, prohibited later capabilities, authority boundaries, digest tampering and browser enforcement. The strict MkDocs build verifies that the page and assets publish correctly.

This is bounded repository/portal OAT only. Protected-site resolution, production scientific calculation, runtime publication, external-reference behavior and operational performance remain outside the increment.

## Rollback

Rollback removes the F3-C adapter, generator, schema, projection, consumer page/assets, workflow and documentation references. F3-B evidence remains accepted and unchanged. The portal link disappears and S10 remains `UNAVAILABLE`; F4, F5, BKL-032 and Safety are unaffected.

## Acceptance evidence

Pull request #261 passed 16/16 exact-head checks on `5d6b7127475c9378e19b1bfc5e65f6ad11f597f1`, merged with expected-head control as `fba1287efea0d1f36b147bc42a4fec5498990756`, and passed all 12 applicable post-merge workflows. The deployed [Observation Planner](https://maininimassimo-bit.github.io/digital-stargate-manual/observation-planner/) route then loaded the exact governed projection successfully.

## Successor gate

F4 forecast source discovery and integration contract is promoted as the next independent gate. Production runtime activation remains separately authorized; S10 remains `UNAVAILABLE` for production.
