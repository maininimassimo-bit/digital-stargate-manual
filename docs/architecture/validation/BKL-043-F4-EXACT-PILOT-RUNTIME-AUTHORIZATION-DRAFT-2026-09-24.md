# BKL-043 F4 — Exact Pilot Runtime Authorization (Decision Draft)

| Field | Value |
|---|---|
| Gate ID | `M-BKL043-F4-EXACT-PILOT-RUNTIME-AUTHORIZATION` |
| Status | **PREPARATION ONLY — OWNER PARAMETERS AND RUNTIME AUTHORIZATION PENDING** |
| Owner / accountable | Massimo Mainini |
| Predecessor disposition | F3 approved for preparation of a separate exact authorization on 2026-09-24 |
| Authority | Repository-only design; `command_authority=NONE`, `execution_authority=NONE`, `safety_authority=NONE` |

## 1. Purpose and authorization boundary

This draft converts the F3 owner disposition into a distinct runtime decision
template. It is not an implementation plan and does not authorize a pilot,
installation, live source access, polling, a boot trigger, persistent writes,
remote heartbeat, incident registration, network egress or deployment.

The F3 disposition authorizes preparation of this gate only. Every field below
must be resolved, reviewed and explicitly approved by the owner before any
runtime preflight or change. `UNSELECTED` is a stop condition, not permission to
inherit a historical default.

## 2. Candidate scope for owner decision

The stated objective is measuring reliability of the whole observatory system.
The F2 design therefore describes two logical planes: an EAGLE-local observer
and a separately durable witness outside the EAGLE failure domain. This is a
candidate topology, not a selected runtime scope. A local-only pilot could
describe only EAGLE-observed component telemetry and cannot claim coverage while
EAGLE is offline. No witness service or storage provider has been selected.

The incident lifecycle remains excluded: OPSC-ALM-001 is a draft and no incident
register exists. N.I.N.A.-logged activity remains the candidate attempt
population; raw logs are not to be copied into telemetry records. Historical
logs may be used only within the already bounded repository/offline analysis
scope, not as live runtime authorization.

## 3. Exact owner decisions required

| Decision field | Current proposal / evidence | Owner decision |
|---|---|---|
| Pilot scope | Two-plane is the F2 logical design; local-only narrows coverage and cannot establish whole-system uptime | **UNSELECTED** |
| Target host and environment | EAGLE host is the stated concept; exact machine identity, OS baseline and maintenance window are not established in this gate | **UNSELECTED** |
| Service identity and operator | Least privilege is mandatory; no new identity selected | **UNSELECTED** |
| Software artifact and configuration | F3 schema/validator are contract tests, not a runtime collector; implementation and immutable artifact digest do not exist | **UNSELECTED** |
| Included sources/components | Candidate source-owned projections only; no live producer/read-only boundary has been revalidated for this pilot | **UNSELECTED** |
| N.I.N.A. logs | User confirmed logs are available; parsing, event grouping, retry/terminal semantics and population reconciliation are not accepted | **OFFLINE ANALYSIS ONLY; runtime ingestion unselected** |
| Independent witness | Required for EAGLE-off coverage; no independent service/provider or durable receipt store is selected | **UNSELECTED** |
| Transport, authentication and egress | No endpoint, protocol, credential, network rule or secret provisioning approved | **UNSELECTED** |
| Sampling/heartbeat cadence, timeout, freshness and gap semantics | Historical producer cadence is not transferable; no approved values | **UNSELECTED** |
| Start mode | User-originated concept mentioned starting with EAGLE; F2/F3 do not authorize boot-start, scheduled task or recurring execution | **UNSELECTED** |
| Observation window/checkpoints | No duration or start/end selected | **UNSELECTED** |
| Local/remote data stores | No journal, database or hosted store approved | **UNSELECTED** |
| Data classification, roles, encryption and backup | Minimum-data design exists; target-specific controls not reviewed | **UNSELECTED** |
| Retention/deletion/disposal | No duration, deletion procedure or approver selected | **UNSELECTED** |
| Resource budget and stop limits | Must be measured against an agreed imaging workload; no numeric limits approved | **UNSELECTED** |
| Installation, disable, uninstall and rollback | Must be exact for the selected artifact/host; not prepared for runtime | **UNSELECTED** |
| Security/privacy review | Required before any live access or persistence | **PENDING** |
| Independent architecture and release-quality review | Required; no reviewer nominated | **PENDING** |
| OAT and acceptance criteria | Must be tied to exact sources, coverage, stop conditions and rollback | **UNSELECTED** |
| Incident lifecycle | Separate contract and authorization required; current default excludes it | **EXCLUDED** |

## 4. Required evidence before the runtime decision can be submitted

1. Close the F3 review findings and preserve the offline test evidence.
2. Select the pilot scope and exact host, identity, artifact and components.
3. Prove every selected source is available through an exact read-only interface;
   exclude direct device probing and command-capable credentials.
4. For a two-plane scope, demonstrate an independent witness and durable receipt
   store outside EAGLE's host, power and network failure domains.
5. Define data minimization, privacy/security controls, retention/deletion,
   resource stop limits, observation window and review checkpoints.
6. Specify install/start/stop/uninstall/rollback and recovery verification.
7. Complete independent reviews and offline, security/privacy and resource
   preflight evidence. The preflight must not access live sources until separately
   authorized.
8. Submit a final decision record with every field exact and no `UNSELECTED`,
   then wait for explicit owner approval naming that exact record/version.

## 5. Fixed constraints

- No device commands, control path, broker, decision scheduler, remediation,
  alert, interlock change, readiness decision or Safety Authority.
- No automatic incident creation or closure; no incident register in this gate.
- Unknown, stale, missing, conflicting and unobserved intervals remain unknown.
- No whole-system uptime, availability, MTBF, MTTR, SLI/SLO or failure-budget
  claim until the population, denominator, event semantics and coverage are
  separately accepted and validated.
- No runtime operation, pilot deployment or live data access is authorized by
  this draft or by the F3 preparation disposition.

```text
command_authority=NONE
execution_authority=NONE
safety_authority=NONE
```

## References

- `docs/architecture/validation/BKL-043-F3-READONLY-PILOT-READINESS-GATE-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F3-PILOT-SPECIFICATION-DRAFT-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F3-EXACT-PILOT-AUTHORIZATION-DECISION-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F2-SYSTEM-DETECTION-ARCHITECTURE-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F1-SOURCE-DISCOVERY-2026-09-24.md`
- `docs/architecture/validation/BKL-043-F1-POPULATION-AND-CONTRACT-GAP-DISCOVERY-2026-09-24.md`
