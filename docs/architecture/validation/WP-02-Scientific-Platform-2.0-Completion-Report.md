# WP-02 — Scientific Platform 2.0 Completion Report

| Campo | Valore |
|---|---|
| Identificativo | DSG-RC2-WP02-CLR-001 |
| Versione | 1.0 |
| Stato | Accepted |
| Data chiusura | 05/08/2026 |
| Baseline sorgente | DSG-BSL-RC1-001 |
| Commit funzionale finale | `e6e03ab01247083dbe41c129471bda412e7647b4` |

## 1. Scopo

Registrare la chiusura tecnica, architetturale e documentale del Work Package WP-02 — Scientific Platform 2.0.

## 2. Outcome consegnati

- Scientific Data Engine evoluto alla versione `2.1.0-rc2`;
- cache con stati `loading`, `ready` ed `error`;
- reload forzato, TTL opzionale e invalidazione esplicita;
- metriche runtime e stato interrogabile;
- integrazione con Enterprise Event Bus;
- preload dei cataloghi;
- Session Store indicizzato per session ID, target e anno;
- query layer additivo;
- Scientific Session Explorer migrato al Component Registry;
- Scientific Session Detail migrato al Component Registry;
- Latest Observation migrato al Component Registry;
- stati loading, ready, error e degraded formalizzati nei componenti scientifici.

## 3. API preservate

Le API RC1 restano disponibili:

```javascript
loadCatalog()
getSessions()
getSession()
getTargets()
getYears()
getKPIs()
filterSessions()
getKnowledgeGraph()
getLineage()
clearCache()
```

## 4. API additive RC2

```javascript
preload()
getSessionsByTarget()
getSessionsByYear()
querySessions()
getStatus()
getMetrics()
```

Nessuna breaking change è stata introdotta.

## 5. Eventi pubblicati

### Scientific Data Engine

- `science-engine-ready`;
- `science-load-start`;
- `science-load-ready`;
- `science-load-error`;
- `science-cache-hit`;
- `science-cache-invalidated`;
- `science-store-ready`.

### Componenti

- `scientific-session-explorer-ready`;
- `scientific-session-explorer-filtered`;
- `scientific-session-explorer-error`;
- `scientific-session-detail-ready`;
- `scientific-session-detail-error`;
- `latest-observation-data-ready`;
- `latest-observation-ready`;
- `latest-observation-degraded`.

## 6. Compatibilità RC1

Verificata la conservazione di:

- URL pubblici;
- markup funzionale del Session Catalog;
- markup funzionale del Session Detail;
- dataset scientifici esistenti;
- authority dello Scientific Data Engine;
- fallback RC1 dei componenti;
- comportamento Aladin Lite e fallback grafico;
- Instant Navigation.

## 7. Quality gate

Sul commit funzionale finale `e6e03ab01247083dbe41c129471bda412e7647b4` risultano completati con esito positivo:

| Gate | Esito |
|---|---|
| Developer Foundation | Success |
| Pubblica documentazione | Success |
| Deploy MkDocs to GitHub Pages | Success |
| Genera manuale Word | Success |
| MkDocs strict build | Success tramite workflow |
| GitHub Pages deployment | Success |

## 8. Debito tecnico residuo

- CSS inline di Latest Observation da estrarre in un componente CSS dedicato;
- eventuali metriche persistenti da trattare nel WP-05 Operations Dashboard;
- test browser automatizzati da valutare nel programma di quality engineering;
- estensioni scientifiche future da esporre tramite Plugin SDK nel WP-06.

Nessuno di questi punti impedisce la chiusura del WP-02.

## 9. Acceptance

Gli acceptance criteria sono soddisfatti. WP-02 è dichiarato **Completed / Accepted**.

Il Work Package successivo è WP-03 — Enterprise Theme Framework.