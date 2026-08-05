# ANA-PIPE-001 — Analytics Data Pipeline Reference

| Campo | Valore |
|---|---|
| Identificativo | ANA-PIPE-001 |
| Package | AP-011 |
| Stato | Proposed for review |
| Data | 30/07/2026 |

## Pipeline stages

1. **Receive** — acquisizione con source, event time, ingestion time, checksum e contract version.
2. **Validate** — schema, type, range, required fields e referential checks.
3. **Classify** — data class, domain, owner, retention e safety relevance.
4. **Quarantine** — separazione dei record non conformi senza perdita silenziosa.
5. **Transform** — conversioni deterministiche e versionate.
6. **Curate** — pubblicazione dei data product governati.
7. **Serve** — semantic view, API, dashboard o export.
8. **Observe** — metriche, log, lineage, freshness e alert.

## Processing rules

- reprocessing deve essere idempotente o dichiarare chiaramente gli effetti;
- input e output sono collegati da lineage;
- le unità di misura sono esplicite;
- timezone e timestamp semantics sono dichiarati;
- `null`, `unknown`, `not_applicable` e valore zero non sono equivalenti;
- record tardivi e fuori ordine seguono una policy documentata;
- errori non recuperabili entrano in quarantine con owner e runbook;
- nessuna trasformazione inventa osservazioni mancanti.

## Quality gate contract

```yaml
quality_gate_id: string
dataset_id: string
contract_version: string
rules: []
input_count: integer
passed_count: integer
warning_count: integer
failed_count: integer
quarantined_count: integer
coverage_start: timestamp
coverage_end: timestamp
executed_at: timestamp
result: passed|warning|failed|unknown
evidence_uri: string
```

## Replay and rebuild

Il replay richiede autorizzazione, scope, input locator, versioni di codice/configurazione, expected output, capacity check e audit. Il rebuild non sovrascrive evidenza precedente senza versioning.

## Failure modes

- source unavailable;
- schema mismatch;
- duplicate delivery;
- late or out-of-order data;
- partial file;
- checksum mismatch;
- storage saturation;
- orchestration timeout;
- reference-data mismatch;
- publication failure.

Per ogni failure mode sono richiesti detection, bounded retry, quarantine o rollback, owner e recovery evidence.

## Validation checklist

- valid, invalid, duplicate, missing e late records;
- deterministic rebuild;
- quarantine visibility;
- freshness propagation;
- lineage completeness;
- capacity and back-pressure;
- restore and reprocessing.