# AP-008 Remediation and Readiness Record — SessionCompleted Shadow Pilot

| Campo | Valore |
|---|---|
| Identificativo | AP008-REM-SESSIONCOMPLETED-2026-09-22 |
| Package | AP-008 |
| Pilot | INT-SESSION-METADATA-PILOT-001 |
| Baseline | main @ c48cfbae76432cf65d6bca338a06c2775d1147be |
| Scope | read-only repository shadow artifact |
| Decision | READY_WITH_CONDITIONS for shadow evidence; NOT_READY for live integration |
| Runtime authorization | NONE |

## 1. Purpose

This record closes the remediation package for the non-safety-critical shadow pilot without
promoting it to a live adapter, broker, scheduler, command path or Safety Authority.

The pilot proves that a real imported session can be represented as a deterministic,
read-only `DSG.Observation.Event.SessionCompleted` artifact and reconciled against its
manifest and projections. It does not prove transport authentication, live replay,
runtime adapter availability or operational command behavior.

## 2. Verified evidence

| Gate | Status | Evidence |
|---|---|---|
| Real session is COMPLETE | PASS | `data/sessions/2026/09/2026-09-21_2026-09-22/manifest.json` |
| Six evidence files and SHA-256 references | PASS | session manifest and shadow event |
| Configuration identity | PASS | `QUATTRO200_TOUPTEK294_BIN1` |
| Contract candidate envelope | PASS | shadow event and versioned schema |
| Fail-closed mutations | PASS | `.github/scripts/test-session-completed-shadow-event.mjs` |
| Contract compatibility fixture | PASS | `.github/scripts/test-session-completed-shadow-contract-compatibility.mjs` |
| Duplicate identity | PASS | deterministic message identity and NO_OP behavior |
| Repository reconciliation | PASS | event manifest digest/files match imported session |
| Portal/consumer reconciliation | PARTIAL | projections are referenced; no independent consumer replay report |
| Security/trust review | OPEN | no adapter security review executed |
| Contract/adapter ownership | OPEN | owner roles not assigned in repository |
| Rollback/disable drill | OPEN | runbook exists; execution evidence not recorded |
| Live transport/authentication/replay | NOT EXECUTED | explicitly outside shadow scope |

## 3. Contract governance

The candidate schema is versioned at:

`contracts/events/observation-session-completed-shadow-v1.schema.json`

The schema is deliberately scoped to the repository shadow artifact. It requires:

- contract identity and version;
- deterministic message and correlation identity;
- COMPLETE report status;
- manifest provenance and SHA-256 evidence;
- diagnostic severity;
- explicit `runtime_published=false`;
- `command_authority=NONE`;
- local Safety Authority preserved.

The schema is not an approval of the broader candidate catalog entry or of a live transport.

## 4. Ownership record

| Responsibility | Required owner | Current status |
|---|---|---|
| Contract registry and lifecycle | Architecture Office / named contract owner | UNASSIGNED |
| Read-only session adapter | Runtime Integration Owner | UNASSIGNED |
| Repository consumer/projection | Analytics/Portal Owner | UNASSIGNED |
| Security/trust review | Security reviewer | UNASSIGNED |
| Operational disable/rollback | Operations owner | UNASSIGNED |

No live activation may proceed while these roles are unassigned.

## 5. Security and safety decision

The shadow pilot has no command authority and does not call N.I.N.A., PHD2, CPWI,
ASCOM, dome, mount, camera, relay or PLC. Local physical interlocks remain authoritative.

A live adapter requires a separate security review covering:

- credential scope and storage;
- trust boundary and input validation;
- log redaction;
- replay and message integrity;
- dependency compromise;
- disable path and audit retention.

That review is not claimed as executed by this record.

## 6. Reconciliation decision

Repository reconciliation is complete for the real fixture:

`session_id`, manifest Git blob, evidence file count, file paths and SHA-256 references
are consistent with the imported session and its normalized projections.

The following remains open for live integration:

- consumer replay against the projection;
- divergence reporting;
- stale/missing consumer state;
- recovery after partial publication.

## 7. Rollback and disable

The shadow artifact can be disabled by stopping its invocation and removing only the
shadow artifact from the working branch while retaining diagnostic evidence. This does
not modify observatory state or local safety controls.

A controlled drill is still required before any live adapter is considered:

1. disable invocation;
2. verify no new artifact is produced;
3. verify existing repository evidence remains immutable;
4. restore the read-only projection;
5. record operator, timestamp and outcome.

## 8. Readiness decision

`READY_WITH_CONDITIONS` applies only to the repository shadow pilot.

`NOT_READY` applies to:

- live event transport;
- authenticated adapter runtime;
- broker/outbox dispatcher;
- production consumer;
- scheduler changes;
- any command or Safety Authority integration.

## 9. Re-review exit criteria

AP-008 may be reconsidered for a broader approval only after:

1. named owners are recorded;
2. security/trust review is completed;
3. rollback/disable drill evidence is recorded;
4. independent consumer reconciliation report is attached;
5. live contract compatibility, replay and failure tests are executed;
6. baseline and traceability references are updated to the actual merge commit.

This record intentionally does not close those unexecuted gates.
