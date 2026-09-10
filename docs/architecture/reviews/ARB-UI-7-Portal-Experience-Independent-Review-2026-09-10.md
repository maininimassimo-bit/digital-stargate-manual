# ARB Independent Review — UI 7.0 Portal Experience

| Campo | Valore |
|---|---|
| Review | ARB-UI-7 |
| Data | 10/09/2026 |
| Oggetto | DSGP-SOL-001, DSG-UI-001 v2.0, DSG-DEV-001 v2.0, DSG-REL-UI-7.0 |
| Exact head valutato | `d6da7a22ba4045e5d3fe088a89e84b1b9abed0da` |
| Base | `b49a7f99ca89d93e8ca55043a810f14abfcba29a` |
| PR | #155 |
| Decisione | **APPROVED** |

## 1. Executive decision

L'Architecture Review Board approva UI 7.0 per l'integrazione. Il package è coerente con l'architettura Digital StarGate, resta nel presentation boundary, non altera contratti scientifici o Safety Authority e corregge il rischio di contenuto stale senza ampliare i workflow privilegiati.

La pubblicazione GitHub Pages e la verifica post-merge restano gate di release, non precondizioni architetturali mancanti.

## 2. Scope reviewed

- information architecture e navigazione MkDocs;
- homepage, hub e shell visuale;
- dynamic content e freshness contract;
- gestione di pagine duplicate, stale e legacy;
- accessibilità e responsive behavior;
- sicurezza, safety, rollback e operabilità;
- traceability tra solution architecture, design system, audit, guideline e release note.

## 3. Assessment

| Area | Esito | Evidenza |
|---|---|---|
| Coerenza con vision e ADR | Conforme | MkDocs/GitHub Pages e URL pubblici preservati; nessun nuovo stack o BFF |
| Domain e layer integrity | Conforme | UI consumer read-only di projection; nessun accesso a log grezzi o dispositivi |
| Dynamic freshness | Conforme | Homepage e Architecture Center leggono projection governate con `cache: no-store` |
| Failure semantics | Conforme | loading/UNKNOWN/UNAVAILABLE espliciti; nessun fallback con KPI storici plausibili |
| Safety | Conforme | nessun device command; stato storico non promosso a stato Safety corrente |
| Security | Conforme | nessuna modifica a permessi Actions, push automatici o deploy privilegiati |
| Information architecture | Conforme | sei percorsi principali più Home; hub primari resi raggiungibili |
| Accessibility | Conforme con verifica post-merge | focus visibile, drawer inert/Escape/focus return, reduced motion e fallback statico |
| Migration e compatibilità | Conforme | nessun rename/delete; progressive enhancement e Material mobile preservati |
| Operabilità e rollback | Conforme | revert UI-only; dataset, workflow, runtime ed evidence invariati |
| Traceability | Conforme | DSGP-SOL-001, DSG-UI-001, audit freshness, guideline e release note coordinati |

## 4. Dynamic-update decision

La scelta di non aggiungere `docs/index.md` a un workflow con write/push/deploy privilegiati è approvata. La homepage usa invece le projection che il processo di import già rigenera e pubblica: catalogo sessioni, latest observation e roadmap. Questo riduce blast radius e rimuove la duplicazione editoriale.

Il comportamento in assenza di JavaScript è intenzionalmente fail-closed: struttura e percorsi restano disponibili, mentre i valori current non vengono simulati.

## 5. Quality evidence on reviewed head

| Gate | Run | Esito |
|---|---:|---|
| Scientific Platform Governance | 34534715089 | SUCCESS |
| Validate documentation (no deploy) | 34534715150 | SUCCESS |
| Genera manuale Word | 34534715152 | SUCCESS |
| JavaScript syntax check locale | exact working copy | PASS |
| YAML syntax e CSS structural check | exact working copy | PASS |
| Primary-surface stale scan | exact working copy | PASS |

## 6. Risks and follow-up

| Rischio residuo | Severità | Disposizione |
|---|---|---|
| Assenza di visual regression automatizzata cross-browser | Bassa | Non bloccante; già registrata nell'audit freshness |
| Validazione del layout sulla URL Pages definitiva | Bassa | Gate obbligatorio post-merge |
| Evoluzione futura degli schema projection | Bassa | I consumer tollerano campi additivi e falliscono chiuso sui campi essenziali |

## 7. Conditions of approval

1. Eseguire CI sull'head che pubblica questa review.
2. Non introdurre modifiche ai workflow privilegiati nel package UI 7.0.
3. Richiedere Release Quality review prima del merge.
4. Verificare deploy Pages e superfici principali sul merge SHA.

## 8. Final statement

**APPROVED.** UI 7.0 è architetturalmente pronta per il gate Release Quality e l'integrazione protetta, subordinatamente alle condizioni sopra elencate.
