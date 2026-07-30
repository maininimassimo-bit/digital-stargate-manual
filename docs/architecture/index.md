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

## Canonical data flow

La rappresentazione autorevole definita da PAA-002 preserva il flusso:

```text
Sorgenti → Ingestion / Collection → Analytics → Dataset validati → Warehouse → Dashboard / Reporting / AI
```

Dashboard, Reporting e AI non devono introdurre pipeline parallele non governate dai log grezzi.

## Safety boundary

Gli interblocchi fisici e locali restano indipendenti dal software applicativo, dalla rete, dal portale, dal cloud e dall’AI. Monitoring e safety non sono equivalenti e uno stato sconosciuto o stale non può essere interpretato come sicuro.