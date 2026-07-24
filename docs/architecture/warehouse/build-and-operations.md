# Build e operatività del Warehouse

## Scopo

Questa pagina descrive il modello operativo per costruire, verificare e
pubblicare il Warehouse.

I nomi esatti degli script devono essere mantenuti allineati ai file presenti
nel repository. Dove il comando non è ancora formalizzato, viene indicato il
comportamento richiesto senza inventare un entry point.

## Prerequisiti

Ambiente raccomandato:

- repository aggiornato;
- branch di lavoro corretto;
- Python supportato dal progetto;
- ambiente virtuale attivo;
- dipendenze installate;
- dataset Analytics disponibili;
- spazio sufficiente per output e file temporanei.

Esempio di attivazione dell'ambiente virtuale:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Verifica preliminare

Dalla root del repository:

```powershell
git status
```

Controllare inoltre:

- percorso degli input Analytics;
- configurazione della build;
- versione dello schema;
- directory di output;
- eventuali variabili d'ambiente;
- disponibilità delle dipendenze Parquet.

## Sequenza operativa

```text
1. Verifica ambiente
2. Verifica input Analytics
3. Esecuzione dei test
4. Costruzione Warehouse
5. Validazione output
6. Generazione metadata
7. Build documentazione
8. Revisione Git
9. Commit e pubblicazione
```

## Test

Eseguire la suite prevista dal repository.

Comando generico:

```powershell
python -m pytest
```

Quando il repository prevede test specifici del Warehouse, utilizzare il
percorso o il marker definito dal progetto.

Esempio da adattare ai file reali:

```powershell
python -m pytest tests\warehouse
```

## Costruzione

La build deve:

- leggere esclusivamente dataset Analytics validati;
- applicare lo schema;
- produrre i cinque dataset approvati;
- scrivere in una directory controllata;
- produrre metadata;
- interrompersi sugli errori bloccanti;
- restituire un exit code non zero in caso di errore.

L'entry point ufficiale deve essere quello già presente nel repository. Non
devono essere introdotti script alternativi senza una decisione esplicita.

## Output attesi

```text
sessions.parquet
targets.parquet
equipment.parquet
quality.parquet
weather.parquet
```

Insieme ai file dati devono essere disponibili metadata sufficienti a
identificare la build.

## Verifica manuale

Dopo la build verificare:

```powershell
Get-ChildItem <directory-output>
```

Controllare:

- presenza dei file;
- dimensione non anomala;
- data di aggiornamento;
- metadata;
- log;
- assenza di file temporanei incompleti.

La dimensione zero non implica sempre errore, ma deve essere compatibile con il
contratto del dataset.

## Verifica automatica

La validazione deve aprire i file Parquet e controllare:

- schema;
- colonne;
- numero di righe;
- tipi;
- duplicati;
- valori null;
- intervalli;
- relazioni;
- metadata.

La sola presenza del file non è una verifica sufficiente.

## Build della documentazione

Dopo l'aggiornamento della documentazione:

```powershell
mkdocs build --strict
```

La build deve terminare senza warning bloccanti.

Per la verifica locale:

```powershell
mkdocs serve
```

Portale locale:

```text
http://127.0.0.1:8000
```

## Aggiornamento della navigazione

Le pagine Warehouse devono essere aggiunte a `mkdocs.yml` soltanto quando
esistono.

Configurazione prevista:

```yaml
- Architettura del Warehouse:
    - Panoramica: architecture/warehouse/index.md
    - Flusso dei dati: architecture/warehouse/data-flow.md
    - Dataset e schema: architecture/warehouse/datasets-and-schema.md
    - Validazione e quality gate: architecture/warehouse/validation-and-quality-gates.md
    - Build e operatività: architecture/warehouse/build-and-operations.md
```

## Gestione degli errori

### Input mancante

Azioni:

1. identificare il dataset;
2. verificare la build Analytics;
3. non creare output fittizi;
4. correggere la causa a monte;
5. rieseguire test e build.

### Schema non valido

Azioni:

1. confrontare input e schema atteso;
2. verificare modifiche recenti;
3. aggiornare schema, validator e test in modo coordinato;
4. verificare i consumer;
5. documentare la modifica.

### Parquet illeggibile

Azioni:

1. eliminare l'output incompleto;
2. controllare spazio disco e dipendenze;
3. verificare i log;
4. rigenerare;
5. eseguire il validator prima della pubblicazione.

### Metadata incoerente

Azioni:

1. non pubblicare la build come valida;
2. rigenerare i metadata dagli output effettivi;
3. verificare numero di righe e stato;
4. aggiungere o correggere un test di regressione.

## Ripristino

La strategia minima di rollback consiste nel:

- conservare l'ultima build valida;
- non sovrascriverla prima del completamento dei controlli;
- produrre gli output in una directory temporanea;
- promuovere la build solo dopo validazione;
- registrare commit e versione dello schema.

Un modello raccomandato è:

```text
warehouse/
├── builds/
│   ├── <build-id-1>/
│   └── <build-id-2>/
└── current -> <build-validata>
```

La realizzazione concreta richiede una decisione di release e deployment.

## Checklist di rilascio

- [ ] Repository aggiornato
- [ ] Ambiente virtuale attivo
- [ ] Dipendenze installate
- [ ] Input Analytics validi
- [ ] Test superati
- [ ] Build Warehouse completata
- [ ] Cinque dataset verificati
- [ ] Metadata coerenti
- [ ] `mkdocs build --strict` superato
- [ ] `git status` controllato
- [ ] Commit descrittivo
- [ ] Push sul branch previsto

## Evoluzioni future

Sono previste, ma non devono essere considerate operative finché non
implementate e validate:

- incremental build;
- delta update;
- DuckDB;
- viste SQL;
- versionamento avanzato dei dataset;
- promozione atomica delle build;
- retention automatica;
- monitoraggio degli SLA;
- deployment automatizzato sull'EAGLE.
