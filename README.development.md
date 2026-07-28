# Sviluppo Digital StarGate

La Release 1.5 introduce la fondazione .NET della piattaforma senza implementare capability applicative.

## Prerequisiti

- .NET SDK definito in `global.json`;
- Python 3.13;
- dipendenze Python definite in `requirements.txt`.

## Verifica completa

```powershell
dotnet restore DigitalStarGate.sln
dotnet build DigitalStarGate.sln --configuration Release
dotnet test DigitalStarGate.sln --configuration Release
dotnet format DigitalStarGate.sln --verify-no-changes
python -m pip install --requirement requirements.txt
mkdocs build --strict
```

La struttura della soluzione e le regole di dipendenza sono descritte nella [guida di sviluppo](docs/developer/development-guide.md).
