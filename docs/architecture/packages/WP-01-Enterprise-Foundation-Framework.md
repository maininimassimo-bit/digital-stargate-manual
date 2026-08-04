# WP-01 — Enterprise Foundation Framework

| Campo | Valore |
|---|---|
| Identificativo | DSG-RC2-WP01 |
| Versione | 1.0 |
| Stato | Implemented |
| Data | 05/08/2026 |
| Baseline sorgente | DSG-BSL-RC1-001 |

## 1. Scopo

Introdurre una fondazione JavaScript condivisa per il Digital StarGate Enterprise Portal senza modificare le API scientifiche o i comportamenti pubblici della RC1.

## 2. Componenti

### Enterprise Core

`docs/javascripts/dsg-enterprise-core.js` espone il solo namespace globale intenzionale `window.DSG`:

```javascript
window.DSG.version
window.DSG.events
window.DSG.components
```

### Component Registry

API pubblica:

```javascript
DSG.components.register(definition)
DSG.components.has(name)
DSG.components.get(name)
DSG.components.status()
DSG.components.run(source)
```

Contratto minimo:

```javascript
DSG.components.register({
  name: 'component-name',
  order: 100,
  initialize(context) {}
});
```

`name` è univoco, `order` determina la sequenza e `initialize` deve essere idempotente.

### Lifecycle Manager

Il lifecycle viene eseguito:

- al DOM ready;
- dopo Instant Navigation di Material;
- su richiesta esplicita tramite `components.run(source)`;
- dopo registrazioni tardive.

Il contesto include:

```javascript
{
  cycle,
  source,
  root,
  events,
  components
}
```

Gli errori di un componente sono isolati e non interrompono gli altri componenti.

### Enterprise Event Bus

API pubblica:

```javascript
DSG.events.on(type, listener)
DSG.events.once(type, listener)
DSG.events.emit(type, detail)
```

Gli eventi vengono pubblicati anche come `CustomEvent` DOM con prefisso `dsg:`.

## 3. Componenti migrati

| Componente | Registry name | Ordine | Stato |
|---|---|---:|---|
| Theme Adapter | `theme-adapter` | 30 | Migrated |
| Roadmap Center | `roadmap-center` | 70 | Migrated |

I componenti RC1 non ancora migrati continuano a funzionare con il lifecycle locale esistente. La migrazione progressiva non è una condizione per l'esistenza del framework e verrà completata nei Work Package proprietari.

## 4. Compatibilità

- nessuna modifica alle API dello Scientific Data Engine;
- nessuna modifica agli URL pubblici;
- nessuna modifica all'authority Material per tema e navigazione;
- fallback RC1 mantenuto nei componenti migrati;
- inizializzazione idempotente obbligatoria;
- nessuna dipendenza esterna introdotta.

## 5. Convenzioni

- nomi componenti ed eventi in `kebab-case`;
- ordini 0–29 core, 30–59 shell e navigazione, 60–89 feature, 90+ estensioni;
- comunicazione tra componenti tramite Event Bus, non chiamate DOM fragili;
- ogni componente gestisce loading, empty, error e degraded state;
- i marker `data-dsg-*` devono impedire inizializzazioni duplicate.

## 6. Acceptance criteria

- core caricato prima dei moduli applicativi;
- registry e event bus disponibili globalmente tramite `window.DSG`;
- lifecycle compatibile con DOM ready e Instant Navigation;
- error isolation attiva;
- almeno due componenti RC1 migrati;
- fallback RC1 verificabile;
- `mkdocs build --strict` positivo;
- build e deploy GitHub Pages positivi;
- nessuna regressione della RC1 rilevata.

## 7. Debito e follow-up

- migrazione dei componenti scientifici nel WP-02;
- migrazione completa del Theme Framework nel WP-03;
- eventuale ottimizzazione della registrazione tardiva se le metriche mostrano cicli superflui;
- Plugin SDK costruito sopra il contratto del registry nel WP-06.

## 8. Decisione

Il framework è additivo e compatibile. Non sostituisce lo Scientific Data Engine e non introduce un secondo data-access layer.