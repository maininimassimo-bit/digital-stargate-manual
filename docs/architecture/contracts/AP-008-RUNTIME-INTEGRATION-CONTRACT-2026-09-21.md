# AP-008 Runtime and Schedule Integration Contract

**Identifier:** `AP-008-RUNTIME-INT-001`  
**Version:** 0.1.0  
**Status:** PROPOSED — NOT APPROVED FOR ACTIVATION  
**Date:** 2026-09-21  
**Owner:** Digital StarGate Project Owner / Architecture Sponsor

## 1. Purpose

Define the repository-level contract required before any future runtime activation for the Digital StarGate read-only telemetry path and schedule intake.

This document does not activate runtime, authorize secrets, install a scheduled task, publish telemetry, or authorize commands to observatory equipment.

## 2. Authority boundaries

- Local physical interlocks and the local Safety Monitor remain the final Safety Authority.
- The integration layer is read-only in the first phase.
- No command may be sent to dome, mount, camera, relay, PLC, CPWI, ASCOM, N.I.N.A. or PHD2.
- Missing, malformed, stale or conflicting evidence produces `UNKNOWN`, `DEGRADED` or `NO_GO`; it never produces `SAFE`.
- `runtimeEnabled=false` is the default and blocks runtime writes, publication, task installation/start and secret access.

## 3. Schedule contract

The application contract has no daily schedule-count limit. A technical API or GitHub rate limit is handled by bounded retry, backoff and explicit `DEGRADED`/failure evidence; it must not be converted into a false success.

Each schedule has:

- immutable `schedule_id`;
- UTC start and end;
- explicit `idempotency_key`;
- lifecycle state `PLANNED`, `CANCELLED`, `COMPLETED` or `FAILED`;
- correlation identifier;
- creation and update timestamps.

Required semantics:

1. 3, 10, 100 and 1,000 distinct schedules on one UTC day are valid at the contract layer.
2. Two submissions with the same idempotency key produce one logical schedule.
3. Distinct schedules may overlap; overlap is recorded and does not silently merge or delete either schedule.
4. Cancellation is idempotent and cannot resurrect a schedule after restart.
5. Restart reconstructs state from the durable journal; incomplete records remain non-successful and fail closed.
6. Dispatch is advisory/read-only until a separate activation gate is approved.
7. A retry never creates a second logical schedule for the same idempotency key.
8. Retention and publication failures are observable and never authorize hardware action.

## 4. Integration and telemetry defaults

The proposed first-phase defaults are:

| Source | Poll | Freshness |
|---|---:|---:|
| CloudWatcher CSV | 15 s | 60 s |
| N.I.N.A. projection | 60 s | 5 min |
| PHD2 projection | 60 s | 5 min |
| EAGLE health | 30 s | 90 s |

Transport is outbound HTTPS only. Public projections and audit records are sanitized, correlation-bound and retained for six months on GitHub subject to repository governance.

## 5. Failure and rollback

The implementation must support:

- `runtimeEnabled=false`;
- local agent stop;
- publisher block;
- restoration of the last valid projection;
- deployment/commit revert;
- diagnostic log preservation;
- secret rotation after compromise;
- reactivation only after a new shadow test.

Rollback must not delete evidence.

## 6. Required approval gates

Before any `-RuntimeEnabled $true` invocation:

1. approve this contract through the AP-008 architecture/release governance path;
2. complete the offline schedule contract suite;
3. complete read-only EAGLE diagnostics;
4. complete shadow, stale/missing-data, network, restart and endurance tests;
5. confirm no-command-path and local-interlock invariants;
6. approve a separate activation decision.

Until then the contract remains proposed and runtime remains disabled.
