# Architettura Digital StarGate

## Scopo

Digital StarGate è una piattaforma per la gestione, il monitoraggio, la documentazione e l’analisi dell’osservatorio astronomico.

La piattaforma integra:

- acquisizione dei dati operativi;
- analisi delle sessioni osservative;
- monitoraggio meteorologico;
- stato dell’osservatorio;
- dashboard e indicatori;
- documentazione tecnica;
- pubblicazione automatica del portale.

La Release 4.0 introduce un’architettura centralizzata nella quale GitHub costituisce la sorgente principale del progetto e `build_all.py` rappresenta l’orchestratore della generazione del portale.

---

## Principi architetturali

L’architettura segue questi principi:

1. Il repository GitHub è la sorgente ufficiale del codice e dei dati versionati.
2. Il PC principale viene utilizzato per lo sviluppo e la manutenzione.
3. L’EAGLE raccoglie e pubblica i dati prodotti dall’osservatorio.
4. GitHub Actions esegue analisi, validazioni e pubblicazione.
5. GitHub Pages distribuisce il portale Digital StarGate.
6. I contenuti generati devono essere riproducibili a partire dai dati presenti nel repository.
7. I moduli devono essere indipendenti e coordinati da un orchestratore centrale.

---

## Architettura generale

```text
                         DIGITAL STAR GATE

                  +-----------------------------+
                  |      Repository GitHub      |
                  |   codice, dati e documenti  |
                  +-------------+---------------+
                                |
               +----------------+----------------+
               |                                 |
               v                                 v
    +----------------------+          +----------------------+
    |    PC principale     |          |        EAGLE         |
    |                      |          |                      |
    | sviluppo             |          | acquisizione dati   |
    | test                 |          | meteo                |
    | nuove funzionalità   |          | sessioni             |
    | manutenzione         |          | stato osservatorio   |
    +----------+-----------+          +----------+-----------+
               |                                 |
               +----------------+----------------+
                                |
                                v
                  +-----------------------------+
                  |       GitHub Actions        |
                  |                             |
                  | analisi                     |
                  | validazione                 |
                  | build_all.py                |
                  | MkDocs                      |
                  +-------------+---------------+
                                |
                                v
                  +-----------------------------+
                  |        GitHub Pages         |
                  |                             |
                  | homepage                    |
                  | dashboard                   |
                  | stato osservatorio          |
                  | analytics                   |
                  | manuale tecnico             |
                  +-----------------------------+
```

---

## Governance architetturale

La baseline enterprise è governata dagli assessment, dalle review indipendenti e dai certificate presenti in `architecture/assessments/`.

AP-001 introduce gli artefatti canonici seguenti:

- [AP-001 — Enterprise Metamodel and Repository Information Architecture](packages/AP-001-Enterprise-Metamodel-and-Repository-Information-Architecture.md)
- [Enterprise Metamodel](enterprise-metamodel.md)
- [Architecture Traceability Register](traceability-register.md)

Questi documenti definiscono vocabolario, relazioni, stati, metadati e tracciabilità. Il loro stato è **Proposed for independent ARB review** e non costituisce certificazione runtime.

## AP-013 — Scientific Image Repository

AP-013 è attivo in modalità **limited automated pilot**. La baseline tecnica pubblicata comprende architettura, modello dati, contratti, session importer, evidenze di discovery e gate di readiness del trasferimento.

### Package e modelli

- [AP-013 — Scientific Image Repository Architecture](packages/AP-013-Scientific-Image-Repository-Architecture.md)
- [AP13-W02 — Current-State Scientific Asset Inventory Specification](scientific-assets/AP13-W02-Current-State-Scientific-Asset-Inventory-Specification.md)
- [DSDM-001 — Scientific Data Manager Conceptual Model](scientific-assets/DSDM-001-Scientific-Data-Manager-Conceptual-Model.md)
- [DSDM-002 — Scientific Data Manager Logical Data Model](scientific-assets/DSDM-002-Scientific-Data-Manager-Logical-Data-Model.md)
- [DSDM-003 — Contract and Manifest Model](scientific-assets/DSDM-003-Contract-and-Manifest-Model.md)
- [DSDM-004 — Session Importer Architecture and Safe Transfer Design](scientific-assets/DSDM-004-Session-Importer-Architecture-and-Safe-Transfer-Design.md)

### Evidenze e readiness

- [E-AP13-W02-01 — Source Authorization and Scope Record](scientific-assets/evidence/AP13-W02/E-AP13-W02-01-Source-Authorization-and-Scope-Record.md)
- [AP-013 — Session Discovery Execution Evidence](validation/AP-013-Session-Discovery-Execution-Evidence.md)
- [AP-013 — Transfer Readiness Gate](validation/AP-013-Transfer-Readiness-Gate.md)

### Stato operativo verificato al 4 agosto 2026

- discovery eseguita su **203 file** e **11 sessioni**;
- **203 file parsed**, zero ambiguous e zero failed;
- motore `COPY_ONLY` e primitive di trasferimento verificati con test automatici;
- pilot reale limitato a un file con verifica SHA-256;
- launcher protetto e attività pianificata giornaliera alle 07:30;
- massimo **1 file per esecuzione** durante il pilot;
- overwrite, bulk transfer e cancellazione della sorgente non autorizzati;
- prima esecuzione unattended ancora richiesta come evidenza operativa.

## Canonical data flow

La rappresentazione autorevole definita da PAA-002 preserva il flusso:

```text
Sorgenti → Ingestion / Collection → Analytics → Dataset validati → Warehouse → Dashboard / Reporting / AI
```

Dashboard, Reporting e AI non devono introdurre pipeline parallele non governate dai log grezzi.

## Safety boundary

Gli interblocchi fisici e locali restano indipendenti dal software applicativo, dalla rete, dal portale, dal cloud e dall’AI. Monitoring e safety non sono equivalenti e uno stato sconosciuto o stale non può essere interpretato come sicuro.
