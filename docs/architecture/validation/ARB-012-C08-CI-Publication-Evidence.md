# ARB-012-C08 — CI and Publication Evidence

| Campo | Valore |
|---|---|
| Evidence ID | E-ARB012-C08-01 |
| Condizione | ARB-012-C08 — Publication and CI Validation |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Branch | `validation/arb-012-conditions` |
| Commit verificato | `fe043b94873ee679baf633893c9dcfb78421a810` |
| Workflow | Developer Foundation |
| Workflow run | `30574988062` — run number 171 |
| Job | `quality-gate` — job ID `90980901267` |
| Data verifica | 30/07/2026 |
| Autorità | Digital StarGate Release and Quality Governor |
| Esito | Passed |

## 1. Scope

Questa evidenza registra l'esecuzione del quality gate CI richiesto da `ARB-012-C08` sull'ultimo commit della campagna contenente l'evidenza di esecuzione simulata C01/C05.

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
- alarm handling e incident lifecycle;
- runbook recovery;
- degraded mode;
- audit retention e time integrity runtime;
- assegnazioni nominative e access review richieste da C04;
- abilitazione di command path operativi.

Le condizioni C01 e C05 risultano validate esclusivamente nell'ambiente simulato descritto dall'evidence package dedicato; tale esito non costituisce autorizzazione runtime.

## 5. Decisione

**ARB-012-C08: PASSED**

La condizione C08 è chiusa per il commit verificato. Il commit documentale che consolida questa evidenza deve a sua volta mantenere positivo il gate finale della PR prima del merge. Ogni modifica successiva a build, workflow, test, documentazione, navigazione o dipendenze richiede una nuova esecuzione CI.