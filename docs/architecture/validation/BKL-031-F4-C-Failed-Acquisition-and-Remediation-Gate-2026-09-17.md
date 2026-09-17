# BKL-031 F4-C — Failed Acquisition Evidence and Remediation Gate

| Field | Value |
|---|---|
| Evidence ID | `BKL-031-F4-C-FAILURE-001` |
| Status | **FIRST REQUEST FAILED / REMEDIATION EXECUTED / HISTORICAL EVIDENCE** |
| Workflow run | [35201479378](https://github.com/maininimassimo-bit/digital-stargate-manual/actions/runs/35201479378) |
| Authorized main | `48bd61a3337523b7790d78a37813eaf5e1228724` |
| Dispatch time | 2026-09-17T08:46Z |
| Requested run | `2026-09-17T00:00Z` |
| Result | Provider HTTP 400 |
| Provider request count | 1 consumed |
| Protected-site use | False |
| Artifact | None; upload step was skipped by the failed original workflow |

The exact-main and confirmation checks passed, followed by a successful local preflight inside the workflow. The acquisition step then issued its single GET and received HTTP 400. No automatic or manual retry was made.

The failure is attributable to a deterministic contract mismatch. The accepted F4-A decision and cited provider documentation require the Open-Meteo Single Runs API for an explicit `run`, while F4-B v1.0 and gate 001 incorrectly bound the request to `previous-runs-api.open-meteo.com`. The official Previous Runs documentation describes fixed lead-time `_previous_dayN` series and directs complete explicit-run retrieval to the Single Runs API. The official ICON-2I page also states that visibility is unavailable for this model.

Remediation gate `BKL-031-F4-C-GATE-002` therefore:

1. corrects the source profile and request host to `single-runs-api.open-meteo.com`;
2. updates the contract to v1.1 and removes `visibility` from requested/evidence variables while recording it as unavailable;
3. requires a distinct one-time replacement confirmation;
4. records the original workflow run and cumulative two-request ceiling;
5. uploads request/failure evidence even when the replacement execution fails;
6. prohibits any third request.

The failed request produced no forecast evidence and grants no F4-D projection, ranking, readiness, production runtime, command or Safety authority.

Gate 002 was subsequently integrated and replacement run `35214129960` returned an HTTP 200 raw response. Its one incomplete initialization instant was rejected online and reconciled offline without imputation. See `BKL-031-F4-C-Acquisition-Evidence-Reconciliation-2026-09-17.md`. Both authorized requests are consumed and no third request is permitted.
