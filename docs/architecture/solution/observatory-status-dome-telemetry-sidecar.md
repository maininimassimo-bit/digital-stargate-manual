# Observatory Status — Dome Telemetry Sidecar

## Status

Solution design for the realtime Observatory Status dome slice.

## Verified runtime evidence

On EAGLE30154, read-only probes established:

- `ASCOM.TS_Shelter.Switch` is installed and exposes metadata, but the probe client was not connected and therefore did not read switch values.
- TS Shelter is backed by FTDI `USB Serial Port (COM47)`, driver `2.12.36.4`.
- `ASCOM.TS_Shelter.SafetyMonitor` is installed and exposes metadata, but the probe client was not connected and therefore did not read `IsSafe`.
- N.I.N.A. was not running during local-interface inventory.
- No N.I.N.A.-owned TCP listening port was present during that inventory.
- No verified N.I.N.A. local telemetry API was identified from the inspected configuration.

These observations do **not** prove that TS Shelter supports safe concurrent clients and do **not** establish a protocol for direct COM47 access.

## Decision

Introduce a local **Dome Telemetry Sidecar** boundary for Observatory Status. The sidecar is an observation component, not an equipment controller.

The sidecar MUST NOT invent or assume a N.I.N.A. API, TS Shelter serial protocol, or ASCOM multi-client capability.

Until a safe live observation source is validated, the sidecar publishes `UNKNOWN` rather than opening a competing equipment connection.

## Responsibilities

The sidecar may:

- detect whether an approved telemetry source is available;
- read already-exported state from that approved source;
- normalize observations into the Observatory Status dome contract;
- timestamp observations and apply freshness rules;
- report source health and diagnostic reason codes.

The sidecar must not:

- open, close, park, unpark, slew, or otherwise command the shelter;
- write switch values;
- change SafetyMonitor state;
- bypass N.I.N.A., TS Shelter, relay-controller, weather, or physical safety logic;
- infer `OPEN`, `CLOSED`, or `SAFE` from process presence alone;
- open COM47 directly without a separately validated and governed adapter;
- create a second ASCOM equipment connection merely to obtain dashboard telemetry unless concurrency safety has been proven.

## Normalized contract

Minimum projection:

```json
{
  "system": "dome",
  "state": "UNKNOWN",
  "safe": null,
  "connected": false,
  "source": "none",
  "observedAt": null,
  "fresh": false,
  "reason": "NO_APPROVED_LIVE_SOURCE"
}
```

`state` is deliberately constrained to values supported by verified source semantics. `UNKNOWN` is mandatory for absent, disconnected, stale, contradictory, or unvalidated input.

## Candidate adapters

Adapters are evaluated in this order:

1. existing N.I.N.A.-owned read-only telemetry/export surface, if later verified while N.I.N.A. is running;
2. an explicitly installed N.I.N.A. telemetry plugin/exporter under controlled configuration;
3. a TS Shelter/ASCOM observation adapter only after multi-client behavior and command isolation are validated;
4. direct serial observation only if the vendor protocol and safe sharing model are formally documented and approved.

No candidate becomes authoritative merely because it is technically reachable.

## Failure behavior

- N.I.N.A. not running: `UNKNOWN` unless another approved source is independently available.
- approved source disconnected: `UNKNOWN`.
- stale observation: `UNKNOWN`.
- contradictory sources: `UNKNOWN` and diagnostic conflict.
- adapter exception: retain no prior value as current; publish `UNKNOWN`.

## Safety boundary

The Observatory Status path is informational. Local physical interlocks and the observatory's existing equipment-control safety mechanisms remain authoritative and independent from the dashboard, sidecar, network, VPN, backend, and UI.

## Next validation

Run a second N.I.N.A. local-interface inventory **while N.I.N.A. is running and TS Shelter is connected through the normal operational workflow**. This validation remains passive: inspect process ownership and listeners only; do not probe candidate HTTP endpoints and do not instantiate a second ASCOM client.

If no safe export surface appears, evaluate a dedicated N.I.N.A.-hosted exporter/plugin as the preferred next implementation slice.
