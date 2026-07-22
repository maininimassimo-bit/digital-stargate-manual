# Digital StarGate Release 4.1

Estrai il contenuto nella radice:

`C:\DigitalStarGate\digital-stargate-manual`

Conferma la sostituzione dei file.

Il pacchetto non sostituisce `platform.yml`.

## Verifica

```powershell
python -m py_compile .\dsg-analytics\config\loader.py
python -m py_compile .\dsg-analytics\orchestration\pipeline.py
python -m py_compile .\dsg-analytics\build_all.py
python .\dsg-analytics\build_all.py --repo-root .
python .\dsg-analytics\build_all.py --repo-root . --skip-dashboard
```
