# Digital StarGate Enterprise Metamodel

| Campo | Valore |
|---|---|
| Documento | Enterprise Metamodel |
| Package | AP-001 |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Stato | Proposed for independent ARB review |
| Data | 30/07/2026 |

## 1. Scopo

Questo documento definisce il vocabolario canonico per descrivere e collegare gli artefatti architetturali, implementativi, probatori e di release di Digital StarGate.

## 2. Concetti canonici

### Capability

Una capability descrive ciò che la piattaforma è in grado di fare o deve essere in grado di fare. Non coincide automaticamente con un componente, un documento o una pagina del portale.

### Architecture Package

Un Architecture Package è un insieme coerente e revisionabile di cambiamenti architetturali, documentali e, quando previsto, implementativi. Deve dichiarare scope, capability interessate, dipendenze, rischi, acceptance criteria, validazioni e handoff ARB.

### Architecture Decision Record

Un ADR registra una decisione architetturale, il contesto, le alternative e le conseguenze. Non sostituisce un Architecture Package e non prova l'implementazione.

### Assessment

Un assessment valuta una baseline o uno scope definito. Deve distinguere fatti verificati, inferenze, raccomandazioni e validazioni non eseguite.

### Architecture Review

Una review ARB è indipendente dall'autore del package. Valuta coerenza, completezza, rischio, safety, operabilità, tracciabilità e qualità delle evidenze.

### Evidence

L'evidenza segue la tassonomia PAA-002:

- `DOC` — documentazione;
- `CFG` — configurazione;
- `SRC` — codice sorgente;
- `TST` — test;
- `INT` — integrazione;
- `OPS` — evidenza operativa;
- `GOV` — governance.

### Release

Una release aggrega cambiamenti approvati e verificati. Deve dichiarare package inclusi, validazioni eseguite, rischi residui, migrazione e rollback quando applicabili.

## 3. Relazioni

| Origine | Relazione | Destinazione | Obbligo |
|---|---|---|---|
| Driver/Risk | motivates | Capability/AP | Obbligatorio per nuovi AP |
| Capability | realized by | Component/Implementation | Quando esiste implementazione |
| AP | governs | Capability/Change | Obbligatorio |
| AP | decides through | ADR | Quando è richiesta una decisione |
| Implementation | evidenced by | Evidence | Obbligatorio per promozione stato |
| AP/Assessment | reviewed by | ARB | Obbligatorio prima dell'approvazione |
| Approved AP | included in | Release | Quando rilasciato |
| Artefatto | supersedes | Artefatto | Quando sostituisce una fonte precedente |

## 4. Regole semantiche

1. Una pagina, directory o configurazione futura non dimostra una capability live.
2. `Implemented` richiede SRC e almeno TST o INT secondo PAA-002.
3. `Operationally Verified` richiede OPS e non può essere dedotto dalla sola documentazione.
4. Monitoring non equivale a safety.
5. Dashboard, Reporting e AI consumano dati governati; non devono creare pipeline parallele dai log grezzi.
6. Gli interblocchi locali restano indipendenti da applicazione, cloud e AI.
7. Gli identificatori esistenti non vengono rinumerati retroattivamente.

## 5. Metadati minimi

```text
Identifier
Title
Artifact type
Repository
Branch or immutable commit
Owner or authority
Status
Date or version
Related artifacts
Validations executed
Validations not executed
```

## 6. Lifecycle

```text
Draft
  |
  v
Proposed for review
  |
  v
Approved / Approved with conditions
  |
  +--> Superseded
  +--> Deprecated
```

Una modifica sostanziale a capability status, canonical data flow, safety boundary o AI tool execution richiede re-review.

## 7. Boundary DDD e C4

- Il **Domain** contiene concetti e regole dell'osservatorio, non dettagli di hosting o rete.
- I **Domain Event** descrivono fatti avvenuti nel dominio.
- Gli **Integration Event** sono contratti pubblicati verso altri bounded context o consumer.
- L'**Outbox** è un pattern di affidabilità, non un event bus.
- Il trasporto è una scelta infrastrutturale separata dal contratto evento.
- Le projection sono modelli di lettura derivati, non la fonte autorevole del dominio.
- Nel modello C4, persone e sistemi esterni appartengono al Context; applicazioni e data store principali al Container; componenti interni al Component view.

## 8. Governance

Il registro canonico delle relazioni è `traceability-register.md`. AP-001 non certifica la piena adozione del metamodel: ne istituisce la baseline documentale da sottoporre a review indipendente.