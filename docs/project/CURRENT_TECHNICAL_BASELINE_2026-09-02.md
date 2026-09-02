# Digital StarGate — Current Technical Baseline — 2026-09-02

| Campo | Valore |
|---|---|
| Stato | Active technical delta baseline |
| Scope | Scientific session producer, SQM evidence packaging, Reporting runtime contract |
| Supersedes | `CURRENT_TECHNICAL_BASELINE_2026-09-01.md` per lo stato operativo corrente |
| Does not supersede | Principi, boundary, ADR, Architecture Package, OAT storiche o decisioni approvate |

## 1. Finalità

Questo documento registra il delta tecnico verificato il 02/09/2026 dopo la remediation del producer automatico di sessione su EAGLE30154. La baseline del 01/09 resta una fotografia storica valida per la pipeline scientifica e le projection allora verificate.

## 2. Runtime Reporting corrente

La baseline runtime corrente su EAGLE30154 è `DigitalStarGate.Reporting 1.0.7`, proveniente dal merge `c5f1bd617eb7b256372f0257a3cf22b60d503d3b` del repository `maininimassimo-bit/DigitalStarGate.Reporting`.

L'installazione runtime è stata verificata in Windows PowerShell con `-ExecutionPolicy Bypass`:

- modulo `DigitalStarGate.Reporting 1.0.7`;
- ModuleBase `C:\Users\PrimaLuceLab\Documents\WindowsPowerShell\Modules\DigitalStarGate.Reporting\1.0.7`;
- `Import-DSGSession` 1.0.7;
- `Publish-DSGSession` 1.0.7.

Le versioni precedenti installate possono restare presenti, ma la catena produttiva deve caricare la baseline corrente secondo il runtime/config governato.

## 3. Session producer contract

La catena produttiva resta:

`Scheduled Task -> Invoke-DSGSessionPreflight.ps1 -> Invoke-DSGAutomaticSession.ps1 -> DigitalStarGate.Reporting`.

Il preflight deve fallire chiuso se il runtime clone non è una working tree Git valida, è dirty, non è su `main`, non riesce a fetch/pull fast-forward o non coincide con `origin/main`.

Il 02/09 il preflight ha correttamente impedito l'avvio quando il clone era rimasto su un branch sessione ed era indietro rispetto a `origin/main`. Questo comportamento è un controllo di integrità, non un difetto.

## 4. SQM evidence packaging

Reporting 1.0.7 integra il packaging SQM nel normale `Import-DSGSession`:

- history source di default: `%LOCALAPPDATA%\DigitalStarGate\telemetry\sqm-history.ndjson`;
- output sessione: `raw/sqm/sqm-history.ndjson`;
- summary: `raw/sqm/sqm-summary.json`;
- manifest generato dopo l'export SQM, così i file SQM entrano nella governance/hash del package.

Test runtime reale sulla finestra della sessione `2026-09-01_2026-09-02`:

- valid samples `1306`;
- quality `AVAILABLE`;
- temporal coverage `0.9886`;
- min `8.91`;
- mean `17.738`;
- max `20.92`;
- median `18.755` mag/arcsec²;
- source `AAG CloudWatcher SOLO HTTP / lightmpsas`.

SQM resta una misura scientifica e non è Safety Authority.

## 5. Publish contract

Reporting 1.0.7 impedisce che stdout dei comandi Git nativi contamini la success stream di `Publish-DSGSession`.

Il test non distruttivo sul runtime EAGLE, senza `-CreateBranch` e senza `-Push`, ha verificato:

```text
Type  = System.Management.Automation.PSCustomObject
Count = 1
SessionId = 2026-09-01_2026-09-02
Committed = False
Pushed = False
```

Il runtime repository è rimasto `main`, clean, con `HEAD...origin/main = 0 0`.

## 6. Sessione 2026-09-01_2026-09-02

La sessione è stata promossa e rianalizzata nella pipeline canonica. Le projection governate riportano SQM `AVAILABLE`, 1306 campioni e coverage `0.9886`. La severity della sessione resta semanticamente separata dalla disponibilità SQM.

## 7. OAT storica AP-014

Le validation page AP-014 che attestano Reporting 1.0.6 descrivono l'OAT storica e non devono essere retroattivamente riscritte. La baseline runtime operativa successiva è invece 1.0.7 e deve essere usata da runbook, bootstrap e handover correnti.

## 8. Debito tecnico residuo

Due hardening item restano aperti:

1. garantire il restore del runtime clone a `main` anche quando il launcher incontra un'eccezione prima del cleanup normale;
2. ripristinare nella Reporting quality gate i controlli storici rimossi durante la 1.0.7, mantenendo anche i nuovi test SQM/publish.

Questi item non modificano Safety Authority e non invalidano i due test runtime 1.0.7 già eseguiti.

## 9. Safety e authority boundary

Restano invariati:

- local physical Safety Authority indipendente;
- telemetry, SQM, health, analytics e AI non sono Safety Authority;
- nessun controllo diretto portale/AI sui device nella baseline corrente;
- evidence scientifica e health non sostituiscono gli interlock locali;
- UNKNOWN/STALE non devono essere rappresentati come current.

## 10. Evoluzione successiva

La capability successiva resta BKL-030 EAGLE Health & Reliability. Il primo incremento è D1/D2 source discovery read-only su `EAGLE30154` tramite `scripts/telemetry/Inspect-EagleHealthSources.ps1`. Nessuna soglia HEALTHY/DEGRADED/CRITICAL o remediation automatica è autorizzata prima della classificazione delle source/evidence.
