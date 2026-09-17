# BKL-031 F4-C — Generalized Forecast Acquisition Gate

| Field | Value |
|---|---|
| Identifier | `BKL-031-F4-C-GATE-002` |
| Status | **EXECUTED — REQUEST BUDGET EXHAUSTED / EVIDENCE RECONCILED** |
| Date | 2026-09-17 |
| First attempt | Run `35201479378`; HTTP 400; request consumed; no artifact |
| Replacement attempt | Run `35214129960`; HTTP 200 raw response; normalization failed closed |
| Request accounting | Two of two requests consumed; no further request authorized |
| Location | Synthetic/generalized `42.0, 12.0` |
| Protected-site use | False |
| Runtime effect | None |

Gate 001 was merged at `48bd61a3337523b7790d78a37813eaf5e1228724`, passed 15/15 post-merge workflows and issued one request to the incorrect Previous Runs host. The provider returned HTTP 400. The request was recorded as consumed and was not retried.

Gate 002 corrected the interface to `single-runs-api.open-meteo.com`, removed model-unavailable `visibility`, fixed the supported vocabulary at ten variables and was merged at `053fc766bfc7908a984828cc335eef07a558909c` after 19/19 exact-head checks and 15/15 post-merge workflows. Replacement run `35214129960` issued the final authorized request and received a 4,723-byte HTTP 200 JSON response with SHA-256 `e51c6935f8e04bcce38983bc03147f4f897a833f90feb6271b2f510ee6eec102`.

The replacement workflow failed closed because `precipitation` was null at the run-initialization instant `2026-09-17T00:00:00Z`. Its always-upload control preserved artifact `10494298154` as `bkl-031-f4c-evidence-35214129960`. No network retry followed.

Offline reconciliation verified the raw digest and all 72 returned hourly positions. It excluded the single incomplete initialization instant, accepted the complete contiguous suffix from `2026-09-17T01:00:00Z` through `2026-09-19T23:00:00Z`, performed zero imputations and produced 71-instant normalized evidence with digest `350a7b9ae8b2de308ba55a7105e56bb4de5040572370ab2715c0fa70088af2f5`. Raw and normalized evidence remain outside the Pages input under `governance/forecast-evidence/`.

The acquisition workflow and executable acquisition script are removed after reconciliation. The repository therefore exposes no third-request dispatch path. F4-C authorizes no protected-site egress, retry loop, schedule, recurring traffic, production use, runtime activation, public projection, ranking, readiness, commands or Safety Authority.

F4-D may now prepare a separately reviewed sanitized read-only projection from the reconciled evidence. It must preserve availability, exclusion, run, model, attribution and no-authority semantics.
