# DSG-ASMT-001 - Enterprise Assessment

| Campo | Valore |
|---|---|
| Documento | Enterprise Assessment |
| Identificativo | `DSG-ASMT-001` |
| Roadmap | `DSG-MR-001` |
| Versione | 1.0 |
| Stato | Approvata per revisione |
| Owner | Massimo Mainini |
| Data baseline | 26/07/2026 |

## 1. Scopo

L'assessment valuta la maturità della baseline enterprise `DSG-MR-001` rispetto a completezza documentale, architettura, rischi, governance, operatività, dati e release readiness.

## 2. Metodo di scoring

Ogni area è valutata da 0 a 5.

| Punteggio | Significato |
|---:|---|
| 0 | Non presente |
| 1 | Presente in forma frammentaria |
| 2 | Presente ma non governato |
| 3 | Adeguato per uso operativo |
| 4 | Maturo e tracciabile |
| 5 | Baseline completa, verificabile e mantenibile |

## 3. Risultati

| Area | Score | Evidenza | Valutazione |
|---|---:|---|---|
| Roadmap | 5 | `DSG-MR-001` con milestone e deliverable | Completa |
| Architettura | 4 | `DSG-EA-001`, ADR e componenti | Matura |
| Rischi | 4 | DSRA con rischi e controlli | Matura |
| Registri | 5 | Requisiti, rischi, controlli, deliverable, change log | Completa |
| Operatività | 4 | SOP con trigger, ruoli e criteri | Matura |
| Governance | 4 | RACI, quality gate e change management | Matura |
| Release | 4 | Readiness e rollback definiti | Matura |
| Appendici | 4 | Glossario, mapping e template | Matura |

Score medio:

```text
4,25 / 5
```

## 4. Gap e raccomandazioni

| ID | Gap | Impatto | Raccomandazione | Priorità |
|---|---|---|---|---|
| `DSG-GAP-001` | Alcune evidenze operative dipendono da esecuzioni future | Medio | Collegare checklist reali dopo le prossime sessioni | Media |
| `DSG-GAP-002` | I controlli di rete e failover richiedono prove periodiche formalizzate | Medio | Pianificare registro test rete | Media |
| `DSG-GAP-003` | La qualità dati richiede schemi versionati continuativi | Alto | Mantenere schema warehouse e quality gate | Alta |
| `DSG-GAP-004` | Le ADR precedenti sono in sezione architettura, non nella sezione enterprise | Basso | Mantenere cross-reference nel registro decisioni | Bassa |

## 5. Checklist di assessment

| Controllo | Esito |
|---|---|
| Roadmap pubblicata | Conforme |
| Sezione MkDocs dedicata | Conforme |
| Registri minimi presenti | Conforme |
| Rischi con controlli | Conforme |
| SOP con trigger e output | Conforme |
| Governance con ruoli | Conforme |
| Release readiness definita | Conforme |
| Marcatori aperti | Conforme, nessun marcatore operativo aperto |

## 6. Criteri di accettazione

La baseline `DSG-MR-001` è idonea alla review quando:

- score medio almeno pari a 4;
- nessun gap critico aperto;
- ogni deliverable minimo è raggiungibile;
- i follow-up sono classificati come non bloccanti.

## 7. Conclusione

La baseline enterprise `DSG-MR-001` è valutata:

```text
IDONEA ALLA REVIEW
```

Il lavoro residuo riguarda l'accumulo di evidenze operative reali nelle release successive, non il completamento della struttura documentale richiesta.
