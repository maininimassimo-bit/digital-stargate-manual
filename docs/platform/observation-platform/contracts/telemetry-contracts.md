# Telemetry Contracts

## 1. Purpose

Telemetry exposes current measurements and operational evidence without replacing authoritative domain state.

## 2. Measurement structure

```json
{
  "metric": "weather.wind.speed",
  "value": 4.8,
  "unit": "m/s",
  "quality": "GOOD",
  "observedAt": "2026-07-28T20:30:00Z",
  "source": "weather-station-01",
  "correlationId": "2b5cc205-7576-43c0-843f-fd6d3242cf6c"
}
```

## 3. Quality values

- `GOOD` — valid and within freshness threshold;
- `STALE` — last known value exceeded freshness threshold;
- `SUSPECT` — validation or range check failed;
- `MISSING` — no usable measurement;
- `ERROR` — source reported a failure.

## 4. Initial metric namespaces

| Namespace | Examples |
|---|---|
| `weather.*` | temperature, humidity, wind.speed, rain.detected |
| `safety.*` | state, lastEvaluationAge |
| `mount.*` | connected, parked, tracking, rightAscension, declination |
| `roof.*` | state, openSensor, closedSensor |
| `camera.*` | temperature, coolerPower, exposureState |
| `guiding.*` | rmsTotal, rmsRa, rmsDec, starLost |
| `runtime.*` | cpu, memory, diskFree, serviceHealth |

## 5. Freshness

Each metric definition must declare its maximum age. A consumer must not interpret stale weather or safety telemetry as safe.

## 6. Health contract

Health states are:

- `HEALTHY`;
- `DEGRADED`;
- `UNHEALTHY`;
- `UNKNOWN`.

Aggregate health must preserve the failing dependency list rather than returning a single opaque status.
