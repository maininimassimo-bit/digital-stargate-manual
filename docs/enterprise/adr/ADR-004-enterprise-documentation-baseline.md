# ADR-004 - Enterprise documentation baseline DSG-MR-001

| Campo | Valore |
|---|---|
| Identificativo | `DSG-ADR-004` |
| Roadmap | `DSG-MR-001` |
| Stato | Approvata |
| Data | 26/07/2026 |
| Owner | Massimo Mainini |
| Ambito | Documentazione enterprise e governance MkDocs |

## Contesto

Digital StarGate dispone di un manuale tecnico MkDocs con capitoli operativi, architettura, analytics, warehouse, release notes e appendici.

La roadmap `DSG-MR-001` richiede una baseline enterprise completa, capace di rendere tracciabili obiettivi, requisiti, rischi, controlli, decisioni, procedure e release senza alterare la struttura documentale esistente.

## Opzioni considerate

| Opzione | Descrizione | Vantaggi | Limiti |
|---|---|---|---|
| A | Integrare tutto nei capitoli esistenti | Continuità con il manuale | Rischio di disperdere roadmap, registri e governance |
| B | Creare una sezione enterprise dedicata in MkDocs | Tracciabilità chiara e navigazione esplicita | Richiede cross-reference con i capitoli tecnici |
| C | Tenere la baseline fuori da MkDocs | Separazione forte | Perdita di visibilità, build e review centralizzata |

## Decisione

Si adotta l'opzione B: creare una sezione MkDocs dedicata a `DSG-MR-001`, mantenendo i capitoli tecnici esistenti e collegandoli tramite registri, matrici e riferimenti.

La sezione enterprise diventa il punto di governo della documentazione, mentre i capitoli tecnici rimangono la fonte descrittiva operativa e specialistica.

## Conseguenze

| Area | Effetto |
|---|---|
| Navigazione | Nuova sezione `Enterprise DSG-MR-001` in `mkdocs.yml` |
| Tracciabilità | ID stabili per requisiti, rischi, controlli, deliverable e decisioni |
| Governance | Workflow di review e release esplicitato |
| Manutenzione | Ogni modifica strutturale richiede aggiornamento dei registri |
| Qualità | Build MkDocs e link interni diventano controlli obbligatori |

## Collegamenti

- Roadmap: [DSG-MR-001](../../enterprise-roadmap/DSG-MR-001-master-roadmap.md)
- Architecture: [DSG-EA-001](../enterprise-architecture.md)
- Registri: [DSG-REG-001](../registries/index.md)
- Governance: [DSG-GOV-001](../governance.md)
- Release documentation: [DSG-REL-001](../release-documentation.md)

## Criteri di validazione

- la sezione enterprise è presente nella navigazione;
- i documenti minimi della roadmap sono disponibili;
- i registri collegano requisiti, rischi, controlli e deliverable;
- nessun documento enterprise contiene marcatori operativi aperti;
- la PR finale documenta commit, milestone e validazioni.
