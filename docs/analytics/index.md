# Digital StarGate Analytics

Benvenuto nel portale Analytics del progetto **Digital StarGate**.

Questa sezione raccoglie gli strumenti di analisi, i report e le projection governate generate dalla pipeline di elaborazione delle sessioni osservative.

---

## Accesso rapido

- [Dashboard Analytics](dashboard.html)
- [Session Comparison](../session-comparison/)
- [Equipment Performance](../equipment-performance/)
- [Validazione dello storico](history-validation.md)
- [Riepilogo configurazioni](configuration-summary.md)

[Apri Session Comparison](../session-comparison/){ .md-button .md-button--primary }

La vista **Session Comparison** confronta in modalità read-only tutte le sessioni che dispongono di evidence comparabile per la dimensione pubblicata. Le sessioni non comparabili restano esplicitamente visibili come exclusions; il portale non crea ranking, score, soglie o decisioni di acceptance.

---

## Cosa puoi consultare

La dashboard e le projection consentono di analizzare:

- andamento delle sessioni osservative;
- ore complessive di acquisizione;
- numero di immagini raccolte;
- target osservati;
- distribuzione dei filtri utilizzati;
- configurazioni strumentali;
- statistiche operative;
- confronto descrittivo multi-sessione con provenance e completeness.

---

## Dashboard

[Apri la Dashboard](dashboard.html){ .md-button .md-button--primary }

---

## Report disponibili

### Validazione dello storico

Contiene l'esito dei controlli di coerenza sui dati acquisiti.

→ [Apri il report](history-validation.md)

### Configurazioni

Mostra il riepilogo delle configurazioni rilevate durante le sessioni.

→ [Apri il riepilogo](configuration-summary.md)

---

## Pipeline Analytics

La pipeline viene eseguita con:

```powershell
python .\dsg-analytics\build_all.py
```

Le principali elaborazioni comprendono:

1. Consolidamento dello storico
2. Analisi delle configurazioni
3. Estrazione delle metriche dei target
4. Aggregazione dei risultati
5. Generazione della dashboard e delle projection scientifiche

La pipeline automatica delle sessioni rigenera inoltre la projection BKL-037 dopo il catalogo scientifico, mantenendo la comparazione allineata alle nuove sessioni senza aggiornamenti manuali del JSON.

---

## Roadmap

### Versione 3.1
- Portale Analytics integrato nel manuale MkDocs
- Navigazione centralizzata
- Accesso ai report

### Versione 3.2
- Validazione avanzata dei target
- Report di qualità dei dati

### Versione 3.3
- Observatory Intelligence
- KPI evoluti
- Analisi stagionali
- Statistiche per telescopio
