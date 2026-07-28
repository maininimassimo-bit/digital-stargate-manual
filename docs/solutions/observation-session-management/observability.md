# SOL-OSM-001 — Monitoring and Observability

## 1. Objectives

Observability must make it possible to answer:

- What state is the session in?
- Why did the latest transition occur?
- Which component or external system caused a delay or failure?
- Is the observatory currently safe?
- Has all mandatory evidence been captured?

## 2. Signals

### Logs

Structured logs include timestamp, session ID, correlation ID, component, severity, event type and sanitized message.

### Metrics

| Metric | Purpose |
|---|---|
| `dsg_session_active_total` | Number of active sessions |
| `dsg_session_transition_total` | State transitions by target state |
| `dsg_adapter_command_duration_seconds` | Adapter latency |
| `dsg_adapter_failure_total` | Failures by adapter and result code |
| `dsg_safety_state` | Encoded current authoritative state |
| `dsg_recovery_attempt_total` | Recovery attempts by category |
| `dsg_evidence_pending_total` | Evidence items not yet finalized |

### Traces

Distributed tracing is optional initially, but correlation IDs must be preserved across orchestrator and adapter calls to support future trace reconstruction.

## 3. Alerts

| Condition | Severity |
|---|---|
| Safety state becomes `UNSAFE` during execution | Critical |
| Safe action does not reach verified completion | Critical |
| Session remains in `RECOVERING` beyond policy limit | Error |
| Evidence repository unavailable | Error |
| Repeated adapter timeout | Warning/Error based on threshold |
| Remote synchronization delayed | Warning only if local evidence is safe |

## 4. Operational dashboard

The minimum dashboard shows:

- session identity and lifecycle state;
- safety state and timestamp;
- current execution step;
- N.I.N.A., PHD2 and CPWI/ASCOM adapter health;
- recovery attempts;
- outstanding evidence and closure status.

## 5. Data protection

Logs and metrics must not expose credentials, VPN secrets or unnecessary personal data. Retention follows the evidence and operational-data policies defined by the platform governance.
