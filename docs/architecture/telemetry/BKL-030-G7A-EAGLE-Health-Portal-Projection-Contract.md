# BKL-030 G7-A — EAGLE Health Portal Projection Contract

| Campo | Valore |
|---|---|
| Identificativo | `BKL-030-G7-A` |
| Capability | BKL-030 — EAGLE Health & Reliability Telemetry |
| Stato | **Architecture ready for implementation** |
| Data | 2026-09-04 |
| Consumer | Digital StarGate Observatory Status Portal |
| Upstream current contract | `BKL-030-EAGLE-Health-Projection-Contract.md` |
| Upstream history contract | `BKL-030-G6-EAGLE-Health-History-Persistence-Design.md` |
| Safety Authority | **No** |

## 1. Objective

Define the public/read-only projection contract that allows the existing Observatory Status portal to render EAGLE host-health current evidence and, in later G7 slices, bounded historical trends without coupling the browser directly to EAGLE-local files or to implementation-specific collector/history formats.

G7-A is a contract slice only. It does not enable a new runtime publisher, scheduler, remote-control endpoint, remediation action or Safety Authority capability.

## 2. Existing portal baseline

The portal already provides:

- `docs/status/index.md` as the Observatory Status surface;
- `docs/javascripts/observatory-status.js` as the browser renderer;
- hosted relay first, static projection fallback second;
- client-side freshness enforcement;
- explicit downgrade of stale/missing evidence to `UNKNOWN`/`STALE`;
- separation between observed Safety telemetry and actual Safety Authority.

G7 SHALL extend this surface rather than create a parallel health portal.

## 3. Projection boundary

The browser must consume a public projection shaped for display, not the EAGLE-local collector file directly.

Canonical logical flow:

```text
EAGLE collector
  -> local eagle-health.json
  -> governed projection/export adapter
  -> hosted/static public EAGLE health projection
  -> Observatory Status browser
```

For history:

```text
EAGLE G6 history
  -> bounded history projection/export adapter
  -> hosted/static public history projection
  -> bounded trend UI
```

The public adapter is downstream and read-only. It cannot mutate collector state or historical evidence.

## 4. Current-state public contract

### 4.1 Envelope

The current-state public projection SHALL expose at minimum:

```json
{
  "schema_version": "1.0",
  "component": "DSG.EagleHealthPortalProjection",
  "host": "EAGLE30154",
  "observed_at_utc": "<source observation UTC>",
  "fresh_until_utc": "<source freshness UTC>",
  "quality": "CURRENT|STALE|UNKNOWN",
  "source_component": "DSG.EagleHostHealthCollector",
  "source_schema_version": "1.0",
  "summary": {
    "state": "UNKNOWN",
    "reason": "POLICY_NOT_ACTIVATED"
  },
  "signals": {}
}
```

The adapter may add transport metadata, but must not remove provenance or source observation timestamps.

### 4.2 Signal envelope

Each public signal SHALL preserve:

```text
signal_id
state
quality
observed_at_utc
fresh_until_utc
source
cadence_class
reason
data
```

The browser is allowed to format fields for presentation, but SHALL NOT reinterpret stale data as current.

### 4.3 Summary semantics

Until a separately governed health severity policy exists:

```text
summary.state  = UNKNOWN
summary.reason = POLICY_NOT_ACTIVATED
```

The projection and UI SHALL NOT manufacture overall `HEALTHY`, `DEGRADED` or `CRITICAL` from raw values.

## 5. Required signal families for G7-B

The current portal slice SHOULD support the current collector signal families without assuming every family is always present.

Expected families include:

- host/OS and uptime evidence;
- CPU evidence;
- memory evidence;
- logical storage capacity evidence;
- physical storage health evidence;
- time/service evidence;
- process/task evidence where already present in the accepted collector contract;
- event/PnP/reboot/update/filesystem evidence where already present and bounded by source policy.

A missing family renders `UNKNOWN`/unavailable; it does not block the entire projection.

## 6. Storage semantics

G7 SHALL keep these two evidence families visually and semantically separate:

```text
logical capacity
  size_bytes
  free_bytes
  free_ratio / free_pct

physical device health
  disk identity
  HealthStatus
  OperationalStatus
  optional governed reliability details
```

The portal must not infer physical disk failure from low free capacity, nor capacity severity from physical health state.

No numeric warning threshold is approved by G7-A.

## 7. Freshness contract

The portal projection SHALL preserve source `observed_at_utc` and `fresh_until_utc`.

Browser rule remains:

```text
valid sample and now <= fresh_until_utc -> use emitted state/quality
valid sample and now > fresh_until_utc  -> force STALE / UNKNOWN display
missing/invalid sample                  -> UNKNOWN
```

The browser may show the last observation timestamp for context, but must not present the last known value as a current healthy state when stale.

Transport freshness cannot extend source freshness.

## 8. Failure semantics

