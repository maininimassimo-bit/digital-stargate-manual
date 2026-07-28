# Automation Architecture

## Componenti logici

```mermaid
flowchart LR
    U[Operator / Schedule] --> S[Scheduler]
    S --> O[Orchestrator]
    O --> G[Safety Gate]
    G --> D[Device Services]
    D --> M[Mount]
    D --> C[Camera]
    D --> F[Focuser]
    D --> R[Dome / Roof]
    D --> W[Weather]
    O --> E[Event Bus]
    O --> T[Telemetry]
    O --> N[Notification]
    O --> RC[Recovery Coordinator]
```

## Responsabilità

- **Scheduler**: seleziona il piano osservativo e la finestra temporale.
- **Orchestrator**: esegue i workflow e mantiene lo stato della sessione.
- **Safety Gate**: autorizza o blocca le transizioni operative.
- **Device Services**: astraggono i singoli apparati.
- **Recovery Coordinator**: gestisce retry, fallback e chiusura sicura.
- **Event Bus**: pubblica gli eventi di dominio.
- **Telemetry**: registra metriche, log e health state.
