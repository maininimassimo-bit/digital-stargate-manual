# BKL-031 F4-C — Replacement Generalized Forecast Acquisition Gate

| Field | Value |
|---|---|
| Identifier | `BKL-031-F4-C-GATE-002` |
| Status | **REMEDIATION REVIEW CANDIDATE — REPLACEMENT NOT EXECUTED** |
| Date | 2026-09-17 |
| Predecessor | F4-C first attempt failed after one provider request |
| First attempt | GitHub Actions run `35201479378`; HTTP 400; request consumed |
| Replacement budget | Exactly one HTTPS GET; cumulative F4-C ceiling two requests |
| Location | Synthetic/generalized `42.0, 12.0` |
| Protected-site use | Prohibited |
| Runtime effect | None |

The original gate was merged at `48bd61a3337523b7790d78a37813eaf5e1228724`, passed 15/15 post-merge workflows and was dispatched once. Its request reached `previous-runs-api.open-meteo.com` and returned HTTP 400. No artifact was produced because the original workflow uploaded evidence only after success. The request is recorded as consumed and is not retried.

The source contract and official documentation identify Open-Meteo Single Runs as the required delivery interface for an explicit `run`. The remediation changes the host to `single-runs-api.open-meteo.com`, removes model-unavailable `visibility`, fixes the supported vocabulary at ten variables and authorizes one replacement request under the exact confirmation `F4C_ONE_REPLACEMENT_REQUEST`.

The manual main-only workflow accepts an exact authorized main SHA and one explicit ICON-2I 00/12 UTC run no older than 18 hours. It checks that the authorized SHA is still the remote main head before executing. The request fixes the generalized point, explicit model, 72 forecast hours, GMT/ISO-8601 output, land-cell selection and provider elevation disabled. It accepts no coordinate inputs.

The script contains one fetch site, denies redirects, permits one request in the replacement attempt, enforces a 10-second timeout and 2,000,000-byte response ceiling, validates JSON, hourly lengths and finite values, and computes the raw SHA-256. Request plan and failure evidence are written before or immediately after the request; the workflow uploads the seven-day artifact even when execution fails. A successful response adds raw and normalized evidence.

This gate authorizes a cumulative maximum of two F4-C provider requests: the consumed failed request in run `35201479378` and one replacement request. It prohibits any third request, protected-site egress, retry loop, schedule, recurring traffic, production use, runtime activation, public projection, ranking, readiness, commands or Safety Authority.

After exact-head review, expected-head merge and post-merge verification, one dispatch may execute the replacement gate. Stop after the evidence artifact is produced and reconcile the run before any F4-D projection work.
