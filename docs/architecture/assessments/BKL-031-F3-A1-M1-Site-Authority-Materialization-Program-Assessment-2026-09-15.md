# BKL-031 F3-A1-M1 — Site Authority Materialization Program Assessment

| Campo | Valore |
|---|---|
| Identificativo | BKL-031-F3-A1-M1-PROGRAM-001 |
| Stato | **OWNER DECISION REQUIRED / NO MATERIALIZATION** |
| Data | 15/09/2026 |
| Baseline | `main@9932bace989565a10fd8e0d6f4a9c3b2cc057c46` |
| Capability | BKL-031 — Observation Planner intelligente |
| Predecessore | F3-A2-D2 accepted/post-merge verified |
| Specialist handoff | Solution Architect after owner decision |
| Runtime / EAGLE | None |

## 1. Program outcome

The setup baseline authority is now integrated and approved. The next dependency-ordered gate is the F3-A1 Site Authority materialization path because a `CurrentSetupAssignment` cannot resolve without an approved site record.

The normative F3-A1 contract is accepted with conditions but not implemented. Repository evidence does not identify the exact protected site facts, their approval source or all materialization semantics. The program therefore stops at an owner decision gate and does not create a site record by inference.

## 2. Maturity assessment

| Area | Maturity | Rationale |
|---|---:|---|
| F3-A1 normative contract | 85/100 | accepted with conditions; source-neutral and post-merge verified |
| Site Authority source/roles | 20/100 | no concrete authority decision or protected registry exists |
| Exact site facts | 0/100 | no approved WGS84 record/evidence is present |
| Elevation semantics | 30/100 | field exists; vertical reference and range remain open |
| Resolver identity/scope | 30/100 | Application port defined; canonical resolver authority is open |
| Privacy/public separation | 55/100 | normative allowlist exists; enforcement and leak tests absent |
| Executable validation | 0/100 | validation plan exists; schema/validator/tests not implemented |
| CurrentSetupAssignment | 0/100 | absent and separately approval-gated |

## 3. Dependency-ordered backlog

1. Owner decision on Site Authority system, roles, approval source and protected data classification.
2. Owner approval of exact WGS84 site facts, elevation semantics and validity.
3. Solution Architecture materialization package: schema, canonicalization/digest, validator, bounded fixtures and executable F3-A1 tests.
4. Protected site-record candidate plus separate exact-digest human approval receipt.
5. Repository adapter and policy/leak tests only after architecture acceptance.
6. Separate `CurrentSetupAssignment` candidate and human approval.
7. S08/S09 consumer integration only after all prior gates and re-review.

## 4. Required owner inputs

| Input | Required decision |
|---|---|
| Authority | source system/path, owner, custodian and human Approval Authority |
| Geodesy | exact WGS84 latitude and longitude plus authoritative source |
| Elevation | numeric metres, vertical reference and admitted range |
| Time | IANA timezone |
| Validity | `validFromUtc`, `EXCLUSIVE` or `UNBOUNDED`, and optional `validToUtc` |
| Resolver | canonical resolver identity and authority scope |
| Publication | generalized public label, timezone-display policy and prohibition of exact coordinates |
| Retention/security | protected-record retention and access boundary |

These inputs include protected location data. They must be explicitly supplied or approved by the Repository Owner; browsing, historical telemetry and third-party maps cannot silently become authority.

## 5. Specialist handoff brief

After the owner decision, the Solution Architect shall produce:

- F3-A1 materialization architecture and versioned schema;
- canonical JSON/digest algorithm and lifecycle envelope;
- fail-closed validator and reason codes;
- executable A1-P01–P10 and A1-N01–N41 coverage;
- privacy allowlist, leak tests and logging redaction;
- migration/rollback and no-runtime/no-safety evidence;
- traceability for `ARB-193-MI01`, `ARB-193-MI02`, `ARB-191-MI01` and the executable remainder of `ARB-191-MI02`.

## 6. Acceptance criteria

The future package may proceed to ARB only when:

- owner decisions are recorded without inferred values;
- no exact coordinate appears in public `docs/` or generated public projection;
- schema, validator and tests are deterministic and fail-closed;
- interval adjacency/overlap/unbounded cases are executable;
- public/internal namespace and digest separation are enforced;
- no assignment, readiness, command path, EAGLE workload or Safety Authority is introduced;
- rollback is repository-local and non-destructive.

## 7. Risks and stop condition

| Risk | Treatment |
|---|---|
| disclosure of exact observatory location | protected registry outside Pages; deny-by-default |
| inferred or stale coordinates | explicit owner approval and source locator required |
| ambiguous elevation | close `ARB-193-MI01` before materialization |
| resolver authority conflict | close `ARB-193-MI02` before materialization |
| internal/public correlation | close `ARB-191-MI01` with executable leak tests |
| site approval confused with assignment | distinct records, digests and receipts |
| safety coupling | keep local physical interlocks independent |

**Stop condition:** implementation and protected site-record creation remain paused until the owner supplies the required decisions. No PC, EAGLE, device, network or observatory action is required.
