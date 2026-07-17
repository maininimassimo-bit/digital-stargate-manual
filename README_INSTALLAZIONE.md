# Digital StarGate Analytics v2.0B.1

Questo blocco consolida e valida lo storico delle sessioni senza modificare il collector EAGLE.

## File installati

- `dsg-analytics/history/history_schema.json`
- `dsg-analytics/history/consolidate_history.py`
- `.github/workflows/validate-history.yml`

## Installazione sul PC principale

1. Estrarre il contenuto dell'archivio nella radice del repository:
   `C:\DigitalStarGate\digital-stargate-manual`
2. Aprire PowerShell nella radice del repository.
3. Eseguire il collaudo locale:

```powershell
python .\dsg-analytics\history\consolidate_history.py --mode update
```

4. Leggere il risultato:

```powershell
Get-Content .\docs\analytics\history-validation.md
```

5. Verificare Git:

```powershell
git status
git diff -- .\data\analytics\history\sessions.csv
git diff -- .\docs\analytics\history-validation.md
```

6. Se il report indica `OK` o soltanto avvisi comprensibili:

```powershell
git add .github/workflows/validate-history.yml `
        dsg-analytics/history/history_schema.json `
        dsg-analytics/history/consolidate_history.py `
        data/analytics/history/sessions.csv `
        data/analytics/history/validation-report.json `
        docs/analytics/history-validation.md

git commit -m "analytics: add historical consolidation and validation"
git push origin main
```

## Modalita disponibili

- `--mode update`: aggiorna o inserisce le sessioni trovate, preservando lo storico.
- `--mode rebuild`: ricostruisce completamente `sessions.csv` dai file `session-metrics.json`.
- `--mode check`: valida soltanto il CSV esistente.
- `--strict-warnings`: restituisce errore anche in presenza di soli avvisi.

## Risultati

- `data/analytics/history/sessions.csv`
- `data/analytics/history/validation-report.json`
- `docs/analytics/history-validation.md`

Il workflow GitHub si avvia automaticamente quando cambia un `session-metrics.json` e pubblica lo storico consolidato.
