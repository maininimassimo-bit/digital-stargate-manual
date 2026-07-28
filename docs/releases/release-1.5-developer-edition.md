# Release 1.5 – Developer Edition

## Stato

In preparazione.

## Obiettivo

La Release 1.5 accorpa le precedenti ipotesi di Release 1.2, 1.3 e 1.4 e prepara il passaggio diretto allo sviluppo delle capability della Release 2.0.

## Piano di rilascio

| Pull Request | Ambito | Stato |
| --- | --- | --- |
| PR 1 | Developer Foundation | In revisione |
| PR 2 | Platform Contracts | Pianificata dopo approvazione PR 1 |
| PR 3 | Observation Session Vertical Slice | Pianificata dopo approvazione PR 2 |

## Manifest PR 1 – Developer Foundation

La prima Pull Request introduce esclusivamente:

- soluzione .NET e progetti iniziali;
- proprietà di compilazione e dipendenze centralizzate;
- progetti di test predisposti senza test fittizi;
- workflow di quality gate;
- guida di sviluppo;
- directory riservate a contratti, infrastruttura, script e strumenti.

Non introduce contratti applicativi, persistenza, autenticazione, osservabilità applicativa o capability di dominio.

## Changelog PR 1

- aggiunta la soluzione `DigitalStarGate.sln`;
- aggiunti i progetti `Api`, `Application`, `Domain`, `Infrastructure` e `SharedKernel`;
- aggiunti i progetti `UnitTests`, `IntegrationTests` e `ArchitectureTests`;
- aggiunte configurazioni condivise per .NET 10, nullable reference types, implicit usings, analisi statica e warning come errori;
- aggiunta gestione centralizzata delle dipendenze;
- aggiunta pipeline GitHub Actions per build, test, formattazione e MkDocs;
- normalizzata la codifica UTF-8 senza BOM dei file modificati.

## Tracciabilità

- [Guida di sviluppo](../developer/development-guide.md)
- [Architettura Digital StarGate](../architecture/index.md)
- [Gestione documentale e release](../chapters/34-gestione-documentale-release.md)