### Current projection unavailable

Render EAGLE Health as `UNKNOWN / UNAVAILABLE`. Other Observatory Status panels continue to function.

### Public projection malformed

Reject the EAGLE Health payload and render the health section unavailable. Do not partially bind fields from an invalid top-level contract unless the implementation includes explicit validated partial-signal support.

### Individual signal missing or malformed

Render only that signal/family as unavailable when the envelope remains valid.

### Hosted endpoint unavailable

The portal MAY use the governed static fallback if available. Static fallback must still undergo freshness validation.

### Both hosted and fallback unavailable

Render `UNKNOWN`, not the last browser value.

## 9. Security and privacy

The public projection must exclude:

- secrets, tokens and credentials;
- arbitrary process command lines;
- local usernames unless separately approved;
- arbitrary file contents;
- sensitive configuration payloads;
- remote-control affordances.

The browser SHALL contain no ingest or EAGLE credential.

G7-A defines read-only display contracts only.

## 10. History projection contract for G7-C

G7-C SHALL NOT publish the entire raw G6 history file directly to the browser.

Instead it must use a bounded projection with an explicit query/export window, for example a governed recent time range or bounded sample count selected during implementation.

Each historical sample exposed to the browser must preserve at minimum:

```text
history_schema_version
record_id
host
signal_id
observed_at_utc
quality
source
cadence_class
reason
data
```

Historical quality is the quality recorded at observation time. The UI may calculate sample age, but must not rewrite historical truth.

No downsampling, aggregation or retention behavior is approved by G7-A unless the raw historical evidence remains authoritative and the transformation is explicitly documented.

## 11. UI contract for G7-B

The EAGLE Health current section SHALL display at minimum:

- overall evidence availability/quality, without health severity invention;
- observation timestamp;
- provenance/source;
- CPU evidence;
- memory evidence;
- storage capacity evidence;
- physical storage-health evidence when available;
- uptime/OS evidence;
- freshness/unknown reasons where useful.

UI wording must distinguish:

```text
Observed / Current evidence
Unavailable / Unknown evidence
Stale evidence
Policy not activated
```

Avoid wording that implies automatic remediation or certified safety.

## 12. Transport neutrality

G7-A does not mandate whether the public EAGLE Health projection is ultimately delivered through the existing telemetry relay, a static generated asset, or a later approved endpoint.

Whichever implementation is selected must preserve:

- browser read-only behavior;
- source provenance;
- freshness;
- fail-closed rendering;
- no browser credential;
- no Safety Authority coupling.

Transport choice belongs to the implementation slice and must reuse existing portal infrastructure when feasible.

## 13. Observability

The projection/export implementation should expose machine-readable evidence including:

```text
run_id
source_observed_at_utc
records/signals_seen
signals_published
signals_rejected
projection_result
last_error
```

Portal failures should remain diagnosable separately from collector failures.

## 14. Delivery sequence

### G7-A — Public projection contract

- this contract;
- validate mapping from G5 current projection and G6 history records;
- no runtime deployment.

### G7-B — Current EAGLE Health UI

- add current-state EAGLE Health panel to existing Observatory Status;
- implement public current projection adapter/path;
- preserve freshness and provenance;
- CI tests for malformed/stale/missing signals.

### G7-C — Bounded history/trends

- expose bounded historical projection;
- add limited trends without severity invention;
- preserve raw-history provenance.

### G7-D — CI/failure injection

- hosted failure;
- static fallback;
- malformed current projection;
- stale projection;
- partial/missing signal;
- malformed history;
- browser rendering regressions.

### G7-E — Portal OAT and acceptance

- hosted/static verification;
- stale/unknown behavior;
- provenance rendering;
- no credentials in browser;
- no Safety Authority wording/coupling;
- independent review before closure.

## 15. Acceptance criteria for G7-A

G7-A is complete when:

1. the browser-facing projection is explicitly separated from EAGLE-local current/history files;
2. current signal/provenance/freshness semantics are defined;
3. `UNKNOWN/STALE` behavior is preserved;
4. `POLICY_NOT_ACTIVATED` remains explicit;
5. storage capacity and physical-health semantics remain separate;
6. history exposure is bounded rather than raw/unbounded;
7. no browser credentials or command surface is introduced;
8. Safety Authority remains outside scope;
9. downstream G7-B/G7-C slices have implementable contracts.

## 16. Out of scope

G7-A does not approve:

- overall health severity thresholds;
- alert thresholds;
- remediation;
- EAGLE control commands;
- Safety Authority integration;
- unbounded raw history download to the public browser;
- destructive retention;
- permanent G6 history scheduling;
- G8 final safety review.

## 17. Disposition

**G7-A is architecture-ready for implementation.**

Next step: implement G7-B current EAGLE Health UI and a validated public current projection adapter/path using the existing Observatory Status surface and transport architecture wherever feasible.
