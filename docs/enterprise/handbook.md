# DSG-HBK-001 - Enterprise Handbook

| Campo | Valore |
|---|---|
| Documento | Enterprise Handbook |
| Identificativo | `DSG-HBK-001` |
| Roadmap | `DSG-MR-001` |
| Versione | 1.0 |
| Stato | Approvata per revisione |
| Owner | Massimo Mainini |
| Data baseline | 26/07/2026 |

## 1. Scopo

L'handbook definisce le regole operative per contribuire, revisionare e mantenere la documentazione Digital StarGate in modo coerente con la roadmap `DSG-MR-001`.

È pensato per contributor, maintainer, revisori tecnici e stakeholder che devono produrre o verificare contenuti enterprise e operativi.

## 2. Regole generali

| Regola | Applicazione |
|---|---|
| Unica fonte primaria | I sorgenti Markdown nel repository sono la fonte ufficiale |
| Navigazione esplicita | Ogni pagina pubblicata deve essere presente in `mkdocs.yml` |
| ID stabili | Requisiti, rischi, controlli, decisioni e deliverable usano identificativi univoci |
| Revisione tracciata | Le modifiche passano da commit e Pull Request |
| Sicurezza | Non inserire segreti, credenziali, chiavi o dati personali |
| Coerenza | Terminologia, stati, date e versioni devono essere allineati |

## 3. Ruoli operativi

| Ruolo | Responsabilità |
|---|---|
| Documentation Owner | Mantiene struttura, qualità e coerenza MkDocs |
| Architecture Owner | Valuta impatti su componenti, dati e decisioni |
| Operations Owner | Valida procedure di avvio, chiusura, recovery e incident |
| Data Owner | Valida warehouse, analytics, KPI e qualità dati |
| Release Owner | Applica readiness, release notes e rollback |
| Reviewer | Controlla contenuti, link, registri e rischi |

## 4. Workflow documentale

1. Identificare il bisogno documentale e collegarlo a `DSG-MR-001` o a una change request.
2. Verificare se esiste una pagina coerente da aggiornare.
3. Creare o modificare il file Markdown mantenendo stile e naming esistenti.
4. Aggiornare registri, link e navigazione.
5. Eseguire i controlli documentali disponibili.
6. Creare commit con messaggio chiaro.
7. Aprire o aggiornare la Pull Request.
8. Registrare eventuali follow-up non bloccanti.

## 5. Convenzioni di naming

| Oggetto | Convenzione | Esempio |
|---|---|---|
| Requisito | `DSG-REQ-AREA-000` | `DSG-REQ-DOC-001` |
| Rischio | `DSG-RSK-AREA-000` | `DSG-RSK-DATA-001` |
| Controllo | `DSG-CTL-AREA-000` | `DSG-CTL-REL-001` |
| Decisione | `DSG-ADR-000` | `DSG-ADR-004` |
| Deliverable | `DSG-DEL-000` | `DSG-DEL-010` |
| Procedura | `DSG-SOP-AREA-000` | `DSG-SOP-DOC-001` |

## 6. Standard contenuti

Ogni documento enterprise importante deve includere:

- scopo e ambito;
- stato, versione e owner;
- riferimento a `DSG-MR-001`;
- responsabilità;
- rischi, controlli o dipendenze rilevanti;
- criteri di accettazione;
- collegamenti a documenti correlati;
- regole di manutenzione quando applicabili.

## 7. Quality gate

| Controllo | Criterio |
|---|---|
| Navigazione | La pagina è presente in `mkdocs.yml` |
| Link interni | I collegamenti relativi puntano a file esistenti |
| Marcatori aperti | Non sono presenti segnaposto operativi o sezioni vuote |
| Tracciabilità | Gli ID citati esistono nei registri o nei documenti collegati |
| Sicurezza | Nessun segreto, token, password o dato personale non necessario |
| Coerenza | Stati e date sono coerenti con la baseline |

## 8. Regole per revisioni

Il reviewer verifica:

- allineamento con roadmap e registri;
- assenza di duplicazioni;
- chiarezza delle responsabilità;
- applicabilità delle SOP;
- correttezza delle matrici;
- impatto su release e governance.

## 9. Collegamenti principali

- [Master Roadmap](DSG-MR-001-master-roadmap.md)
- [Registri](registries/index.md)
- [SOP](sop.md)
- [Governance](governance.md)
- [Release documentation](release-documentation.md)
