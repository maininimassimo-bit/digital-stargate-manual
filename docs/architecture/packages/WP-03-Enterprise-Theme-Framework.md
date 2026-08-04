# WP-03 — Enterprise Theme Framework

| Campo | Valore |
|---|---|
| Identificativo | DSG-RC2-WP03 |
| Versione | 1.0 |
| Stato | In Progress |
| Data | 05/08/2026 |
| Baseline sorgente | DSG-BSL-RC1-001 |

## 1. Scopo

Evolvere la gestione del tema da adapter Light/Dark a servizio enterprise centralizzato, compatibile con Material for MkDocs, Instant Navigation e futuri profili di branding.

## 2. Architettura

### Theme Service

`docs/javascripts/dsg-theme-manager.js` è l'unico owner della logica tema e pubblica:

```javascript
DSGThemeService.getTheme()
DSGThemeService.setTheme(preference)
DSGThemeService.toggleTheme()
DSGThemeService.onThemeChanged(listener)
DSGThemeService.refresh()
```

Le preferenze supportate sono:

```text
light
dark
system
```

Lo stato distingue:

- `preference`: scelta persistita dell'utente;
- `resolvedTheme`: tema effettivamente applicato;
- `materialTheme`: palette Material attiva;
- `followsSystem`: indicatore della modalità System;
- `version`: versione del servizio.

### Material Adapter

Il servizio individua gli input palette nativi di Material e applica il tema tramite i controlli ufficiali. Material conserva l'authority sul rendering della palette.

Non è consentita la modifica diretta e parallela di classi o proprietà interne del tema Material.

### Theme Token Layer

`docs/styles/theme-tokens.css` definisce i token enterprise `--dsg-*` per:

- superfici;
- testo;
- bordi;
- accenti;
- focus;
- ombre;
- `color-scheme`.

Il foglio token viene caricato una sola volta dal Theme Service tramite un elemento `link` identificato da `dsg-theme-tokens`. L'URL viene derivato dal percorso dello script, risultando compatibile con pagine a profondità differenti.

## 3. Lifecycle

Il Theme Service è registrato nel Component Registry come:

```javascript
{
  name: 'theme-service',
  order: 30
}
```

L'inizializzazione è idempotente e supporta:

- DOM ready;
- Instant Navigation;
- refresh esplicito;
- cambi del media query `prefers-color-scheme`.

## 4. Persistenza

La preferenza è salvata in:

```text
dsg-theme-preference
```

Il valore di default è `system` quando non esiste una preferenza valida o quando `localStorage` non è disponibile.

## 5. Eventi

Ogni variazione pubblica:

```text
dsg:theme-change
```

tramite Enterprise Event Bus e `CustomEvent` DOM.

Il payload include:

```javascript
{
  preference,
  resolvedTheme,
  materialTheme,
  followsSystem,
  version,
  source
}
```

## 6. Attributi DOM

Il servizio mantiene sul nodo `html`:

```text
data-dsg-theme-preference
data-dsg-theme-resolved
```

I componenti CSS devono usare tali attributi e i token `--dsg-*`, evitando dipendenze dirette dalla struttura interna di Material.

## 7. Compatibilità RC1

- pulsante Enterprise Navigation preservato;
- Light e Dark preservati;
- Instant Navigation preservata;
- Material mantiene authority sulla palette;
- nessuna logica tema aggiunta a `page-enhancements.js`;
- nessuna dipendenza esterna introdotta.

## 8. Acceptance criteria

- modalità Light, Dark e System disponibili;
- preferenza persistita;
- variazione del tema OS recepita in modalità System;
- Theme API pubblica e documentata;
- Theme Token Layer caricato una sola volta;
- controlli UI aggiornati automaticamente;
- Event Bus integrato;
- build strict e GitHub Pages positivi;
- nessuna regressione della baseline RC1.

## 9. Follow-up

- progressiva sostituzione dei colori hard-coded con token `--dsg-*`;
- branding configurabile dopo stabilizzazione RC2;
- metriche di utilizzo del tema nel WP-05;
- estensioni tema tramite Plugin SDK nel WP-06.