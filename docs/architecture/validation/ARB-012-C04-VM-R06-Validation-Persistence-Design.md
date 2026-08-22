# ARB-012-C04 — VM-R06 Validation Persistence Design

| Field | Value |
|---|---|
| Design ID | ARB-012-C04-VM-R06-DES-001 |
| Work item | C04-W06 |
| Controls | PRV-007 / PRV-008 / ENV-008 |
| Target model | Two-Person Limited Operations Model |
| Date | 2026-08-22 |
| Status | Approved for validation execution |
| Scope | Non-production validation VM only |

## 1. Purpose

Define the smallest persistence arrangement needed to complete VM-R06 without making a production architecture decision by accident.

The repository reference architecture assigns audit persistence to Infrastructure and leaves the audit-store implementation open. VM-R06 therefore adopts a local-only validation design that is intentionally replaceable.

## 2. Decision

Use **SQLite** for the isolated validation environment, with two physically separate local database files:

- test database: `/var/lib/digitalstargate-validation/dsoc-validation.db`;
- audit evidence store: `/var/lib/digitalstargate-validation/dsoc-audit.db`.

No TCP listener, remote database endpoint, production credential or observatory-network dependency is permitted.

This is a **validation-only implementation decision**. It does not establish SQLite as the production persistence technology for Digital StarGate.

## 3. Responsibilities

| Store | Purpose | Allowed content | Prohibited content |
|---|---|---|---|
| `dsoc-validation.db` | non-production application/test state for VM validation | synthetic principals, validation requests, role-state fixtures, reset markers | production sessions, observatory credentials, production endpoints |
| `dsoc-audit.db` | attributable validation audit/evidence records | event ID, UTC timestamp, actor ID, action, decision, reason, correlation ID, test/run reference | passwords, MFA secrets, private keys, production tokens |

## 4. Isolation and access

Directory target:

```text
/var/lib/digitalstargate-validation
```

Required properties:

- local filesystem only;
- no database network listener;
- owner `dsgoperator` for validation administration;
- directory mode `0750`;
- database files mode `0640`;
- `dsgmassimo` and `dsgleonardo` do not receive Linux sudo or direct administrative ownership merely because they are application validation identities;
- application authorization remains in DSOC Application, not Linux groups.

## 5. Minimal schema

### Test database

```sql
CREATE TABLE validation_state (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at_utc TEXT NOT NULL
);
```

### Audit evidence store

```sql
CREATE TABLE audit_event (
    event_id TEXT PRIMARY KEY,
    observed_at_utc TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    action TEXT NOT NULL,
    decision TEXT NOT NULL,
    reason TEXT NOT NULL,
    correlation_id TEXT NOT NULL,
    evidence_ref TEXT NULL
);

CREATE INDEX ix_audit_event_correlation
    ON audit_event(correlation_id);
```

The schema is deliberately minimal. It is sufficient for VM-R06 and prepares VM-R08 correlation testing without claiming a final production event model.

## 6. Retention and reset

For the validation environment:

- audit evidence is retained until the associated ARB-012-C04 evidence is versioned/reconciled;
- test database state may be reset as part of VM-R07;
- audit evidence must not be silently deleted when test state is reset;
- any audit reset used solely for repeatable testing must be separately attributable and must not overwrite retained evidence already referenced by governance records.

## 7. Acceptance criteria

VM-R06 passes when attributable VM evidence proves:

1. SQLite is available on the validation VM;
2. `/var/lib/digitalstargate-validation` exists with the intended ownership/mode;
3. both database files are created locally;
4. the minimal schemas are present;
5. no TCP listener is opened by the persistence implementation;
6. file ownership/modes match the design;
7. the stores are explicitly identified as non-production;
8. no production secret or endpoint is required.

## 8. Safety and architecture boundaries

- No physical-device command is part of VM-R06.
- No observatory route is required; VM-R01 isolation remains authoritative.
- Domain remains persistence-independent.
- Application authorization remains independent from storage technology.
- Persistence belongs to Infrastructure when application integration is added.

## 9. Current disposition

**READY FOR VM EXECUTION.**

The next step is to inspect whether `sqlite3` is already installed on `dsg-arb012-c04-val`. Installation or schema creation must occur only after that check.