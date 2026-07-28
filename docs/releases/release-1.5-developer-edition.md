# Release 1.5 – Developer Edition

## Stato

In preparazione.

## Obiettivo

La Release 1.5 accorpa le precedenti ipotesi di Release 1.2, 1.3 e 1.4 e prepara il passaggio diretto allo sviluppo delle capability della Release 2.0.

## Piano di rilascio

| Pull Request | Ambito | Stato |
| --- | --- | --- |
| PR 1 | Developer Foundation | Base della PR 2 |
| PR 2 | Platform Contracts & Canonical Model | In revisione |
| PR 3 | Observation Session Vertical Slice | Pianificata dopo approvazione PR 2 |

## Manifest PR 1 – Developer Foundation

La prima Pull Request introduce:

- soluzione .NET e progetti iniziali;
- proprietà di compilazione e dipendenze centralizzate;
- progetti di test predisposti senza test fittizi;
- workflow di quality gate;
- guida di sviluppo;
- directory riservate a contratti, infrastruttura, script e strumenti.

## Manifest PR 2 – Platform Contracts & Canonical Model

La seconda Pull Request introduce esclusivamente il linguaggio comune della piattaforma:

- progetto `DigitalStarGate.Contracts`;
- Canonical Information Model e Value Object condivisi;
- cataloghi Command, Query ed Event;
- DTO e contratti API;
- modello Problem Details conforme a RFC 9457;
- contratti di osservabilità e configurazione;
- specifica OpenAPI iniziale;
- JSON Schema degli Event;
- regole di versionamento e compatibilità.

Non introduce handler, persistenza, endpoint eseguibili, autenticazione operativa o integrazioni con dispositivi.

## Changelog PR 1

- aggiunta la soluzione `DigitalStarGate.sln`;
- aggiunti i progetti `Api`, `Application`, `Domain`, `Infrastructure` e `SharedKernel`;
- aggiunti i progetti `UnitTests`, `IntegrationTests` e `ArchitectureTests`;
- aggiunte configurazioni condivise per .NET 10, nullable reference types, implicit usings, analisi statica e warning come errori;
- aggiunta gestione centralizzata delle dipendenze;
- aggiunta pipeline GitHub Actions per build, test, formattazione e MkDocs;
- normalizzata la codifica UTF-8 senza BOM dei file modificati.

## Changelog PR 2

- aggiunto il progetto `DigitalStarGate.Contracts`;
- definiti identificativi tipizzati e Value Object condivisi;
- definito il modello canonico iniziale della piattaforma;
- aggiunti i cataloghi Command, Query ed Event;
- aggiunti contratti per errori, telemetria, configurazione, notifiche e confine AI;
- aggiunta la specifica `contracts/openapi/digital-stargate-v1.yaml`;
- aggiunto lo schema `contracts/events/platform-events.schema.json`;
- pubblicato il documento canonico dei contratti;
- aggiornata la guida di sviluppo e la navigazione MkDocs.

## Tracciabilità

- [Guida di sviluppo](../developer/development-guide.md)
- [Contratti canonici della piattaforma](../developer/platform-contracts.md)
- [Architettura Digital StarGate](../architecture/index.md)
- [Dataset e schema Warehouse](../architecture/warehouse/datasets-and-schema.md)
- [Gestione documentale e release](../chapters/34-gestione-documentale-release.md)
