# Guida di sviluppo

## Scopo

Questa guida descrive la fondazione di sviluppo introdotta dalla Release 1.5 “Developer Edition”. La PR 1 prepara compilazione, test, analisi statica e pubblicazione documentale senza introdurre logica applicativa.

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
  DigitalStarGate.Domain
  DigitalStarGate.Infrastructure
  DigitalStarGate.SharedKernel
tests/
  DigitalStarGate.UnitTests
  DigitalStarGate.IntegrationTests
  DigitalStarGate.ArchitectureTests
contracts/
infrastructure/
scripts/
tools/
```

## Responsabilità dei progetti

| Progetto | Responsabilità iniziale |
| --- | --- |
| `DigitalStarGate.Api` | Host ASP.NET Core e composizione dell’applicazione |
| `DigitalStarGate.Application` | Casi d’uso, command, query e porte applicative |
| `DigitalStarGate.Domain` | Modello di dominio e regole di business |
| `DigitalStarGate.Infrastructure` | Persistenza e integrazioni tecniche |
| `DigitalStarGate.SharedKernel` | Primitive condivise prive di dipendenze infrastrutturali |
| `DigitalStarGate.UnitTests` | Test unitari di Domain e Application |
| `DigitalStarGate.IntegrationTests` | Test di integrazione dell’host e delle dipendenze esterne |
| `DigitalStarGate.ArchitectureTests` | Verifica automatica dei confini architetturali |

La direzione delle dipendenze è dall’esterno verso l’interno. `Domain` non deve dipendere da `Application`, `Infrastructure` o `Api`.

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

Questa fondazione non include contratti API, persistenza, autenticazione, health check, osservabilità applicativa o vertical slice. Tali elementi sono riservati alle PR 2 e 3 della Release 1.5.
