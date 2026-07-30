# Digital StarGate Integration Contract Catalog

| Campo | Valore |
|---|---|
| Identificativo | INT-CAT-001 |
| Package | AP-008 |
| Data | 30/07/2026 |
| Stato | Initial candidate catalog — not operationally authorized |

## 1. Regole

- Il catalogo registra contratti pubblici candidati dell'Enterprise Integration Fabric.
- `Candidate` non equivale a `Approved` o `Active`.
- Gli eventi descrivono fatti; i comandi richiedono azioni; le query leggono stato senza effetti collaterali.
- Nessun contratto autorizza il bypass di interlock, policy IAM o readiness gate.
- Ogni attivazione richiede owner, schema, compatibility test, security review, runbook, telemetry ed evidence.

## 2. Command catalog

| Contract ID | Versione | Dominio | Finalità | Safety relevance | Stato |
|---|---:|---|---|---|---|
| `DSG.Observation.Command.StartSession` | 1.0.0 | Observation | richiedere l'avvio di una sessione governata | da classificare | Candidate |
| `DSG.Observation.Command.AbortSession` | 1.0.0 | Observation | richiedere arresto controllato della sessione | safety-relevant potential | Candidate |
| `DSG.Dome.Command.RequestOpen` | 1.0.0 | Dome | richiedere apertura soggetta a interlock locale | safety-relevant | Candidate |
| `DSG.Dome.Command.RequestClose` | 1.0.0 | Dome | richiedere chiusura soggetta a interlock locale | safety-relevant | Candidate |
| `DSG.Processing.Command.RegisterProcessingRun` | 1.0.0 | Processing | registrare manifest e provenance | non-safety | Candidate |

## 3. Event catalog

| Contract ID | Versione | Producer candidate | Consumer candidate | Stato |
|---|---:|---|---|---|
| `DSG.Observation.Event.SessionStarted` | 1.0.0 | N.I.N.A. adapter | DSAP, DSOC, audit | Candidate |
| `DSG.Observation.Event.SessionCompleted` | 1.0.0 | N.I.N.A. adapter | warehouse, portal, catalog | Candidate |
| `DSG.Observation.Event.SessionAborted` | 1.0.0 | observation application | operations, analytics | Candidate |
| `DSG.Guiding.Event.StateChanged` | 1.0.0 | PHD2 adapter | operations, telemetry | Candidate |
| `DSG.Mount.Event.StateChanged` | 1.0.0 | CPWI adapter | operations, telemetry | Candidate |
| `DSG.Dome.Event.StateChanged` | 1.0.0 | dome adapter | operations, safety evidence | Candidate |
| `DSG.Weather.Event.ConditionChanged` | 1.0.0 | weather adapter | automation, DSOC | Candidate |
| `DSG.Safety.Event.UnsafeConditionDetected` | 1.0.0 | local safety boundary | operations, audit | Candidate |
| `DSG.Asset.Event.ConfigurationChanged` | 1.0.0 | configuration management | operations, audit | Candidate |
| `DSG.Processing.Event.ProcessingRunRegistered` | 1.0.0 | processing registry | catalog, knowledge layer | Candidate |
| `DSG.Storage.Event.ScientificAssetRegistered` | 1.0.0 | repository adapter | catalog, analytics | Candidate |
| `DSG.Integration.Event.ReconciliationDivergenceDetected` | 1.0.0 | reconciliation service | operations, problem management | Candidate |

## 4. Query catalog

| Contract ID | Versione | Risposta minima | Stato |
|---|---:|---|---|
| `DSG.Observatory.Query.GetCurrentState` | 1.0.0 | observed state, source, timestamp, freshness | Candidate |
| `DSG.Weather.Query.GetLatestConditions` | 1.0.0 | measures, units, source, timestamp, freshness | Candidate |
| `DSG.Observation.Query.GetSession` | 1.0.0 | session metadata e provenance locator | Candidate |
| `DSG.Asset.Query.GetConfigurationBaseline` | 1.0.0 | baseline ID, CI versions, effective time | Candidate |
| `DSG.Processing.Query.GetProcessingRun` | 1.0.0 | immutable processing manifest | Candidate |
| `DSG.Integration.Query.GetAdapterHealth` | 1.0.0 | component health, dependency health, freshness | Candidate |

## 5. Minimum activation record

```yaml
contract_id: string
version: semver
owner: string
status: draft|proposed|approved|active|deprecated|retired
schema_uri: string
classification: public|internal|restricted
producers: []
consumers: []
compatibility_policy: string
security_review: string
safety_class: non_safety|safety_relevant|unknown
sli: []
runbooks: []
test_evidence: []
deprecation_date: timestamp|null
```

## 6. Open decisions

- naming authority e ownership del registry;
- schema format e repository locator;
- unità canoniche per weather e telemetry;
- payload massimi e binary-reference policy;
- consumer registration e compatibility automation;
- retention di eventi, outbox, inbox e dead-letter;
- classificazione definitiva dei comandi;
- protocolli e trasporti da definire con AP-009.

## 7. Validation status

Il catalogo è stato prodotto come baseline documentale. Non sono stati eseguiti schema validation, consumer compatibility test, adapter test, command authorization test o runtime publication.