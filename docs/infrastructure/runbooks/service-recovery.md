# Runbook — Service Recovery

## Trigger

A required infrastructure or control service is unavailable.

## Procedure

1. identify the failed service and dependencies;
2. assess whether the observatory is in a safe state;
3. collect current logs and status evidence;
4. restart only the affected service where possible;
5. validate device and automation connectivity;
6. run a controlled functional test;
7. return to normal operation only after validation;
8. document the incident and corrective actions.
