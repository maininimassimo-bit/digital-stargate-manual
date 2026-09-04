# BKL-030 G7 — Cloud Run EAGLE Health Transport Amendment

| Campo | Valore |
|---|---|
| Package | `BKL-030` |
| Gate | `G7 — Portal` |
| Amendment | Hosted EAGLE Health transport |
| Date | 2026-09-04 |
| Decision | **Approved for implementation** |
| Approval | Explicit user/architecture-owner approval in active G7 execution |
| Safety Authority | **Outside scope** |

## 1. Decision

G7 is amended before merge to reuse the already deployed Google Cloud Run Observatory Status telemetry relay for EAGLE Health current-state transport.

This is the explicit approval required by section 8 of the original G7 design for a new remote API route. It does not approve a new cloud provider, a new durable database, browser credentials, host-health severity policy, remediation or Safety Authority integration.

## 2. Target topology

```text
EAGLE30154
  -> DSG.EagleHostHealthCollector
  -> local eagle-health.json
  -> Export-EagleHealthPortalProjection.ps1
  -> public filtered projection
  -> Publish-EagleHealthTelemetry.ps1
  -> HTTPS POST /v1/eagle-health
  -> existing Google Cloud Run telemetry relay
  -> GET /v1/eagle-health
  -> Observatory Status / EAGLE Health

If hosted GET fails:
  -> docs/data/realtime/eagle-health.json
  -> freshness validation
  -> UNKNOWN/STALE fail-closed behavior
```

Observatory telemetry remains independently available at `/v1/observatory-status`.

## 3. Trust boundaries

- bearer token exists only on EAGLE publishing side and Cloud Run secret injection;
- browser GET is credential-free;
- relay accepts only authorized host `EAGLE30154`;
- relay validates the public projection contract and source freshness before atomic storage;
- relay cannot extend source freshness;
- relay exposes no command/remediation endpoint;
- EAGLE Health cannot produce observatory `SAFE`;
- local physical interlocks remain authoritative and independent.

## 4. Failure modes

| Failure | Required behavior |
|---|---|
| EAGLE offline | hosted snapshot eventually becomes stale; browser renders stale/unknown |
| Internet/Starlink unavailable | local collector unaffected; cloud publication fails without remediation |
| Cloud Run unavailable | browser tries static fallback; local safety unaffected |
| hosted EAGLE snapshot missing | GET 404; browser fallback/UNKNOWN |
| malformed EAGLE payload | relay rejects with 422; prior valid store remains |
| wrong host | relay rejects with 403 |
| wrong/missing token | relay rejects with 401 |
| stale source payload | relay rejects with 422 |
| power loss | no cloud action changes local equipment state or safety authority |
| controller/interlock failure | outside EAGLE Health authority; existing local safety procedures apply |
| emergency stop/manual override | remain local/physical and independent of relay availability |

## 5. Persistence

The Cloud Run relay stores only the latest accepted public EAGLE Health projection in its existing pilot persistence model. G6 append-only history on EAGLE remains authoritative historical evidence.

This amendment does **not** approve upload of raw G6 NDJSON history or a new cloud history database. Bounded history transport remains separately governed by the existing G7-C contract.

## 6. Implementation impact

Approved changes:

- extend `infrastructure/telemetry-relay/app.py` with `POST/GET /v1/eagle-health`;
- add independent EAGLE Health store path;
- add per-channel relay counters;
- add `Publish-EagleHealthTelemetry.ps1`;
- change Observatory Status EAGLE fetch order to hosted Cloud Run first, static fallback second;
- extend CI/failure-injection coverage;
- update relay documentation and G7 OAT.

## 7. Review reset

Because this amendment adds an explicitly approved remote API route after the first G7 ARB/RQ reviews, those reviews remain historical evidence but are no longer sufficient for final merge readiness.

Required before merge:

1. CI green on amended package;
2. local/contract relay tests green;
3. updated pre-merge OAT;
4. independent ARB re-review;
5. Release Quality re-review;
6. deploy updated relay to Google Cloud Run;
7. real EAGLE POST/GET OAT with matching correlation id;
8. hosted Observatory Status verification.

G7 remains open until these gates pass.
