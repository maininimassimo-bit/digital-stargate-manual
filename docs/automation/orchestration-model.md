# Orchestration Model

## Stati principali della sessione

```text
Planned
  ↓
Validating
  ↓
Starting
  ↓
Ready
  ↓
Acquiring
  ↓
Paused / Recovering
  ↓
ShuttingDown
  ↓
Completed | Aborted | Failed
```

## Regole

- Una sessione entra in `Starting` solo dopo validazione meteo, safety e disponibilità apparati.
- Una condizione unsafe ha priorità su qualsiasi workflow in corso.
- `Paused` è reversibile; `Aborted` è terminale.
- Tutte le transizioni devono produrre un evento e aggiornare la telemetria.
