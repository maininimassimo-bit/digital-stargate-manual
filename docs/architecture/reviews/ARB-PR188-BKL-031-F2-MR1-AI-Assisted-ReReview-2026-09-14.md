# ARB — PR #188 BKL-031 F2 M-R1 Remediation Re-Review

| Field | Value |
|---|---|
| Review ID | ARB-PR188-BKL031-F2-AI-003 |
| Review mode | AI-assisted, owner-authorized; not an independent human approval |
| Date | 2026-09-14 |
| Pull request | #188 |
| Exact M-R1 remediation head reviewed | `8e46ae3eccdaca5763aee7103063e020f97e2946` |
| Base | `f6c4b253a56406c930f009af0658b46a12bc088a` |
| Previous ARB decision | Rework Required — 97/100 |
| Decision | **APPROVED** |
| Score | **99 / 100** |

## 1. Independence and authorization disclosure

This re-review was produced by an AI acting in the Architecture Review Board role after explicit repository-owner authorization for exact head `8e46ae3eccdaca5763aee7103063e020f97e2946`.

It is AI-assisted and is **not equivalent to an independent human approval**. It does not authorize merge, waiver, BKL-031 F3, providers, ranking or runtime activity. The reviewer did not modify the package while assessing it.

## 2. Reviewed scope and repository truth

The review examined the M-R1 correction and the complete BKL-031 F2 package:

- normative validator, 37-test suite and JSON Schema;
- bounded M 27 fixture and source registry S01–S11;
- architecture and validation evidence;
- previous findings M-01–M-04 and M-R1;
- exact-head workflow evidence and PR governance state.

Verified repository state:

- `main`: `f6c4b253a56406c930f009af0658b46a12bc088a`;
- PR #188: open, draft, mergeable, not merged;
- reviewed head: seven commits ahead / zero behind, 17 changed files;
- repository rulesets: none;
- exact-head workflows: 7/7 SUCCESS;
- Developer Foundation: normative fixture PASS and Node suite 37/37 PASS.

## 3. Finding disposition

| Finding | Disposition | Verified evidence |
|---|---|---|
| M-01 validator totality | **Closed** | structural guards and 250 malformed JSON variants return errors with zero throws |
| M-02 exact Citation/Provenance binding | **Closed** | source-field equality and exact input/output/Citation-set regressions pass |
| M-03 semantic smuggling | **Closed** | per-dimension vocabulary and prohibited semantic/value checks pass |
| M-04 coordinate authority/conflict | **Closed** | exact triplet, domains, S02 evidence reconciliation and conflict-state checks pass |
| M-R1 unsupported S04 coordinate attestation | **Closed** | S04 removed from coordinate source contracts; direct S04 Citation rejected; dedicated regression passes |

The correction takes the minimum bounded path: S04 remains registered historical evidence but has no F2 coordinate-fact authority until a future governed coordinate-bearing projection exists.

## 4. Scoring matrix

| Dimension | Score | Evidence-based assessment |
|---|---:|---|
| Program and enterprise alignment | 100 | F2 remains bounded; BKL-031/BKL-032 separation is intact |
| Source authority and ownership | 100 | coordinate facts are restricted to the only current machine-readable authority, S02 |
| Domain and semantic integrity | 99 | fact vocabularies, units, source classes and value domains are closed |
| Layer and dependency integrity | 100 | repository/CI only; no provider, runtime or EAGLE dependency |
| Safety | 100 | action and Safety authority remain NONE; no command/readiness path |
| Security and privacy | 98 | public locator allowlist and non-public S02/S04 detail boundaries remain explicit |
| Freshness, missingness and conflict | 99 | unavailable/current/forecast separation and coordinate conflicts fail closed |
| Contract integrity and fail-closed behavior | 99 | malformed structures and semantic/source mismatches return deterministic errors |
| Traceability and documentation | 98 | architecture, validation, review history, PR metadata and navigation are coherent |
| Migration and rollback | 100 | additive repository change with revert-only rollback |
| Validation evidence | 99 | 37/37 tests, 250 malformed probes and 7/7 workflows are verified |

Rounded ARB score: **99 / 100**.

## 5. Findings

### Blocker

None.

### Major

None.

### Minor

None.

### Observations

- O-01 — The fixture remains bounded to one candidate, one context and seven dimensions.
- O-02 — S07–S11 remain unavailable/current-unknown; no provider data is invented.
- O-03 — S04 remains discoverable only as historical normalized evidence and must resolve through S03; it cannot attest coordinates in F2.
- O-04 — No runtime, device, network, power, EAGLE or physical Safety behavior changes.
- O-05 — No `main` ruleset exists. This is a merge-control risk, not an architecture defect, and this review grants no waiver.
- O-06 — The review is AI-assisted and does not provide independent human approval.

## 6. Executed validation evidence

Exact-head GitHub Actions on `8e46ae3eccdaca5763aee7103063e020f97e2946`:

- Developer Foundation #1389 — SUCCESS;
- Validate documentation #1026 — SUCCESS;
- Genera manuale Word #1452 — SUCCESS;
- Scientific Platform Governance #89 — SUCCESS;
- BKL-041 F4 Governance #91 — SUCCESS;
- BKL-046 F4 governance #65 — SUCCESS;
- BKL-046 F5 governance #50 — SUCCESS.

Developer Foundation logs verify:

```text
BKL-031 F2 context contract OK: 11 sources / 1 candidate / 7 dimensions / no ranking
tests 37
pass 37
fail 0
```

The named M-R1 test confirms that the current S04 artifact cannot substantiate coordinate facts. Independent inspection confirms that the S04 direct-Citation branch and S04 coordinate-source allowance are absent, while the schema fixes celestial coordinate `source_ref` to S02.

Not executed or claimed:

- provider/API, ephemeris, lunar or forecast runtime validation;
- ranking effectiveness or target ordering;
- portal consumer or PC Principale/EAGLE OAT;
- independent human review;
- merge or post-merge validation.

## 7. Decision

**APPROVED** for the bounded BKL-031 F2 architecture package at exact head `8e46ae3eccdaca5763aee7103063e020f97e2946`.

This architecture decision does not authorize merge. Release Quality, exact-head review-publication checks and repository-owner merge governance remain separate.
