# ARB-012-C08 — CI and Publication Evidence

| Campo | Valore |
|---|---|
| Evidence ID | E-ARB012-C08-01 |
| Condizione | ARB-012-C08 — Publication and CI Validation |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Branch | `validation/arb-012-conditions` |
| Commit verificato | `a413ebca34544cd019ff49868bd2c281d60c5582` |
| Workflow | Developer Foundation |
| Workflow run | `30573665900` — run number 163 |
| Job | `quality-gate` — job ID `90976462938` |
| Data verifica | 30/07/2026 |
| Autorità | Digital StarGate Release and Quality Governor |
| Esito | Passed |

## 1. Scope

Questa evidenza registra l'esecuzione del quality gate CI richiesto da `ARB-012-C08` sul commit della campagna di validazione.

## 2. Risultato workflow

Il workflow `Developer Foundation` ha completato con stato `completed` e conclusione `success`.

Tutti i passi obbligatori hanno completato con esito positivo:

| Passo | Esito |
|---|---|
| Checkout | Passed |
| Setup .NET | Passed |
| Restore | Passed |
| Build | Passed |
| Test | Passed |
| Verify formatting | Passed |
| Setup Python | Passed |
| Install documentation dependencies | Passed |
| Verify MkDocs | Passed |

## 3. Gate coverage

La pipeline ha eseguito:

```text
dotnet restore DigitalStarGate.sln
dotnet build DigitalStarGate.sln --configuration Release --no-restore
dotnet test DigitalStarGate.sln --configuration Release --no-build
dotnet format DigitalStarGate.sln --verify-no-changes --no-restore
python -m pip install --requirement requirements.txt
mkdocs build --strict
```

Il successo di `mkdocs build --strict` fornisce evidenza di parsing della configurazione MkDocs, risoluzione della navigazione e pubblicabilità documentale secondo il quality gate configurato.

## 4. Limitazioni

Questa evidenza non certifica:

- rendering visuale manuale di ogni diagramma Mermaid;
- comportamento runtime del DSOC;
- command authorization;
- alarm handling;
- recovery, break-glass, degraded mode o audit integrity runtime;
- chiusura delle condizioni C01–C07.

## 5. Decisione

**ARB-012-C08: PASSED**

La condizione C08 è chiusa per il commit verificato. Una modifica successiva ai file di build, workflow, documentazione, navigazione o dipendenze richiede una nuova esecuzione CI; il gate finale della PR deve comunque risultare positivo sull'ultimo head commit prima del merge.
