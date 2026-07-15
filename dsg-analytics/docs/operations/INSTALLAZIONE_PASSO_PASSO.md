# Installazione DSG Analytics - Fase 1

## 1. Copia nel repository
Copia l'intera cartella come:

`C:\DigitalStarGate\digital-stargate-manual\dsg-analytics`

## 2. Verifica Python

```powershell
python --version
```

Richiesto Python 3.11 o successivo.

## 3. Analizza la sessione iniziale

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

& 'C:\DigitalStarGate\digital-stargate-manual\dsg-analytics\collector\Invoke-DSGDailyAnalysis.ps1' `
  -SessionId '2026-07-14_2026-07-15' `
  -RepositoryRoot 'C:\DigitalStarGate\digital-stargate-manual'
```

## 4. Verifica output

- `data\sessions\2026\07\2026-07-14_2026-07-15\normalized\session-metrics.json`
- `docs\session-reports\2026\07\2026-07-14_2026-07-15\report-sessione.md`

## 5. Pubblica

```powershell
cd C:\DigitalStarGate\digital-stargate-manual
git add dsg-analytics data/sessions docs/session-reports .github/workflows/analyze-session.yml
git commit -m 'Add DSG session analytics phase 1'
git push
```
