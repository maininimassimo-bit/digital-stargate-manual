# ADR-004 - Operational Architecture

| Campo | Valore |
|---|---|
| Identificativo | ADR-004 |
| Titolo | Operational Architecture |
| Stato | Accepted |
| Data | 26/07/2026 |
| Ambito | Digital StarGate |
| Decisione | Separazione permanente tra sviluppo e nodo operativo |

## 1. Contesto

Digital StarGate utilizza due ambienti con finalità differenti:

- il PC Principale, destinato allo sviluppo, alla documentazione, alla validazione e alla governance del repository;
- l'EAGLE, installato presso l'osservatorio, destinato esclusivamente alle attività operative e alla produzione dei dati.

La separazione era già applicata nella pratica, ma non era formalizzata come decisione architetturale vincolante.

## 2. Decisione

Viene adottata una separazione permanente dei ruoli.

### 2.1 PC Principale

Il PC Principale è l'unica workstation autorizzata per:

- sviluppo software;
- manutenzione del codice;
- produzione e revisione della documentazione;
- aggiornamento di MkDocs e del Design System;
- sviluppo di Analytics, Dashboard e Portal;
- creazione di branch, pull request, merge e release;
- validazione con `mkdocs build --strict`;
- governance Git e gestione delle baseline documentali.

### 2.2 EAGLE

L'EAGLE è un nodo operativo ed è utilizzato esclusivamente per:

- controllo dell'osservatorio;
- acquisizione astronomica;
- raccolta di telemetria e dati meteorologici;
- generazione di log e report operativi;
- pubblicazione nel repository degli artefatti prodotti dall'osservatorio;
- sincronizzazione in sola ricezione con il branch `main`, salvo i flussi automatici autorizzati per dati e log.

Sull'EAGLE non si effettuano sviluppo software, revisione documentale, gestione di release o modifiche manuali all'architettura del progetto.

## 3. Flusso Git

```text
PC Principale
  sviluppo e documentazione
          |
          v
feature branch -> pull request -> validazione -> merge su main
                                                |
                                                v
                                             EAGLE
                                  sincronizzazione e operatività
                                                |
                                                v
                               log, telemetria e report operativi
```

## 4. Regole operative

1. Ogni modifica applicativa o documentale nasce sul PC Principale o tramite strumenti autorizzati collegati a GitHub.
2. Ogni modifica deve essere isolata in un branch dedicato.
3. Il branch `main` rappresenta lo stato approvato del progetto.
4. L'EAGLE sincronizza il contenuto approvato da `main`.
5. I dati operativi generati dall'EAGLE devono essere separati dal codice e dalla documentazione progettuale.
6. Eventuali automazioni di pubblicazione dall'EAGLE devono essere riproducibili, tracciate e limitate ai percorsi autorizzati.

## 5. Conseguenze

### Benefici

- riduzione del rischio di modifiche accidentali sul nodo operativo;
- maggiore riproducibilità delle release;
- separazione chiara tra engineering e operations;
- tracciabilità delle responsabilità;
- possibilità di ripristinare l'EAGLE a partire da una baseline approvata.

### Vincoli

- le modifiche urgenti non vengono sviluppate direttamente sull'EAGLE;
- ogni correzione segue il normale ciclo branch, validazione e merge;
- il PC Principale rimane il punto di riferimento per l'integrazione.

## 6. Collegamenti

- `docs/architecture/index.md`
- `docs/developer/portal-publication-guidelines.md`
- `docs/releases/documentation-modernization-charter.md`
- `docs/releases/milestone-package-standard.md`

## 7. Decisione finale

La separazione tra PC Principale ed EAGLE è parte integrante dell'architettura di Digital StarGate e deve essere rispettata in tutte le milestone future.