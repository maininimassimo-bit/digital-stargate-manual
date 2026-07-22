# Digital StarGate — Milestone 5.1, Sprint 1

## Obiettivo

Questo sprint introduce l'architettura dell'Observatory Data Warehouse
senza modificare ancora il formato o le sorgenti dati usate da dashboard
e homepage.

## File inclusi

```text
dsg-analytics/
    config/
        pipeline.yml
    warehouse/
        __init__.py
        models.py
        validators.py
        repository.py
        builder.py
        build_warehouse.py
```

## Installazione

Estrarre lo ZIP nella radice del repository:

```text
C:\DigitalStarGate\digital-stargate-manual
```

Confermare la sostituzione di `pipeline.yml`.

## Backup consigliato

Prima dell'estrazione:

```powershell
Copy-Item `
  .\dsg-analytics\config\pipeline.yml `
  .\dsg-analytics\config\pipeline.yml.release-4.2.bak
```

## Verifica sintattica

```powershell
python -m py_compile .\dsg-analytics\warehouse\models.py
python -m py_compile .\dsg-analytics\warehouse\validators.py
python -m py_compile .\dsg-analytics\warehouse\repository.py
python -m py_compile .\dsg-analytics\warehouse\builder.py
python -m py_compile .\dsg-analytics\warehouse\build_warehouse.py
```

## Test isolato del Warehouse

```powershell
python .\dsg-analytics\warehouse\build_warehouse.py --repo-root .
```

Output atteso:

```text
Observatory Data Warehouse architecture initialized.
- Datasets defined: 5
- Population status: deferred to Sprint 2
```

## Build completa

```powershell
python .\dsg-analytics\build_all.py --repo-root .
```

La pipeline deve mostrare 8 step e il seguente ordine logico:

```text
history
configuration
target-metrics
targets
warehouse
dashboard
status
homepage
```

L'ordine tra rami indipendenti può rispettare la stabilità definita nel
file YAML.

## Output generati

```text
data\analytics\warehouse\warehouse-schema.json
data\analytics\warehouse\warehouse-metadata.json
```

In questo sprint i cinque file `.parquet` non vengono ancora creati.
Saranno popolati nello Sprint 2.

## Controllo rapido

```powershell
Get-Content .\data\analytics\warehouse\warehouse-schema.json
Get-Content .\data\analytics\warehouse\warehouse-metadata.json
```

## Test propagazione dipendenze

```powershell
python .\dsg-analytics\build_all.py --repo-root . --skip-dashboard
```

Con la configurazione attuale, `homepage` deve essere saltata perché
dipende da `dashboard`. Lo step `warehouse` deve invece essere eseguito.
