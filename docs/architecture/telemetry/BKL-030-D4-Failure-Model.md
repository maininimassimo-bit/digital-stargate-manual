# BKL-030 — D4 EAGLE Host Health Collector Failure Model

| Campo | Valore |
|---|---|
| Identificativo | BKL-030-D4 |
| Stato | **DESIGNED — validation pending G2/G3 implementation** |
| Target | EAGLE30154 |
| Boundary | Read-only host observability; no remediation/control authority |
| Safety Authority | External/local and independent from collector availability |

## 1. Purpose

Define deterministic failure semantics for the future `DSG.EagleHostHealthCollector` before implementation. D4 converts the verified D1/D2 source limitations and D3 overhead evidence into fail-safe behavior without inventing hardware thresholds or remediation actions.

D4 is an architecture failure model. It does not claim that the permanent collector, projection writer, watchdog or portal integration already exists.

## 2. Failure principles

1. A single source failure must not terminate the whole collection cycle.
2. Missing evidence is represented explicitly; it is never silently converted to `HEALTHY`.
3. Source access denial does not authorize privilege elevation.
4. Stale data must remain distinguishable from current data.
5. The last valid projection may be retained for continuity only with stale/age semantics; it must never be presented as current.
6. Projection publication must be atomic so consumers do not observe partially written JSON.
7. Probe timeout/hang must be bounded so one source cannot block the collector indefinitely.
8. Collector failure must not stop, restart, kill or reconfigure N.I.N.A., PHD2, ASCOM or Windows services.
9. Host health must never become Safety Authority input that can command dome/mount/power/network.
10. Recovery is observational and automatic where safe: retry a later collection cycle, not device/service remediation.

## 3. Failure-mode matrix

| Failure mode | Required collector behavior | Projection semantics | Recovery | Forbidden response |
|---|---|---|---|---|
| Source unavailable/not installed | Continue remaining probes | affected signal `UNKNOWN` with reason/provenance | retry at next class cadence | fabricate value; mark healthy |
| Access denied/non-elevated limitation | Continue remaining probes | signal `UNKNOWN` / `UNAVAILABLE_NON_ELEVATED` | retry later; preserve low privilege | auto-elevate; change ACL/registry |
| Source returns zero rows where presence is not guaranteed | Treat as valid empty evidence unless source contract requires data | raw empty result plus source quality | normal next cadence | infer device failure without policy |
| Malformed/unparseable source output | Isolate parse failure | signal `UNKNOWN`, reason `MALFORMED_SOURCE` | retry later; diagnostic log | crash whole collector |
| Probe exception | Catch per probe | signal `UNKNOWN`, exception category without secrets | next cadence | crash loop |
| Probe timeout/hang | terminate/abandon bounded probe execution path when implementation supports it | signal `UNKNOWN`, reason `TIMEOUT` | next cadence, optionally slower/backoff in G3 | wait indefinitely; kill unrelated process |
| Collector process stopped/crashed | no new projection can be current | consumer derives `STALE` after freshness expiry | normal process restart mechanism to be governed in G3/OAT | command equipment to compensate |
| Collector CPU contention / cycle overrun | skip overlap; do not create concurrent collection pile-up | retain last valid sample with correct age | next non-overlapping cycle; cadence tuning | increase priority over imaging workload |
| Projection serialization failure | do not replace last valid projection | last valid file ages toward `STALE`; diagnostic evidence | retry next cycle | publish malformed JSON |
| Projection write/disk failure | preserve existing valid projection if possible | last valid projection becomes stale | retry; expose write failure when possible | delete valid projection first; free disk automatically |
| Process interruption during write | atomic temp/write/replace design prevents partial canonical file | old valid projection remains | next cycle | in-place partial write |
| Partial source success | publish cycle only if contract permits per-signal quality | current envelope with explicit per-signal `UNKNOWN` reasons | failed signals retry by cadence | collapse all signals to HEALTHY |
| System clock evidence unavailable | preserve observed local collection timestamp source semantics and mark time-sync signal unknown/unverified | `time_sync` not healthy by assumption | retry slow/medium cadence | alter Windows Time service |
| Event Log query too expensive/fails | isolate Event Log signal | Event Log signal unknown/stale; host collector continues | slow/on-change retry | block fast health path |
| Detailed SMART unavailable non-elevated | keep optional/unavailable disposition | raw physical disk health may remain available; detailed reliability unknown | only separately governed adapter could change this | elevate collector automatically |
| Scheduled Task result non-zero | record raw result; classification requires governed mapping | no automatic CRITICAL inference | policy mapping in G2/G3 | rerun task automatically |
| Pending reboot evidence present | record raw evidence | classification requires governed policy | next slow cadence | reboot automatically |
| USB/COM source disagreement | preserve provenance; use governed composite/PnP policy | do not fabricate consensus | retry appropriate cadence | reset USB/COM |
| Network loss | local collection may continue; downstream delivery/portal may stale independently | local projection semantics independent from portal reachability | downstream reconnect/retry outside Safety | alter router/failover policy |
| Host power loss | collector unavailable | all remote health becomes stale/unknown by consumer freshness semantics | host/local infrastructure recovery | software claim of safe state |

