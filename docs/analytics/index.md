# Digital StarGate Analytics

Benvenuto nel portale Analytics del progetto **Digital StarGate**.

Questa sezione raccoglie gli strumenti di analisi, i report e le projection governate generate automaticamente dalla pipeline delle sessioni osservative.

---

## Accesso rapido

- [Dashboard Analytics](dashboard/)
- [Session Comparison](../session-comparison/)
- [Equipment Performance](../equipment-performance/)
- [Validazione dello storico](history-validation.md)
- [Riepilogo configurazioni](configuration-summary.md)

[Apri la Dashboard](dashboard/){ .md-button .md-button--primary }
[Apri Session Comparison](../session-comparison/){ .md-button }

La **Dashboard Analytics** viene rigenerata dallo storico consolidato dopo ogni sessione importata. **Session Comparison** confronta in modalità read-only tutte le sessioni che dispongono di evidence comparabile per la dimensione pubblicata. Le sessioni non comparabili restano esplicitamente visibili come exclusions; il portale non crea ranking, score, soglie o decisioni di acceptance.

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

## Report disponibili

### Validazione dello storico

Contiene l'esito dei controlli di coerenza sui dati acquisiti.

→ [Apri il report](history-validation.md)

### Configurazioni

Mostra il riepilogo delle configurazioni rilevate durante le sessioni.

→ [Apri il riepilogo](configuration-summary.md)

---

## Aggiornamento automatico

Dopo l'import automatico di una sessione completa, il workflow governato:

1. analizza la sessione e aggiorna lo storico;
2. consolida e valida lo storico;
3. rigenera target e riepilogo configurazioni;
4. rigenera la Dashboard Analytics nativa MkDocs;
5. rigenera Equipment Performance, cataloghi scientifici e Session Comparison;
6. verifica la coerenza tra le viste;
7. committa soltanto gli output versionati modificati;
8. ridistribuisce il portale GitHub Pages.

La pipeline completa può essere eseguita anche localmente con:

```powershell
python .\dsg-analytics\build_all.py
```

---

## Roadmap

### Versione 3.1
- Portale Analytics integrato nel manuale MkDocs
- Navigazione centralizzata
- Accesso ai report
- Rigenerazione automatica delle viste Analytics dalle sessioni importate

### Versione 3.2
- Validazione avanzata dei target
- Report di qualità dei dati

### Versione 3.3
- Observatory Intelligence
- KPI evoluti
- Analisi stagionali
- Statistiche per telescopio
