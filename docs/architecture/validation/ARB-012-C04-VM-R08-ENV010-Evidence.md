# ARB-012-C04 — VM-R08 / ENV-010 Evidence

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-VM-R08 |
| Work item | C04-W06 |
| Control | VM-R08 / ENV-010 |
| Host | `dsg-arb012-c04-val` |
| DSOC repository | `maininimassimo-bit/DigitalStarGate.Control` |
| Validated commit | `8147c7a7a1263801f98baea4ffdefd43acee5891` |
| Date | 2026-08-22 |
| Result | **PASS** |

## 1. Purpose

Verify that a single validation request can be correlated across application log, audit persistence and exported evidence using one stable correlation identifier and UTC timestamp.

## 2. Execution result

Validation harness result:

```text
ENV010_RESULT=ALLOW
CORRELATION_ID=1ea67173-c596-423e-b49d-d470abe88cb3
OCCURRED_AT_UTC=2026-08-22T14:38:32.7212201+00:00
LOG_PATH=/var/lib/digitalstargate-validation/env010-validation.log.jsonl
AUDIT_DB_PATH=/var/lib/digitalstargate-validation/dsoc-audit.db
EVIDENCE_PATH=/var/lib/digitalstargate-validation/evidence/ENV-010-1ea67173-c596-423e-b49d-d470abe88cb3.json
```

## 3. Correlation proof

The same correlation ID was independently observed in all three evidence surfaces.

### Application log

```text
{"schema_version":"1.0","environment":"ARB-012-C04-NONPROD","control":"ENV-010","occurred_at_utc":"2026-08-22T14:38:32.7212201+00:00","correlation_id":"1ea67173-c596-423e-b49d-d470abe88cb3","actor_id":"dsgmassimo","action":"RequestC3","decision":"ALLOW","reason":"authorized-validation-action"}
```

### Audit database

```text
2026-08-22T14:38:32.7212201+00:00|1ea67173-c596-423e-b49d-d470abe88cb3|dsgmassimo|RequestC3|ALLOW|authorized-validation-action
```

### Evidence export

```json
{
  "schema_version": "1.0",
  "environment": "ARB-012-C04-NONPROD",
  "control": "ENV-010",
  "occurred_at_utc": "2026-08-22T14:38:32.7212201+00:00",
  "correlation_id": "1ea67173-c596-423e-b49d-d470abe88cb3",
  "actor_id": "dsgmassimo",
  "action": "RequestC3",
  "decision": "ALLOW",
  "reason": "authorized-validation-action"
}
```

Evidence JSON SHA-256:

```text
a394357f8d8ba960d6a5cdb78abea255f3934af1033e572d9f8edb210cba990f
```

## 4. Disposition

**VM-R08 / ENV-010: PASS.**

The same request identity, UTC timestamp, actor, action, decision and reason are traceable across log, audit persistence and exported evidence. This establishes the correlation substrate required for VM-R09 through VM-R11 denial/revocation scenarios.