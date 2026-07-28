# Digital StarGate Development Playbook

## 1. Visione

Digital StarGate evolve come piattaforma modulare per l'automazione, l'osservazione, la raccolta dati e l'analisi astronomica. Lo sviluppo deve produrre capability autonome, verificabili e integrabili senza compromettere i contratti condivisi o i confini architetturali.

Il presente Playbook definisce il processo metodologico ufficiale per progettare, implementare, verificare e rilasciare le capability della Release 2.0 e successive.

Il Playbook si applica a:

- codice applicativo e infrastrutturale;
- API ed Event;
- Contracts e schemi machine-readable;
- test e osservabilità;
- documentazione tecnica e tracciabilità di release.

Non sostituisce i documenti specialistici. Per struttura della soluzione, prerequisiti e comandi operativi si usa la [Guida di sviluppo](development-guide.md). Per DTO, Command, Query, Event e regole di compatibilità si usa il documento [Contratti canonici della piattaforma](platform-contracts.md). La [Capability 001 – Observation Session](capability-001-observation-session.md) costituisce il primo esempio concreto di vertical slice. Manifest e stato della baseline sono descritti nelle [Release Notes 1.5](../releases/release-1.5-developer-edition.md). Le regole generali Docs as Code e di pubblicazione restano nel capitolo [Gestione Documentale e Release](../chapters/34-gestione-documentale-release.md).

## 2. Principi architetturali

### Clean Architecture

Le dipendenze puntano verso il nucleo applicativo e di dominio. I dettagli tecnici non governano il modello di business.

### Vertical Slice

Ogni caso d'uso attraversa i layer necessari come unità coerente e verificabile. La progettazione evita grandi blocchi orizzontali privi di valore utilizzabile.

### Capability Driven Development

Il lavoro è organizzato per capability con risultato osservabile, confini chiari, test e documentazione propri.

### Contracts First

Prima dell'implementazione si verifica se il linguaggio necessario esiste già nei Contracts canonici. Nuovi DTO, Command, Query o Event sono introdotti solo quando indispensabili.

### API First

Quando una capability espone interazioni HTTP, il comportamento pubblico è definito e verificato rispetto a OpenAPI prima della stabilizzazione dell'implementazione.

### Docs as Code

Documentazione e codice sono versionati, revisionati e validati nello stesso flusso Git. La documentazione descrive decisioni e uso reale, non intenzioni non implementate.

### Event Driven

Gli Event rappresentano fatti già avvenuti. Producer e consumer dipendono dal contratto, non dall'implementazione reciproca.

### Backward Compatibility

Le modifiche additive sono preferite. Le modifiche incompatibili richiedono nuova major version e un piano esplicito di migrazione.

## 3. Layer della piattaforma

| Layer | Responsabilità metodologica |
| --- | --- |
| `SharedKernel` | primitive interne realmente condivise e prive di dipendenze infrastrutturali |
| `Contracts` | linguaggio pubblico e inter-processo: DTO, Command, Query, Event, errori e identificativi |
| `Domain` | aggregati, Entity, Value Object, invarianti e regole di business |
| `Application` | casi d'uso, handler, validazione, mapping, porte e coordinamento |
| `Infrastructure` | repository, adapter, provider, publisher e integrazioni tecniche |
| `API` | endpoint, composizione dell'host, gestione HTTP, health e Problem Details |
| `Tests` | verifica di comportamento, integrazione, confini architetturali e convenzioni |
| Documentazione | processo, contratti, capability, decisioni, release e tracciabilità |

I dettagli della struttura corrente e dei comandi di sviluppo sono mantenuti nella [Guida di sviluppo](development-guide.md).

## 4. Capability Model

Una capability rappresenta una capacità funzionale della piattaforma con valore osservabile, confini definiti e responsabilità verificabili.

Ogni capability valuta e, quando applicabile, comprende:

- Domain;
- Application;
- Infrastructure;
- API;
- Contracts;
- Event;
- test;
- documentazione;
- osservabilità;
- Release Notes;
- ADR, quando esiste una decisione architetturale significativa;
- Definition of Done.

Non tutti gli elementi richiedono sempre un nuovo file. Quando un contratto o una decisione esiste già, la capability lo riusa e lo collega.

