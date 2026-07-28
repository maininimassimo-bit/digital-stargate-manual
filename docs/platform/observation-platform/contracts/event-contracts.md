# Event Contracts

## 1. Event model

Platform events are immutable facts. They describe a state transition or observed condition and are not used as mutable records.

Every event uses the shared event envelope schema and includes:

- `eventId`;
- `eventType`;
- `eventVersion`;
- `occurredAt`;
- `source`;
- `subject`;
- `correlationId`;
- optional `causationId`;
- `data`.

## 2. Event naming

Event types use completed facts in PascalCase:

```text
SessionCreated
SessionValidated
SessionStarted
SessionPaused
SessionResumed
SessionCompleted
SessionAborted
SafetyStateChanged
WeatherBecameUnsafe
RoofOpened
RoofClosed
MountParked
GuidingStarted
ExposureCompleted
```

## 3. Core session events

| Event | Trigger | Minimum data |
|---|---|---|
| `SessionCreated` | Session persisted | sessionId, planId |
| `SessionValidated` | Preconditions evaluated | sessionId, validationResult |
| `SessionStarted` | Runtime execution begins | sessionId, startedBy |
| `SessionPaused` | Execution suspended | sessionId, reason |
| `SessionCompleted` | Normal completion | sessionId, outcome |
| `SessionAborted` | Controlled or emergency abort | sessionId, reason, safetyRelated |

## 4. Safety events

Safety events have priority over ordinary orchestration events. Consumers must process them even when the session service is degraded.

```json
{
  "eventType": "SafetyStateChanged",
  "eventVersion": "1.0",
  "data": {
    "previousState": "SAFE",
    "currentState": "UNSAFE",
    "reasonCodes": ["RAIN_DETECTED"],
    "authority": "independent-safety-controller"
  }
}
```

## 5. Delivery semantics

The baseline delivery model is at-least-once. Consumers must deduplicate by `eventId` and implement idempotent handlers.

Event ordering is guaranteed only within the same subject stream where the transport supports partitioning by `subject`.
