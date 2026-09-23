# ARB — AP-015 / CAP-40 Architecture Review

| Campo | Valore |
|---|---|
| Review ID | `ARB-AP015-CAP40-001` |
| Data | 23/09/2026 |
| Esito | ACCEPTED WITH LIMITATIONS |
| Metodo | AI-assisted repository review, owner-authorized |
| Owner-witness | Massimo Mainini |

## Findings

Il package definisce un modello minimo coerente con BKL-015, BKL-044, AP-011, AP-013 e AP-014. Preserva l’autorità delle fonti, rende citation e provenance first-class, espone conflict/unknown senza imputazione e mantiene la SKL come projection non autoritativa.

## Conditions

- la review AI-assisted non equivale a una review umana indipendente;
- la fixture è bounded e non dimostra ingestione completa o efficacia scientifica;
- graph/vector/RAG, provider, runtime AI, API, scheduler, command e remediation restano non autorizzati;
- ogni futura materializzazione richiederà un package e gate separati con volumi, ownership e query misurabili.

## Decision

AP-015 è accettato come architecture/design baseline di CAP-40. Nessuna modifica a Safety Authority o authority delle fonti è introdotta.
