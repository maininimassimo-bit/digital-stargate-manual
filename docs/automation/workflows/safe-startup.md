# AUTO-002 — Safe Startup

## Sequenza

```mermaid
sequenceDiagram
    participant S as Scheduler
    participant O as Orchestrator
    participant W as Weather/Safety
    participant D as Dome
    participant M as Mount
    participant C as Camera

    S->>O: StartSession
    O->>W: ValidateSafeState
    W-->>O: Safe
    O->>D: Open
    D-->>O: OpenConfirmed
    O->>M: ConnectAndUnpark
    M-->>O: Ready
    O->>C: ConnectAndCool
    C-->>O: Ready
    O-->>S: SessionReady
```

## Failure handling

- meteo unsafe: sessione non avviata;
- cupola non aperta: abort e notifica;
- montatura non disponibile: chiusura controllata;
- camera non raffreddata: retry limitato o prosecuzione secondo policy.
