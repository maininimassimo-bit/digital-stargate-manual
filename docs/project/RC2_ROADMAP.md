# Digital StarGate Enterprise Portal — RC2 Roadmap

| Campo | Valore |
|---|---|
| Identificativo | DSG-RC2-RDM-001 |
| Versione | 1.4 |
| Stato | Active |
| Data avvio | 05/08/2026 |
| Baseline di partenza | `docs/architecture/baselines/RC1_BASELINE.md` |

## 1. Obiettivo

Portare il Digital StarGate Enterprise Portal dalla baseline RC1 a una piattaforma estendibile, osservabile e governata tramite componenti con lifecycle comune, servizi condivisi e capability modulari.

## 2. Principi

- nessuna regressione rispetto alla baseline RC1;
- compatibilità degli URL pubblici e delle API scientifiche;
- responsabilità singola per ogni componente;
- lifecycle, event bus e registry condivisi;
- dati scientifici accessibili solo tramite Scientific Data Engine;
- nessuna nuova dipendenza esterna senza approvazione;
- ogni Work Package deve chiudere CI, Pages, governance e acceptance prima del successivo.

## 3. Work Package

| WP | Titolo | Stato | Outcome |
|---|---|---|---|
| WP-01 | Enterprise Foundation Framework | Completed | Component Registry, lifecycle comune, Event Bus e bootstrap centralizzato |
| WP-02 | Scientific Platform 2.0 | Completed | SDE 2.1 con cache, eventi, metriche, Session Store indicizzato e componenti scientifici migrati |
| WP-03 | Enterprise Theme Framework | Completed | modalità System, Theme API, token enterprise e adapter Material governato |
| WP-04 | Enterprise Search Center | Completed | ricerca federata, filtri, ranking e integrazione con i servizi della piattaforma |
| WP-05 | Operations Dashboard | Completed | repository health, CI/CD, runtime telemetry e KPI piattaforma |
| WP-06 | Enterprise Plugin SDK | Completed | estensioni modulari senza modifica del core |

## 4. Sequenza

```text
WP-01 Foundation [Completed]
  -> WP-02 Scientific Platform 2.0 [Completed]
  -> WP-03 Theme Framework [Completed]
  -> WP-04 Search Center [Completed]
  -> WP-05 Operations Dashboard [Completed]
  -> WP-06 Plugin SDK [Completed]
  -> RC2 Baseline and Acceptance
```

## 5. Gate trasversali

Ogni WP deve superare:

- Architecture Review interna;
- compatibility check con RC1;
- `mkdocs build --strict`;
- GitHub Actions verdi;
- artifact Pages verificato;
- test Instant Navigation;
- aggiornamento Backlog, Decision Log e Technical Debt;
- documento di closure del WP.

## 6. Definition of Done RC2

RC2 è completata quando tutti i WP sono chiusi, la baseline RC2 è congelata, le API pubbliche sono documentate, la migrazione da RC1 è verificata e GitHub Pages è accettata senza regressioni.
