# Digital StarGate Enterprise Portal — RC2 Baseline

| Campo | Valore |
|---|---|
| Identificativo | `DSG-BSL-RC2-001` |
| Versione | 1.0 |
| Stato | Frozen / Accepted |
| Data baseline | 23/09/2026 |
| Baseline precedente | `docs/architecture/baselines/RC1_BASELINE.md` |
| Owner | Massimo Mainini |

## Scopo

Congelare la baseline RC2 dopo la chiusura dei sei Work Package Enterprise Portal e la verifica integrata post-merge. RC2 estende RC1 con foundation, Scientific Data Platform, tema enterprise, Search Center, Operations Dashboard e Plugin SDK, mantenendo compatibilità degli URL, delle API scientifiche e dei confini read-only.

## Componenti accettati

- Component Registry, lifecycle comune, Event Bus e bootstrap centralizzato;
- Scientific Data Engine 2.1, cache, eventi, metriche, Session Store indicizzato e componenti scientifici migrati;
- Enterprise Theme Framework con Theme API, modalità System e adapter Material governato;
- Enterprise Search Center con ricerca federata e filtri;
- Operations Dashboard con repository health, CI/CD, runtime telemetry e KPI;
- Enterprise Plugin SDK senza modifica del core.

## Invarianti RC1 preservati

- GitHub resta la fonte autorevole e i JSON restano proiezioni governate;
- le API pubbliche dello Scientific Data Engine restano compatibili;
- gli URL pubblici, la navigazione enterprise, Light/Dark e Instant Navigation restano disponibili;
- non esiste un comando diretto dal portale agli apparati;
- nessun broker, remediation, target selection automatica o Safety Authority è introdotto;
- ogni inizializzazione di componente resta idempotente con Instant Navigation.

## Evidenza di acceptance

- WP-01–WP-06: completion report `Accepted`;
- `mkdocs build --strict`: verificato;
- Developer Foundation e workflow applicabili: verdi sul commit `9108dcab`;
- GitHub Pages deploy: run `35794969006`, successo;
- Word generation: run `35794968948`, successo;
- Roadmap pubblica verificata dopo il deploy, con RC2 baseline chiusa e AP-015 come successore;
- test di compatibilità RC1, API pubbliche e Instant Navigation ricondotti ai report WP e alla baseline RC1.

## Limiti e successore

Questa baseline non autorizza una tecnologia di knowledge graph, un provider esterno, un runtime AI, un event broker decisionale o una nuova authority. Il successore governato è AP-015 — Scientific Knowledge Platform Architecture, limitato alla preparazione architetturale e semantica di CAP-40.
