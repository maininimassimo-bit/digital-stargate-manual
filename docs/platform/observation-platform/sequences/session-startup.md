# Session Startup Sequence

## Preconditions

- session plan is valid;
- observatory runtime is reachable;
- safety state is `SAFE` and fresh;
- roof and mount state are known;
- required device adapters are healthy.

## Sequence

```mermaid
sequenceDiagram
    actor Operator
    participant API
    participant Orchestrator
    participant Safety
    participant Roof
    participant Mount
    participant NINA
    participant PHD2

    Operator->>API: POST /sessions/{id}/commands START
    API->>Orchestrator: StartSession
    Orchestrator->>Safety: EvaluateStartupSafety
    Safety-->>Orchestrator: SAFE
    Orchestrator->>Roof: Open
    Roof-->>Orchestrator: RoofOpened
    Orchestrator->>Mount: Unpark and initialize
    Mount-->>Orchestrator: MountReady
    Orchestrator->>NINA: Start sequence
    NINA->>PHD2: Connect and begin guiding
    PHD2-->>NINA: GuidingStarted
    NINA-->>Orchestrator: AcquisitionStarted
    Orchestrator-->>API: SessionStarted
    API-->>Operator: 202 Accepted
```

## Failure rules

- no opening command is sent when safety is unknown;
- roof-open timeout triggers controlled closure where safe;
- mount initialization failure prevents sequence start;
- every partial startup records compensating actions and evidence.