La [Capability 001 – Observation Session](capability-001-observation-session.md) è il riferimento iniziale per dimensione e tracciabilità di un vertical slice minimo.

## 5. Vertical Slice Workflow

### Analisi

1. Definire risultato, confini ed esclusioni.
2. Verificare documentazione, Contracts, API ed Event esistenti.
3. Identificare rischi, dipendenze e necessità di ADR.
4. Definire test e quality gate prima della scrittura del codice.

### Domain

Definire il modello minimo capace di proteggere invarianti e regole. Non inserire dettagli di persistenza, HTTP o provider esterni.

### Application

Implementare Command o Query handler, validazione, mapping e porte necessarie. Il layer coordina il caso d'uso ma non incorpora dettagli infrastrutturali.

### Infrastructure

Implementare gli adapter richiesti dalle porte. Usare InMemory per dimostrazioni e test quando la persistenza reale non è parte dello scope; usare database o provider reali solo con requisiti espliciti.

### API

Esporre esclusivamente gli endpoint richiesti, usando Contracts canonici, versionamento, Problem Details, CorrelationId e health check quando applicabile.

### Tests

Aggiungere test che dimostrino comportamento reale, integrazione e rispetto dei confini. Non creare test fittizi o privi di asserzioni significative.

### Documentation

Aggiornare il documento della capability, la navigazione e gli artefatti di release realmente interessati. Collegare i documenti canonici invece di copiarli.

### Review

La Pull Request deve consentire di valutare scope, architettura, contratti, test, documentazione, rischi e controlli eseguiti.

### Quality Gate

Eseguire i controlli indicati nella sezione 16. Un controllo non osservato resta esplicitamente pendente.

### Merge

Il merge avviene solo dopo approvazione, quality gate verde e risoluzione dei rilievi. È vietato usare il merge per nascondere controlli falliti.

### Deployment

Il deployment segue il modello previsto dalla capability e dalla release. Una capability non è dichiarata deployable se mancano configurazione, secret management, health e istruzioni operative richieste dal suo ambiente.

## 6. Dependency Rules

### Dipendenze consentite

- `Domain` può dipendere da `Contracts` e da primitive interne strettamente necessarie.
- `Application` può dipendere da `Domain`, `Contracts` e astrazioni condivise.
- `Infrastructure` può dipendere da `Application`, `Domain` e `Contracts` per implementare porte e adapter.
- `API` può comporre `Application`, `Infrastructure` e `Contracts`.
- i progetti di test possono dipendere dai layer sottoposti a verifica.

### Dipendenze vietate

- `Domain` non dipende da `Application`, `Infrastructure` o `API`;
- `Application` non dipende da implementazioni `Infrastructure`;
- `Contracts` non dipende da layer applicativi o infrastrutturali;
- un adapter non viene richiamato direttamente dal Domain;
- una capability non accede internamente a un'altra capability aggirandone Contracts o porte pubbliche.

### Isolamento

Le capability condividono solo contratti e primitive approvate. Tabelle, classi infrastrutturali o dettagli di serializzazione non diventano scorciatoie di integrazione.

Le dipendenze circolari sono vietate e devono essere intercettate tramite Architecture Test e review.

## 7. Contracts Governance

Il catalogo e le regole di versione sono mantenuti nei [Contratti canonici della piattaforma](platform-contracts.md).

### Aggiungere un DTO

Aggiungere un DTO solo quando rappresenta un confine pubblico o inter-processo non coperto dal modello esistente. Evitare DTO equivalenti con nomi diversi.

### Modificare un DTO

Preferire proprietà additive e opzionali. Cambi di significato, rimozioni o rinomine richiedono valutazione di compatibilità e versione.

### Aggiungere un Event

Un nuovo Event è ammesso quando rappresenta un fatto di dominio o piattaforma utile a consumer identificati. Devono essere definiti producer, consumer, payload, versione e schema.

### Aggiungere un Command

Un Command esprime un'intenzione con responsabilità chiara e un unico obiettivo applicativo. Non deve essere usato come contenitore generico di operazioni eterogenee.

### Aggiungere una Query

Una Query descrive una lettura priva di effetti osservabili sul dominio. Il risultato riusa DTO canonici o modelli di lettura esplicitamente approvati.

### Versionare i Contracts

