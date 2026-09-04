# BKL-030 G7 — Portal OAT — 2026-09-04

| Campo | Valore |
|---|---|
| Identificativo | `BKL-030-G7-OAT-2026-09-04` |
| Capability | BKL-030 — EAGLE Health & Reliability Telemetry |
| Scope | G7 — Portal |
| PR | #89 |
| Production relay revision | `dsg-observatory-status-relay-00005-rof` |
| Production relay URL | `https://dsg-observatory-status-relay-cfjug35c6q-ew.a.run.app` |
| Safety Authority | **No** |
| Remediation | **None** |

## 1. OAT model

G7-E uses separate evidence stages:

1. **Pre-merge static/contract OAT** — CI and fail-closed browser/projection validation.
2. **Hosted relay OAT** — real EAGLE30154 -> Cloud Run transport validation.
3. **Published Pages verification** — final Observatory Status rendering after PR merge/deploy.

The hosted relay may be deployed independently of GitHub Pages. The final page rendering cannot be claimed before the G7 portal code reaches the authoritative Pages deployment from `main`.

## 2. Pre-merge CI evidence

The G7 package passed its current projection, bounded history and browser failure-injection gates together with strict documentation/build gates before controlled runtime deployment.

G7-specific coverage includes:

- current public projection contract;
- removal of non-public process evidence;
- storage capacity / physical-health separation;
- bounded history projection and `MaxRecords` enforcement;
- exclusion of disallowed history signals;
- no destructive retention;
- current/stale browser rendering;
- malformed and missing projection fail-closed behavior;
- `POLICY_NOT_ACTIVATED` preservation;
- browser source check for ingest credential material.

## 3. Cloud Run controlled deployment

Project/region/service:

```text
project  = digital-stargate-telemetry
region   = europe-west1
service  = dsg-observatory-status-relay
```

Image built from PR #89 relay source:

```text
europe-west1-docker.pkg.dev/digital-stargate-telemetry/dsg-telemetry/observatory-status-relay:g7-eagle-ff3d561
digest sha256:7030ee01f8eaa2f0cae35fccf8709dfb444c3b17ab8d213ccccc90f74fbec8d7
```

Cloud Build result:

```text
build b7b2a10d-80a6-4ea1-8290-325f11368ec1
status SUCCESS
```

The revision was first deployed with `--no-traffic --tag g7-eagle`:

```text
dsg-observatory-status-relay-00005-rof
canary traffic = 0%
previous production revision 00004-5br = 100%
```

Canary `/health` returned `RUNNING`; both data endpoints initially returned `404`, demonstrating isolated empty snapshot stores rather than inherited state.

## 4. Real EAGLE Health canary OAT

Host: `EAGLE30154`.

The existing ingest secret was reused from the EAGLE DPAPI LocalMachine store:

```text
C:\DigitalStarGate\TelemetryRuntime\secrets\ingest-token.dpapi
```

No token value was written to repository or browser code.

A fresh current collector projection was filtered through `DSG.EagleHealthPortalProjection` and validated locally before publication.

First accepted canary publish:

```text
HTTP 202
observed_at_utc  = 2026-09-04T20:17:12.142Z
correlation_id   = 154ef80d-6220-4ce4-b14f-235ffeb627f3
signals_published = 5
```

Independent GET returned the same projection and correlation ID:

```text
component = DSG.EagleHealthPortalProjection
host = EAGLE30154
quality = CURRENT
summary = UNKNOWN / POLICY_NOT_ACTIVATED
automatic_remediation = false
safety_authority = OUTSIDE_SCOPE
signals_published = 5
```

Canary health after the EAGLE publish:

```text
eagle_health.accepted = 1
eagle_health.rejected = 0
```

A deliberately stale local projection had previously been rejected by the publisher before network transmission, confirming fail-closed freshness enforcement.

## 5. N.I.N.A. compatibility OAT on the same canary

A fresh Observatory Status/N.I.N.A. snapshot was published to the same revision:

