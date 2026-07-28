# Capability 001 – Observation Session

## Scopo

La capability dimostra il primo vertical slice completo di Digital StarGate utilizzando i Contracts canonici della Release 1.5.

## Ambito

Sono implementati esclusivamente:

- creazione di una `ObservationSession`;
- lettura di una `ObservationSession` tramite identificativo;
- persistenza InMemory;
- pubblicazione InMemory dell'Event `SessionCreated`;
- logging strutturato con `CorrelationId`;
- health check dell'host API.

## Endpoint

```text
POST /api/v1/observation-sessions
GET  /api/v1/observation-sessions/{id}
GET  /health
```

Gli endpoint utilizzano `CreateObservationSession`, `GetObservationSession` e `ObservationSessionDto` definiti in `DigitalStarGate.Contracts`.

## Flusso

```text
API
  -> CreateObservationSessionHandler
  -> ObservationSession
  -> IObservationSessionRepository
  -> IPlatformEventPublisher
  -> SessionCreated
```

La lettura usa lo stesso repository InMemory e restituisce il DTO canonico.

## Validazioni

La creazione verifica:

- `ObservationSessionId` non vuoto;
- `TargetId` non vuoto;
- `ObservatoryId` non vuoto;
- identificativo dell'Observation Plan non vuoto;
- data di creazione valorizzata;
- `CorrelationId` non vuoto.

## Limiti

La persistenza e la pubblicazione Event sono intenzionalmente InMemory. Non sono inclusi database, Event Bus, N.I.N.A., ASCOM, PHD2, PixInsight, scheduler o funzioni astronomiche avanzate.