Applicare Semantic Versioning e le regole di backward e forward compatibility già definite. Ogni modifica contrattuale deve aggiornare artefatti C#, OpenAPI o JSON Schema interessati nello stesso change set.

## 8. Domain Guidelines

### Aggregates

Un Aggregate protegge un confine di consistenza e modifica il proprio stato attraverso operazioni esplicite.

### Entity

Una Entity possiede identità stabile e ciclo di vita. Non viene modellata come Entity quando un Value Object è sufficiente.

### Value Object

Un Value Object è immutabile, validato e confrontato per valore. Unità e significato devono essere inequivocabili.

### Domain Events

I Domain Event descrivono fatti avvenuti nel dominio. La loro pubblicazione verso l'esterno usa gli Event canonici quando attraversa un confine di processo.

### Invariants

Le invarianti sono protette nel Domain e non affidate esclusivamente alla validazione dell'API.

### Business Rules

Le regole sono espresse con nomi e metodi comprensibili. Evitare logica di business dispersa in controller, repository o configurazioni tecniche.

## 9. Application Guidelines

### Commands e Queries

Usare i Contracts canonici. Un handler gestisce un caso d'uso specifico e mantiene separati flussi di scrittura e lettura.

### Handlers

Gli handler coordinano Domain e porte. Non contengono SQL, chiamate HTTP dirette o dettagli di provider.

### Validation

La validazione applicativa controlla completezza, formato e precondizioni del caso d'uso. Le invarianti restano nel Domain.

### Mapping

Il mapping tra Domain e DTO è esplicito, testabile e centralizzato nel perimetro della capability.

### Ports

Repository, publisher e provider sono esposti come interfacce definite dal layer che li usa.

### Dependency Injection

Le registrazioni sono raggruppate per layer o capability. L'API compone le dipendenze senza conoscere dettagli interni non necessari.

## 10. Infrastructure Guidelines

### Repository e Persistence

Il repository implementa una porta applicativa o di dominio. La scelta di persistenza non modifica il contratto del caso d'uso.

### Adapter e Provider

Ogni sistema esterno è incapsulato in un adapter con gestione esplicita di errori, timeout, retry e osservabilità quando richiesti.

### Publisher

Un publisher espone la pubblicazione degli Event senza vincolare Application a uno specifico Event Bus.

### External Systems

Le integrazioni esterne devono avere confini, configurazione, health e test di integrazione chiaramente identificati.

### InMemory

Le implementazioni InMemory sono ammesse per vertical slice, test e sviluppo locale. Non devono essere presentate come persistenza durevole.

### Database

Un database viene introdotto con schema, migration, configurazione, strategia di test e note operative. È vietato accedere direttamente al database di un'altra capability.

## 11. API Guidelines

- adottare REST per le risorse HTTP della piattaforma;
- versionare gli endpoint nel percorso previsto da OpenAPI;
- utilizzare Problem Details per gli errori HTTP;
- propagare o generare `CorrelationId`;
- esporre health check coerenti con le dipendenze reali;
- mantenere OpenAPI allineata al comportamento pubblico;
- evitare modelli API duplicati quando esiste un DTO canonico.

Le definizioni correnti di OpenAPI, error model e versionamento sono descritte nei [Contratti canonici della piattaforma](platform-contracts.md).

## 12. Testing Strategy

### Unit Test

Verificano invarianti, transizioni e comportamento isolato di Domain e componenti puri.

### Application Test

Verificano handler, validazione, mapping e interazione con porte controllate.

### Integration Test

Verificano composizione DI, API, serializzazione, repository, provider e dipendenze tecniche interessate.

### Architecture Test

Verificano dipendenze consentite, isolamento dei layer e assenza di riferimenti vietati.

### Convention Test

Verificano convenzioni ripetibili quali naming, registrazioni, serializzazione o conformità dei Contracts quando il rischio giustifica l'automazione.

### Quality Rules

I test devono essere deterministici, leggibili e indipendenti dall'ordine di esecuzione. Ogni test deve dimostrare un comportamento o un vincolo reale.

### Coverage philosophy

La coverage è un indicatore diagnostico, non un obiettivo numerico universale. La priorità è coprire invarianti, errori significativi, integrazioni e percorsi critici.

## 13. Observability

Ogni capability definisce il livello di osservabilità necessario al proprio funzionamento:

