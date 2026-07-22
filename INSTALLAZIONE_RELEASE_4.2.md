# Digital StarGate Analytics — Release 4.2

## Funzioni introdotte

- logging centralizzato su console e file;
- un file di log distinto per ogni build;
- misurazione della durata complessiva;
- misurazione della durata di ogni step;
- report JSON dell'ultima build;
- storico append-only in formato JSON Lines;
- registrazione degli step saltati;
- registrazione degli errori e degli exit code;
- opzione `--verbose`.

## File sostituiti o aggiunti

- `dsg-analytics/build_all.py`
- `dsg-analytics/orchestration/__init__.py`
- `dsg-analytics/orchestration/reporting.py`

I file della Release 4.1 non inclusi nel pacchetto restano invariati.

## Installazione

Estrarre lo ZIP nella radice del repository:

`C:\DigitalStarGate\digital-stargate-manual`

Confermare la sostituzione dei file esistenti.

## Verifica sintattica

```powershell
python -m py_compile .\dsg-analytics\orchestration\reporting.py
python -m py_compile .\dsg-analytics\orchestration\__init__.py
python -m py_compile .\dsg-analytics\build_all.py
```

## Build completa

```powershell
python .\dsg-analytics\build_all.py --repo-root .
```

## Build con log dettagliato

```powershell
python .\dsg-analytics\build_all.py --repo-root . --verbose
```

## Test propagazione skip

```powershell
python .\dsg-analytics\build_all.py --repo-root . --skip-dashboard
```

## Output prodotti

Log per singola build:

```text
data\analytics\builds\logs\build-<BUILD_ID>.log
```

Ultimo report:

```text
data\analytics\builds\latest-build.json
```

Storico completo:

```text
data\analytics\builds\build-history.jsonl
```

## Verifica rapida del report

```powershell
Get-Content .\data\analytics\builds\latest-build.json
```

## Verifica ultime build

```powershell
Get-Content .\data\analytics\builds\build-history.jsonl -Tail 5
```
