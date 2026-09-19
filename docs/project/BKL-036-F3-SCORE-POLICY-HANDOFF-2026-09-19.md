# BKL-036-F3 — Score Policy Handoff

| Field | Value |
|---|---|
| Identifier | `BKL-036-F3-HANDOFF-001` |
| Status | Implementation candidate |
| Date | 2026-09-19 |
| Capability | Observatory Health Score |
| Scope | Repository-archived evidence score, public read-only projection |
| Runtime impact | None |

## Owner decisions captured

- source data: telemetry already acquired and archived in the repository;
- publication: public Digital StarGate portal;
- scale: `0–100`;
- equal weights across weather, dome, mount, camera, power, network and EAGLE health;
- qualifying domain value: `100`;
- any non-comparable mandatory domain: `UNAVAILABLE`;
- source-specific freshness and retention remain authoritative;
- portal labels timestamp, source, repository evidence and non-live/non-real-time status.

## Disposition

The implementation is bounded to a deterministic static projection. Current archived evidence produces `UNAVAILABLE`; no synthetic or default value is promoted to `100`.

The projection is not BKL-032 readiness, does not alter local physical interlocks and cannot command or schedule observatory equipment.

## Acceptance boundary

Acceptance requires exact-head CI, ARB and Release Quality review, expected-head merge verification and complete post-merge workflow verification. Future live telemetry use or operational interpretation remains separately gated.
