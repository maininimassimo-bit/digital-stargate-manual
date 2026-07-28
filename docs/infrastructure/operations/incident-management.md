# Incident Management

## Incident lifecycle

```text
Detection
   ↓
Classification
   ↓
Containment
   ↓
Recovery
   ↓
Validation
   ↓
Closure and Lessons Learned
```

## Severity model

| Severity | Meaning | Example |
|---|---|---|
| SEV-1 | Immediate safety risk or total loss of control | Dome cannot close during unsafe weather |
| SEV-2 | Major operational interruption | Automation unavailable |
| SEV-3 | Degraded service with workaround | Primary WAN unavailable, LTE active |
| SEV-4 | Minor issue | Non-critical telemetry gap |

Every SEV-1 and SEV-2 incident requires a documented review.
