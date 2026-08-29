# Digital StarGate

Repository principale della piattaforma **Digital StarGate** per l'osservatorio remoto di Manciano (GR).

Il repository non contiene soltanto il manuale tecnico: governa documentazione operativa, architettura enterprise, portale MkDocs, telemetria e Observatory Status, catalogo scientifico e session reporting, automazioni, contratti, tooling e quality gate.

## Punto di ingresso

Per qualsiasi attività di sviluppo, manutenzione, analisi o assistenza automatizzata partire da:

- [`AI_BOOTSTRAP.md`](AI_BOOTSTRAP.md) — bootstrap canonico e gerarchia delle fonti;
- [`docs/project/index.md`](docs/project/index.md) — Project Governance Center;
- [`docs/project/BACKLOG.md`](docs/project/BACKLOG.md) — lavoro pianificato e priorità;
- [`docs/project/TECHNICAL_DEBT.md`](docs/project/TECHNICAL_DEBT.md) — debito tecnico governato;
- [`docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md`](docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md) — roadmap architetturale autorevole.

**Regola fondamentale:** il repository e le evidence versionate sono la source of truth. Dataset JSON, dashboard e pagine del portale sono proiezioni e non sostituiscono le fonti canoniche.

## Cosa contiene

Il repository riunisce quattro prodotti correlati:

1. **Manuale tecnico dell'osservatorio** — infrastruttura, rete, alimentazione, cupola, montatura, camere, N.I.N.A., PHD2, CPWI/ASCOM, meteo, safety, recovery e manutenzione.
2. **Enterprise Architecture Repository** — Architecture Package AP-001–AP-015, ADR, capability, assessment ARB, evidence e roadmap.
3. **Digital StarGate Enterprise Portal** — sito MkDocs Material con Mission Control, Observatory Status, Roadmap, Architecture Center, Scientific Platform, catalogo sessioni e viste analytics.
4. **Developer Foundation** — solution .NET, contratti, test, script, pipeline scientifiche, workflow CI/CD e tooling di governance.

La mappa completa dei domini e delle responsabilità è in [`docs/project/REPOSITORY_KNOWLEDGE_MAP.md`](docs/project/REPOSITORY_KNOWLEDGE_MAP.md).

## Observatory Status e telemetria

La sezione **Observatory Status** pubblica una proiezione read-only dello stato osservato dell'osservatorio.

Le source integrate comprendono la telemetria N.I.N.A. per i sistemi osservati e gli adapter Digital StarGate per **Network** e **Power**. La perdita o la mancata freschezza della source decade in modo fail-safe a `UNKNOWN`/`STALE`.

Per Power, il sensing della presenza rete è basato sul TS Shelter SafetyMonitor/J6; per Network, l'osservazione è raccolta dal boundary N.I.N.A. e non introduce funzioni di controllo del router.

Il portale **non è una Safety Authority e non comanda direttamente gli apparati**. Gli interlock locali, il controller fisico e la catena safety dell'osservatorio restano autorevoli.

## Scientific platform e session reporting

Il repository contiene il catalogo delle sessioni scientifiche, metadata governati, lineage/provenance, proiezioni per il portale e pipeline di reporting delle sessioni N.I.N.A./PHD2/CloudWatcher.

I dataset pubblicati sotto `docs/data` sono proiezioni generate. Le evidence scientifiche e operative versionate restano la fonte primaria.

## Struttura principale

```text
.github/                 workflow, roadmap source, evidence e quality gate
contracts/               contratti OpenAPI / eventi / schema
DigitalStarGate.*/       Developer Foundation .NET
docs/                    portale, manuale, architettura, governance e proiezioni
dsg-analytics/           analytics e generatori delle projection
integrations/             integrazioni runtime, incluso plug-in N.I.N.A.
scripts/                  automazione, telemetry e tooling operativo
data/                     evidence/session package governati
release/                  artifact documentali generati
```

La struttura reale del repository prevale sempre su questo riepilogo.

## Documentazione e GitHub Pages

La pubblicazione GitHub Pages ha un solo owner:

```text
.github/workflows/deploy-pages.yml
```

Il workflow genera le projection governate, costruisce il sito con `mkdocs.pages.yml`, verifica l'integrità dell'artifact e pubblica su GitHub Pages.

Il workflow:

```text
.github/workflows/docs.yml
```

è **validation-only** e non dispone dei permessi di deploy Pages.

## Manuale Word

Il manuale tecnico `DSG-TM-001` continua a essere prodotto dal repository tramite il workflow dedicato:

```text
.github/workflows/word.yml
```

che genera l'artifact Word dalla documentazione governata.

## Developer Foundation

La solution principale è:

```text
DigitalStarGate.sln
```

La baseline di sviluppo e le regole architetturali sono definite nei documenti del Project Governance Center e nei file di configurazione root (`global.json`, `Directory.Build.props`, `Directory.Packages.props`).

Non dedurre la toolchain da un ambiente runtime come EAGLE: gli SDK di sviluppo e la CI sono governati separatamente dagli host operativi.

## Regole operative essenziali

- una milestone alla volta: repository truth → architettura → implementazione → test → commit → workflow → Pages → governance;
- nessuna affermazione di build, deploy o acceptance senza evidence verificata;
- nessuna duplicazione di authority fra portale, plugin e controller locali;
- nessun comando diretto UI-to-device;
- dataset e dashboard sono projection, non source of truth;
- safety e security prevalgono sulla continuità;
- modifiche strutturali a boundary, authority o contratti richiedono governance architetturale appropriata.

## Stato e roadmap

Il README non replica intenzionalmente lo stato dinamico del programma, per evitare una seconda fonte di verità.

Per lo stato corrente consultare, nell'ordine:

1. [`docs/project/BACKLOG.md`](docs/project/BACKLOG.md);
2. [`docs/project/TECHNICAL_DEBT.md`](docs/project/TECHNICAL_DEBT.md);
3. [`AMP-002`](docs/architecture/assessments/AMP-002-Architecture-Program-Roadmap-Realignment.md);
4. workflow, commit ed evidence effettivi del repository.

---

**Digital StarGate** — osservatorio remoto, piattaforma scientifica e repository enterprise governati come un unico sistema.