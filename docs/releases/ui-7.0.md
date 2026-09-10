# UI 7.0 — Portal Experience Redesign

| Campo | Valore |
|---|---|
| Identificativo | DSG-REL-UI-7.0 |
| Versione | 1.0 |
| Stato | Merged / Pages remediation in progress |
| Data | 10/09/2026 |
| Ambito | Portale GitHub Pages |
| Architecture | DSGP-SOL-001 |
| Design System | DSG-UI-001 v2.0 |
| Architecture review | ARB-UI-7 — APPROVED |
| Release Quality | RQ-UI-7 — READY FOR MERGE |

## Outcome

UI 7.0 ridisegna il portale Digital StarGate come esperienza unificata per osservatorio, scienza, analytics, operations, architettura e documentazione. Mantiene MkDocs, GitHub Pages, URL pubblici e contratti dati esistenti.

## User experience

- homepage task-first con accesso immediato a Mission Control e sessioni;
- snapshot governato di package corrente, ultima notte e patrimonio scientifico;
- sei percorsi principali al posto della frammentazione precedente;
- navigation desktop compatta e drawer accessibile;
- navigazione Material mobile riallineata alla stessa tassonomia;
- typography, spacing, card, tabelle, focus e responsive behavior aggiornati;
- chiara distinzione tra realtime, storico, governance e manuale.

## Dynamic content

La homepage entra nel ciclo automatico di import senza modificare i workflow privilegiati:

- legge roadmap, catalogo e latest observation con cache no-store;
- mostra loading/UNKNOWN quando una projection non è disponibile;
- usa i dataset che analyze-session-automatic.yml già rigenera e pubblica;
- valida al build i binding del consumer e rifiuta fallback stale senza riscrivere la pagina;
- il deploy Pages continua ad avvenire dopo il commit delle projection.

## Corrective note C1

Il primo deploy sul merge `7bcc1d75590c2c6e8d102e63146e011fe4fb5d9c` ha identificato l'incompatibilità del precedente generatore statico con il nuovo shell. La correzione C1 conserva il passo workflow ma lo converte in validator non mutante; non cambia permessi, trigger, dataset o runtime.

Le altre superfici session-driven mantengono i generatori esistenti: latest observation, catalogo, report, Analytics, Equipment Performance e Session Comparison.

## Freshness and legacy remediation

- rimossi stato AP-013 e KPI homepage hard-coded;
- Scientific Intelligence convertita a projection corrente;
- Repository Intelligence e Repository Analytics ritirate come viste statiche duplicate;
- fallback Documentation Center privati di valori plausibili ma obsoleti;
- cache-buster BKL-040 rimosso dalla Roadmap;
- UI 6.1 marcata storica;
- handover e baseline datati conservati come snapshot, non come current state.

## Compatibility

- nessun URL pubblico rinominato o eliminato;
- nessuna modifica agli schema JSON accettati;
- nessuna nuova dipendenza frontend;
- supporto Instant Navigation mantenuto;
- light/dark mode e mobile mantenuti;
- nessun impatto su EAGLE, device, interlock o Safety Authority.

## Validation plan

- JavaScript syntax check;
- YAML parsing;
- verifica dei contratti projection e dei fallback;
- mkdocs build --strict;
- exact-head GitHub Actions;
- ARB review;
- Release Quality review;
- Pages post-merge.

## Rollback

Revert del package UI 7.0. Il rollback interessa soltanto presentation, navigation e consumer homepage; non modifica workflow, evidence o runtime.

## Acceptance criteria

- homepage coerente con BKL-041 e con lo storico corrente;
- aggiornamento automatico dimostrato dal consumo delle projection session-driven già pubblicate;
- nessun contenuto stale nelle superfici primarie;
- build e CI verdi;
- ARB Approved;
- Release Quality Ready;
- Pages post-merge SUCCESS.
