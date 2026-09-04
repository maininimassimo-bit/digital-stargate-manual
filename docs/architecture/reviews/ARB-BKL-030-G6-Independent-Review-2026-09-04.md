# ARB-BKL-030-G6 — Independent Architecture Review — 2026-09-04

| Campo | Valore |
|---|---|
| Review ID | `ARB-BKL-030-G6` |
| Capability | BKL-030 — EAGLE Health & Reliability Telemetry |
| Scope | G6 — Health History & Persistence |
| PR | #87 |
| Reviewed HEAD | `77de4a556ce771a1add581483421f5ca3669cdcc` |
| Decision | **Approved with Conditions** |

## 1. Executive decision

The Architecture Review Board independently reviewed the G6 package against repository truth, the BKL-030 projection contract, prior G1-G5 decisions, CI evidence and the real EAGLE30154 runtime pilot.

**Decision: Approved with Conditions.**

No Blocker or Major finding prevents merge of the G6 implementation. The package preserves the read-only telemetry boundary, keeps Safety Authority external, introduces append-only duplicate-safe persistence, fails closed on malformed/unavailable input, and demonstrates real runtime idempotency with no deletion.

The approval does **not** authorize a permanent Scheduled Task/service, destructive retention, health thresholds, remediation, or Safety Authority integration.

## 2. Scores

| Dimension | Score | Evidence summary |
|---|---:|---|
| Architecture consistency | 96 | Downstream writer preserves G5 collector boundary and source contract |
| Domain/layer integrity | 98 | Telemetry persistence remains infrastructure-side; no Domain coupling introduced |
| Safety separation | 100 | `READ_ONLY`, `automatic_remediation=false`, Safety Authority outside scope |
| Persistence integrity | 95 | Versioned records, deterministic identity, duplicate-safe replay, atomic validated writes |
| Failure handling / recovery | 94 | Missing/malformed/schema/write/corrupt-segment failure injection covered |
| Operability / observability | 92 | Cycle evidence, checkpoint, run IDs and counters available |
| Security / privacy | 94 | No new remote API; history limited to approved projection evidence |
| Traceability | 91 | Design, implementation, tests, CI and OAT evidence linked in one PR |
| Runtime evidence quality | 90 | Real EAGLE write + replay validated; pilot is intentionally bounded |
| Release readiness | 89 | CI green; permanent orchestration and long-horizon storage remain explicitly unapproved |

Overall assessment: **93.9 / 100**.

## 3. Findings

### No Blocker findings

None.

### No Major findings

None.

### ARB-BKL-030-G6-C01 — Minor — Permanent orchestration not yet governed

The G6 writer is runtime-validated manually, but no permanent Scheduled Task/service cadence has been designed or accepted.

**Required condition:** do not deploy permanent orchestration as part of this merge. Any recurring execution mechanism must be introduced through a separately reviewed operational increment with cadence, overlap, startup/restart and rollback semantics.

### ARB-BKL-030-G6-C02 — Minor — Long-horizon storage growth not yet measured

The OAT measured one real projection: 14 records / 13,945 bytes. This is sufficient for bounded pilot mechanics but not for destructive retention policy design.

**Required condition:** keep `retention_deletion_enabled=false` and `historical_records_deleted=0`. Any compaction/deletion policy requires measured multi-day growth and explicit governance approval.

### ARB-BKL-030-G6-C03 — Observation — Imaging-window non-interference remains limited

G6-D demonstrates bounded write duration and isolation, but the submitted evidence does not constitute a dedicated N.I.N.A./PHD2 imaging-window performance trial for the history writer itself.

**Disposition:** acceptable for merge because permanent orchestration is not being enabled. Validate non-interference before enabling a recurring production cadence during imaging sessions.

## 4. Verified evidence

The reviewed package contains:

- versioned signal-history serializer;
- append-only monthly NDJSON writer;
- deterministic `record_id` identity;
- duplicate replay suppression;
- checkpoint and cycle evidence;
- mutex-based non-overlap;
- G6-C failure injection;
- runtime OAT evidence from EAGLE30154.

Final PR workflow state on reviewed HEAD:

```text
Validate documentation (no deploy)  success
Genera manuale Word                 success
Developer Foundation                success
```

Developer Foundation completed the G6 serializer, writer and failure-injection steps successfully.

Runtime OAT verified:

```text
first write: 14 seen / 14 appended / 0 duplicate / PASS
replay:      14 seen / 0 appended / 14 duplicate / PASS
segment:     14 records / 13,945 bytes unchanged on replay
write_failures = 0
historical_records_deleted = 0
retention_deletion_enabled = false
```

## 5. Safety disposition

G6 does not acquire authority over dome, mount, camera, power, network, Windows Update or observatory Safety Authority. No automated remediation is introduced.

Local physical interlocks remain independent.

## 6. Merge / release conditions

G6 may proceed toward merge provided all of the following remain true:

1. no permanent scheduler/service is introduced in PR #87;
2. destructive retention remains disabled;
3. automatic remediation remains disabled;
4. Safety Authority remains outside scope;
5. reviewed CI remains green at final merge HEAD;
6. Release Quality review confirms package and rollback/readiness disposition.

## 7. Re-review criteria

ARB re-review is required if the package is changed to add any of:

- recurring production orchestration;
- deletion/compaction/retention enforcement;
- health severity thresholds;
- remediation actions;
- Safety Authority coupling;
- new external persistence or network dependency.

## 8. Final decision

**Approved with Conditions.**

G6 implementation and bounded runtime pilot are architecturally acceptable for merge. Conditions C01-C03 intentionally keep recurring production execution, destructive retention and imaging-window performance validation outside the current merge scope.
