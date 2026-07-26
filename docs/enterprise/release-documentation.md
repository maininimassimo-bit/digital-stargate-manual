# DSG-REL-001 - Release Documentation

| Campo | Valore |
|---|---|
| Documento | Release Documentation |
| Identificativo | `DSG-REL-001` |
| Roadmap | `DSG-MR-001` |
| Versione | 1.0 |
| Stato | Approvata per revisione |
| Owner | Massimo Mainini |
| Data baseline | 26/07/2026 |

## 1. Scopo

Questo documento definisce criteri, readiness, note e rollback per il rilascio della documentazione enterprise `DSG-MR-001`.

## 2. Release scope

La release include:

- nuova sezione MkDocs `Enterprise DSG-MR-001`;
- master roadmap;
- enterprise architecture;
- DSRA;
- ADR-004;
- registri;
- handbook;
- SOP;
- assessment;
- governance;
- appendici.

## 3. Readiness checklist

| ID | Controllo | Esito atteso |
|---|---|---|
| `DSG-REL-RDY-001` | Tutti i deliverable minimi sono presenti | Conforme |
| `DSG-REL-RDY-002` | `mkdocs.yml` include la sezione enterprise | Conforme |
| `DSG-REL-RDY-003` | Link relativi principali risolti | Conforme |
| `DSG-REL-RDY-004` | Registri aggiornati | Conforme |
| `DSG-REL-RDY-005` | ADR-004 presente e collegato | Conforme |
| `DSG-REL-RDY-006` | Nessun marcatore operativo aperto | Conforme |
| `DSG-REL-RDY-007` | PR verso `main` con riepilogo milestone | Conforme a valle dell'apertura PR |

## 4. Note di release

### Aggiunte

- Baseline enterprise `DSG-MR-001`.
- Sezione MkDocs dedicata.
- Matrici di tracciabilità tra obiettivi, requisiti, rischi, controlli e deliverable.
- DSRA con piano di trattamento e controlli.
- Governance RACI e quality gate.
- SOP documentazione, dati, release, incident e change management.
- Assessment di maturità e appendici operative.

### Impatti

| Area | Impatto |
|---|---|
| Lettori | Nuova vista enterprise del progetto |
| Maintainer | Registri e quality gate diventano riferimento operativo |
| Reviewer | PR più verificabili grazie a criteri espliciti |
| Release | Readiness e rollback documentati |

### Compatibilità

Non sono modificati i percorsi dei capitoli tecnici esistenti. La release aggiunge una sezione di governo e cross-reference.

## 5. Rollback

In caso di regressione documentale:

1. rimuovere la sezione enterprise da `mkdocs.yml`;
2. mantenere i file enterprise sul branch di lavoro per correzione;
3. correggere link, naming o contenuti incoerenti;
4. ripetere i controlli documentali;
5. riaprire la PR o aggiornarla con commit correttivo.

Il rollback non impatta i dati osservativi né le procedure fisiche dell'osservatorio.

## 6. Evidenze di validazione

Le evidenze attese includono:

- diff dei file Markdown;
- diff di `mkdocs.yml`;
- controllo link interni;
- controllo marcatori aperti;
- riepilogo commit;
- PR verso `main`.

## 7. Follow-up non bloccanti

| ID | Follow-up | Motivazione |
|---|---|---|
| `DSG-FUP-001` | Collegare evidenze operative reali alle checklist dopo le prossime sessioni | Le evidenze nascono dall'uso operativo |
| `DSG-FUP-002` | Riesaminare DSRA dopo test failover e safety | Il rischio residuo migliora con dati reali |
| `DSG-FUP-003` | Allineare future release notes alla baseline `DSG-REL-001` | Mantiene continuità governance |

## 8. Criterio di pubblicazione

La release può essere proposta a `main` quando la PR contiene:

- milestone completate;
- commit logici;
- validazioni eseguite;
- limiti noti non bloccanti;
- riferimento esplicito a `DSG-MR-001`.
