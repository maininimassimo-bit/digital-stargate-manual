# REST API Contract

## 1. Session resources

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/sessions` | List observation sessions |
| POST | `/api/v1/sessions` | Create a planned session |
| GET | `/api/v1/sessions/{sessionId}` | Read session state |
| PATCH | `/api/v1/sessions/{sessionId}` | Update mutable planning data |
| POST | `/api/v1/sessions/{sessionId}/commands` | Request a lifecycle transition |

Example command:

```json
{
  "command": "START",
  "requestedBy": "operator",
  "reason": "Night plan approved"
}
```

Supported initial commands:

- `VALIDATE`;
- `START`;
- `PAUSE`;
- `RESUME`;
- `ABORT`;
- `SHUTDOWN`.

## 2. Observatory resources

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/observatories/{observatoryId}` | Read observatory metadata |
| GET | `/api/v1/observatories/{observatoryId}/state` | Read current aggregate state |
| GET | `/api/v1/observatories/{observatoryId}/health` | Read component health summary |

## 3. Device resources

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/devices` | List registered devices |
| GET | `/api/v1/devices/{deviceId}` | Read device capabilities and state |
| POST | `/api/v1/devices/{deviceId}/commands` | Submit an allowed device command |

Direct device commands are policy-controlled. Safety-sensitive commands may be rejected even when the caller is authorized.

## 4. Response envelope

Successful responses use:

```json
{
  "requestId": "f14412aa-63f7-4df5-a131-7c5733dbbcb2",
  "correlationId": "2b5cc205-7576-43c0-843f-fd6d3242cf6c",
  "timestamp": "2026-07-28T20:30:00Z",
  "data": {},
  "warnings": []
}
```

## 5. Status codes

| Code | Meaning |
|---|---|
| 200 | Successful read or synchronous command result |
| 201 | Resource created |
| 202 | Command accepted for asynchronous execution |
| 400 | Invalid request |
| 401 | Authentication required |
| 403 | Authorization or safety policy denied the operation |
| 404 | Resource not found |
| 409 | State conflict or idempotency conflict |
| 422 | Semantically invalid command |
| 429 | Rate limit exceeded |
| 503 | Required platform dependency unavailable |
