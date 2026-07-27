# SOP - Validate Weather State

| Campo | Valore |
|---|---|
| SOP | Validate Weather State |
| Capability | `CAP-WEA-001` |
| Stato | Baseline |
| Scope | Validation of weather evidence and state |

## Purpose

Define the procedure for validating weather evidence before it is used for schedule or session decisions.

## Preconditions

- Weather evidence has been collected or source outage has been detected.
- Applicable threshold or qualitative rule reference is known, or marked OPEN for review.

## Procedure

| Step | Action | Expected Evidence |
|---|---|---|
| 1 | Confirm source identity and Equipment Registry reference if available. | Source reference. |
| 2 | Confirm timestamp and freshness. | Fresh/stale indicator. |
| 3 | Check completeness of required weather dimensions. | Completeness result. |
| 4 | Check consistency between sources if more than one source exists. | Conflict result. |
| 5 | Evaluate conditions against governed threshold/rule references. | Threshold evaluation. |
| 6 | Assign operational assessment and confidence. | Assessment record. |
| 7 | Produce Safety Decision: SAFE, CAUTION, UNSAFE or UNKNOWN. | Decision record. |
| 8 | Publish or escalate based on decision. | Published snapshot or alert. |

## Validation Rules

| Condition | Result |
|---|---|
| Evidence fresh and coherent | Continue to operational assessment. |
| Evidence stale | Mark stale and produce `UNKNOWN` or `CAUTION` according to governance. |
| Evidence unavailable | Produce `UNKNOWN` and initiate recovery. |
| Evidence conflicting | Produce `CAUTION` or `UNKNOWN`; invoke conflict runbook. |
| Unsafe threshold breached | Produce `UNSAFE` and initiate suspend/prevent procedure. |

## Outputs

- Validation result.
- Operational Assessment.
- Safety Decision.
- Weather Alert when required.

## Related Documents

- `docs/capabilities/weather-monitoring/adr/WEA-ADR-001-authoritative-weather-state.md`
- `docs/capabilities/weather-monitoring/adr/WEA-ADR-002-operational-safety-thresholds.md`
- `docs/capabilities/weather-monitoring/runbooks/conflicting-weather-data.md`
