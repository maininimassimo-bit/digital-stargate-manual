# ARB-012-C04 — VM-R07 / ENV-009 Evidence

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-VM-R07 |
| Work item | C04-W06 |
| Controls | PRV-011 / ENV-009 |
| Host | `dsg-arb012-c04-val` |
| DSOC commit | `436c143f36e687609165fb56d3457eacd18c1034` |
| Date | 2026-08-22 |
| Result | **PASS** |

## 1. Purpose

Prove that the validation stores can be reset and rebuilt from versioned repository assets into the same governed logical baseline.

## 2. Versioned rebuild assets

The DSOC repository contains:

- `validation/sql/reset-validation.sql`;
- `validation/sql/reset-audit.sql`;
- `validation/sql/rebuild-validation-stores.sh`.

The rebuild script removes only the two validation SQLite files under `/var/lib/digitalstargate-validation`, recreates them from the versioned SQL files, restores `0640` permissions, and emits metadata/schema/count evidence.

## 3. Pre-reset logical baseline

Validation store:

```text
CREATE TABLE validation_metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
environment|ARB-012-C04-NONPROD
purpose|validation-only
```

Audit store:

```text
CREATE TABLE audit_events (id INTEGER PRIMARY KEY AUTOINCREMENT, occurred_at_utc TEXT NOT NULL, correlation_id TEXT NOT NULL, actor_id TEXT NOT NULL, action TEXT NOT NULL, decision TEXT NOT NULL, reason TEXT NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
```

Pre-reset SHA-256 values were retained as evidence but are not the determinism criterion:

- validation DB: `c6e5df053867de95a1edc70ec43f6f68548af04e42710330f394a7a5f6d5431b`;
- audit DB: `ca729e0f9adc289f69b698845b02e27ce07bd13b725c56e6fe6123cb715539e0`.

## 4. Rebuild execution

Executed:

```text
bash validation/sql/rebuild-validation-stores.sh
```

Observed output confirmed:

- `environment|ARB-012-C04-NONPROD`;
- `purpose|validation-only`;
- the expected `validation_metadata` schema;
- the expected `audit_events` schema;
- audit event row count `0`.

Independent post-run queries reproduced the same logical state.

Post-rebuild SHA-256 values changed to:

- validation DB: `16120a563ce681af2ff7cbfd0712c89ec57d3bfbb3721c41b3eb48ea79fd4fe8`;
- audit DB: `3bab706b89f24afe2a4445abdca21590fa87533569d70bbf01674749773434bc`.

The differing file hashes are expected and do not invalidate the test: SQLite physical file layout is not the governed determinism criterion. Determinism is defined by the versioned schema, seed metadata and empty audit baseline.

## 5. Disposition

**VM-R07 / PRV-011 / ENV-009: PASS.**

The validation persistence baseline can be destroyed and rebuilt from repository-controlled assets into the same expected logical state without production dependencies or observatory device interaction.