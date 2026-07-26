# DSG-SOP-001 - Standard Operating Procedures

| Campo | Valore |
|---|---|
| Documento | Standard Operating Procedures enterprise |
| Identificativo | `DSG-SOP-001` |
| Roadmap | `DSG-MR-001` |
| Versione | 1.0 |
| Stato | Approvata per revisione |
| Owner | Massimo Mainini |
| Data baseline | 26/07/2026 |

## 1. Scopo

Questo documento definisce le procedure operative standard necessarie a governare documentazione, dati, release e incidenti nel contesto `DSG-MR-001`.

Le SOP non duplicano le procedure specialistiche già presenti nei capitoli tecnici: le collegano a trigger, ruoli, output e controlli enterprise.

## 2. SOP documentazione - `DSG-SOP-DOC-001`

| Campo | Valore |
|---|---|
| Trigger | Nuovo documento o modifica strutturale |
| Ruoli | Documentation Owner, Reviewer |
| Output | Documento aggiornato, registri aggiornati, navigazione coerente |
| Controlli | `DSG-CTL-DOC-001`, `DSG-CTL-QA-001` |

### Passi

1. Identificare il documento impattato.
2. Verificare se la modifica è collegata a un requisito, rischio o deliverable.
3. Aggiornare il contenuto mantenendo lo stile MkDocs.
4. Aggiornare `mkdocs.yml` se la pagina deve essere pubblicata.
5. Aggiornare registri e change log.
6. Verificare link interni e marcatori aperti.
7. Preparare commit e PR.

### Criterio di controllo

La modifica è accettabile quando il documento è navigabile, tracciato e privo di marcatori aperti.

## 3. SOP dati e analytics - `DSG-SOP-DATA-001`

| Campo | Valore |
|---|---|
| Trigger | Nuova sessione osservativa, ricalcolo KPI o variazione schema |
| Ruoli | Data Owner, Architecture Owner |
| Output | Dataset validato, report aggiornato, eventuale nota di release |
| Controlli | `DSG-CTL-DATA-001` |

### Passi

1. Identificare origine dati e periodo.
2. Verificare completezza minima di sessione, target, integrazione e qualità guida.
3. Applicare quality gate warehouse/analytics.
4. Registrare dati mancanti come `N/D` quando il valore non è disponibile.
5. Aggiornare dashboard o report collegati.
6. Documentare anomalie e record esclusi.

### Criterio di controllo

I KPI pubblicati devono indicare fonte, periodo e stato di qualità.

## 4. SOP release - `DSG-SOP-REL-001`

| Campo | Valore |
|---|---|
| Trigger | Preparazione release documentale o milestone enterprise |
| Ruoli | Release Owner, Documentation Owner, Reviewer |
| Output | Release notes, readiness checklist, rollback plan |
| Controlli | `DSG-CTL-REL-001`, `DSG-CTL-QA-001` |

### Passi

1. Confermare deliverable e milestone completate.
2. Verificare navigazione e registri.
3. Controllare link e sezioni incomplete.
4. Preparare note di release.
5. Definire criteri di rollback.
6. Aprire PR verso `main`.
7. Conservare evidenze di validazione.

### Criterio di controllo

La release è pronta quando tutte le condizioni di readiness sono soddisfatte o documentate come follow-up non bloccanti.

## 5. SOP incident - `DSG-SOP-INC-001`

| Campo | Valore |
|---|---|
| Trigger | Stato non sicuro, perdita accesso, errore cupola, meteo avverso o blocco EAGLE |
| Ruoli | Operations Owner, Infrastructure Owner |
| Output | Stato conservativo, log incidente, azione correttiva |
| Controlli | `DSG-CTL-SAF-001`, `DSG-CTL-OPS-001` |

### Passi

1. Assumere la condizione più conservativa.
2. Verificare stato meteo, copertura, montatura e alimentazione.
3. Se la chiusura è sicura, completare la chiusura osservatorio.
4. Se lo stato è incerto, evitare comandi potenzialmente distruttivi.
5. Registrare timestamp, sintomo, azione e risultato.
6. Aprire un post-mortem se l'incidente è ricorrente o ad alto impatto.
7. Aggiornare rischio, controllo o SOP interessata.

### Criterio di controllo

La procedura è chiusa solo quando stato fisico, stato documentale e azione correttiva sono allineati.

## 6. SOP change management - `DSG-SOP-CHG-001`

| Campo | Valore |
|---|---|
| Trigger | Modifica hardware, software, dati, architettura o governance |
| Ruoli | Governance Owner, Architecture Owner, Documentation Owner |
| Output | Change log, ADR se necessario, registri aggiornati |
| Controlli | `DSG-CTL-ADR-001`, `DSG-CTL-DOC-001` |

### Passi

1. Descrivere cambiamento, motivazione e impatto.
2. Classificare l'area interessata.
3. Valutare rischi e dipendenze.
4. Redigere ADR se la decisione è strutturale.
5. Aggiornare registri e documenti.
6. Validare con checklist o test appropriati.
7. Chiudere il cambiamento nella release o nel change log.

## 7. Collegamenti

- [DSRA](DSRA-risk-assessment.md)
- [Registri](registries/index.md)
- [Governance](governance.md)
- [Release documentation](release-documentation.md)
