# Contratti canonici della piattaforma

## Stato

Versione iniziale `1.0.0`, proposta dalla Release 1.5.

## Scopo

Questo documento definisce il linguaggio comune usato dai componenti Digital StarGate. Il progetto `DigitalStarGate.Contracts` e gli artefatti nella directory `contracts/` sono le rappresentazioni machine-readable canoniche.

Non introduce logica applicativa, persistenza o integrazioni operative.

## Relazione con i contratti esistenti

Gli schemi Analytics e Warehouse già pubblicati descrivono dataset operativi e storici. Non vengono sostituiti. Il Canonical Information Model definisce invece concetti condivisi tra API, servizi, eventi e future capability della Release 2.0.

## Canonical Information Model

| Concetto | Responsabilità canonica |
| --- | --- |
| `ObservationSession` | ciclo di vita di una sessione astronomica |
| `Target` | oggetto astronomico e coordinate |
| `Equipment` | componente tecnico generico |
| `Observatory` | sito osservativo e riferimento temporale |
| `Camera` | camera scientifica o di guida |
| `Mount` | montatura e stato di parcheggio |
| `FilterWheel` | ruota portafiltri e filtri disponibili |
| `ImageFrame` | posa scientifica acquisita |
| `CalibrationFrame` | frame di calibrazione |
| `WeatherSnapshot` | condizioni meteorologiche puntuali |
| `TelemetrySample` | misura tecnica con unità e sorgente |
| `ObservationPlan` | piano di osservazione dichiarativo |
| `SafetyStatus` | valutazione della sicurezza operativa |
| `User` | identità applicativa |
| `Role` | insieme di permessi |
| `Permission` | autorizzazione atomica |
| `Notification` | comunicazione indirizzata a uno o più utenti |
| `Alert` | anomalia o condizione che richiede attenzione |
| `SystemConfiguration` | valore di configurazione e relativa provenienza |

## Value Object

Gli identificativi sono tipizzati e non intercambiabili. Le unità sono espresse nel nome della proprietà o nel relativo Value Object.

Identificativi iniziali:

- `ObservationSessionId`;
- `EquipmentId`;
- `TargetId`;
- `ImageId`;
- `ObservatoryId`;
- `UserId`;
- `AlertId`;
- `NotificationId`;
- `CorrelationId`;
- `CausationId`.

Value Object quantitativi e astronomici:

- `Coordinates`;
- `ExposureTime`;
- `Gain`;
- `Offset`;
- `Temperature`;
- `Humidity`;
- `WindSpeed`;
- `SkyQuality`;
- `RightAscension`;
- `Declination`.

## Catalogo Command

| Command | Finalità |
| --- | --- |
| `CreateObservationSession` | richiede la creazione di una sessione |
| `StartObservationSession` | richiede l’avvio di una sessione |
| `AbortObservationSession` | richiede l’interruzione motivata |
| `ParkMount` | richiede il parcheggio della montatura |
| `OpenRoof` | richiede l’apertura del tetto |
| `CloseRoof` | richiede la chiusura del tetto |
| `AcquireTarget` | richiede il puntamento e l’acquisizione del target |
| `StartExposure` | richiede l’avvio di una posa |
| `CalibrateFrames` | richiede la calibrazione dei frame |
| `PublishObservation` | richiede la pubblicazione di un’osservazione |

Un Command esprime intenzione e non garantisce il completamento dell’operazione.

## Catalogo Query

| Query | Risultato atteso |
| --- | --- |
| `GetObservationSession` | sessione identificata |
| `SearchObservationSessions` | elenco paginato e filtrato |
| `GetEquipmentStatus` | stato corrente del componente |
| `GetWeather` | snapshot meteorologico |
| `GetTelemetry` | campioni nel periodo richiesto |

## Catalogo Event

Tutti gli Event usano versione `1.0.0`, `CorrelationId`, `CausationId` opzionale e schema comune `contracts/events/platform-events.schema.json`.

