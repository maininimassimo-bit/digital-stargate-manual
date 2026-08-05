# WP-04 — Enterprise Search Center

| Campo | Valore |
|---|---|
| Identificativo | DSG-RC2-WP04 |
| Versione | 1.0 |
| Stato | Implemented |
| Data | 05/08/2026 |
| Baseline sorgente | DSG-BSL-RC1-001 |

## 1. Scopo

Introdurre una capability di ricerca federata che unifichi documentazione versionata e sessioni scientifiche senza sostituire la ricerca nativa di Material for MkDocs.

## 2. Architettura

### Search Service

`docs/javascripts/dsg-search-service.js` espone:

```javascript
DSGSearchService.load()
DSGSearchService.search(query, options)
DSGSearchService.getFacets()
DSGSearchService.getStatus()
DSGSearchService.clear()
```

Il servizio è registrato nel Component Registry come `search-service` con ordine 45.

### Sorgenti federate

- indice MkDocs `search/search_index.json` per la documentazione;
- Scientific Data Engine per le sessioni scientifiche.

Il Search Service non accede direttamente al dataset scientifico quando il motore è disponibile. Lo Scientific Data Engine resta l'unico data-access layer condiviso del dominio scientifico.

### Search Center UI

`docs/javascripts/dsg-search-center.js` gestisce:

- query con debounce;
- filtri per tipo, anno, target e qualità;
- rendering dei risultati;
- reset dei filtri;
- stati loading, ready, searching, empty ed error;
- eventi di lifecycle e telemetria.

Il componente è registrato come `search-center` con ordine 75.

### Presentation Layer

`docs/styles/search-center.css` contiene esclusivamente la presentazione del componente e usa i token `--dsg-*` del Theme Framework.

## 3. Integrazione nel portale

Il Search Center è pubblicato nel Documentation Center, già governato dalla navigazione enterprise. La ricerca nativa Material resta disponibile come funzione rapida distinta.

Questa scelta evita:

- duplicazione di pagine;
- una seconda navigazione concorrente;
- dipendenza da una modifica estesa di `mkdocs.yml`;
- una pagina orfana fuori dalla repository truth.

## 4. Ranking

Il ranking usa token normalizzati e pesi decrescenti per:

1. titolo;
2. sezione;
3. testo;
4. parole chiave.

Le corrispondenze esatte ricevono peso maggiore rispetto a prefissi e contenimenti.

## 5. Facets

Il servizio espone facets dinamiche per:

- tipo contenuto;
- sezione;
- target scientifico;
- anno osservativo;
- stato di qualità.

## 6. URL e site root

Gli asset e i risultati sono risolti dalla site root derivata dal percorso dello script. Il comportamento è quindi indipendente dalla profondità della pagina MkDocs.

## 7. Eventi

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

## 8. Compatibilità RC1

- ricerca Material preservata;
- URL pubblici esistenti preservati;
- Scientific Data Engine preservato come authority;
- nessuna dipendenza esterna introdotta;
- Component Registry ed Event Bus riutilizzati;
- Instant Navigation non modificata.

## 9. Acceptance criteria

- ricerca federata tra documentazione e sessioni scientifiche;
- ranking e filtri funzionanti;
- facets derivate dai dati caricati;
- stati operativi gestiti;
- link risultati risolti dalla site root;
- integrazione nel Documentation Center;
- nessuna pagina duplicata o orfana;
- workflow applicabili completati senza failure;
- nessuna regressione della baseline RC1.

## 10. Follow-up

- sorgenti Repository Intelligence e Mission Control da integrare quando esporranno contratti dati stabili;
- metriche persistenti e dashboard nel WP-05;
- provider di ricerca estendibili tramite Plugin SDK nel WP-06.