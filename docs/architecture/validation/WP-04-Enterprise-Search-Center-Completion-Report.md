# WP-04 — Enterprise Search Center Completion Report

| Campo | Valore |
|---|---|
| Identificativo | DSG-RC2-WP04-CLR-001 |
| Versione | 1.0 |
| Stato | Accepted |
| Data chiusura | 05/08/2026 |
| Baseline sorgente | DSG-BSL-RC1-001 |
| Commit funzionale finale | `5c6dedab73d64f92d2caec171bef69f671a1144f` |
| Commit architetturale | `7856f8526197ccd2b9e702e819313a5073969808` |

## 1. Scopo

Registrare la chiusura tecnica, architetturale e documentale del Work Package WP-04 — Enterprise Search Center.

## 2. Outcome consegnati

- `DSGSearchService` come servizio condiviso di ricerca federata;
- federazione tra indice documentale MkDocs e sessioni scientifiche;
- accesso ai dati scientifici esclusivamente tramite Scientific Data Engine;
- ranking testuale normalizzato;
- facets per tipo, sezione, target, anno e qualità;
- metriche runtime e stato interrogabile;
- `dsg-search-center.js` integrato nel Component Registry;
- `search-center.css` separato e basato sui token enterprise;
- Search Center pubblicato nel Documentation Center;
- ricerca nativa Material preservata come capability distinta;
- risoluzione degli asset e degli URL dalla site root;
- eliminazione della pagina Search Center duplicata e non governata.

## 3. API pubblica

```javascript
DSGSearchService.load()
DSGSearchService.search(query, options)
DSGSearchService.getFacets()
DSGSearchService.getStatus()
DSGSearchService.clear()
```

## 4. Sorgenti governate

| Sorgente | Access layer | Stato |
|---|---|---|
| Documentazione | indice `search/search_index.json` generato da MkDocs | Federated |
| Sessioni scientifiche | Scientific Data Engine | Federated |

I dataset JSON restano proiezioni e non diventano fonte primaria.

## 5. Eventi

### Search Service

- `search-service-ready`;
- `search-load-start`;
- `search-load-ready`;
- `search-load-error`;
- `search-source-degraded`;
- `search-query-complete`;
- `search-cache-cleared`.

### Search Center

- `search-center-ready`;
- `search-center-results`;
- `search-center-error`.

## 6. Compatibilità RC1/RC2

Sono preservati:

- ricerca nativa Material;
- URL pubblici esistenti;
- Scientific Data Engine come authority;
- Component Registry ed Event Bus;
- Instant Navigation;
- layout e navigazione del Documentation Center;
- assenza di nuove dipendenze esterne.

## 7. Quality gate

Per il commit funzionale finale e per il commit della specifica architetturale risultano quattro workflow applicabili completati senza failure rilevate.

| Gate | Esito |
|---|---|
| Developer Foundation | Success |
| Pubblica documentazione | Success |
| Deploy MkDocs to GitHub Pages | Success |
| Genera manuale Word | Success |
| Duplicazione pagina Search Center | Eliminata |
| Repository truth | Allineata |

## 8. Debito tecnico residuo

- integrazione futura di Repository Intelligence e Mission Control quando saranno disponibili contratti dati stabili;
- persistenza e visualizzazione delle metriche di ricerca nel WP-05;
- provider di ricerca estendibili tramite Plugin SDK nel WP-06;
- test browser automatizzati da integrare nel programma di quality engineering.

Nessun elemento residuo impedisce la chiusura del Work Package.

## 9. Acceptance

Gli acceptance criteria risultano soddisfatti. WP-04 è dichiarato **Completed / Accepted**.

Il Work Package successivo è WP-05 — Operations Dashboard.