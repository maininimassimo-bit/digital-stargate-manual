# ARB-012-C04 — VM-R10 / ENV-007 Evidence

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-VM-R10 |
| Work item | C04-W06 |
| Control | VM-R10 / ENV-007 |
| Host | `dsg-arb012-c04-val` |
| DSOC repository | `maininimassimo-bit/DigitalStarGate.Control` |
| Validated commit | `2493eb1e1c26a5191895df50ebd8704fafe87dbf` |
| Date | 2026-08-22 |
| Result | **PASS** |

## 1. Purpose

Verify that an identity that is valid before suspension is deterministically denied after suspension, with correlated audit evidence and no downstream execution.

## 2. Execution result

```text
ENV007_RESULT=PASS
BASELINE_DECISION=ALLOW
SUSPENDED=true
DECISION=DENY
REASON=principal-suspended
EXECUTION_ATTEMPTED=false
CORRELATION_ID=c1d35282-e64d-4b2d-a793-750c4b8c950d
OCCURRED_AT_UTC=2026-08-22T15:29:42.5216539+00:00
LOG_PATH=/var/lib/digitalstargate-validation/env007-validation.log.jsonl
AUDIT_DB_PATH=/var/lib/digitalstargate-validation/dsoc-audit.db
EVIDENCE_PATH=/var/lib/digitalstargate-validation/evidence/ENV-007-c1d35282-e64d-4b2d-a793-750c4b8c950d.json
```

## 3. Correlation and audit proof

The JSONL log recorded the same correlation ID with:

```text
actor_id=dsgmassimo
action=RequestC3
baseline_decision=ALLOW
suspended=true
decision=DENY
reason=principal-suspended
execution_attempted=false
result=PASS
```

The audit database independently returned:

```text
2026-08-22T15:29:42.5216539+00:00|c1d35282-e64d-4b2d-a793-750c4b8c950d|dsgmassimo|RequestC3|DENY|principal-suspended
```

The exported JSON evidence contains the same correlation ID, UTC timestamp, actor, action, baseline decision, suspension state, denial reason and `execution_attempted: false`.

Evidence SHA-256:

```text
cf7e2f52783b69cd96898ca032d9eb70c5d7262ab4d7333f475a1f37b7b319bb
```

## 4. Disposition

**VM-R10 / ENV-007: PASS.**

The applicable validation principal is authorized before suspension and denied immediately after suspension with reason `principal-suspended`. No downstream execution was attempted and the result is correlated across log, audit persistence and exported evidence.