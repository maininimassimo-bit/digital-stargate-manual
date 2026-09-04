# ARB — BKL-030 G8 Safety Review — 2026-09-04

| Campo | Valore |
|---|---|
| Identificativo | `ARB-BKL-030-G8-2026-09-04` |
| Capability | BKL-030 — EAGLE Health & Reliability Telemetry |
| Gate | G8 — Safety review |
| Baseline reviewed | `a15d85b27ebfbe8a6488330920d10dda8db79a78` |
| Decisione | **APPROVED WITH CONDITIONS** |
| Blocker | 0 |
| Major | 0 |

## 1. Review scope

Independent review of the completed BKL-030 chain G1-G7 with emphasis on the canonical G8 requirement: confirm that EAGLE Health has no control/remediation path and remains independent from the observatory Safety Authority.

Reviewed repository/runtime evidence includes the collector/projection contract, G5 EAGLE runtime OAT, G6 history/persistence closure, G7 hosted portal/Cloud Run OAT, production wrapper, relay implementation and post-merge Pages workflow.

## 2. Verified safety invariants

1. `DSG.EagleHostHealthCollector` is observational/read-only and does not command N.I.N.A., PHD2, ASCOM, dome, mount, power, network, USB or Windows remediation actions.
2. EAGLE Health public projection must remain `summary.state=UNKNOWN` and `summary.reason=POLICY_NOT_ACTIVATED` until a separate governed health policy exists.
3. Public projection requires `automatic_remediation=false` and `safety_authority=OUTSIDE_SCOPE`.
4. The publisher refuses a projection that violates those invariants and requires HTTPS outside localhost integration tests.
5. The hosted relay validates the same invariants server-side before atomic storage.
6. The relay exposes telemetry GET/POST routes only; no command, control, remediate or reboot route is present in the reviewed baseline.
7. Browser code contains no ingest token and consumes read-only projections.
8. Missing, malformed or stale EAGLE evidence fails closed to `UNKNOWN/STALE`; last-known evidence is not promoted to current state.
9. EAGLE Health cannot infer observatory SAFE/UNSAFE and cannot override local physical interlocks.
10. Cloud Run loss, browser loss or EAGLE Health publication failure does not alter the local Safety Authority or physical interlocks.

## 3. Runtime evidence

G5 OAT on `EAGLE30154` verified collector execution during real N.I.N.A./PHD2 workload with bounded probes, per-signal isolation, mutex non-overlap and no remediation.

G7 production OAT verified independent Observatory Status and EAGLE Health channels on Cloud Run. The production EAGLE payload preserved:

```text
summary.state = UNKNOWN
summary.reason = POLICY_NOT_ACTIVATED
automatic_remediation = false
safety_authority = OUTSIDE_SCOPE
```

The governed EAGLE publication wrapper subsequently completed a production publish with HTTP 202 and correlation ID:

```text
7c3e7a02-d8db-4178-885f-17330648c364
```

PR #89 was merged as `a15d85b27ebfbe8a6488330920d10dda8db79a78`. The authoritative GitHub Pages workflow then completed both build/site-integrity and deploy jobs successfully.

## 4. Findings

### Blocker

None.

### Major

None.

### Minor G8-C01 — Health policy remains deliberately inactive

Storage capacity, Windows Time, reboot evidence, Event Log and other host observations remain raw evidence. No HEALTHY/DEGRADED/CRITICAL thresholds are governed.

**Condition:** any future severity/health-score policy must be a separate governed change and must remain distinct from observatory Safety Authority.

### Minor G8-C02 — Automatic remediation remains prohibited

BKL-030 acceptance covers evidence collection, history and presentation, not automatic repair.

**Condition:** restart/reboot/service/task/USB/power/network/device remediation requires a new architecture/safety package and explicit approval.

### Observation G8-O01 — Hosted relay storage is transport state, not safety state

Cloud Run snapshot storage is not authoritative safety persistence. Loss/replacement of hosted state may make the portal UNKNOWN but must never change observatory operation.

### Observation G8-O02 — Operational host risks remain evidence, not G8 blockers

Low C: capacity, Windows Time state, pending reboot evidence, unavailable detailed SMART and configuration-drift baseline gaps remain operational follow-up inputs. They do not authorize inferred severity or remediation.

## 5. Scorecard

| Dimensione | Score |
|---|---:|
| Safety boundary clarity | 100 |
| Control/remediation isolation | 100 |
| Fail-closed semantics | 98 |
| Safety Authority independence | 100 |
| Security/credential separation | 96 |
| Runtime evidence | 96 |
| Failure containment | 97 |
| Traceability | 94 |
| Operability | 91 |
| Overall | **96.9** |

## 6. Decision

**APPROVED WITH CONDITIONS.**

G8 is accepted. No Blocker or Major finding prevents BKL-030 capability closure for its approved read-only telemetry/history/portal scope.

The conditions are forward constraints, not closure blockers:

- no health severity policy without separate governance;
- no automatic remediation without separate architecture/safety approval;
- no elevation of EAGLE Health, Cloud Run or the browser portal to Safety Authority;
- stale/missing evidence must continue to fail closed.

## 7. Re-review triggers

A new independent safety review is required if a future change introduces any of:

- device/process/service/task control;
- restart/reboot/update/reset actions;
- automatic remediation;
- SAFE/UNSAFE inference from EAGLE host health;
- change to physical-interlock authority;
- browser or cloud command endpoint;
- health thresholds reused as safety thresholds.
