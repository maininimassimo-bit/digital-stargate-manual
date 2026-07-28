# API Governance

## 1. Base path and versioning

All public platform endpoints use:

```text
/api/v1
```

The major version is encoded in the URI. Minor and patch changes remain backward compatible within the same major version.

## 2. Resource naming

Resource names use lowercase plural nouns:

```text
/sessions
/devices
/observatories
/weather-snapshots
/telemetry
```

Commands that do not map cleanly to CRUD are represented as subordinate action resources:

```text
POST /sessions/{sessionId}/commands
POST /devices/{deviceId}/commands
```

## 3. Media types

The default media type is:

```text
application/json
```

All timestamps use RFC 3339 UTC format. Identifiers use UUID strings unless an external system supplies a stable identifier.

## 4. Correlation and causation

Clients should send:

```text
X-Correlation-ID: <uuid>
```

The platform generates one when absent and returns it in the response. Commands and resulting events also carry `correlationId` and, where applicable, `causationId`.

## 5. Idempotency

State-changing requests that may be retried accept:

```text
Idempotency-Key: <client-generated-value>
```

A repeated request with the same key and equivalent payload returns the original outcome.

## 6. Pagination

Collections use cursor pagination:

```text
?limit=50&cursor=<opaque-token>
```

Responses include `nextCursor` only when more records exist.

## 7. Compatibility rules

Backward-compatible changes include:

- adding optional properties;
- adding new enum values only when consumers are required to tolerate unknown values;
- adding endpoints;
- adding non-mandatory response headers.

Breaking changes include removing or renaming fields, changing field meaning, narrowing accepted values, or changing resource identifiers.

## 8. Contract review gate

Every contract change must include:

- affected consumers;
- compatibility classification;
- migration notes;
- schema validation;
- example requests and responses;
- architecture approval for breaking changes.
