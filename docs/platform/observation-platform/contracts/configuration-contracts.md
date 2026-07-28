# Configuration Contracts

## 1. Configuration hierarchy

Effective configuration is resolved in this order:

1. platform defaults;
2. observatory profile;
3. equipment profile;
4. session plan overrides;
5. emergency policy overrides.

Higher-priority safety limits may only become more restrictive.

## 2. Configuration document

```json
{
  "configurationId": "obs-manciano-primary",
  "version": 12,
  "effectiveFrom": "2026-07-28T18:00:00Z",
  "scope": "OBSERVATORY",
  "values": {
    "weather.maxWindMps": 10.0,
    "weather.maxHumidityPercent": 85,
    "roof.closeOnTelemetryLossSeconds": 60
  },
  "approvedBy": "platform-owner"
}
```

## 3. Rules

- configuration is immutable after publication;
- updates create a new version;
- secrets are referenced, never embedded;
- units are explicit in property names or schema metadata;
- safety policy changes require approval and audit evidence;
- runtime components report the active configuration version.

## 4. Validation

Configuration is rejected when:

- a required property is absent;
- a value is outside the declared range;
- a safety threshold is weakened without authorization;
- a referenced device or profile does not exist;
- incompatible versions are combined.
