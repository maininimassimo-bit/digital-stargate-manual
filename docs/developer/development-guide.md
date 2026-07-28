# Guida di sviluppo

## Scopo

Questa guida descrive la fondazione di sviluppo, i contratti canonici e il primo vertical slice introdotti dalla Release 1.5 “Developer Edition”.

## Prerequisiti

- .NET SDK `10.0.302`, selezionato tramite `global.json`;
- Python 3.13 per la documentazione MkDocs;
- Git con supporto ai nomi di file UTF-8.

## Struttura della soluzione

```text
DigitalStarGate.sln
src/
  DigitalStarGate.Api
  DigitalStarGate.Application
  DigitalStarGate.Contracts
  DigitalStarGate.Domain
  DigitalStarGate.Infrastructure
  DigitalStarGate.SharedKernel
tests/
  DigitalStarGate.UnitTests
  DigitalStarGate.IntegrationTests
  DigitalStarGate.ArchitectureTests
contracts/
  openapi/
  events/
infrastructure/
scripts/
tools/
```

## Responsabilità dei progetti

| Progetto | Responsabilità iniziale |
| --- | --- |
| `DigitalStarGate.Api` | Host ASP.NET Core e composizione dell’applicazione |
| `DigitalStarGate.Application` | Casi d’uso, Command, Query e porte applicative |
| `DigitalStarGate.Contracts` | DTO, Command, Query, Event, errori, telemetria e configurazione condivisi |
| `DigitalStarGate.Domain` | Modello di dominio e regole di business |
| `DigitalStarGate.Infrastructure` | Persistenza e integrazioni tecniche |
| `DigitalStarGate.SharedKernel` | Primitive interne condivise prive di dipendenze infrastrutturali |
| `DigitalStarGate.UnitTests` | Test unitari di Domain e Application |
| `DigitalStarGate.IntegrationTests` | Test di integrazione dell’host e delle dipendenze esterne |
| `DigitalStarGate.ArchitectureTests` | Verifica automatica dei confini architetturali |

La direzione delle dipendenze è dall’esterno verso l’interno. `Domain` non deve dipendere da `Application`, `Infrastructure` o `Api`.

## Uso dei contratti

Prima di introdurre un nuovo DTO, Command, Query, Event o identificativo verificare il [catalogo canonico](platform-contracts.md). Un contratto esistente deve essere esteso secondo le regole di versionamento, non duplicato.

Gli artefatti machine-readable sono:

- `contracts/openapi/digital-stargate-v1.yaml`;
- `contracts/events/platform-events.schema.json`.

## Capability implementata

La [Capability 001 – Observation Session](capability-001-observation-session.md) dimostra il primo vertical slice con:

- `CreateObservationSessionHandler`;
- `GetObservationSessionHandler`;
- repository InMemory;
- pubblicazione InMemory di `SessionCreated`;
- endpoint POST e GET;
- health check;
- test unitari, applicativi, di integrazione e architetturali.

## Build

```powershell
dotnet restore DigitalStarGate.sln
dotnet build DigitalStarGate.sln --configuration Release
```

## Test

```powershell
dotnet test DigitalStarGate.sln --configuration Release
```

I test devono verificare comportamento reale. Non devono essere aggiunti test fittizi per aumentare il conteggio.

## Analisi statica e formattazione

```powershell
dotnet format DigitalStarGate.sln --verify-no-changes
```

Le proprietà comuni attivano nullable reference types, implicit usings, analizzatori raccomandati e trattamento dei warning come errori.

## Documentazione

```powershell
python -m pip install --requirement requirements.txt
mkdocs build --strict
```

## Pipeline

La workflow `.github/workflows/developer-foundation.yml` esegue restore, build Release, test, verifica della formattazione e build MkDocs strict.

## Ambito escluso

La Release 1.5 non introduce database reale, Event Bus, N.I.N.A., ASCOM, PHD2, PixInsight, scheduler completo, Kubernetes o alta disponibilità. Queste capability appartengono alla Release 2.0.
