# BKL-031 F4-C — One-Request Generalized Forecast Acquisition Gate

| Field | Value |
|---|---|
| Identifier | `BKL-031-F4-C-GATE-001` |
| Status | **REVIEW CANDIDATE — NOT EXECUTED** |
| Date | 2026-09-17 |
| Predecessor | F4-B Accepted / Post-Merge Verified |
| Request budget | Exactly one HTTPS GET |
| Location | Synthetic/generalized `42.0, 12.0` |
| Protected-site use | Prohibited |
| Runtime effect | None |

The manual main-only workflow accepts an exact authorized main SHA, one explicit ICON-2I 00/12 UTC run no older than 18 hours, and the exact confirmation `F4C_ONE_GENERALIZED_REQUEST`. It checks that the authorized SHA is still the remote main head before executing. The acquisition script constructs one fixed request to `previous-runs-api.open-meteo.com/v1/forecast` for the eleven accepted variables, GMT/ISO-8601 output, land-cell selection and provider elevation disabled.

The script contains one fetch site, denies redirects, limits execution to one request, enforces a 10-second timeout and 2,000,000-byte response ceiling, rejects non-JSON/provider-error responses, validates hourly lengths and finite values, computes the raw SHA-256 and writes raw plus normalized evidence into a seven-day GitHub artifact. No secret or cloud credential is used.

The outbound point is deliberately generalized and unrelated to the protected observatory record. The gate does not accept coordinate inputs. It authorizes no protected-site egress, retry loop, schedule, recurring traffic, production use, runtime activation, public projection, ranking, readiness, commands or Safety Authority.

After exact-head review, expected-head merge and post-merge verification, one dispatch may execute this gate. Stop after the evidence artifact is produced and reconcile the run before any F4-D projection work.