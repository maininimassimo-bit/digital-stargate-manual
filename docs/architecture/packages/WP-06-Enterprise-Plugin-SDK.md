# WP-06 — Enterprise Plugin SDK

| Campo | Valore |
|---|---|
| Identificativo | DSG-RC2-WP06 |
| Versione | 0.1 |
| Stato | In Progress |
| Data avvio | 05/08/2026 |
| Baseline sorgente | DSG-BSL-RC1-001 |

## 1. Scopo

Definire e implementare un SDK leggero per estendere il Digital StarGate Enterprise Portal senza modificare il core della piattaforma e senza distribuire logica trasversale nei componenti esistenti.

## 2. Obiettivi

Il Plugin SDK dovrà consentire di:

- registrare estensioni tramite contratto stabile;
- dichiarare dipendenze e ordine di inizializzazione;
- utilizzare Component Registry ed Enterprise Event Bus;
- aggiungere provider per servizi, widget e data source;
- isolare errori e lifecycle delle estensioni;
- esporre metadata e capability interrogabili;
- preservare la compatibilità con Instant Navigation;
- evitare modifiche dirette al core per ogni nuova capability.

## 3. Non obiettivi

WP-06 non introduce:

- esecuzione di codice remoto;
- download dinamico di plugin da marketplace esterni;
- accesso diretto ai dataset scientifici;
- bypass del Scientific Data Engine;
- comandi operativi o di safety;
- dipendenze JavaScript esterne non approvate.

## 4. Principi architetturali

- plugin manifest come contratto dichiarativo;
- lifecycle unico e governato;
- registrazione idempotente;
- dependency resolution deterministica;
- failure isolation;
- API pubbliche versionate;
- capability discovery;
- nessuna dipendenza implicita da DOM o ordine casuale degli script;
- nessuna duplicazione del Component Registry.

## 5. Contratto preliminare

Un plugin dovrà dichiarare almeno:

```javascript
{
  id: 'plugin-id',
  version: '1.0.0',
  apiVersion: '1',
  capabilities: [],
  dependencies: [],
  initialize(context) {},
  dispose(context) {}
}
```

Il contratto definitivo sarà congelato dopo il primo incremento implementativo e i relativi compatibility test.

## 6. Layer previsti

### Plugin Registry

Responsabile di:

- registrazione;
- validazione del manifest;
- rilevazione duplicati;
- stato e metadata;
- capability discovery.

### Dependency Resolver

Responsabile di:

- verifica delle dipendenze;
- ordinamento deterministico;
- rilevazione cicli;
- gestione delle dipendenze mancanti.

### Plugin Runtime

Responsabile di:

- initialize/dispose;
- isolamento degli errori;
- context injection;
- integrazione con lifecycle ed Event Bus;
- supporto a Instant Navigation.

### Provider Contracts

Prime categorie previste:

- `operations-widget`;
- `search-provider`;
- `scientific-view`;
- `repository-intelligence-provider`;
- `navigation-extension`.

## 7. Context API preliminare

Il runtime potrà fornire al plugin un context read-only contenente:

- `events`;
- `components`;
- `services`;
- `theme`;
- `navigation`;
- `logger`;
- metadata del plugin;
- lifecycle cycle corrente.

L'accesso ai servizi dovrà avvenire tramite contratti pubblici e capability dichiarate.

## 8. Sicurezza e governance

- nessun `eval` o esecuzione dinamica di stringhe;
- nessun caricamento automatico da URL esterni;
- manifest e plugin versionati nel repository;
- errori del plugin non devono bloccare il core;
- permessi/capability espliciti;
- log e telemetria pubblicati tramite Event Bus;
- nessuna promozione automatica di stati di governance.

## 9. Milestone interne

1. inventario dei punti di estensione esistenti;
2. definizione del manifest e delle API;
3. implementazione Plugin Registry;
4. dependency resolver e cycle detection;
5. runtime initialize/dispose;
6. primo provider dimostrativo;
7. integration test con Instant Navigation;
8. documentazione, quality gate e completion report.

## 10. Acceptance criteria preliminari

- registrazione plugin idempotente;
- rifiuto dei manifest non validi;
- rilevazione di ID duplicati;
- dependency resolution deterministica;
- rilevazione dei cicli;
- isolamento degli errori di initialize/dispose;
- capability discovery interrogabile;
- nessuna regressione del Component Registry;
- nessuna dipendenza esterna;
- workflow GitHub e Pages verdi;
- documentazione pubblica del contratto SDK.

## 11. Primo incremento

Il primo incremento implementativo sarà il `DSGPluginRegistry`, costruito sopra il lifecycle RC2 senza sostituire o duplicare il Component Registry.