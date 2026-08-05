# Digital StarGate Enterprise Portal — RC1 Baseline

| Campo | Valore |
|---|---|
| Identificativo | DSG-BSL-RC1-001 |
| Versione | 1.0 |
| Stato | Frozen |
| Data baseline | 05/08/2026 |
| Commit di riferimento | `801c6246983af85fba571515f48fc038cccfcbcf` |

## 1. Scopo

Congelare la baseline funzionale, architetturale e operativa della Digital StarGate Enterprise Portal RC1 dopo la chiusura della hotfix RC1-HF01.

Questa baseline è il riferimento per ogni confronto con RC2 e release successive.

## 2. Componenti inclusi

- Home Enterprise;
- Enterprise Navigation;
- Documentation Center;
- Roadmap Center;
- Architecture Center;
- Scientific Platform;
- Scientific Session Catalog;
- Scientific Session Detail;
- Scientific Data Engine;
- Mission Control;
- Repository Intelligence;
- Scientific Intelligence;
- Project Governance Center;
- Enterprise Theme Adapter.

## 3. Componenti JavaScript congelati

- `homepage-effects.js`;
- `latest-observation.js`;
- `mission-control.js`;
- `nav-scroll.js`;
- `page-enhancements.js` — Navigation Manager;
- `roadmap.js`;
- `scientific-data-engine.js`;
- `scientific-session-explorer.js`;
- `scientific-session-detail.js`;
- `dsg-theme-manager.js` — Material-native Theme Adapter.

## 4. API pubbliche congelate

Lo Scientific Data Engine espone:

```javascript
loadCatalog()
getSessions()
getSession()
getTargets()
getYears()
getKPIs()
filterSessions()
getKnowledgeGraph()
getLineage()
```

Ogni variazione breaking richiede una nuova major o un ADR.

## 5. Invarianti architetturali

- repository GitHub come fonte autorevole;
- dataset JSON come proiezioni;
- nessun accesso scientifico parallelo fuori dallo Scientific Data Engine;
- JavaScript separato per responsabilità;
- CSS separato per componente;
- nessun comando diretto dal portale agli apparati;
- Material for MkDocs mantiene authority su palette, persistenza e lifecycle;
- `page-enhancements.js` resta privo di logica tema;
- `dsg-theme-manager.js` resta un adapter sottile verso i controlli nativi Material;
- Instant Navigation supportata tramite inizializzazione idempotente.

## 6. Quality gate della baseline

Verificati sul commit di riferimento:

- restore .NET: successo;
- build .NET: successo;
- test .NET: successo;
- format verification: successo;
- `mkdocs build --strict`: successo;
- GitHub Pages build: successo;
- artifact Pages: generato;
- deploy Pages: successo;
- verifica manuale Light/Dark: positiva;
- persistenza tema: positiva;
- rendering Home e pagine interne: positivo.

## 7. Debito tecnico residuo

Restano fuori dalla baseline funzionale e sono governati separatamente:

- razionalizzazione workflow documentali;
- riallineamento README root;
- consistency checks tra roadmap autorevole e proiezioni JSON;
- riduzione progressiva degli script inline;
- contestualizzazione del materiale storico;
- Knowledge Graph machine-readable;
- modalità tema `system` come evoluzione RC2.

## 8. Compatibilità

RC2 deve preservare:

- URL pubblici esistenti salvo redirect governati;
- struttura dei dati scientifici consumata dai componenti RC1;
- comportamento della navigazione enterprise;
- compatibilità Light/Dark;
- assenza di regressioni nelle pagine statiche e dinamiche.

## 9. Modifiche consentite in RC2

Sono consentite solo modifiche compatibili o esplicitamente governate dalla roadmap RC2.

Qualunque deviazione da questa baseline richiede:

- registrazione nel Decision Log;
- aggiornamento del backlog;
- ADR se cambia boundary, authority, contratto o invarianti;
- aggiornamento della baseline RC2.

## 10. Stato

La RC1 è dichiarata stabile, pubblicata e congelata. Le nuove evoluzioni appartengono alla RC2.