## 4. Freshness and stale semantics

G2 must define explicit `observed_at_utc` and `fresh_until_utc` semantics. Until those values are governed, D4 does not invent durations.

Required rule:

```text
current valid projection + freshness not expired -> CURRENT
valid projection + freshness expired             -> STALE
no valid projection / unreadable projection      -> UNKNOWN
```

`STALE` is not equivalent to `CRITICAL`, and `UNKNOWN` is not equivalent to `HEALTHY`. Any later summary-state policy must remain explainable through reasons.

## 5. Non-overlap and workload protection

D3-B showed the monolithic discovery can take more than 20 seconds under normal imaging load. Therefore G3 must prevent overlapping collector cycles and must not use the full discovery as a fast-cadence operation.

If a cadence tick occurs while the same class is still running, the implementation should skip/coalesce the tick and record an overrun rather than launch a competing copy. Exact cadence and backoff values remain G2/G3 decisions.

Collector/process priority must not be raised to compete with N.I.N.A./PHD2.

## 6. Atomic projection publication

Target design for G3:

1. collect into an in-memory cycle model;
2. serialize to a temporary file in the same controlled Digital StarGate telemetry directory;
3. validate serialization before publication;
4. atomically replace/move the canonical `eagle-health.json` where supported;
5. if publication fails, retain the previous valid canonical projection and record diagnostic evidence.

No implementation is claimed by D4.

## 7. Diagnostic containment

Diagnostics should identify component, probe/source, UTC observation time, failure category and bounded error text. They must not copy credentials, secrets or arbitrary sensitive configuration into the public projection.

Repeated source failures may be counted for diagnostics, but D4 does not define a numeric threshold for escalation.

## 8. Safety review

### Loss of connectivity
Host collection remains local where possible. Loss of portal/network connectivity does not authorize equipment commands. Remote consumers eventually see stale/unknown telemetry.

### Stale or absent telemetry
Stale/absent telemetry is explicit. It cannot be converted into a safe-state assertion.

### Power loss / controller failure
Power loss means the collector cannot attest current host health. Physical/local observatory interlocks remain authoritative and independent.

### Partial closure / emergency stop / manual override
These are outside BKL-030 host-health authority. The collector must neither override nor mask local safety/interlock state.

### Safe-state verification
BKL-030 does not verify physical safe state. That responsibility remains with the approved local Safety Authority and equipment-specific telemetry paths.

## 9. Validation implications

D4 architecture is complete when this model is reviewed and integrated. Runtime validation remains future work:

- G2: encode provenance, freshness, cadence class and failure reason contract;
- G3: implement per-probe isolation, bounded execution, non-overlap and atomic publication;
- G4: CI tests for malformed source, access denied, timeout, serialization/write failure and partial success;
- G5: OAT on EAGLE30154 including imaging-context non-interference;
- G8: confirm no control/remediation path and Safety Authority independence.

## 10. D4 disposition

**D4 failure model DESIGNED. No runtime validation is claimed. BKL-030 remains In Progress and must proceed through G1–G8 before closure.**
