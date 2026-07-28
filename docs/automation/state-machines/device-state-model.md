# Device State Model

## Stati comuni

```text
Unknown
Disconnected
Connecting
Ready
Busy
Degraded
Faulted
Recovering
Safe
```

## Vincoli

- `Busy` richiede una connessione valida.
- `Faulted` deve produrre un errore strutturato.
- `Recovering` deve avere timeout e risultato esplicito.
- `Safe` rappresenta la condizione fisica compatibile con lo shutdown.
