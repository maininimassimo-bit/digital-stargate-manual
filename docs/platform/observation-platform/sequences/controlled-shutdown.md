# Controlled Shutdown Sequence

## Sequence

```mermaid
sequenceDiagram
    participant Orchestrator
    participant NINA
    participant PHD2
    participant Mount
    participant Roof
    participant Safety

    Orchestrator->>NINA: Stop acquisition
    NINA->>PHD2: Stop guiding
    PHD2-->>NINA: GuidingStopped
    NINA-->>Orchestrator: AcquisitionStopped
    Orchestrator->>Mount: Park
    Mount-->>Orchestrator: MountParked
    Orchestrator->>Safety: Confirm closure permitted
    Safety-->>Orchestrator: ClosureAuthorized
    Orchestrator->>Roof: Close
    Roof-->>Orchestrator: RoofClosed
    Orchestrator->>Orchestrator: Complete session and persist evidence
```

## Invariants

- roof closure has precedence over non-essential data operations;
- the mount must be parked or confirmed in a closure-safe position;
- failure to confirm roof closure raises a critical alert;
- telemetry and event evidence remain available after shutdown.