```text
HTTP 202
schema_version = 1.1
source_instance = EAGLE30154
quality = CURRENT
correlation_id = d432bc91-9ee1-435f-8eb1-fe6fc40062e1
```

Canary health then showed independent successful channels:

```text
observatory_status.accepted = 1
observatory_status.rejected = 0
eagle_health.accepted = 1
eagle_health.rejected = 0
```

This demonstrates that the G7 relay revision preserves the existing N.I.N.A. telemetry path while adding the independent EAGLE Health path.

## 6. Production cutover

After canary acceptance, Cloud Run traffic was moved atomically to the validated revision:

```text
dsg-observatory-status-relay-00005-rof = 100%
```

The production `/health` endpoint remained `RUNNING` with zero rejected requests.

Fresh production publishes were then accepted for both channels. Verified EAGLE Health production publish:

```text
HTTP 202
observed_at_utc = 2026-09-04T20:23:30.720Z
fresh_until_utc = 2026-09-04T20:25:30.720Z
correlation_id = 996c1f9e-39fd-4523-8321-1147a7cd71ab
```

Production GET returned the same values:

```text
component = DSG.EagleHealthPortalProjection
host = EAGLE30154
quality = CURRENT
summary.state = UNKNOWN
summary.reason = POLICY_NOT_ACTIVATED
automatic_remediation = false
safety_authority = OUTSIDE_SCOPE
signals_published = 5
correlation_id = 996c1f9e-39fd-4523-8321-1147a7cd71ab
```

Production relay counters after cutover:

```text
state = RUNNING
accepted = 21
rejected = 0
observatory_status.accepted = 19
observatory_status.rejected = 0
eagle_health.accepted = 2
eagle_health.rejected = 0
```

The N.I.N.A. production endpoint simultaneously returned current `schema_version=1.1` evidence from `EAGLE30154`, confirming no regression of the existing channel.

## 7. Static fallback disposition

The repository static EAGLE Health fallback remains deliberately fail-closed:

```text
quality = UNKNOWN
summary.state = UNKNOWN
summary.reason = POLICY_NOT_ACTIVATED
signals = {}
automatic_remediation = false
safety_authority = OUTSIDE_SCOPE
```

It cannot accidentally advertise healthy/current state when hosted telemetry is unavailable.

## 8. Acceptance matrix

| Criterion | Evidence | Status |
|---|---|---|
| Public current projection contract | G7-A/G7-B + CI | PASS |
| Public signal filtering | G7-B CI + real payload | PASS |
| `UNKNOWN/STALE` fail-closed | G7-D + stale publish rejection | PASS |
| `POLICY_NOT_ACTIVATED` preserved | CI + real GET | PASS |
| Capacity / physical health separated | projection/UI contract | PASS |
| Bounded history | G7-C + CI | PASS |
| No browser credentials | CI + DPAPI publisher pattern | PASS |
| No remediation / Safety Authority | real production payload | PASS |
| Cloud Run canary deployment | revision 00005-rof at 0%, tested | PASS |
| EAGLE Health POST/GET | 202 / 200 with matching correlation ID | PASS |
| Existing N.I.N.A. compatibility | independent POST/GET on same revision | PASS |
| Production cutover | 00005-rof at 100%, relay RUNNING | PASS |
| Production dual-channel transport | accepted, rejected=0 | PASS |
| Published Observatory Status page | requires PR merge + Pages deploy | **PENDING** |
| Final independent review after runtime evidence | required before closure | **PENDING** |

## 9. Runtime safety disposition

The hosted relay remains telemetry transport only. It exposes no command endpoint, does not calculate host-health severity, does not extend source freshness, and does not become Safety Authority.

Loss of Cloud Run or either hosted snapshot does not alter the local collector, N.I.N.A., CloudWatcher or local physical interlocks.

## 10. Current disposition

**Hosted relay OAT: PASS. Production transport cutover: PASS.**

G7 is not yet Closed because two gates remain:

1. merge PR #89 and verify the published Observatory Status page after authoritative Pages deployment;
2. complete final independent/release review against the runtime evidence and any automation added after this OAT.
