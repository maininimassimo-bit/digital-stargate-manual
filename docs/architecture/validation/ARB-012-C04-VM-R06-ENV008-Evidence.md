# ARB-012-C04 — VM-R06 / ENV-008 Evidence

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-VM-R06 |
| Work item | C04-W06 |
| Controls | PRV-007 / PRV-008 / ENV-008 |
| Host | `dsg-arb012-c04-val` |
| Date | 2026-08-22 |
| Result | **PASS** |
| Runtime effect | Validation-only local persistence; no observatory runtime effect |

## 1. Test database

Local SQLite store:

`/var/lib/digitalstargate-validation/dsoc-validation.db`

Properties observed:

- SQLite 3.x database;
- created with SQLite CLI 3.46.1;
- permissions `0640`;
- owner/group `dsgoperator:dsgoperator`;
- explicit metadata:
  - `environment = ARB-012-C04-NONPROD`;
  - `purpose = validation-only`;
- SHA-256 at evidence time:
  `c6e5df053867de95a1edc70ec43f6f68548af04e42710330f394a7a5f6d5431b`.

## 2. Audit evidence store

Local SQLite store:

`/var/lib/digitalstargate-validation/dsoc-audit.db`

Schema includes `audit_events` with fields for UTC timestamp, correlation ID, actor ID, action, decision and reason.

Properties observed:

- SQLite 3.x database;
- permissions `0640`;
- owner/group `dsgoperator:dsgoperator`;
- SHA-256 at evidence time:
  `ca729e0f9adc289f69b698845b02e27ce07bd13b725c56e6fe6123cb715539e0`.

## 3. Network exposure

`ss -lntup` filtered for common database listeners and SQLite returned:

```text
Nessun listener database rilevato
```

The stores are therefore local files and expose no database network listener in the validation VM.

## 4. Scope and architecture note

SQLite is selected only for the ARB-012-C04 non-production validation environment. This evidence does not establish SQLite as the production persistence technology. The observatory automation reference architecture still treats audit persistence as an Infrastructure responsibility whose production implementation remains separately governed.

## 5. Disposition

**VM-R06 / PRV-007 / PRV-008 / ENV-008: PASS.**

The validation test database and audit evidence store are explicitly non-production, local, permission-restricted, independently identified, checksummed and not exposed through a DB listener.