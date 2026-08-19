# Observatory Status — Dome Telemetry Sidecar

## Status

Solution design for the realtime Observatory Status dome slice.

## Verified runtime evidence

On EAGLE30154, read-only probes established:

- `ASCOM.TS_Shelter.Switch` is installed and exposes metadata, but the probe client was not connected and therefore did not read switch values.
- TS Shelter is backed by FTDI `USB Serial Port (COM47)`, driver `2.12.36.4`.
- `ASCOM.TS_Shelter.SafetyMonitor` is installed and exposes metadata, but the probe client was not connected and therefore did not read `IsSafe`.
- An initial N.I.N.A. local-interface inventory, taken while N.I.N.A. was not running, found no N.I.N.A.-owned TCP listener and no verified local telemetry API in the inspected configuration.
- A second passive inventory was then executed with N.I.N.A. running under the normal operational workflow. Two N.I.N.A. processes and `ASCOM.TS_Shelter.exe -Embedding` were present.
- During that operational inventory, no TCP listener, established TCP connection, or matching named-pipe candidate was found for the N.I.N.A./TS Shelter target processes.

These observations do **not** prove that TS Shelter supports safe concurrent clients and do **not** establish a protocol for direct COM47 access. They also mean that no existing passive N.I.N.A./TS Shelter IPC surface has been verified for Observatory Status.

## Decision

Introduce a local **Dome Telemetry Sidecar** boundary for Observatory Status. The sidecar is an observation component, not an equipment controller.

The sidecar MUST NOT invent or assume a N.I.N.A. API, TS Shelter serial protocol, or ASCOM multi-client capability.

The preferred live source is now an explicitly installed **N.I.N.A.-hosted read-only dome exporter/plugin**. The exporter runs inside N.I.N.A.'s existing equipment-owning context and publishes a local observation projection; the Digital StarGate sidecar consumes that projection without opening another TS Shelter connection.

Until that exporter is implemented, installed, and validated, the sidecar publishes `UNKNOWN`.

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

## Selected exporter contract

The N.I.N.A.-hosted exporter is a read-only adapter. It MUST obtain dome state only from N.I.N.A.'s already-owned in-process equipment model and MUST NOT instantiate another ASCOM dome, switch, SafetyMonitor, serial, or relay connection.

The first implementation uses an atomic local file projection rather than an HTTP server. This keeps the observatory control surface non-networked and allows the Digital StarGate producer to consume telemetry without calling into N.I.N.A.

Proposed projection path:

`%LOCALAPPDATA%\DigitalStarGate\telemetry\nina-dome.json`

Minimum exporter payload:

```json
{
  "schemaVersion": 1,
  "source": "nina-dome-exporter",
  "connected": true,
  "state": "OPEN",
  "observedAt": "2026-08-18T19:30:00+02:00"
}
```

`state` values MUST be mapped only from semantics actually provided by the N.I.N.A. plugin API used by the implementation. The implementation must not guess a state from unrelated flags. If the source is disconnected, unavailable, unsupported, or cannot be mapped unambiguously, it writes `UNKNOWN` with the corresponding diagnostic reason.

The writer must publish atomically (temporary file followed by same-volume replace/rename) so consumers never observe a partially written JSON document.

Safety (`safe`) remains separate from dome position. It MUST NOT be synthesized from OPEN/CLOSED state. A future exporter may add `safe` only when an approved, semantically verified in-process safety source is available.

## Failure behavior

- N.I.N.A. not running: `UNKNOWN` unless another approved source is independently available.
- exporter file absent: `UNKNOWN` / `NO_APPROVED_LIVE_SOURCE`.
- exporter source disconnected: `UNKNOWN`.
- stale observation: `UNKNOWN`.
- malformed projection: `UNKNOWN` and diagnostic parse failure.
- contradictory sources: `UNKNOWN` and diagnostic conflict.
- adapter exception: retain no prior value as current; publish `UNKNOWN`.

## Safety boundary

The Observatory Status path is informational. Local physical interlocks and the observatory's existing equipment-control safety mechanisms remain authoritative and independent from the dashboard, sidecar, network, VPN, backend, and UI.

## Next implementation slice

1. Identify the exact installed N.I.N.A. version/plugin SDK surface available on EAGLE30154.
2. Implement the smallest read-only N.I.N.A. plugin/exporter that observes the already-owned dome model.
3. Write the atomic local projection without opening any new equipment connection.
4. Add a Digital StarGate file adapter that validates schema, timestamp, freshness, and state values.
5. Validate first with N.I.N.A. disconnected from TS Shelter, then under the normal connected workflow, without issuing equipment commands.
6. Only after validation, allow the producer to project verified dome state into `systems.dome`.
