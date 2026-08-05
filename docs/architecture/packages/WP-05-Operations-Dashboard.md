# WP-05 — Operations Dashboard

| Campo | Valore |
|---|---|
| Identificativo | DSG-RC2-WP05 |
| Versione | 1.0 |
| Stato | Implemented |
| Data | 05/08/2026 |
| Baseline sorgente | DSG-BSL-RC1-001 |

## 1. Scopo

Introdurre una capability di osservabilità read-only per la piattaforma RC2, aggregando stato, KPI e telemetria esclusivamente tramite le API pubbliche dei servizi enterprise.

## 2. Architettura

### Operations Service

`docs/javascripts/dsg-operations-service.js` espone:

```javascript
DSGOperationsService.getSnapshot()
DSGOperationsService.getKPIs()
DSGOperationsService.getTelemetry()
DSGOperationsService.refresh()
```

Il servizio è registrato nel Component Registry come `operations-service` con ordine 50.

### Operations Widgets

`docs/javascripts/dsg-operations-widgets.js` espone widget di rendering riutilizzabili:

```javascript
DSGOperationsWidgets.kpiCards(items)
DSGOperationsWidgets.healthList(items)
DSGOperationsWidgets.serviceList(items)
DSGOperationsWidgets.eventTimeline(items, limit)
DSGOperationsWidgets.ap013Card(status)
```

Il widget layer non accede ai servizi e non contiene logica di raccolta dati.

### Operations Dashboard

`docs/javascripts/dsg-operations-dashboard.js` orchestra snapshot, KPI e widget. Il componente è registrato come `operations-dashboard` con ordine 80.

### Presentation Layer

`docs/styles/operations-dashboard.css` contiene esclusivamente layout e presentazione, utilizzando i token enterprise `--dsg-*` quando disponibili.

## 3. Sorgenti osservate

La dashboard interroga esclusivamente contratti pubblici:

- Enterprise Core e Component Registry;
- Scientific Data Engine;
- Search Service;
- Theme Service;
- Enterprise Event Bus;
- stato governato AP-013.

Non sono consentiti accessi diretti agli stati interni dei componenti.

## 4. Snapshot operativo

Lo snapshot contiene:

- timestamp di generazione;
- versione del servizio;
- uptime del layer Operations;
- disponibilità dell'Enterprise Core;
- health del Component Registry;
- stato e metriche scientifiche;
- stato dell'indice di ricerca;
- stato del Theme Service;
- stato di validation AP-013;
- telemetria runtime osservata.

## 5. KPI

La prima versione espone:

- componenti registrati;
- componenti ready;
- errori componenti;
- sessioni scientifiche indicizzate;
- failure scientifiche;
- documenti nell'indice di ricerca;
- sessioni scientifiche nell'indice federato;
- eventi runtime osservati;
- stato di validation AP-013.

## 6. Telemetria

Il servizio osserva eventi pubblici dell'Enterprise Event Bus e mantiene:

- conteggio per tipo evento;
- totale eventi osservati;
- ultimi 50 eventi della sessione browser.

La telemetria è volatile e non costituisce repository evidence.

## 7. AP-013

La dashboard distingue esplicitamente:

- completamento dichiarato dall'operatore;
- disponibilità delle evidenze nel repository;
- stato formale di validation.

Fino al versionamento del pacchetto OAT finale, lo stato rimane:

```text
PENDING_EVIDENCE_REVIEW
```

La dashboard non può promuovere autonomamente lo stato ad `ACCEPTED`.

## 8. Integrazione nel portale

La dashboard è pubblicata nell'Operations Center esistente. Gli asset sono caricati in questo ordine:

1. Scientific Data Engine;
2. Search Service;
3. Operations Service;
4. Operations Widgets;
5. Operations Dashboard.

## 9. Safety boundary

La capability è esclusivamente read-only:

- nessun comando fisico;
- nessun controllo di safety;
- nessuna modifica di task schedulati;
- nessuna modifica dei dataset;
- nessuna scrittura verso servizi enterprise.

Gli interblocchi fisici e la safety locale restano indipendenti dal portale.

## 10. Eventi

- `operations-service-ready`;
- `operations-snapshot-ready`;
- `operations-dashboard-ready`;
- `operations-dashboard-error`.

## 11. Compatibilità RC1/RC2

- Operations Center esistente preservato;
- URL pubblici preservati;
- Component Registry ed Event Bus riutilizzati;
- Scientific Data Engine preservato come authority;
- nessuna dipendenza esterna introdotta;
- Instant Navigation non modificata;
- dashboard separata dalle fonti autorevoli.

## 12. Acceptance criteria

- servizio read-only disponibile;
- snapshot e KPI interrogabili;
- widget layer separato dal controller;
- dashboard integrata nell'Operations Center;
- health di componenti e servizi visualizzata;
- telemetria runtime visualizzata;
- stato AP-013 rappresentato senza promozioni non supportate;
- ordine delle dipendenze corretto;
- quattro workflow applicabili completati con successo;
- nessuna regressione della baseline RC1.

## 13. Follow-up

- persistenza delle metriche in una futura capability dedicata;
- integrazione Repository Intelligence tramite contratto stabile;
- integrazione CI/CD dettagliata quando disponibile un provider governato;
- provider widget estendibili tramite Plugin SDK nel WP-06;
- promozione AP-013 ad `ACCEPTED` dopo versionamento del pacchetto OAT finale.