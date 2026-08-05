# Enterprise Plugin SDK Specification

| Campo | Valore |
|---|---|
| Identificativo | DSG-SDK-PLUGIN-001 |
| Versione | 1.0 |
| API version | `1` |
| Stato | RC2 Candidate |
| Work Package | WP-06 — Enterprise Plugin SDK |

## 1. Scopo

L'Enterprise Plugin SDK estende il Digital StarGate Enterprise Portal tramite plugin versionati nel repository, senza modificare il core. Usa Component Registry, Enterprise Event Bus, lifecycle enterprise e servizi pubblici della piattaforma RC2.

## 2. Componenti

| Componente | Responsabilità | API globale |
|---|---|---|
| Plugin Registry | validazione manifest, registrazione e capability discovery | `DSGPluginRegistry` |
| Dependency Resolver | dipendenze mancanti, cycle detection e ordine deterministico | `DSGPluginDependencyResolver` |
| Plugin Runtime | initialize, dispose, context injection e failure isolation | `DSGPluginRuntime` |
| Provider Contracts | validazione delle estensioni per capability | `DSGPluginProviderContracts` |

## 3. Manifest

```javascript
{
  id: 'plugin-id',
  name: 'Plugin name',
  description: 'Descrizione',
  provider: 'Digital StarGate',
  version: '1.0.0',
  apiVersion: '1',
  capabilities: [],
  dependencies: [],
  initialize(context) {},
  dispose(context) {}
}
```

Campi obbligatori:

- `id`: lowercase kebab-case e univoco;
- `version`: semantic versioning;
- `apiVersion`: valore `1`;
- `initialize`: funzione.

Capability e dipendenze sono array di stringhe non vuote e senza duplicati. Un plugin non può dipendere da sé stesso.

## 4. Plugin Registry

```javascript
DSGPluginRegistry.register(manifest)
DSGPluginRegistry.validate(manifest)
DSGPluginRegistry.has(id)
DSGPluginRegistry.get(id)
DSGPluginRegistry.list()
DSGPluginRegistry.findByCapability(capability)
DSGPluginRegistry.capabilities()
DSGPluginRegistry.status()
```

La registrazione è idempotente soltanto quando la definizione coincide. Una definizione incompatibile con lo stesso ID viene rifiutata.

## 5. Dependency Resolver

```javascript
const report = DSGPluginDependencyResolver.analyze(['my-plugin']);
const order = DSGPluginDependencyResolver.resolve(['my-plugin']);
```

`analyze()` restituisce validità, plugin richiesti, ordine, plugin mancanti, dipendenze mancanti, ciclo e grafo normalizzato. `resolve()` restituisce l'ordine topologico o genera un errore motivato. Tra nodi equivalenti viene applicato l'ordinamento lessicografico.

## 6. Plugin Runtime

```javascript
await DSGPluginRuntime.run(['my-plugin'], 'page-load');
await DSGPluginRuntime.dispose(['my-plugin'], 'page-leave');
const status = DSGPluginRuntime.status();
```

Il runtime inizializza nell'ordine risolto, isola gli errori, conserva il cleanup e dispone i plugin in ordine inverso.

## 7. Context API

```javascript
{
  cycle,
  source,
  root,
  events,
  components,
  services,
  plugin,
  logger
}
```

Il catalogo `services` può contenere `scientific`, `search`, `operations`, `theme` e `plugins`. Ogni plugin deve verificare la disponibilità del servizio e usare soltanto la sua API pubblica.

## 8. Provider Contracts

| Contratto | Capability | Funzione richiesta |
|---|---|---|
| `operations-widget` | `operations-widget` | `render(context)` |
| `search-provider` | `search-provider` | `search(query, options)` |
| `scientific-view` | `scientific-view` | `mount(context)` |
| `repository-intelligence-provider` | `repository-intelligence-provider` | `getSnapshot()` |
| `navigation-extension` | `navigation-extension` | `getItems(context)` |

```javascript
DSGPluginProviderContracts.validate('operations-widget', provider);
```

## 9. Lifecycle

Prima di un nuovo ciclo, il lifecycle enterprise esegue il cleanup restituito da `initialize()` e la funzione `destroy()` del componente. I plugin devono essere idempotenti, rimuovere listener e DOM creato e non conservare riferimenti stale.

## 10. Ordine di caricamento

```text
Enterprise Core
  -> Plugin Registry
  -> Dependency Resolver
  -> Plugin Runtime
  -> Provider Contracts
  -> Plugin implementations
```

## 11. Vincoli

- plugin e manifest versionati nel repository;
- nessuna esecuzione dinamica di stringhe;
- nessun caricamento automatico da sorgenti esterne;
- nessun accesso diretto agli stati interni dei servizi;
- nessun bypass dello Scientific Data Engine;
- nessun comando operativo o di safety;
- nessuna promozione automatica di stati di governance.

## 12. Quality gate

```bash
node --test .github/scripts/test-plugin-sdk.mjs
```

Il test è eseguito dal workflow `Developer Foundation` insieme ai gate .NET, formattazione e MkDocs strict.

## 13. Compatibilità

`apiVersion: '1'` è il contratto pubblico della RC2. Una modifica incompatibile richiede una nuova API version e una decisione architetturale esplicita.