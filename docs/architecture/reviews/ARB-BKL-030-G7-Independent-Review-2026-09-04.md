# ARB-BKL-030-G7 — Independent Architecture Review — 2026-09-04

| Campo | Valore |
|---|---|
| Review ID | `ARB-BKL-030-G7` |
| Capability | BKL-030 — EAGLE Health & Reliability Telemetry |
| Scope | G7 — Portal |
| PR | #89 |
| Reviewed HEAD | `cafeed859786ff7bdd74e642721971e463e269d6` |
| Decision | **Approved with Conditions** |

## 1. Executive decision

The Architecture Review Board independently reviewed the G7 package against repository truth, the accepted G5 current-projection contract, G6 history/persistence, the existing Observatory Status portal architecture, CI evidence and the pre-merge G7-E OAT.

**Decision: Approved with Conditions.**

No Blocker or Major finding prevents merge. G7 preserves the read-only telemetry boundary, explicitly retains `UNKNOWN/STALE` and `POLICY_NOT_ACTIVATED`, filters browser-facing evidence, separates logical storage capacity from physical disk health, bounds history exposure, contains no browser ingest credential and introduces no remediation or Safety Authority coupling.

The approval is intentionally conditional because the authoritative Pages workflow deploys only from `main`; therefore hosted verification of the newly merged G7 surface is not yet executable and must remain a post-deploy acceptance gate.

## 2. Scores

| Dimension | Score | Evidence summary |
|---|---:|---|
| Architecture consistency | 97 | Extends existing Observatory Status instead of creating a parallel portal |
| Domain/layer integrity | 98 | Browser projection remains downstream/read-only; collector/history contracts remain authoritative |
| Safety separation | 100 | No command surface, no remediation, Safety Authority outside scope |
| Security/privacy | 96 | Public adapter filters process evidence; no ingest credential in browser source |
| Freshness/fail-closed semantics | 98 | `STALE/UNKNOWN` enforced in projection/browser tests |
| History integrity | 96 | Bounded public history; raw G6 NDJSON remains authoritative |
| Storage semantics | 98 | Capacity and physical-health evidence explicitly separated |
| Operability/observability | 92 | Projection diagnostics and CI coverage are present; hosted path still awaits post-deploy observation |
| Traceability | 95 | Design, G7-A contract, implementation, tests and OAT are in one PR |
| Release readiness | 91 | CI green; hosted verification correctly pending |

Overall assessment: **96.1 / 100**.

## 3. Findings

### No Blocker findings

None.

### No Major findings

None.

### ARB-BKL-030-G7-C01 — Minor — Hosted verification is post-deploy only

The authoritative GitHub Pages workflow deploys from `main`. The pre-merge package cannot provide direct evidence that the newly added `EAGLE Health` surface is rendered correctly on the final hosted site.

**Required condition:** merge is permitted only with hosted acceptance still open. After successful Pages deployment, verify the published Observatory Status page against the G7-E checklist before declaring G7 closed.

### ARB-BKL-030-G7-C02 — Minor — Public EAGLE projection currently uses static delivery path

The browser-facing G7 implementation uses a static public projection path for EAGLE Health rather than introducing a new hosted relay endpoint. This is acceptable for the bounded G7 increment because the projection is fail-closed and read-only, but production freshness depends on a separately governed publication/export mechanism.

**Required condition:** do not claim realtime EAGLE Health unless a governed publication mechanism exists and source freshness remains authoritative. A static `UNKNOWN` fallback is acceptable and preferable to fabricated current state.

### ARB-BKL-030-G7-C03 — Observation — No health severity policy is active

The portal correctly retains `UNKNOWN / POLICY_NOT_ACTIVATED` and does not derive `HEALTHY`, `DEGRADED` or `CRITICAL` from raw evidence.

**Disposition:** preserve this behavior until a separately governed severity/threshold policy exists.

## 4. Verified evidence

Reviewed changes include:

- public current EAGLE Health projection adapter;
- filtered browser-facing evidence set;
- EAGLE Health UI within Observatory Status;
- fail-closed static fallback projection;
- bounded public history projection;
- current/history contract tests;
- browser failure-injection tests;
- G7-E pre-merge OAT evidence.

Final reviewed CI state on `cafeed859786ff7bdd74e642721971e463e269d6`:

```text
Genera manuale Word                 success
Validate documentation (no deploy)  success
Developer Foundation                success
```

Developer Foundation explicitly passed:

```text
Test EAGLE health portal projection
Test EAGLE health portal bounded history
Test EAGLE health portal browser failure injection
Verify MkDocs
```

The feature branch is ahead of `main` with no reported divergence at review time.

## 5. Safety disposition

G7 is an observational portal increment only. It does not control EAGLE, dome, mount, camera, power, Windows Update or network infrastructure. No browser write/control endpoint is introduced.

Local physical interlocks remain authoritative and independent.

## 6. Security disposition

The public current and history projections deliberately expose a reduced evidence subset. Process-table evidence is excluded from the public projection. Browser tests verify absence of ingest token/authorization material in portal JavaScript.

No new credential-bearing client flow is approved.

## 7. Merge conditions

G7 may proceed toward merge provided:

1. final PR HEAD CI remains green;
2. no command/remediation endpoint is added;
3. no browser credential is added;
4. no health severity thresholds are introduced;
5. history remains bounded and raw G6 history remains authoritative;
6. post-deploy hosted verification remains an explicit closure gate.

## 8. Re-review criteria

ARB re-review is required if G7 is changed to add:

- browser write/control actions;
- ingest credentials in client code;
- overall health severity or alert thresholds;
- unbounded/raw history publication;
- new external persistence dependency;
- Safety Authority coupling;
- automatic remediation.

## 9. Final decision

**Approved with Conditions.**

The G7 package is architecturally acceptable for merge, but G7 must not be marked fully Accepted/Closed until the authoritative Pages deployment succeeds and the hosted G7-E verification checklist passes on the published site.
