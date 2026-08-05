# ADR-006 – Enterprise Plugin SDK

**Status:** Accepted  
**Date:** 2026-08-05  
**Release:** RC2

## Context

Il Digital StarGate Enterprise Portal dispone di Component Registry, Enterprise Event Bus, lifecycle comune e servizi pubblici modulari. L'aggiunta di nuove capability direttamente nel core aumenterebbe l'accoppiamento, distribuirebbe responsabilità trasversali e renderebbe più fragile Instant Navigation.

## Decision Drivers

- estendere il portale senza modificare il core per ogni capability;
- mantenere dependency resolution e lifecycle deterministici;
- isolare errori di initialize e dispose;
- rendere capability e provider interrogabili;
- conservare plugin e manifest nel repository;
- impedire caricamento dinamico non governato e accesso alle API private;
- integrare i test nel quality gate esistente senza nuove dipendenze.

## Considered Options

1. Estendere direttamente `dsg-enterprise-core.js` per ogni nuova capability.
2. Usare moduli indipendenti caricati senza registro o lifecycle comune.
3. Adottare un Enterprise Plugin SDK sopra il core RC2 esistente.

## Decision

Adottare l'opzione 3.

L'Enterprise Plugin SDK è composto da:

- `DSGPluginRegistry` per manifest, registrazione idempotente e capability discovery;
- `DSGPluginDependencyResolver` per dipendenze mancanti, cycle detection e ordine topologico deterministico;
- `DSGPluginRuntime` per initialize, dispose, context injection e failure isolation;
- `DSGPluginProviderContracts` per validare provider associati a capability pubbliche.

Il contratto pubblico iniziale usa `apiVersion: '1'`.

Il Plugin SDK riutilizza Component Registry ed Event Bus ma non ne duplica le responsabilità. Il core continua a essere l'autorità del lifecycle dei componenti; il runtime gestisce esclusivamente il lifecycle dei plugin registrati.

## Regole obbligatorie

- ID plugin lowercase kebab-case e univoco;
- versione del plugin in semantic versioning;
- dipendenze esplicite e acicliche;
- registrazione idempotente solo per definizioni equivalenti;
- inizializzazione nell'ordine risolto e dispose in ordine inverso;
- cleanup prima del nuovo lifecycle cycle;
- plugin e manifest versionati nel repository;
- nessun `eval` o caricamento automatico da URL esterni;
- uso esclusivo delle API pubbliche dei servizi;
- nessun comando operativo o di safety attraverso il Plugin SDK;
- nessuna promozione automatica di stati di governance.

## Provider Contracts iniziali

- `operations-widget`;
- `search-provider`;
- `scientific-view`;
- `repository-intelligence-provider`;
- `navigation-extension`.

## Consequences

### Positive

- core più stabile e meno accoppiato;
- estensioni interrogabili e testabili;
- lifecycle compatibile con Instant Navigation;
- dipendenze e failure espliciti;
- possibilità di aggiungere provider senza modificare il runtime.

### Negative

- maggiore disciplina richiesta nella dichiarazione di manifest e capability;
- ordine di caricamento degli asset da governare;
- necessità di mantenere compatibilità tra versioni del contratto SDK.

### Risks

- plugin che non rimuovono listener o DOM durante il cleanup;
- dipendenze dichiarate in modo incompleto;
- uso improprio del catalogo servizi come accesso a implementazioni interne;
- crescita incontrollata dei Provider Contracts.

## Validation

- suite Node.js dependency-free in `.github/scripts/test-plugin-sdk.mjs`;
- manifest validation e duplicate detection;
- missing dependency e cycle detection;
- ordine deterministico di initialize e reverse dispose;
- failure isolation;
- provider validation;
- cleanup e destroy tra lifecycle cycle;
- esecuzione automatica nel workflow `Developer Foundation`;
- build MkDocs strict.

## Traceability

- [WP-06 — Enterprise Plugin SDK](packages/WP-06-Enterprise-Plugin-SDK.md)
- [Plugin SDK Specification](../developer/plugin-sdk-specification.md)
- [Come sviluppare un plugin](../developer/how-to-build-a-plugin.md)
- [Operations Center](../operations/index.md)
- [RC2 Roadmap](../project/RC2_ROADMAP.md)