# Runbook — Failed Deployment

## Trigger

Use this runbook when deployment does not complete or post-deployment checks fail.

## Procedure

1. Stop further promotion and place the target environment in a controlled state.
2. Determine whether safety-critical functions are affected.
3. Capture deployment logs, version, configuration and observed health.
4. Execute the approved rollback when service integrity cannot be restored quickly.
5. Verify the previous baseline, monitoring and automation readiness.
6. Open an incident record and identify corrective actions before retrying.
