# ARB-012 Validation Campaign

| Campo | Valore |
|---|---|
| Identificativo | ARB-012-VAL-001 |
| Titolo | Validation Campaign for ARB-012 Conditions C01–C08 |
| Package | AP-012 — Enterprise Operations Center Architecture |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Branch | `validation/arb-012-conditions` |
| Data | 30/07/2026 |
| Autorità | Digital StarGate Release and Quality Governor |
| Stato | Active validation campaign — evidence pending |
| Readiness | Not Ready for runtime enablement |

## 1. Scopo

Questa campagna governa la produzione, verifica e registrazione delle evidenze richieste dalle condizioni `ARB-012-C01…C08`. La campagna distingue la validazione documentale e CI dalla validazione runtime, organizzativa, security e safety.

La pubblicazione di questo documento non chiude alcuna condizione. Una condizione può essere dichiarata `Passed` solo quando l'evidenza richiesta è presente, riproducibile, collegata al relativo scenario e approvata dall'autorità competente.

## 2. Regole di classificazione

Ogni gate usa esclusivamente uno dei seguenti stati:

- `Passed`: criteri soddisfatti con evidenza verificata;
- `Failed`: prova eseguita con esito negativo;
- `Not Executed`: prova definita ma non ancora eseguita;
- `Blocked`: prova non eseguibile per dipendenza, ambiente, ruolo o capability assente;
- `Not Applicable`: gate non pertinente, con motivazione approvata.

Non sono ammesse chiusure basate sulla sola ispezione documentale per i gate runtime.

## 3. Quality-gate matrix

| Condizione | Ambito | Stato iniziale | Gate di chiusura | Evidenza minima |
|---|---|---|---|---|
| ARB-012-C01 | Command Authorization Validation | Not Executed | policy, ruoli, freshness, safety denial, expiry, idempotency e audit verificati | test report con casi positivi e negativi, log correlati e decision record |
| ARB-012-C02 | Alarm and Incident Validation | Not Executed | lifecycle, correlation, suppression, escalation, acknowledgement e closure verificati | scenario report con timeline, alarm/incident records e audit trail |
| ARB-012-C03 | Runbook Drill and Recovery | Not Executed | precondizioni, checkpoint, stop condition, rollback, recovery e evidence collection verificati | drill report con esito, tempi, deviazioni e rollback evidence |
| ARB-012-C04 | Role Assignment and Four-Eyes Enforcement | Blocked | ruoli nominativi, deleghe, conflitti, approver distinti e access review attivi | role assignment register, delegation records e prova four-eyes |
| ARB-012-C05 | Security and Break-Glass Validation | Not Executed | least privilege, privileged access, break-glass, revoca e post-review verificati | access logs, approval record, revocation evidence e post-review |
| ARB-012-C06 | Degraded Mode and Dependency Failure | Not Executed | failure di telemetry, notification, audit sink, correlation e identity gestiti senza bypass safety | fault-injection report e degraded-mode evidence |
| ARB-012-C07 | Audit, Retention and Time Integrity | Not Executed | append-only trail, timestamp, correlation, payload hash, retention e time integrity verificati | audit integrity report, retention configuration e clock evidence |
| ARB-012-C08 | Publication and CI Validation | Not Executed | restore, build, test, format e `mkdocs build --strict` completati | GitHub Actions run, job logs e commit SHA |

## 4. Validation scenarios

### 4.1 ARB-012-C01 — Command Authorization Validation

Eseguire almeno i seguenti scenari:

1. comando C1 autorizzato con identità, ruolo e scope validi;
2. comando C3/C4 senza secondo approvatore;
3. comando con autorizzazione scaduta;
4. comando con telemetry `stale`, `unknown` o `conflicting`;
5. comando negato dalla Safety Authority;
6. duplicazione dello stesso command ID;
7. retry dopo timeout senza doppia esecuzione;
8. revoca del privilegio tra approval ed execution;
9. audit completo di request, policy version, decision, execution ed outcome.

**Pass criteria:** nessun comando non autorizzato viene eseguito; safety denial prevale; duplicati non producono doppio effetto; ogni decisione è correlata e auditabile.

### 4.2 ARB-012-C02 — Alarm and Incident Validation

Eseguire almeno:

1. event → alarm → incident;
2. acknowledgement senza falsa risoluzione;
3. correlation di eventi con causa comune;
4. suppression temporanea con owner e scadenza;
5. rifiuto di suppression safety-relevant;
6. escalation funzionale, gerarchica e safety;
7. riapertura dopo falsa recovery;
8. chiusura SEV-1 con verifica del safe state;
9. Major Incident con timeline e post-incident review.

**Pass criteria:** nessun evento originario viene perso; suppression non nasconde condizioni safety; escalation e closure producono evidenza completa.

### 4.3 ARB-012-C03 — Runbook Drill and Recovery

Eseguire drill controllati per:

1. avvio con precondizione mancante;
2. stop condition durante esecuzione;
3. rollback di un passo reversibile;
4. failure di un passo non reversibile;
5. timeout e handover;
6. recovery dopo dipendenza indisponibile;
7. return-to-service con approvatore distinto;
8. raccolta automatica e manuale dell'evidence.

**Pass criteria:** il runbook si arresta in modo sicuro, non bypassa interlock, registra deviazioni e consente recovery verificabile.

### 4.4 ARB-012-C04 — Role Assignment and Four-Eyes Enforcement

Produrre:

- assegnazione nominativa per Operations Lead, Service Owner, Technical Owner, Operator, Incident Coordinator, Maintainer, Safety Authority, Security Authority, Documentation Governor e Auditor;
- sostituti e validità delle deleghe;
- conflict register;
- matrice accessi per classi C1–C4;
- prova che requester e approver C3/C4 siano distinti;
- prova che Maintainer e return-to-service approver siano distinti per attività safety-relevant.

