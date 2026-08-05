# ABC-001 — Architecture Baseline Evidence Annex

| Campo | Valore |
|---|---|
| Documento | Architecture Baseline Evidence Annex |
| Identificativo | ABC-001-EA |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `main` |
| Commit della capability baseline | `c668eb67c61cf4bc69258d5da15adda4a3a40ee4` |
| PAA di riferimento | PAA-002 v1.1 |
| Review di riferimento | ARB-002 |
| Data | 30/07/2026 |
| Stato | Evidence annex issued |

---

## 1. Scopo

Questo allegato soddisfa la condizione ARB2-MAJ-01 fornendo locator puntuali e immutabili per le capability classificate `Implemented` in PAA-002 v1.1.

L'allegato prova l'esistenza degli artefatti nella baseline indicata. Non certifica esecuzione runtime, deployment, operatività continua o successo di test non osservati durante il ciclo ABC-001.

## 2. Regole probatorie

- `SRC`: codice sorgente presente al commit certificato.
- `TST-PRESENT`: test presente nel repository, ma non necessariamente eseguito nel ciclo di certificazione.
- `DOC`: documentazione architetturale o operativa presente.
- `OPS`: evidenza runtime osservata. Nessuna evidenza OPS è attribuita dal presente allegato.
- Le pull request aperte e non integrate sono escluse.

## 3. Evidence register

| Capability | Classificazione PAA-002 | Evidence locator immutabile | Tipo | Stato validazione | Limite |
|---|---|---|---|---|---|
| CAP-01 Analytics pipeline | Implemented | `dsg-analytics/dashboard/build_dashboard_v31.py`, blob `3f86faf26d8d23533ced3e2bdac793aac04bae7e` | SRC | Ispezionato | Nessuna esecuzione osservata; operatività continua non certificata |
| CAP-01 Analytics pipeline | Implemented | `docs/analytics/index.md` e documentazione Analytics presente nel commit baseline | DOC | Presenza verificata nella baseline | La documentazione non prova runtime |
| CAP-02 Historical Analytics Dashboard | Implemented | `dsg-analytics/dashboard/build_dashboard_v31.py`, blob `3f86faf26d8d23533ced3e2bdac793aac04bae7e` | SRC | Ispezionato | Output e freshness non verificati nel ciclo ABC-001 |
| CAP-02 Historical Analytics Dashboard | Implemented | `docs/analytics/dashboard-integrated.md` | DOC | Presenza verificata nella baseline | Deployment e pubblicazione non certificati |
| CAP-03 Data Warehouse | Implemented | `dsg-analytics/warehouse/builder.py`, blob `262d4d423b7c5cc632f9088e035743b5254d47ee` | SRC | Ispezionato | Nessuna build Warehouse eseguita nel ciclo ABC-001 |
| CAP-03 Data Warehouse | Implemented | `dsg-analytics/warehouse/Tests/test_builder.py`, blob `56c600d9e79d25dc8e3ec2e83c929ab0c3160ff8` | TST-PRESENT | Test ispezionato, non eseguito | La presenza del test non equivale a esito positivo corrente |
| CAP-04 Warehouse metadata and validation | Implemented | `dsg-analytics/warehouse/builder.py`, blob `262d4d423b7c5cc632f9088e035743b5254d47ee` | SRC | Ispezionato | Il builder richiama schema, metadata e validazione; esecuzione non osservata |
| CAP-04 Warehouse metadata and validation | Implemented | `dsg-analytics/warehouse/Tests/test_builder.py`, blob `56c600d9e79d25dc8e3ec2e83c929ab0c3160ff8` | TST-PRESENT | Ispezionato | Verifica prevista per file, Parquet e coerenza row count; test non eseguito |

## 4. Relazioni producer–contract–consumer

| Area | Producer | Contratto o modello | Consumer | Evidenza | Stato |
|---|---|---|---|---|---|
| Warehouse build | Dataset builder in `warehouse.builder` | `WarehouseSchema`, `WarehouseMetadata`, dataset Parquet | `WarehouseRepository` e consumer futuri | SRC presente | Collegamento interno dimostrato per ispezione; consumer layer SQL canonico ancora `Missing` |
| Historical dashboard | Dataset Analytics letti dal core dashboard | `DashboardModel` | Renderer MkDocs dashboard | SRC presente | Flusso applicativo ispezionato; freshness runtime non verificata |

Non viene attribuita evidenza `INT` end-to-end a sistemi esterni, deployment o consumer non presenti nella baseline.

## 5. Comandi di validazione applicabili

I seguenti comandi sono pertinenti ma **non sono stati eseguiti** nel ciclo ABC-001:

```powershell
python -m pytest -q
mkdocs build --strict
```

Eventuali esiti storici descritti in assessment precedenti non vengono convertiti in nuova evidenza osservata.

## 6. Esclusioni

Il presente allegato non certifica:

- telemetria live, heartbeat o freshness;
- AllSky integrato;
- observability end-to-end;
- automazione operativa dell'osservatorio;
- safety hardware o fault injection;
- rete, VPN o failover;
- CI GitHub Actions;
- pull request non integrate;
- capability con stato `Partial`, `Prepared`, `Planned` o `Missing`.

## 7. Conclusione

I locator supportano la classificazione architetturale `Implemented` di CAP-01…CAP-04 come presenza sostanziale di codice e test nel repository. La certificazione resta limitata alla baseline architetturale e documentale; il livello `Operationally Verified` non è attribuito.