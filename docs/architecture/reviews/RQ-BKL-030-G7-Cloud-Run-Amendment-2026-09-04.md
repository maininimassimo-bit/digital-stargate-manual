# Release Quality — BKL-030 G7 Cloud Run EAGLE Health Amendment

| Campo | Valore |
|---|---|
| Package | BKL-030 |
| Gate | G7 — Portal |
| Reviewed implementation head | `c1d44cccecd21a121fe8e85cbf772817b21fae4a` |
| ARB amendment review | Approved with Conditions |
| Date | 2026-09-04 |
| Recommendation | **Conditionally Ready for controlled deployment/OAT** |

## Release impact

The amendment extends the existing hosted Observatory Status relay with an independent EAGLE Health current-projection channel. It adds no remote-control operation, no severity policy, no Safety Authority integration and no destructive persistence behavior.

## Quality-gate matrix

| Gate | Result | Evidence |
|---|---|---|
| Architecture amendment | Passed | User-approved amendment; ARB re-review Approved with Conditions |
| Documentation | Passed | Validate documentation #549 |
| Manual generation | Passed | Genera manuale Word #973 |
| Developer tests | Passed | Developer Foundation #942 |
| Browser credential exclusion | Passed | G7-D failure-injection test and source contract |
| Freshness/fail-closed semantics | Passed | Relay validation + browser fallback/freshness logic |
| Safety isolation | Passed | No command endpoint; Safety Authority OUTSIDE_SCOPE |
| Destructive retention | Not Applicable | No deletion/compaction introduced |
| Cloud Run deployment | Not Executed | Required controlled runtime gate |
| Real EAGLE publication | Not Executed | Required runtime OAT |
| Hosted portal verification | Not Executed | Required after deployment/publication |
| G8 Safety review | Blocked | Begins only after G7 acceptance |

## Risks / waivers

- Runtime transport behavior is not yet proven against the deployed Cloud Run revision. No waiver: deployment/OAT is mandatory.
- Bearer secret must remain outside repository/browser output. No waiver.
- A permanent recurring publisher is outside this review and remains unauthorized.
- Hosted/static fallback can expose stale static evidence only as STALE/UNKNOWN; it must not masquerade as current.

## Rollback

Rollback is operationally bounded: route Cloud Run traffic back to the previous relay revision or redeploy the previous image/revision; the browser static fallback remains fail-closed. EAGLE collector and G6 history are downstream-independent and require no rollback mutation.

## Recommendation

**Conditionally Ready for controlled deployment/OAT — G7 scope only.** Do not declare G7 complete and do not merge as final accepted functionality until Cloud Run deployment, real EAGLE publication and hosted verification have passed. After those gates, re-evaluate final merge readiness and proceed to G8 Safety review.
