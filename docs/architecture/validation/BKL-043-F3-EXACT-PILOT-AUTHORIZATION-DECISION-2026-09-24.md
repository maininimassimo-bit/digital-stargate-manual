# BKL-043 F3 — Exact Pilot Authorization Decision Record

| Field | Value |
|---|---|
| Decision ID | `BKL043-F3-EXACT-PILOT-AUTHORIZATION-DECISION-2026-09-24` |
| Status | **OWNER APPROVED PREPARATION OF A SEPARATE EXACT PILOT AUTHORIZATION — NO RUNTIME AUTHORIZATION** |
| Owner / accountable | Massimo Mainini |
| Related proposal | `BKL-043-F3-PILOT-SPECIFICATION-DRAFT-2026-09-24.md` |
| Authority | `command_authority=NONE`, `execution_authority=NONE`, `safety_authority=NONE` |

> **Continuity update — 25/09/2026.** This is the historical F3 disposition that
> authorized preparation only. For the current partial owner selections, use
> `BKL-043-F4-EXACT-PILOT-RUNTIME-AUTHORIZATION-DRAFT-2026-09-24.md`, which
> records the selected two-plane scope, target `EAGLE30154`, GitHub witness-provider
> candidate and nominated reviewer. F4 remains a draft and no runtime authorization
> is created by either record.

## Decision requested

Select one disposition after reviewing the repository-only specification:

- [ ] `RETURNED` — revise the design; comments/required changes: ____________________
- [x] `APPROVED FOR A SEPARATE EXACT PILOT AUTHORIZATION` — continue preparing a
  runtime gate, but **this does not authorize installation, live reads, polling,
  writes, transport or deployment**.
- [ ] `APPROVED WITH CONDITIONS` — conditions and evidence required before a
  separate runtime decision: ________________________________________________

This disposition was explicitly selected by Massimo Mainini on 2026-09-24.
It authorizes preparation of a distinct exact-scope runtime decision only. It
does not supply or approve any runtime parameter below and is not consent to
access live systems.

## Scope fields required before any runtime action

Every field must be completed and explicitly accepted in a separate runtime gate.
“TBD”, inherited defaults, historical commissioning values, or this draft alone
are not authorization.

| Decision | Exact value / owner disposition |
|---|---|
| Pilot scope: local-only (narrow observed-coverage claim) or two-plane | **UNSELECTED** |
| Target host(s), environment, accountable operator and service identity | **UNSELECTED** |
| Exact software artifact/version/hash and configuration | **UNSELECTED** |
| Included components and explicit exclusions | **UNSELECTED** |
| Per-source interface, source owner and read-only boundary evidence | **UNSELECTED** |
| Independent witness/provider and proof it is outside EAGLE failure domain | **UNSELECTED** |
| Transport, authentication, network egress and secret provisioning | **UNSELECTED** |
| Sampling/heartbeat cadence, timeout, freshness and gap semantics | **UNSELECTED** |
| Observation start/end, maximum duration and review checkpoints | **UNSELECTED** |
| Local/remote persistence locations and data schema/version | **UNSELECTED** |
| Data classification, access roles, encryption, backup/export | **UNSELECTED** |
| Retention, deletion, disposal and accountable approver | **UNSELECTED** |
| Resource stop thresholds and measurement method during imaging workload | **UNSELECTED** |
| Installation/start mode (including whether boot/recurring execution is allowed) | **UNSELECTED** |
| Stop conditions, disable/uninstall, rollback and recovery owner | **UNSELECTED** |
| Offline test evidence, security/privacy review and independent reviewer | Synthetic offline envelope tests are implemented; CI/review evidence pending; security/privacy review and independent reviewer **UNSELECTED** |
| Post-change OAT and acceptance criteria | **UNSELECTED** |
| Whether any incident lifecycle is in scope (default: excluded) | **EXCLUDED unless separately gated** |

## Mandatory constraints

- No device commands, control, scheduler decisions, automatic remediation,
  alerts, interlock changes or Safety Authority.
- No source may be accessed unless its exact read-only boundary and source owner
  are approved. No direct probing of equipment is implied by “read-only”.
- No raw N.I.N.A. logs or secrets in the detector store; no automatically created
  incident register; no relay modification/redeployment under this decision.
- Unknown, stale, missing, conflicting or unobserved intervals remain unknown;
  no whole-system uptime, MTBF/MTTR or SLO claim without separately approved
  population, denominator, event semantics and coverage evidence.
- Pilot results do not imply production acceptance or permanent recurring
  operation. Any extension requires a new decision.

## Owner record

- Owner decision: **APPROVED FOR A SEPARATE EXACT PILOT AUTHORIZATION**
- Name: Massimo Mainini
- Date/time and decision reference: **2026-09-24; explicit owner message in the project task, recorded in this decision sheet**
- Conditions / rationale: **Preparation of the separate exact pilot authorization only; all runtime parameters remain unselected and no pilot operation is authorized**
- Signature or explicit recorded approval reference: **Massimo Mainini's explicit approval recorded 2026-09-24**

The approved disposition advances design preparation. Until the separate exact
runtime gate is fully completed and explicitly approved, the authorized scope
remains repository-only design and synthetic/offline validation.

```text
command_authority=NONE
execution_authority=NONE
safety_authority=NONE
```
