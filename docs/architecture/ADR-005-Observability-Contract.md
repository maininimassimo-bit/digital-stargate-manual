# ADR-005 – Observability Contract

## Status

Proposed

## Versione

1.0

## Scopo

Definire un contratto minimo e stabile per la telemetria prodotta dai componenti Digital StarGate, in modo che monitoraggio, troubleshooting, dashboard e audit utilizzino segnali coerenti e confrontabili.

## Ambito

La decisione si applica ai componenti che producono eventi operativi, metriche o informazioni di stato, inclusi:

- pipeline Analytics e Warehouse;
- processi di acquisizione eseguiti su EAGLE;
- automazioni GitHub Actions;
- pubblicazione del portale MkDocs;
- monitoraggio dello stato dell’osservatorio.

Non definisce ancora una piattaforma centralizzata di log management né impone uno specifico prodotto di osservabilità.

## Contesto e driver

Digital StarGate integra processi eseguiti su ambienti differenti. Senza un contratto comune, i segnali operativi tendono a usare nomi, severità, timestamp e identificativi non uniformi. Questo rende più difficile correlare un errore di acquisizione con una build, una sessione osservativa o un aggiornamento del Warehouse.

I driver principali sono:

- diagnosi più rapida degli incidenti;
- correlazione tra esecuzioni distribuite;
- indicatori affidabili per dashboard e report;
- compatibilità con future soluzioni di log aggregation;
- riduzione delle dipendenze da formati proprietari.

## Decisione

Ogni componente che emette telemetria strutturata deve adottare un envelope comune con i seguenti campi obbligatori:

| Campo | Descrizione |
| --- | --- |
| `timestamp_utc` | Timestamp ISO 8601 in UTC |
| `service` | Identificativo stabile del componente |
| `environment` | Ambiente di esecuzione, ad esempio `eagle`, `github-actions`, `workstation` |
| `severity` | Livello normalizzato: `debug`, `info`, `warning`, `error`, `critical` |
| `event_name` | Nome evento leggibile e stabile |
| `correlation_id` | Identificativo della sessione, build o processo correlato |
| `message` | Descrizione sintetica dell’evento |
| `schema_version` | Versione del contratto di telemetria |

I componenti possono aggiungere campi specifici, purché non ridefiniscano il significato dei campi obbligatori.

Esempio:

```json
{
  "timestamp_utc": "2026-07-28T08:15:30Z",
  "service": "warehouse-builder",
  "environment": "github-actions",
  "severity": "info",
  "event_name": "warehouse.build.completed",
  "correlation_id": "run-1842",
  "message": "Build Warehouse completata",
  "schema_version": "1.0",
  "records_written": 428
}
```

## Responsabilità e confini

- Ogni componente è responsabile della correttezza dei propri eventi.
- Il contratto definisce semantica e campi minimi, non il trasporto.
- Dashboard e report devono consumare solo campi documentati.
- Eventuali dati sensibili o credenziali non devono essere inclusi nella telemetria.

## Sicurezza e aspetti operativi

La telemetria non deve contenere password, token, chiavi API, coordinate di accesso VPN o altri segreti. I messaggi di errore devono essere utili al troubleshooting senza esporre configurazioni riservate.

La conservazione e la rotazione dei log restano responsabilità del rispettivo ambiente finché non verrà introdotto un servizio centralizzato.

## Attributi di qualità

Questa decisione supporta:

- **osservabilità**, tramite segnali uniformi;
- **manutenibilità**, grazie a una semantica condivisa;
- **interoperabilità**, tramite JSON e timestamp standard;
- **auditabilità**, mediante identificativi di correlazione;
- **evolvibilità**, attraverso `schema_version`.

## Conseguenze

### Positive

- correlazione più semplice tra processi e ambienti;
- riduzione dei parser specifici;
- base stabile per KPI operativi e incident analysis;
- migrazione futura più semplice verso strumenti centralizzati.

### Negative

- adeguamento progressivo dei componenti esistenti;
- necessità di governare nomi evento e versioni;
- lieve aumento della quantità di dati prodotti.

## Vincoli

- Il formato canonico è UTF-8 senza BOM.
- I timestamp devono essere espressi in UTC.
- I nomi evento devono usare la forma gerarchica `dominio.azione.esito` quando applicabile.
- Le modifiche incompatibili richiedono una nuova major version dello schema.

## Tracciabilità

- [Panoramica architetturale](index.md)
- [ADR-002 – Analytics Quality Gates](ADR-002-Analytics-Quality-Gates.md)
- [ADR-003 – Warehouse Engine](ADR-003-Warehouse-Engine.md)
- [Metodologia troubleshooting](../chapters/30-metodologia-troubleshooting.md)
- [Reportistica e KPI](../chapters/29-reportistica-operativa-kpi.md)

## Questioni aperte

- definizione di un registro canonico degli `event_name`;
- scelta del formato di persistenza per la telemetria storica;
- valutazione di metriche OpenTelemetry in una fase successiva;
- definizione delle policy di retention per ciascun ambiente.
