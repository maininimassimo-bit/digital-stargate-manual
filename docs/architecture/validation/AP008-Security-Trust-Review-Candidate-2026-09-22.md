# AP-008 Security and Trust Review Candidate — 2026-09-22

| Campo | Valore |
|---|---|
| Package | AP-008 |
| Review status | AI-assisted, owner-authorized — independent human review still required |
| Scope | shadow transport and bounded read-only integration boundary |
| Accountable owner | Massimo Mainini |
| Runtime authorization | NONE |

## 1. Trust boundary

```text
EAGLE30154 governed publishers
  -> HTTPS Cloud Run ingress
  -> bearer token validation and source validation
  -> schema/freshness/idempotency checks
  -> append-only or snapshot object in Cloud Storage-backed /data
  -> unauthenticated read-only GET consumers
```

The channel remains shadow-only. It has no broker, scheduler, command route or Safety Authority
integration.

## 2. Controls evidenced

| Control | Result | Evidence |
|---|---|---|
| HTTPS transport | PASS | all publisher endpoints use HTTPS |
| Bearer secret injection | PASS | existing Secret Manager path preserved; token not committed or sent to browser |
| Authorized source | PASS | `EAGLE30154` boundary preserved |
| Body limit | PASS | `DSG_RELAY_MAX_BODY_BYTES=65536` preserved |
| Contract validation | PASS | SessionCompleted, Observatory Status and EAGLE Health validators exercised |
| Freshness fail-closed | PASS | stale/missing snapshots return `404 snapshot_unavailable` |
| Replay handling | PASS | duplicate `message_id` returns `NO_OP` without a second append |
| Persistence | PASS | Cloud Storage bucket mounted at `/data`; cross-revision read-back verified |
| Command isolation | PASS | `/v1/command` returned `404`; command authority remains `NONE` |
| Safety isolation | PASS | safety authority remains `NONE`; no device command path |
| Production isolation | PASS | canary remained at 0%; previous revision retained at 100% |

## 3. Review items requiring independent disposition

1. Secret rotation, expiry, revocation and recovery procedure.
2. Cloud Run ingress, IAM, service-account and bucket IAM least-privilege review.
3. Public read endpoint exposure, CORS policy and data-classification assessment.
4. Log and trace redaction, including authorization/header handling.
5. Replay, tampering, duplicate and partial-publication threat analysis.
6. Cloud Storage retention, deletion, backup and incident-recovery policy.
7. Dependency and supply-chain review for the container image and deployment path.
8. Independent consumer reconciliation and divergence handling.
9. Disable/rollback authority and four-eyes requirements for any future live scope.

## 4. Findings before approval

| Finding | Severity | Status |
|---|---|---|
| Same-person interim ownership combines accountable, security-coordination and operations roles | Major governance risk | OPEN; waiver recorded, separation required for live approval |
| No independent security/trust disposition recorded | Blocker for live readiness | OPEN |
| No new independent ARB decision recorded | Blocker for live readiness | OPEN |
| Shadow technical OAT and rollback evidence complete | — | PASS for shadow scope |

## 5. Review disposition

This document is a review candidate and evidence index. The companion AI-assisted review is
owner-authorized under `W-AP008-SECURITY-REVIEW-INDEPENDENCE-2026-09-22`; it is not equivalent
to an independent human security approval, not an ARB decision and not authorization to promote
traffic or activate live semantics.

Required next action: assign an independent security/trust reviewer, record the disposition on
this exact package, then submit the package and the completed OAT to ARB for a new decision.