| Event | Payload minimo | Producer | Consumer iniziali | Compatibilità |
| --- | --- | --- | --- | --- |
| `SessionCreated` | sessione, target, osservatorio | session service | API, analytics, audit | additiva nella major 1 |
| `SessionStarted` | sessione | session service | orchestrator, analytics | additiva nella major 1 |
| `SessionCompleted` | sessione | session service | analytics, publication | additiva nella major 1 |
| `SessionAborted` | sessione, motivo | session service | safety, alerting, analytics | additiva nella major 1 |
| `TargetAcquired` | sessione, target | acquisition service | session service, telemetry | additiva nella major 1 |
| `ExposureStarted` | sessione, durata | acquisition service | telemetry, analytics | additiva nella major 1 |
| `ExposureCompleted` | sessione, immagine | acquisition service | storage, analytics | additiva nella major 1 |
| `CalibrationCompleted` | sessione, immagini | calibration service | analytics, storage | additiva nella major 1 |
| `WeatherUnsafeDetected` | osservatorio, motivo | weather service | safety, alerting | additiva nella major 1 |
| `RoofOpened` | tetto | roof controller | safety, telemetry | additiva nella major 1 |
| `RoofClosed` | tetto | roof controller | safety, telemetry | additiva nella major 1 |
| `MountParked` | montatura | mount controller | safety, telemetry | additiva nella major 1 |
| `TelemetryCollected` | sorgente, metrica, valore, unità | ogni componente autorizzato | telemetry store, monitoring | additiva nella major 1 |
| `AlertRaised` | alert, severità, codice, messaggio | alerting service | notification, operations | additiva nella major 1 |
| `ConfigurationChanged` | sezione, chiave, sorgente | configuration service | audit, affected services | additiva nella major 1 |

## OpenAPI e Problem Details

La specifica iniziale è `contracts/openapi/digital-stargate-v1.yaml` e usa OpenAPI `3.1.0`.

Il modello di errore segue RFC 9457 e aggiunge:

- `errorCode` stabile;
- categoria `Validation`, `Business`, `Infrastructure` o `Security`;
- `correlationId`;
- elenco opzionale di `ValidationError`.

Gli endpoint sono versionati nel percorso `/api/v1`. Le modifiche incompatibili richiedono una nuova major version dell’API.

## Osservabilità

Ogni operazione distribuita propaga:

- `CorrelationId`, per la correlazione end-to-end;
- `CausationId`, per collegare causa ed effetto;
- `TraceId` e `SpanId`, quando è disponibile OpenTelemetry.

Convenzioni iniziali:

- `service.namespace`: `digital-stargate`;
- `service.name`: nome stabile del componente in kebab-case;
- `ActivitySource`: `DigitalStarGate.<Component>`;
- `Meter`: `DigitalStarGate.<Component>`;
- nomi Event: PascalCase per i contratti e forma gerarchica per i log strutturati.

## Configurazione

La gerarchia è ordinata dal livello meno specifico al più specifico:

1. valori predefiniti versionati;
2. file di configurazione dell’ambiente;
3. environment variables;
4. provider di secret;
5. override operativi espliciti.

I secret sono rappresentati solo tramite `SecretReference`. Nessun valore segreto deve transitare nei DTO, negli Event o nei log.

## Versionamento

- OpenAPI, DTO, Event e JSON Schema adottano Semantic Versioning.
- Una modifica additiva e opzionale incrementa la minor version.
- Una correzione editoriale o una restrizione non osservabile incrementa la patch version.
- Rimozioni, rinomine o cambi di significato richiedono una nuova major version.
- I producer devono tollerare consumer della stessa major version.
- I consumer devono ignorare proprietà additive sconosciute, salvo vincoli di sicurezza.

## Tracciabilità

- [Guida di sviluppo](development-guide.md)
- [Release 1.5 – Developer Edition](../releases/release-1.5-developer-edition.md)
- [Dataset e schema Warehouse](../architecture/warehouse/datasets-and-schema.md)
- [ADR-002 – Analytics Quality Gates](../architecture/ADR-002-Analytics-Quality-Gates.md)
