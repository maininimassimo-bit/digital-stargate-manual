# Runbook — Pipeline Failure

## Trigger

Use this runbook when a CI/CD job fails or produces incomplete evidence.

## Procedure

1. Identify the first failing stage and preserve logs.
2. Confirm whether the failure is deterministic by rerunning only when the cause may be transient.
3. Check dependency availability, runner capacity, credentials and environment changes.
4. Reproduce locally or in an isolated validation environment.
5. Correct the underlying issue; do not disable mandatory gates without approval.
6. Re-run the complete required pipeline.
7. Record recurring failures as engineering debt or an incident where appropriate.