- structured logging con proprietà stabili;
- metriche per volume, esito, latenza e risorse quando utili;
- tracing distribuito per flussi tra componenti;
- propagazione di CorrelationId e CausationId;
- telemetria coerente con le convenzioni OpenTelemetry canoniche.

Non registrare secret, credenziali o payload sensibili. Le convenzioni di naming e i Value Object sono descritti nei [Contratti canonici della piattaforma](platform-contracts.md).

## 14. Documentation Process

La documentazione viene aggiornata nello stesso change set quando cambia il comportamento o il processo.

| Artefatto | Quando aggiornarlo |
| --- | --- |
| Developer Guide | cambiano prerequisiti, struttura o comandi comuni |
| Capability Document | cambia scope, flusso, endpoint, limiti o comportamento della capability |
| Release Notes | cambia il contenuto consegnato dalla release |
| ADR | viene assunta una decisione architetturale significativa con alternative e conseguenze |
| MkDocs Navigation | viene pubblicato, spostato o ritirato un documento navigabile |
| Roadmap | cambia sequenza, priorità o perimetro delle capability future |
| Manifest | cambia l'elenco ufficiale degli artefatti della release |

Le regole generali di fonte unica, pubblicazione e conservazione non sono duplicate qui e restano nel capitolo [Gestione Documentale e Release](../chapters/34-gestione-documentale-release.md).

## 15. Git Workflow

### Naming Branch

Usare branch dedicati e leggibili, ad esempio:

```text
feature/<capability>-<scope>
fix/<capability>-<issue>
docs/<document-or-scope>
release/<version>-<scope>
hotfix/<version>-<issue>
```

Il branch parte dalla baseline approvata prevista dal piano di rilascio.

### Commit

Usare commit atomici in stile Conventional Commits, con scope coerente:

```text
feat(session): implement create handler
test(session): add API integration coverage
docs(capability): document observation session
```

### Pull Request

La PR descrive obiettivo, scope, esclusioni, file, test, controlli eseguiti, controlli pendenti e rischi residui.

### Review

La review valuta correttezza, semplicità, contratti, dipendenze, test, sicurezza, osservabilità e documentazione.

### Merge

Il merge è consentito solo con base corretta, review approvata e quality gate verde. Non usare force push o riscritture distruttive senza autorizzazione esplicita.

### Hotfix

Un hotfix modifica il minimo indispensabile, include test di regressione e documenta impatto e strategia di riallineamento dei branch attivi.

### Release

Tag, manifest, changelog e artifact seguono il processo ufficiale descritto in [Gestione Documentale e Release](../chapters/34-gestione-documentale-release.md).

## 16. Quality Gates

Ogni capability deve verificare, quando applicabile:

```text
restore
build Release
test
format
MkDocs strict
zero warning
Architecture Test
link validation
```

Comandi di riferimento:

```powershell
dotnet restore DigitalStarGate.sln
dotnet build DigitalStarGate.sln --configuration Release
dotnet test DigitalStarGate.sln --configuration Release
dotnet format DigitalStarGate.sln --verify-no-changes
python -m pip install --requirement requirements.txt
mkdocs build --strict
```

Un controllo è dichiarato superato solo quando il relativo risultato è stato osservato. Eccezioni e incompatibilità devono essere motivate nella PR.

## 17. Definition of Done

Una capability è completata quando:

- scope ed esclusioni sono espliciti;
- il comportamento richiesto è implementato;
- Contracts esistenti sono riusati e le eventuali modifiche sono versionate;
- invarianti e regole risiedono nel layer corretto;
- dipendenze e isolamento rispettano l'architettura;
- API ed Event sono coerenti con gli artefatti canonici;
- configurazione, error handling e osservabilità sono adeguati allo scope;
- test reali coprono comportamento e rischi principali;
- quality gate applicabili sono verdi;
- documentazione, navigazione e Release Notes sono aggiornate quando necessario;
- ADR è presente se la capability introduce una decisione architetturale significativa;
- non sono presenti secret, file generati indesiderati, warning o dipendenze circolari;
- la Pull Request è approvata e pronta al merge;
- rischi residui e attività differite sono dichiarati.

La Definition of Done non può essere soddisfatta tramite dichiarazioni: deve essere supportata da evidenze osservabili nel repository, nei test e nella pipeline.