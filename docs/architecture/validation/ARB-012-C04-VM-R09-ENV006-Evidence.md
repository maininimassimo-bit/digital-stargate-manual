# ARB-012-C04 — VM-R09 / ENV-006 Evidence

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-VM-R09 |
| Work item | C04-W06 |
| Control | VM-R09 / ENV-006 |
| Host | `dsg-arb012-c04-val` |
| DSOC repository | `maininimassimo-bit/DigitalStarGate.Control` |
| Validated commit | `948b49a66c740716e55eec69c2e63ad2b2ddf692` |
| Date | 2026-08-22 |
| Result | **PASS** |

## 1. Purpose

Verify that a C3 approval attempted by the same identity that is also identified as requester is deterministically denied, audited and prevented from reaching execution.

## 2. Execution result

```text
ENV006_RESULT=PASS
DECISION=DENY
REASON=self-approval-prohibited
EXECUTION_ATTEMPTED=false
CORRELATION_ID=d1d8a55d-1771-43a5-8a39-a0063d5eef93
OCCURRED_AT_UTC=2026-08-22T15:06:06.1852336+00:00
LOG_PATH=/var/lib/digitalstargate-validation/env006-validation.log.jsonl
AUDIT_DB_PATH=/var/lib/digitalstargate-validation/dsoc-audit.db
EVIDENCE_PATH=/var/lib/digitalstargate-validation/evidence/ENV-006-d1d8a55d-1771-43a5-8a39-a0063d5eef93.json
```

## 3. Correlation and audit proof

The JSONL log recorded:

```text
actor_id=dsgleonardo
requester_id=dsgleonardo
action=ApproveC3
decision=DENY
reason=self-approval-prohibited
execution_attempted=false
```

The audit database independently returned:

```text
2026-08-22T15:06:06.1852336+00:00|d1d8a55d-1771-43a5-8a39-a0063d5eef93|dsgleonardo|ApproveC3|DENY|self-approval-prohibited
```

The exported JSON evidence contains the same correlation ID, timestamp, actor, requester, action, decision and reason and explicitly records `execution_attempted: false`.

Evidence SHA-256:

```text
bc5cfad39cc14269317dfbcd6604c88c972114fbf29cab60966e8e0c222f0476
```

## 4. Disposition

**VM-R09 / ENV-006: PASS.**

Same-identity C3 approval is denied by the real Application authorization policy before downstream execution. The denial is attributable and correlated across log, audit persistence and exported evidence.