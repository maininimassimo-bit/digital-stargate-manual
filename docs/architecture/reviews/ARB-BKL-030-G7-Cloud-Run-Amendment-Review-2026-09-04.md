# ARB — BKL-030 G7 Cloud Run EAGLE Health Transport Amendment

| Campo | Valore |
|---|---|
| Package | BKL-030 |
| Gate | G7 — Portal |
| Review scope | Cloud Run EAGLE Health transport amendment |
| Reviewed head | `c1d44cccecd21a121fe8e85cbf772817b21fae4a` |
| Date | 2026-09-04 |
| Decision | **Approved with Conditions** |

## Evidence reviewed

- Existing G7 portal design and G7-A public projection contract.
- Approved amendment introducing the existing hosted telemetry relay as the primary public transport for EAGLE Health.
- Relay implementation with independent `/v1/eagle-health` channel and atomic store.
- EAGLE publisher and browser hosted-first/static-fallback behavior.
- GitHub Actions on reviewed head: Developer Foundation #942 PASS; Validate documentation #549 PASS; Genera manuale Word #973 PASS.
- PR #89 remains open/draft and is mergeable at review time.

## Architecture findings

No Blocker or Major finding identified in the reviewed repository package.

### Security and trust boundary

The amendment reuses the existing authenticated relay boundary. Browser access remains GET-only and credential-free; publication requires bearer authentication and validates host identity, projection component, source component, freshness, policy semantics, read-only mode, remediation disabled and Safety Authority outside scope.

### Safety

Host-health evidence remains observational. The relay exposes no command/remediation endpoint and does not elevate EAGLE health into observatory Safety Authority. Local physical interlocks remain independent and authoritative.

### Failure semantics

Hosted EAGLE Health and Observatory Status use independent stores/channels. Browser behavior is hosted-first with static fallback and freshness enforcement; missing, malformed or stale evidence fails closed to UNKNOWN/STALE.

### Persistence

The relay stores only the latest public projection atomically. G6 append-only history remains authoritative for historical evidence. No history deletion, compaction or retention activation is introduced.

## Score

| Dimension | Score |
|---|---:|
| Architecture consistency | 96 |
| Boundary/dependency integrity | 96 |
| Security | 96 |
| Safety isolation | 98 |
| Failure/freshness semantics | 96 |
| Persistence/data integrity | 95 |
| Observability/operability | 91 |
| Test/CI evidence | 94 |
| Deployment/rollback readiness | 88 |
| Traceability/documentation | 94 |
| **Overall** | **94.4** |

## Conditions

1. Cloud Run deployment of the amended relay must be executed and verified before formal G7 closure.
2. Real EAGLE publication to `/v1/eagle-health` must demonstrate accepted fresh evidence without exposing the bearer token.
3. Hosted browser verification must demonstrate Cloud Run primary transport, static fallback, stale/unknown fail-closed behavior and independent failure from other Observatory Status panels.
4. No severity thresholds, automatic remediation, command endpoint or Safety Authority integration may be introduced under this approval.
5. No permanent recurring publisher/history scheduler is authorized by this review; recurring production orchestration requires the already-governed non-interference/cadence review.
6. G8 Safety review remains mandatory after G7 acceptance.

## Decision

**Approved with Conditions.** The repository implementation is architecturally acceptable for controlled Cloud Run deployment and runtime OAT. The conditions above are runtime acceptance gates, not evidence already executed.
