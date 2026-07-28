# Guida di sviluppo

## Scopo

Questa guida descrive la fondazione di sviluppo e i contratti canonici introdotti dalla Release 1.5 “Developer Edition”. Le prime due Pull Request preparano compilazione, test, analisi statica e linguaggio comune senza introdurre logica applicativa.

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

La direzione delle dipendenze è dall’esterno verso l’interno. `Domain` non deve dipendere da `Application`, `Infrastructure` o `Api`. I contratti pubblici e inter-processo appartengono a `DigitalStarGate.Contracts`; le primitive strettamente interne restano in `SharedKernel`.

## Uso dei contratti

Prima di introdurre un nuovo DTO, Command, Query, Event o identificativo verificare il [catalogo canonico](platform-contracts.md). Un contratto esistente deve essere esteso secondo le regole di versionamento, non duplicato in un altro progetto.

Gli artefatti machine-readable sono:

- `contracts/openapi/digital-stargate-v1.yaml`;
- `contracts/events/platform-events.schema.json`.

## Build

```powershell
dotnet restore DigitalStarGate.sln
dotnet build DigitalStarGate.sln --configuration Release
```

## Test

```powershell
dotnet test DigitalStarGate.sln --configuration Release
```

I progetti di test sono inizialmente vuoti. I test reali saranno introdotti insieme alle capability, evitando test fittizi creati solo per aumentare il conteggio.

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

Le PR 1 e 2 non includono persistenza, handler applicativi, autenticazione operativa, health check eseguibili o vertical slice. Questi elementi sono riservati alla PR 3 della Release 1.5 o alla Release 2.0.
