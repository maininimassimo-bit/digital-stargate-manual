# SOL-OSM-001 — Interface Contracts

## 1. Contract principles

- Interfaces expose intent and state, not uncontrolled device access.
- Every command has a correlation identifier and timeout.
- Adapters normalize external-system responses into canonical result codes.
- Credentials are managed outside the contract payload.
- Commands affecting safety or equipment are auditable.

## 2. Canonical command result

```json
{
  "command_id": "uuid",
  "correlation_id": "uuid",
  "status": "SUCCEEDED",
  "started_at": "2026-07-28T21:15:00+02:00",
  "completed_at": "2026-07-28T21:15:03+02:00",
  "result_code": "OK",
  "message": "Sequence prepared",
  "evidence_refs": []
}
```

## 3. Adapter contracts

### 3.1 Safety Adapter

| Operation | Response |
|---|---|
| `getSafetyState()` | `SAFE`, `UNSAFE` or `UNKNOWN`, timestamp and reason codes |
| `subscribeSafetyChanges()` | Stream or polling abstraction for authoritative changes |
| `requestSafeAction(reason)` | Acknowledgement only; authority remains with safety controller |

### 3.2 N.I.N.A. Adapter

| Operation | Purpose |
|---|---|
| `prepareSequence(planRef)` | Load and validate the execution sequence |
| `startSequence()` | Begin execution after authorization |
| `pauseSequence(reason)` | Request controlled pause |
| `resumeSequence()` | Resume after guards pass |
| `stopSequence(mode)` | Controlled stop or emergency-compatible termination |
| `getSequenceStatus()` | Return canonical execution status |

### 3.3 PHD2 Adapter

| Operation | Purpose |
|---|---|
| `getGuidingStatus()` | Return guiding state and health indicators |
| `startGuiding(profileRef)` | Start guiding where delegated |
| `stopGuiding()` | Stop guiding during close or abort |

### 3.4 CPWI/ASCOM Adapter

Provides normalized mount, focuser, camera, cover and related equipment status. Commands are permitted only when ownership is unambiguous and no conflicting controller is active.

## 4. Timeouts and retries

| Interaction class | Default approach |
|---|---|
| Read-only status | Short timeout, bounded retry |
| Idempotent command | Bounded retry with same command ID |
| Non-idempotent movement | No blind retry; verify state first |
| Safety-related command | Immediate acknowledgement plus independent state verification |

## 5. Versioning

Contracts use semantic versions. Backward-compatible additions increment the minor version; breaking changes require a new major version and a migration decision.
