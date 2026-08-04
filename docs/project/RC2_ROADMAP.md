# Digital StarGate Enterprise Portal — RC2 Roadmap

| Campo | Valore |
|---|---|
| Identificativo | DSG-RC2-RDM-001 |
| Versione | 1.0 |
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
| WP-01 | Enterprise Foundation Framework | In Progress | Component Registry, lifecycle comune, Event Bus e bootstrap centralizzato |
| WP-02 | Scientific Platform 2.0 | Planned | SDE v2 con cache, eventi, lazy loading, metriche e contratti |
| WP-03 | Enterprise Theme Framework | Planned | modalità System, Theme API e branding governato |
| WP-04 | Enterprise Search Center | Planned | ricerca federata e filtri enterprise |
| WP-05 | Operations Dashboard | Planned | repository health, CI/CD e KPI piattaforma |
| WP-06 | Enterprise Plugin SDK | Planned | estensioni modulari senza modifica del core |

## 4. Sequenza

```text
WP-01 Foundation
  -> WP-02 Scientific Platform 2.0
  -> WP-03 Theme Framework
  -> WP-04 Search Center
  -> WP-05 Operations Dashboard
  -> WP-06 Plugin SDK
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