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