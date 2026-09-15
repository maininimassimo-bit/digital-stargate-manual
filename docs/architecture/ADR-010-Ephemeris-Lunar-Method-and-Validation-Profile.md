# ADR-010 — Ephemeris/Lunar Method and Validation Profile

| Field | Value |
|---|---|
| Status | **PROPOSED — OWNER DECISION REQUIRED / NOT IMPLEMENTED** |
| Date | 2026-09-15 |
| Release | Release 2.x planning increment |
| Capability | BKL-031 F3-A3 |
| Baseline | `main@4f76f6646769df378859fbb15147851b4d0543fe` |
| Decision authority | Repository Owner after evidence and ARB review |
| Runtime impact | None until separately authorized |

## Context

F3-A1 and F3-A2 have completed repository authority, but S08/S09 remain unavailable to runtime and S10 remains `UNAVAILABLE`. The accepted F3 architecture requires a provider/library, scientific-data, error-budget, time-data, privacy, host and request-bound decision before any ephemeris/lunar implementation.

The Program Architect authorized a decision-preparation package, not provider selection or spike execution.

## Decision drivers

- reproducibility and exact artifact identity;
- sufficient scientific accuracy for an owner-approved planner use case;
- local/offline determinism where practical;
- explicit frame/time/refraction semantics;
- protected site privacy;
- independent validation;
- bounded resource use;
- replaceable adapters behind one source-neutral port;
- fail-closed behavior and no silent fallback;
- license and redistribution compliance.

## Considered options

### Option A — Astropy local primary candidate

Observed decision baseline: Astropy 8.0.1, jplephem 2.24 and a future governed JPL SPK.

Benefits: explicit units, frames, time and Earth location; broad astronomy ecosystem.

Costs/risks: Python >=3.11; IERS and kernel acquisition; refraction and frame policy must be pinned; artifact set is larger.

### Option B — Skyfield local primary candidate

Observed decision baseline: Skyfield 1.55 and a future governed JPL SPK.

Benefits: direct timescale/topos model, SPK visibility and almanac functions.

Costs/risks: separate dependency/convention mapping; independent validation remains necessary; kernel/time-data governance still applies.

### Option C — Horizons remote primary

Benefits: official observer/vector service and explicit output controls.

Costs/risks: external availability, service/parser drift, HTTP 200 semantic errors, exact-site transmission, retention/terms and weaker offline determinism.

### Option D — No selection

S10 remains `UNAVAILABLE`; no spike or implementation proceeds.

## Proposed decision hypothesis

For owner consideration only:

- choose one local library as primary;
- use the other local implementation as an explicit cross-check, not runtime fallback;
- allow Horizons only as an optional validation reference using geocentric or synthetic/generalized sites unless exact-site transmission is separately approved;
- use an exact, checksummed JPL SPK with approved coverage;
- use an exact, freshness-governed IERS/EOP snapshot;
- execute only on an authorized off-EAGLE host;
- reject any unbounded request profile.

**No option is selected by this ADR version.**

## Required owner dispositions

| ID | Required exact decision | Current value |
|---|---|---|
| F3-OD04 | primary library/version; secondary/reference roles | PENDING |
| F3-OD05 | kernel/data artifact, coverage, provenance and checksum policy | PENDING |
| F3-OD06 | per-metric scientific error budget and independent reference | PENDING |
| F3-OD07 | IERS/EOP/leap-second version and freshness/update policy | PENDING |
| F3-OD08 | cache/retention, license/notice and external-site privacy policy | PENDING |
| F3-OD09 | authorized execution host and resource/performance budget | PENDING |
| F3-OD10 | maximum targets, instants, date span and request size | PENDING |

## Decision

`NO_DECISION_RECORDED`.

ADR-010 remains Proposed. S10 remains `UNAVAILABLE`. Presence or merge of this file cannot be interpreted as provider approval.

## Consequences

### Positive

- owner choices are atomic and reviewable;
- method selection cannot be inferred from adapter order;
- privacy and scientific thresholds are explicit gates;
- future validation evidence has a stable decision target.

### Negative

- F3-B remains blocked;
- no ephemeris/lunar evidence can be published;
- owner input and a separate spike increment are required.

### Risks

- accepting a local library without independent vectors;
- using shared kernel agreement as proof of accuracy;
- remote coordinate disclosure;
- mutable dependency/data aliases;
- one aggregate tolerance hiding directional or timing failures.

## Migration

1. owner completes F3-OD04–F3-OD10 on an exact commit;
2. ARB reviews the completed ADR and spike authorization;
3. dependencies/data are acquired only in an isolated authorized increment;
4. validation evidence is recorded;
5. ADR is Accepted or Rejected;
6. F3-B remains blocked until acceptance conditions are satisfied.

## Validation

Normative plan: `docs/architecture/validation/BKL-031-F3-A3-Ephemeris-Lunar-Method-Validation-Spike-Plan.md`.

Current evidence:

- official sources reviewed on 2026-09-15;
- repository architecture and authority state verified;
- spike and scientific campaign `NOT EXECUTED`;
- dependency installation/download `NOT EXECUTED`;
- privacy/runtime/OAT `NOT EXECUTED`.

## Traceability

- BKL-031-F3-A3-PROGRAM-001;
- BKL-031-F3-A3-SOLUTION-001;
- BKL-031-F3-VAL-001;
- ADR-009;
- F3-OD04–F3-OD10;
- ARB-204-MI01 and ARB-204-MI02.

## Acceptance rule

ADR-010 may become Accepted only when every required owner disposition is explicit, source and artifact terms are reviewed, exact pins/checksums and coverage are recorded, the authorized validation campaign passes the owner-approved error budget, and ARB/Release Quality gates complete.

## Rollback

Reject or revert ADR-010. S10 remains `UNAVAILABLE`; no runtime rollback is needed.

## Governance stop

Stop at owner decision. This Proposed ADR does not authorize dependencies, kernels, external calls, protected-site transmission, spike execution, schemas, adapters or runtime.
