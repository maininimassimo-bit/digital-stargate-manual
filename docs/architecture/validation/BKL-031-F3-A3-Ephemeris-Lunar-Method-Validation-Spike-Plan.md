# BKL-031 F3-A3 — Ephemeris/Lunar Method Validation Spike Plan

| Field | Value |
|---|---|
| Identifier | BKL-031-F3-A3-VAL-001 |
| Status | **PROPOSED VALIDATION PLAN — NOT EXECUTED / NOT AUTHORIZED** |
| Version | 1.0 |
| Date | 2026-09-15 |
| Architecture | BKL-031-F3-A3-SOLUTION-001 |
| Proposed ADR | ADR-010 |
| Baseline | `main@4f76f6646769df378859fbb15147851b4d0543fe` |
| Runtime / PC Principale / EAGLE | None |

## 1. Objective

Define the smallest reproducible evidence campaign that can inform F3-OD04–F3-OD10 without using production runtime, real protected site fixtures or implicit provider selection.

## 2. Entry gates

All must be satisfied before execution:

- ADR-010 contains explicit owner dispositions applicable to the spike;
- exact package/data versions and artifact digests are approved;
- license, notices, provenance and redistribution review is recorded;
- synthetic/generalized site and target inputs are approved;
- execution host is explicitly authorized and is not EAGLE;
- numeric per-metric error budget is approved;
- bounded grid and resource limits are approved;
- external access is disabled unless separately authorized;
- rollback and evidence destination are approved.

Until then, every case is `NOT EXECUTED`.

## 3. Candidate manifests to prepare after authorization

| Track | Observed candidate baseline | Required execution pin |
|---|---|---|
| A | Astropy 8.0.1 + jplephem 2.24 | package artifact hashes, Python/runtime identity, exact JPL SPK and IERS data |
| B | Skyfield 1.55 | package artifact hash, Python/runtime identity, exact JPL SPK and timescale data |
| C | Horizons API v1.3 | response contract snapshot, request policy, service version evidence and privacy authorization |

Observed versions are decision inputs, not approved pins. Refresh them immediately before owner approval.

## 4. Test-data policy

- no exact Manciano coordinates, elevation, address, protected locator or protected record digest in public artifacts;
- use at least two unmistakably synthetic/generalized sites with `environment=TEST` and `authority=NONE`;
- use public celestial target coordinates with citations and immutable fixture digests;
- use UTC instants only; local-time displays are derived and never calculation inputs;
- real protected coordinates may be used only in a separately authorized protected campaign;
- Horizons receives geocentric or synthetic/generalized site data unless explicit exact-site approval exists;
- no golden vector is authoritative without generator/reference identity and digest.

## 5. Grid dimensions

The owner must set exact maxima before execution.

| Dimension | Required coverage | Bound |
|---|---|---|
| target declination | representative north/equatorial/south targets | F3-OD10 |
| hour angle | rise/set vicinity, transit and off-meridian | F3-OD10 |
| lunar geometry | multiple phases and separations | F3-OD10 |
| date | normal dates, time-data boundary, kernel boundaries | F3-OD10 |
| site | synthetic latitude/longitude/elevation classes | F3-OD10 |
| refraction | airless baseline; refracted only as separate profile | F3-OD10 |
| failure mutation | dependency/data/time/cache/provider errors | bounded case list |

The grid generator must reject expansion beyond the accepted manifest.

## 6. Metrics and units

| Metric | Calculation | Owner threshold |
|---|---|---|
| altitude difference | absolute angular difference in arcseconds | `E_alt` |
| azimuth difference | circular angular difference in arcseconds | `E_az` |
| transit difference | absolute time difference in seconds | `E_transit` |
| target–Moon separation difference | absolute angular difference in arcseconds | `E_sep` |
| lunar illumination difference | absolute fraction difference | `E_illum` |
| repeatability | same normalized input/profile across repeated executions | `E_repeat` |
| performance | duration and peak resource observations | F3-OD09 budget |

Each metric passes independently. No average or weighted score is permitted.

## 7. Validation stages

### Stage V0 — Static decision evidence

Verify documents, identifiers, links, official-source snapshot, candidate manifests and owner dispositions. No dependency installation.

### Stage V1 — Isolated acquisition

On the authorized host only, acquire exact package/data artifacts, record hashes/attestations/licenses and prevent implicit network retrieval during calculation.

### Stage V2 — Synthetic execution

Execute the bounded grid for each authorized candidate. Store normalized inputs/results, raw protected evidence where authorized, metrics and digests.

### Stage V3 — Independent comparison

Compare implementation cross-checks separately from the approved independent reference. Record per-vector results and disagreement classification.

### Stage V4 — Failure, privacy and resource campaign

Execute negative cases, public-artifact scanning, parser/service failures, bounds and rollback.

### Stage V5 — Decision review

Produce a sanitized evidence matrix. ADR-010 is Accepted, Rejected or left Proposed. No adapter enters runtime.

## 8. Positive cases

| ID | Case | Expected evidence |
|---|---|---|
| A3-P01 | exact manifest resolves | all artifact identities and coverage recorded |
| A3-P02 | one normalized instant, airless topocentric | typed result with complete lineage |
| A3-P03 | bounded vector batch | every vector within accepted bounds |
| A3-P04 | repeated clean execution | repeatability within `E_repeat` |
| A3-P05 | target and Moon same instant/profile | shared request/profile digest |
| A3-P06 | meridian-transit comparison | per-method time and `E_transit` result |
| A3-P07 | lunar phase/illumination comparison | explicit convention and `E_illum` result |
| A3-P08 | target–Moon separation | consistent frame/time and `E_sep` result |
| A3-P09 | exact cache hit | identical artifact/request/profile identity |
| A3-P10 | sanitized publication | no protected value or correlatable digest |

