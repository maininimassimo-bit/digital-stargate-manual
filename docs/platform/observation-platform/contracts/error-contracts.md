# Error Contracts

## 1. Problem representation

Errors use a platform-specific profile compatible with RFC 9457 Problem Details.

```json
{
  "type": "urn:digital-stargate:problem:safety-policy-denied",
  "title": "Safety policy denied the command",
  "status": 403,
  "code": "DSG-SAF-001",
  "detail": "Roof opening is not allowed while the safety state is UNSAFE.",
  "instance": "/api/v1/devices/roof-01/commands/7bf3",
  "correlationId": "2b5cc205-7576-43c0-843f-fd6d3242cf6c",
  "severity": "CRITICAL",
  "recoverable": false,
  "retryAfterSeconds": null
}
```

## 2. Code namespaces

| Namespace | Domain |
|---|---|
| `DSG-API` | API validation and protocol |
| `DSG-SES` | Session lifecycle |
| `DSG-SAF` | Safety authority |
| `DSG-WTH` | Weather integration |
| `DSG-RFG` | Roof or dome |
| `DSG-MNT` | Mount |
| `DSG-CAM` | Camera |
| `DSG-GUI` | Guiding |
| `DSG-FOC` | Focuser |
| `DSG-INF` | Runtime and infrastructure |

## 3. Severity

- `INFO`;
- `WARNING`;
- `ERROR`;
- `CRITICAL`.

## 4. Recovery metadata

`recoverable` indicates whether an automated retry or operator action may restore service. It must not be interpreted as permission to retry a safety-sensitive command without re-evaluating safety.

## 5. Logging

Error logs must include the error code, correlation identifier, affected resource, active configuration version and sanitized dependency details. Credentials and secrets must never be logged.
