# Coding Standards

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-CODE-001 |
| Versione | 1.0 |
| Stato | Active |
| Ambito | .NET, JavaScript, CSS, Markdown, contratti e dataset |

## 1. Principi generali

- responsabilità singola e confini espliciti;
- nessuna duplicazione di logica, dati o stili;
- nomi descrittivi e contratti stabili;
- compatibilità retroattiva per contratti pubblici;
- sicurezza, safety, osservabilità e testabilità considerate nel design;
- nessun warning ignorato senza motivazione registrata;
- nessun segreto in codice, documenti, DTO, eventi, dataset o log.

## 2. .NET e architettura

La solution usa .NET 10, C# 14, nullable, warnings come errori, analisi latest-recommended, code style enforced e build deterministica.

Regole di dipendenza:

```text
Api/Presentation -> Application -> Domain
Infrastructure -> Application + Domain
Contracts -> tipi pubblici indipendenti
Domain -> nessun framework o adapter
```

- Domain contiene invarianti, aggregate, value object e domain event.
- Application orchestra use case e definisce port.
- Infrastructure implementa persistence, messaging e adapter esterni.
- API compone dipendenze e traduce HTTP/contract.
- Contracts non espone entity di dominio o tipi di persistenza.
- SharedKernel contiene solo primitive realmente condivise e stabili.

Standard:

- async end-to-end per I/O;
- `CancellationToken` nei boundary asincroni;
- dependency injection esplicita;
- errori applicativi tradotti in Problem Details;
- correlation e causation ID propagati;
- logging strutturato senza dati sensibili;
- test unitari per invarianti, integration test per adapter e architecture test per boundary.

## 3. Eventi e integrazione

Distinguere sempre:

- Domain Event;
- Integration Event versionato;
- Outbox Record;
- Dispatcher;
- Event Bus;
- Projection;
- retry e dead-letter handling.

Non pubblicare direttamente dagli aggregate. Quando l'affidabilità è richiesta, stato e Outbox devono essere persistiti nella stessa transazione.

## 4. JavaScript del portale

- un file per componente o responsabilità;
- IIFE o modulo incapsulato, evitando globali accidentali;
- inizializzazione idempotente;
- supporto `DOMContentLoaded` e `document$.subscribe(...)`;
- selettori stabili `data-dsg-*`;
- event delegation quando appropriato;
- gestione di loading, empty, error e degraded state;
- nessun accesso diretto ai cataloghi scientifici fuori dallo Scientific Data Engine;
- nessuna nuova logica tema in `page-enhancements.js`;
- niente dipendenze da posizione o struttura interna fragile di Material;
- custom event nel namespace `dsg:*` per comunicazione disaccoppiata;
- script inline vietati per nuova logica riusabile.

## 5. CSS e Design System

- file sotto `docs/styles`;
- prefisso classi `dsg-`;
- BEM-like naming per componenti complessi;
- design token e custom property per valori condivisi;
- nessuna regola globale invasiva;
- responsive rule nel file proprietario del componente;
- light/dark mode e contrasto verificati;
- focus visibile;
- stati standard: `is-active`, `is-open`, `is-loading`, `is-empty`, `is-error`, `is-degraded`;
- nessuna informazione affidata solo al colore.

## 6. Markdown e documentazione

Ogni documento governato deve includere, quando applicabile:

- identificativo, versione, stato e data;
- scopo, ambito e dipendenze;
- current state e target state;
- regole, acceptance criteria e open issue;
- riferimenti e traceability;
- registro revisioni.

Convenzioni file:

- minuscolo e trattini per contenuti ordinari;
- maiuscolo e underscore solo per registri governance già standardizzati;
- link relativi;
- Mermaid per diagrammi mantenibili;
- nessuna affermazione di test, build o acceptance senza evidence.

## 7. Contratti e dataset

- Semantic Versioning per OpenAPI, eventi e JSON Schema;
- modifiche breaking richiedono nuova major;
- proprietà additive opzionali richiedono minor;
- correzioni editoriali compatibili richiedono patch;
- dataset di proiezione dichiarano authority, schema version e updatedAt;
- i consumer tollerano proprietà additive sconosciute salvo vincoli safety/security;
- valori unknown, stale o non disponibili non vengono convertiti in valori validi simulati.

## 8. Quality gate

Prima del merge, quando applicabile:

```bash
dotnet restore DigitalStarGate.sln
dotnet build DigitalStarGate.sln --configuration Release --no-restore
dotnet test DigitalStarGate.sln --configuration Release --no-build
dotnet format DigitalStarGate.sln --verify-no-changes --no-restore
mkdocs build --strict
```

Per modifiche UI aggiungere verifica light/dark, desktop/tablet, refresh diretto, Instant Navigation e tastiera.
