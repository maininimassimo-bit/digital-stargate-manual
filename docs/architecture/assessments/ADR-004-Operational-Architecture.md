# ADR-004 – Operational Architecture

## Status
Accepted

# Purpose

Questo ADR definisce la separazione permanente tra la workstation di sviluppo e il nodo operativo EAGLE.

## Principi

- Lo sviluppo avviene esclusivamente sul PC Principale.
- EAGLE è un nodo operativo di produzione.
- EAGLE riceve esclusivamente aggiornamenti dal branch `main`.

# High Level Architecture

```text
                   GitHub Repository
                main / releases / tags
                        ▲
                        │
        ┌───────────────┴───────────────┐
        │                               │
 PC Principale                    EAGLE
 Development                      Operations
```

# Development Workstation

## Mission
Realizzare e mantenere il software Digital StarGate.

## Attività consentite

- sviluppo software
- refactoring
- documentazione
- Design System
- MkDocs
- gestione branch
- merge
- release
- test e validazione

## Attività non consentite

- acquisizione osservativa
- controllo della cupola
- produzione dei log operativi

# EAGLE Operational Node

## Mission
Gestire l'osservatorio in produzione.

## Attività consentite

- pull del branch `main`
- sincronizzazione repository
- esecuzione pipeline operative
- acquisizione dati
- produzione log
- produzione report
- pubblicazione degli artefatti operativi

## Attività non consentite

- sviluppo software
- modifica documentazione
- modifica MkDocs
- creazione branch
- merge
- release

# Git Workflow

```text
feature/* -> review -> main -> GitHub -> EAGLE -> git pull
```

# Responsibilities Matrix

| Attività | PC Principale | EAGLE |
|---|:---:|:---:|
| Sviluppo software | ✓ | |
| Refactoring | ✓ | |
| Documentazione | ✓ | |
| MkDocs | ✓ | |
| Merge | ✓ | |
| Release | ✓ | |
| Pull da GitHub | ✓ | ✓ |
| Build di verifica | ✓ | ✓ |
| Controllo osservatorio | | ✓ |
| Automazione cupola | | ✓ |
| Acquisizione immagini | | ✓ |
| Produzione log | | ✓ |
| Produzione report | | ✓ |
| Pubblicazione artefatti operativi | | ✓ |

# Decision

La separazione tra Development Workstation e Operational Node è una decisione architetturale permanente del progetto Digital StarGate.
