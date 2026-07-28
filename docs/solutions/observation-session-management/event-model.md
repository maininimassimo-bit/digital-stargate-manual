# SOL-OSM-001 — Event Model

## 1. Event envelope

All solution events use a common envelope:

```json
{
  "event_id": "uuid",
  "event_type": "session.execution.started",
  "event_version": "1.0",
  "occurred_at": "2026-07-28T21:15:00+02:00",
  "producer": "session-orchestrator",
  "session_id": "DSG-SESSION-20260728-001",
  "correlation_id": "uuid",
  "causation_id": "uuid",
  "severity": "info",
  "payload": {}
}
```

## 2. Event catalogue

| Event | Producer | Typical consumers |
|---|---|---|
| `session.created` | Session Management Service | Repository, UI |
| `session.validation.started` | Orchestrator | UI, repository |
| `session.validation.failed` | Orchestrator | UI, notification, repository |
| `session.ready` | Orchestrator | UI, scheduler |
| `session.execution.started` | Orchestrator | UI, monitoring, repository |
| `session.execution.paused` | Orchestrator | UI, monitoring |
| `session.recovery.started` | Orchestrator | UI, notification |
| `session.abort.requested` | Operator or safety policy | Orchestrator, repository |
| `session.safety.changed` | Safety Adapter | Orchestrator, monitoring |
| `session.execution.completed` | N.I.N.A. Adapter | Orchestrator, repository |
| `session.closed` | Session Management Service | Reporting, analytics, repository |
| `adapter.command.failed` | Any adapter | Orchestrator, monitoring |

## 3. Delivery semantics

The target semantics are at-least-once delivery within the local solution boundary. Consumers must therefore be idempotent and use `event_id` for duplicate detection.

## 4. Ordering

Events are ordered per session using the persisted transition sequence. Global ordering across sessions is not required.

## 5. Severity rules

- `info`: expected lifecycle activity;
- `warning`: degraded but controlled behavior;
- `error`: operation failed and requires recovery;
- `critical`: safety or observatory integrity is at risk.