## 9. Negative and boundary cases

| ID | Mutation/failure | Expected result |
|---|---|---|
| A3-N01 | package version range or `latest` | manifest rejected |
| A3-N02 | package/artifact hash mismatch | acquisition rejected |
| A3-N03 | kernel ID/hash mismatch | no calculation |
| A3-N04 | instant outside kernel coverage | `OUT_OF_COVERAGE` |
| A3-N05 | IERS/EOP missing or stale | `TIME_DATA_UNAVAILABLE` |
| A3-N06 | time scale/frame/epoch absent | invalid request/profile |
| A3-N07 | refraction requested without profile | invalid request/profile |
| A3-N08 | near-horizon refracted instability | separate-profile failure; airless baseline unaffected |
| A3-N09 | local adapter exception | S10 unavailable; no alternate adapter |
| A3-N10 | Horizons 503/timeout | reference unavailable; no promotion |
| A3-N11 | Horizons HTTP 200 with error payload | semantic failure |
| A3-N12 | malformed/unexpected remote payload | parser failure |
| A3-N13 | exact site data in remote request without approval | privacy failure |
| A3-N14 | protected coordinates/digest in public artifact/log | publication failure |
| A3-N15 | candidate disagreement over metric budget | conflicted evidence |
| A3-N16 | implementation agreement without independent reference | insufficient evidence |
| A3-N17 | target/instant/span exceeds bound | `REQUEST_BOUND_EXCEEDED` |
| A3-N18 | cached response identity mismatch | cache rejected |
| A3-N19 | previous result served after refresh failure as current | failure |
| A3-N20 | unavailable/conflicted result contains value | contract failure |
| A3-N21 | reference used as runtime fallback | architecture failure |
| A3-N22 | execution on EAGLE | placement failure |
| A3-N23 | forecast/ranking/readiness/command field appears | scope regression |
| A3-N24 | Safety state inferred | critical boundary failure |

## 10. Evidence manifest

Every run records:

- campaign ID and exact repository commit;
- execution host authorization reference;
- sanitized fixture-set digest;
- package/runtime artifact identities and hashes;
- kernel/data/IERS identities, hashes, coverage and freshness;
- method profile, time scale, frame, epoch, datum and refraction mode;
- normalized request/result digests;
- per-vector, per-metric difference and pass/fail;
- failure state/reason code;
- duration and bounded resource observations;
- external-call count and approved destination if applicable;
- privacy scan result;
- raw/sanitized evidence locations with access classification.

## 11. Independence rules

- Astropy and Skyfield using the same JPL SPK constitute an implementation cross-check, not full data-model independence.
- Horizons may serve as an external reference only within its accepted privacy/availability profile.
- A second kernel/report or another owner-approved reference is required if the accepted error budget demands data-model independence.
- No majority vote, averaging or silent normalization resolves disagreement.
- Any unexplained over-budget vector blocks acceptance.

## 12. Supply-chain and licensing gates

- verify package metadata, license and exact artifact hashes;
- verify JPL SPK source, coverage, checksum, notices and permitted retention/redistribution;
- verify IERS/EOP source, version, freshness and redistribution;
- generate an SBOM or equivalent manifest for the isolated spike;
- record vulnerability review at the exact versions;
- disable unpinned transitive resolution;
- prove rollback/removal of acquired artifacts.

## 13. Privacy and security gates

- scan public diff, generated site, logs and artifacts for coordinate pairs, protected IDs/digests, local hosts/paths and credentials;
- prove remote payload minimization;
- prove TLS verification and bounded timeouts if remote access is authorized;
- no remote request retry with a different site or method;
- malformed provider content remains untrusted input;
- public evidence uses non-correlatable references.

## 14. Quality-gate matrix

| Gate | Current state | Execution evidence required |
|---|---|---|
| architecture/ADR traceability | DEFINED | exact accepted ADR |
| package/data pins | NOT SELECTED | manifests and hashes |
| license/provenance | REVIEWED AT SOURCE LEVEL | exact artifact review |
| scientific error budget | OWNER DECISION REQUIRED | accepted per-metric values |
| synthetic grid | DEFINED / UNBOUNDED | accepted limits and fixture digest |
| candidate execution | NOT EXECUTED | normalized result evidence |
| independent reference | NOT SELECTED | accepted reference and vectors |
| failure/privacy tests | NOT EXECUTED | A3-N01–N24 results |
| performance/resource | NOT EXECUTED | measurements against F3-OD09 |
| runtime/OAT | NOT AUTHORIZED | not part of spike |

## 15. Acceptance criteria

The spike may support ADR acceptance only when:

- every entry gate is satisfied;
- all artifact identities and coverage are exact;
- all positive cases pass;
- all negative/boundary cases produce expected fail-closed outcomes;
- every vector passes every owner-approved metric;
- independent-reference semantics are satisfied;
- no protected/public boundary violation occurs;
- resource bounds pass on the authorized host;
- evidence is reproducible from the manifest;
- ARB and Release Quality review the exact evidence commit.

## 16. Rollback

Delete or quarantine the isolated environment and acquired artifacts according to approved retention, retain audit evidence, reject/leave ADR-010 Proposed and keep S10 `UNAVAILABLE`. No operational rollback or EAGLE action is required.

## 17. Current execution status

All stages V1–V5 and cases A3-P01–P10/A3-N01–N24 are `NOT EXECUTED`. Only repository/source inspection and documentation preparation have occurred.

## 18. Governance stop

Stop before owner dispositions and separate spike authorization. This plan does not authorize installation, download, network calls, real-site use, host selection, tests, schema, adapter or runtime work.
