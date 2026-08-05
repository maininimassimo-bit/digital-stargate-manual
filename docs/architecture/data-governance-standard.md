# Digital StarGate Enterprise Data Governance Standard

| Campo | Valore |
|---|---|
| Documento | Enterprise Data Governance Standard |
| Package | AP-002 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Data | 30/07/2026 |
| Stato | Proposed for independent ARB review |
| Owner proposto | Digital StarGate Data Governance Owner |

## 1. Autorità e applicabilità

Questo standard governa nuovi data product, dataset, API, DTO, Event, JSON Schema, metadata e trasformazioni di Digital StarGate. Gli schema eseguibili e il codice restano autorevoli per la forma implementata; questo standard governa ownership, lifecycle, qualità, compatibilità e decisioni.

## 2. Ruoli

- **Data Governance Owner:** mantiene lo standard e approva eccezioni.
- **Data Product Owner:** risponde di finalità, consumer, qualità e lifecycle.
- **Data Steward:** mantiene schema, glossary, metadata, lineage e issue.
- **Producer Owner:** garantisce conformità del dato prodotto.
- **Consumer Owner:** verifica compatibilità e uso conforme.
- **Release Authority:** accetta evidenze e rischi residui.
- **ARB:** esegue review indipendente dei cambiamenti architetturali o incompatibili.

Autore e reviewer ARB devono essere distinti.

## 3. Data product record minimo

Ogni data product deve registrare:

```text
identifier
name
purpose
classification
owner
steward
producer
consumers
authoritative_contract
schema_version
grain
keys
timezone
units
null_semantics
quality_rules
lineage
retention_rule
compatibility_policy
evidence_locators
status
```

## 4. Catalogo iniziale dei data product

| ID candidato | Data product | Grain documentato/proposto | Contratto autorevole | Owner proposto | Stato |
|---|---|---|---|---|---|
| DP-001 | `sessions.parquet` | una riga per sessione consolidata | schema eseguibile Warehouse | Warehouse Data Product Owner | Candidate baseline |
| DP-002 | `targets.parquet` | deve essere dichiarato nello schema; possibili sessione-target-filtro/configurazione | schema eseguibile Warehouse | Warehouse Data Product Owner | Candidate baseline |
| DP-003 | `equipment.parquet` | configurazione strumentale normalizzata e aggregata | schema eseguibile Warehouse | Warehouse Data Product Owner | Candidate baseline |
| DP-004 | `quality.parquet` | indicatore per sessione/target/filtro secondo schema | schema eseguibile Warehouse | Analytics Quality Owner | Candidate baseline |
| DP-005 | `weather.parquet` | campione temporale associabile a sessione | schema eseguibile Warehouse | Weather Data Steward | Candidate baseline |

Gli ID sono proposti da AP-002 e non promuovono gli oggetti a data product certificati. Grain, schema locator, owner e consumer devono essere verificati prima dell'approvazione.

## 5. Classificazione

- `Operational`
- `Historical`
- `Reference`
- `Configuration`
- `Derived`
- `Security-sensitive`
- `Safety-relevant`

Un oggetto può avere più attributi di classificazione, ma deve avere una classificazione primaria per retention e accesso.

## 6. Schema e semantica

- nomi tecnici stabili e preferibilmente `snake_case`;
- identificatori stabili e adatti alle join;
- grain esplicito;
- tipi coerenti;
- timezone esplicita;
- unità esplicite;
- zero, missing, false, empty ed error distinti;
- nessuna sostituzione silenziosa di missing con zero;
- derived data marcati e riproducibili.

## 7. Versionamento e compatibilità

| Tipo di modifica | Versione | Requisiti |
|---|---|---|
| editoriale non osservabile | patch | documentazione e review leggera |
| additiva opzionale | minor | schema, validator, test e consumer awareness |
| rimozione, rinomina, cambio tipo, unità, grain o significato | major | impact analysis, migration, rollback, consumer test e ARB |

I consumer devono dipendere dal contratto e non dall'ordine fisico delle colonne o da dettagli accidentali di generazione.

## 8. Quality rule record

Ogni regola deve dichiarare:

```text
rule_id
dataset_or_contract
field_or_scope
dimension
condition_or_threshold
severity
owner
validation_command_or_procedure
last_result
last_execution_date
evidence_locator
failure_action
```

Severity consentite:

- `Block`
- `Warn`
- `Observe`

## 9. Lineage record

Ogni relazione deve registrare:

```text
lineage_id
producer
source_artifact
transformation
output_data_product
consumer
schema_version
repository_path
commit_or_build_id
owner
evidence_type
```

Il lineage minimo per la baseline deve coprire Analytics → Warehouse → Dashboard/Reporting.

## 10. Retention rule record

Ogni retention rule deve dichiarare:

```text
retention_id
data_product
classification
working_retention
published_retention
historical_retention
backup_retention
log_retention
archive_location
disposal_method
legal_or_operational_basis
owner
approval
review_date
```

Questo standard non impone durate non verificate. Le durate devono essere deliberate per data product.

## 11. Change control

Un cambiamento dati deve includere:

1. change request;
2. owner e motivazione;
3. compatibility assessment;
4. producer impact;
5. consumer impact;
6. schema e validator update;
7. test evidence;
8. migration e rollback per major change;
9. lineage e traceability update;
10. release decision.

## 12. Waiver

Una waiver dati deve includere:

- identificativo;
- regola derogata;
- scope;
- rischio accettato;
- owner;
- approvatore;
- data di scadenza;
- compensating control;
- criterio di chiusura.

Una waiver scaduta non è valida e richiede nuova decisione.

## 13. Regole di precedenza

In caso di conflitto:

1. decisione ARB più recente e applicabile;
2. ADR approvato;
3. Architecture Package approvato;
4. schema eseguibile versionato;
5. standard e documentazione architetturale;
6. documentazione operativa;
7. snapshot o assessment storico.

Il conflitto deve comunque essere registrato e corretto; la precedenza non autorizza incoerenza permanente.

## 14. Safety e security

- i dati `Safety-relevant` non sostituiscono gli interblocchi fisici locali;
- stale, missing o degraded non equivalgono a safe;
- i secret sono referenziati, non serializzati;
- i dati personali sono minimizzati;
- AI e reporting usano dati governati e read-only per default;
- le trasformazioni conservano provenienza e significato degli eventi safety-relevant.

## 15. Compliance evidence

La conformità a questo standard richiede evidence locator immutabili verso:

- schema;
- validator;
- test;
- build metadata;
- lineage;
- consumer compatibility;
- release decision.

La sola presenza di questo documento non dimostra conformità o operatività.