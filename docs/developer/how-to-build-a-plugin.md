# Come sviluppare un plugin Digital StarGate

## Scopo

Questa guida descrive il percorso minimo per creare, registrare, validare e testare un plugin compatibile con l'Enterprise Plugin SDK `apiVersion: '1'`.

Prima di iniziare leggere la [specifica ufficiale del Plugin SDK](plugin-sdk-specification.md) e i [contratti della piattaforma](platform-contracts.md).

## 1. Scegliere un identificativo

L'identificativo deve essere lowercase kebab-case, stabile e univoco.

Esempi validi:

```text
session-summary-widget
scientific-search-provider
repository-health-panel
```

Non rinominare un plugin già distribuito: un cambio di ID equivale a introdurre un nuovo plugin.

## 2. Creare il file del plugin

I plugin del portale sono versionati sotto `docs/javascripts/` e caricati dopo i componenti core del Plugin SDK.

```javascript
(() => {
  'use strict';

  const plugin = {
    id: 'session-summary-widget',
    name: 'Session Summary Widget',
    description: 'Riepilogo non operativo delle sessioni osservative.',
    provider: 'Digital StarGate',
    version: '1.0.0',
    apiVersion: '1',
    capabilities: ['operations-widget'],
    dependencies: [],

    initialize(context) {
      const provider = {
        id: 'session-summary-widget',
        render(renderContext) {
          const root = renderContext.root;
          if (!root) return;

          const element = document.createElement('section');
          element.dataset.plugin = 'session-summary-widget';
          element.textContent = 'Session summary ready';
          root.appendChild(element);
        }
      };

      context.services.plugins.contracts.validate(
        'operations-widget',
        provider
      );

      return () => {
        document
          .querySelectorAll('[data-plugin="session-summary-widget"]')
          .forEach((element) => element.remove());
      };
    },

    dispose(context) {
      context.logger.info('Plugin disposed');
    }
  };

  window.DSGPluginRegistry.register(plugin);
})();
```

## 3. Dichiarare le capability

Dichiarare soltanto capability realmente implementate. I contratti disponibili nella API version 1 sono:

| Capability | Funzione richiesta |
|---|---|
| `operations-widget` | `render(context)` |
| `search-provider` | `search(query, options)` |
| `scientific-view` | `mount(context)` |
| `repository-intelligence-provider` | `getSnapshot()` |
| `navigation-extension` | `getItems(context)` |

Validare sempre il provider prima di esporlo:

```javascript
DSGPluginProviderContracts.validate('search-provider', provider);
```

## 4. Dichiarare le dipendenze

Le dipendenze usano gli ID dei plugin richiesti:

```javascript
dependencies: ['scientific-data-provider']
```

Il resolver:

- segnala dipendenze non registrate;
- rifiuta dipendenze cicliche;
- produce un ordine deterministico;
- inizializza i provider prima dei consumer.

Verifica manuale:

```javascript
DSGPluginDependencyResolver.analyze(['session-summary-widget']);
```

## 5. Usare il context senza accoppiarsi al core

Il plugin riceve il context seguente:

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

Regole:

- verificare sempre che un servizio esista;
- usare soltanto API pubbliche;
- non leggere proprietà interne del registry o dei servizi;
- non modificare direttamente lo stato del core;
- non introdurre comandi operativi o bypass di safety.

Esempio difensivo:

```javascript
const search = context.services.search;
if (search?.query) {
  const result = await search.query('M31');
}
```

## 6. Gestire il lifecycle

`initialize()` deve essere idempotente e può restituire una funzione di cleanup. `dispose()` è opzionale, ma consigliata quando il plugin gestisce risorse aggiuntive.

Il cleanup deve rimuovere:

- listener;
- timer;
- nodi DOM creati dal plugin;
- subscription;
- riferimenti a context di cicli precedenti.

Non conservare riferimenti globali a elementi della pagina.

## 7. Isolare gli errori

Un plugin non deve impedire l'avvio degli altri plugin. Gli errori vanno registrati tramite `context.logger` e lasciati gestire al runtime.

```javascript
initialize(context) {
  try {
    // setup
  } catch (error) {
    context.logger.error('Initialization failed', error);
    throw error;
  }
}
```

## 8. Registrare il file nella pagina

Il caricamento deve rispettare l'ordine:

```text
Enterprise Core
Plugin Registry
Dependency Resolver
Plugin Runtime
Provider Contracts
Plugin implementations
```

Aggiungere il file a `extra_javascript` in `mkdocs.yml` soltanto dopo i quattro moduli del Plugin SDK.

## 9. Aggiungere i test

La suite ufficiale è:

```bash
node --test .github/scripts/test-plugin-sdk.mjs
```

Per ogni nuovo contratto o comportamento aggiungere almeno un test che copra:

- manifest valido e invalido;
- dipendenze;
- ordine di inizializzazione;
- cleanup e dispose;
- isolamento dei failure;
- validazione del provider.

Gli oggetti restituiti da un contesto `vm` devono essere convertiti in primitive o strutture del realm del test runner prima del confronto strutturale.

## 10. Eseguire il quality gate completo

```bash
dotnet restore DigitalStarGate.sln
dotnet build DigitalStarGate.sln --configuration Release
dotnet test DigitalStarGate.sln --configuration Release
dotnet format DigitalStarGate.sln --verify-no-changes
node --test .github/scripts/test-plugin-sdk.mjs
python -m pip install --requirement requirements.txt
mkdocs build --strict
```

## 11. Checklist di pubblicazione

- ID stabile e kebab-case;
- semantic version aggiornata;
- `apiVersion: '1'`;
- capability validate tramite Provider Contracts;
- dipendenze esplicite e acicliche;
- cleanup verificato su un secondo lifecycle cycle;
- nessuna sorgente esterna caricata dinamicamente;
- nessun accesso a API private;
- test e MkDocs strict verdi;
- documentazione e ADR aggiornate quando cambia un contratto pubblico.