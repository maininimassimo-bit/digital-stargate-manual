# BKL-042 bounded read-only AI relay

This is a separate server-side adapter for the future BKL-042 AI pilot. It is
not the telemetry relay and it is not a command, scheduler, broker, remediation
or Safety Authority component.

The relay is fail-closed by default. It requires all of the following at
runtime before making an external request:

- `BKL042_RUNTIME_ENABLED=true`;
- `OPENAI_API_KEY` injected from a secret manager, never from the browser or repository;
- `BKL042_QUOTA_LEDGER_PATH` pointing to a persistent quota ledger.

The pilot limit defaults to 100 requests. The intended usage mix is 80% Luna
triage, 18% Sol consultative analysis, and 2% Astra escalation, selected by the
explicit bounded mode. Tools, actions, command authority, safety authority and
runtime event publication are disabled.

No deployment is included in this change. Deployment requires a separately
approved Secret Manager binding and runtime readiness gate.