**Pass criteria:** nessun ruolo critico resta implicito; conflitti sono registrati e mitigati; four-eyes è tecnicamente o proceduralmente impedibile da aggirare.

### 4.5 ARB-012-C05 — Security and Break-Glass Validation

Eseguire:

1. privileged access approvato e time-bound;
2. accesso fuori scope negato;
3. break-glass con motivazione e durata limitata;
4. revoca automatica;
5. notifica e post-review;
6. tentativo di riuso del privilegio revocato;
7. verifica che Security Authority non possa dichiarare safe state;
8. verifica che un ruolo amministrativo non acquisisca command authority implicita.

**Pass criteria:** accessi fuori policy sono negati; break-glass è minimo, temporaneo, auditato e riesaminato.

### 4.6 ARB-012-C06 — Degraded Mode and Dependency Failure

Eseguire fault injection per:

- telemetry source indisponibile;
- telemetry `stale` o conflittuale;
- notification channel indisponibile;
- correlation engine indisponibile;
- audit sink indisponibile;
- identity provider indisponibile;
- command dispatcher indisponibile;
- rete remota o VPN indisponibile.

**Pass criteria:** il sistema non interpreta assenza o inconsistenza come stato sicuro, non auto-risolve e non abilita command path in assenza di evidenza valida.

### 4.7 ARB-012-C07 — Audit, Retention and Time Integrity

Verificare:

- timeline append-only;
- actor o system principal;
- previous state e new state;
- reason code e policy version;
- correlation ID e payload hash;
- timestamp affidabile e comportamento con clock drift;
- retention e protezione da modifica/cancellazione non autorizzata;
- export per audit e post-incident review;
- collegamento tra command, alarm, incident, runbook, change ed evidence.

**Pass criteria:** ogni transizione critica è ricostruibile e le alterazioni non autorizzate sono impedite o rilevate.

### 4.8 ARB-012-C08 — Publication and CI Validation

La pipeline autorevole è `.github/workflows/developer-foundation.yml` e deve eseguire:

```powershell
dotnet restore DigitalStarGate.sln
dotnet build DigitalStarGate.sln --configuration Release
dotnet test DigitalStarGate.sln --configuration Release
dotnet format DigitalStarGate.sln --verify-no-changes
python -m pip install --requirement requirements.txt
mkdocs build --strict
```

Verifiche aggiuntive richieste:

- parsing di `docs/data/roadmap.json`;
- parsing YAML di `mkdocs.yml`;
- presenza dei documenti referenziati nella nav;
- assenza di link interni rotti;
- rendering Mermaid almeno per ispezione o build compatibile;
- commit SHA e run ID registrati.

**Pass criteria:** tutti i job obbligatori completano con esito positivo sul commit della campagna.

## 5. Evidence register

| Evidence ID | Condizione | Descrizione | Stato | Riferimento |
|---|---|---|---|---|
| E-ARB012-C01-01 | C01 | Command authorization scenario report | Missing | da produrre |
| E-ARB012-C02-01 | C02 | Alarm and incident scenario report | Missing | da produrre |
| E-ARB012-C03-01 | C03 | Runbook drill and recovery report | Missing | da produrre |
| E-ARB012-C04-01 | C04 | Role assignment and four-eyes evidence | Blocked | nomine e access review richieste |
| E-ARB012-C05-01 | C05 | Security and break-glass report | Missing | da produrre |
| E-ARB012-C06-01 | C06 | Degraded-mode fault-injection report | Missing | da produrre |
| E-ARB012-C07-01 | C07 | Audit, retention and time-integrity report | Missing | da produrre |
| E-ARB012-C08-01 | C08 | CI and publication run | Pending | PR e workflow richiesti |

## 6. Risk and waiver register

| ID | Rischio | Severità | Trattamento | Waiver |
|---|---|---|---|---|
| R-ARB012-01 | command path abilitato prima di C01 | Critical | mantenere runtime disabilitato | non ammesso |
| R-ARB012-02 | safety state dedotto da telemetry assente o incoerente | Critical | fail-safe e blocco azioni dipendenti | non ammesso |
| R-ARB012-03 | ruoli critici non nominati | High | completare C04 prima dell'operatività | non ammesso per C3/C4 |
| R-ARB012-04 | break-glass persistente o non auditato | Critical | scope minimo, expiry e post-review | non ammesso |
| R-ARB012-05 | audit trail incompleto | High | chiudere C07 prima della readiness | solo ambienti non operativi |
| R-ARB012-06 | build documentale non riproducibile | Medium | chiudere C08 tramite CI | nessuna dichiarazione di pubblicabilità |

## 7. Ordine di esecuzione

1. C08 — attivare CI e verificare pubblicazione;
2. C04 — nominare ruoli e definire access matrix;
3. C01 e C05 — validare authorization e privileged access;
4. C07 — validare audit e time integrity;
5. C02 — validare alarm e incident lifecycle;
6. C03 — eseguire runbook drill e recovery;
7. C06 — fault injection e degraded mode;
8. re-review finale delle evidenze C01–C08.

C01–C07 devono essere eseguite inizialmente in ambiente simulato o non operativo. Nessuna prova può disabilitare interlock locali o mettere a rischio persone, cupola, montatura o altri asset fisici.

## 8. Readiness recommendation

**NOT READY FOR RUNTIME ENABLEMENT**

Il package AP-012 è approvato come baseline documentale, ma nessuna condizione ARB-012 è ancora chiusa all'avvio della campagna. È consentita la preparazione di test harness, configurazioni, simulazioni, role register ed evidence collection. Rimane vietata l'attivazione di command path operativi fino alla chiusura verificata delle condizioni applicabili e alla decisione finale di re-review.