# BKL-031 F3-A2-D4 — Protected CurrentSetupAssignment DRAFT Materialization

**Identifier:** BKL-031-F3-A2-D4-SOLUTION-001  
**Status:** Review Candidate  
**Version:** 1.0  
**Release:** BKL-031 / F3-A2  
**Date:** 15/09/2026  
**Baseline:** `main@d8e999a2104aa6d420e713fc1872f4317373484b`

## 1. Purpose

Materialize the first governed site-to-setup relationship as a protected, immutable DRAFT while preserving the separate human approval gate required by ADR-009.

## 2. Scope

D4 includes schemas, canonical payload identity, repository validation, deterministic fail-closed resolution semantics, privacy enforcement, tests, workflow and rollback guidance.

It excludes approval receipt, APPROVED lifecycle, runtime adapter, public setup activation, provider selection, EAGLE or observatory activity, readiness/go-no-go, device command and Safety Authority changes.

## 3. Architectural drivers

- bind only already approved authority revisions;
- close `ARB-206-MI01` with an executable closed schema for owner-decision evidence;
- preserve human-only exact-digest approval;
- keep DRAFT and RETIRED records resolver-ineligible;
- reject latest-wins, history, projection, host and operator-memory fallback;
- prevent protected identifiers, digests, locators and exact site facts from entering public outputs.

## 4. Current state

The setup baseline and Site Authority are independently approved. Owner decisions for assignment source, roles and validity are integrated. No approved assignment or runtime authority adapter exists; S09 is `UNAVAILABLE_CURRENT`.

## 5. Target state for D4

| Component | Responsibility | D4 outcome |
|---|---|---|
| Assignment schema | closed envelope, payload, lifecycle and evidence keys | implemented |
| Decision schema | closed D3 decisions, exact references, roles and validity | implemented |
| Protected DRAFT | immutable site-to-baseline relation | materialized, ineligible |
| Validator | digest, binding, interval, authority and privacy gates | implemented |
| Contract suite | positive, negative, property and mutation behavior | 57 cases |
| Governance workflow | execute gates with redacted output | implemented |
| Runtime adapter | serve an application port | excluded |

## 6. Architecture model

The protected DRAFT references but does not copy authority payloads. The validator resolves both exact protected references, recomputes their payload identities, verifies lifecycle and approval-evidence locators, then verifies the assignment payload identity. Resolution evaluates all approved interval candidates; zero is unavailable, more than one is conflicted, and no ordering attribute is a tie-break.

D4 is repository tooling, not a production Infrastructure adapter. The logical ports defined by the accepted F3-A2 contract remain future runtime work.

## 7. Rules and constraints

1. Only the assignment payload is covered by the D4 canonical digest.
2. Object keys are recursively sorted; array order is preserved; compact JSON is encoded as UTF-8 and hashed with SHA-256.
3. Assignment validity uses a half-open interval and begins with the approved setup-baseline effective start.
4. A DRAFT carries no approval or retirement evidence and has `eligibleForResolution=false`.
5. Baseline, site and assignment approvals remain separate.
6. Public projection is deny-by-default and uses an independent namespace and digest if later authorized.
7. Logs and public evidence contain no protected payload content.
8. Local physical interlocks and Safety Authority are unchanged.

## 8. Migration strategy

1. integrate the protected DRAFT and executable gate;
2. verify exact-head CI and AI-assisted process-separated reviews;
3. merge and verify post-merge continuity;
4. present the exact protected assignment digest to the human Approval Authority;
5. only after explicit approval, prepare a separate receipt/promotion package.

No activation pointer or runtime consumer changes in D4.

## 9. Security, safety and operations

The registry remains outside the Pages input. The workflow has read-only contents permission and emits only redacted status. No credentials, serials or runtime locators are introduced. Rollback is a reviewed Git revert; S09 is already unavailable, so there is no runtime rollback.

## 10. Risks and trade-offs

| Risk | Control |
|---|---|
| implicit approval by materialization | DRAFT lifecycle and null receipt fields |
| reference drift | exact identity, version and digest checks |
| ambiguity from overlaps | all-candidate evaluation and `CONFLICTED` |
| public disclosure | deny-by-default policy and repository leak scan |
| premature runtime claim | adapter and OAT explicitly excluded |

## 11. Traceability

| Source | D4 coverage |
|---|---|
| ADR-009 | registry, roles, canonicalization and separate approval |
| F3-A2 contract | identity, lifecycle, intervals, binding and failure semantics |
| F3-A2 validation plan | A2-P01–P12 and A2-N01–N33 |
| F3-A2-D3 evidence | authority, roles and validity decisions |
| F3-A2-D4 handoff | protected DRAFT, tests, workflow and rollback |
| ARB-206-MI01 | closed decision-evidence schema and parity test |
| ARB-204-MI02 | retained before any runtime adapter |

## 12. Acceptance criteria

- closed schemas match validator coverage;
- protected DRAFT binds exact approved sources and recomputes deterministically;
- DRAFT resolves `UNAVAILABLE_CURRENT`;
- 57 tests pass;
- public tree has no protected assignment or exact site literals;
- exact-head workflows are green with no open Blocker/Major;
- rollback is documented.

## 13. Open issues

- mandatory human approval of the exact protected assignment digest;
- separate approval-receipt and lifecycle-promotion package;
- runtime adapter architecture and OAT, subject to `ARB-204-MI02`.
