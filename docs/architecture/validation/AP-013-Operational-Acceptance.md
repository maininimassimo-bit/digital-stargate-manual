# AP-013 — Formal Operational Acceptance

| Campo | Valore |
|---|---|
| Identificativo | `OA-AP013-001` |
| Package | AP-013 — Scientific Image Repository Architecture |
| Data | 11/08/2026 |
| Stato | Accepted |
| Architecture review | ARB-013 — Approved with conditions |
| OAT | AP-013-OAT-001 — Passed |
| Operational increment | AP-013B — Limited Production |

## 1. Decisione

AP-013 è **formalmente accettato** come Architecture Package e come baseline governante del Scientific Image Repository di Digital StarGate.

L'accettazione comprende il percorso operativo di ingestion scientifica COPY_ONLY validato e promosso tramite AP-013B. Non estende la certificazione a capability non eseguite quali long-term preservation/restore, completa provenance PixInsight, migrazione integrale dell'archivio o scale-out a 1000 file.

## 2. Condizioni vincolanti

Restano valide le condizioni ARB-013:

- `ARB-013-C01` — nessuna dichiarazione di preservation/RPO/RTO certificata senza restore evidence;
- `ARB-013-C02` — nessuna provenance retroattiva o completa dichiarata senza evidence;
- `ARB-013-C03` — migrazione e scale-out restano phased e richiedono nuova validazione;
- `ARB-013-C04` — distinguere contract architecture da schema/runtime effettivamente implementato.

Per AP-013B restano inoltre obbligatori:

- `MaxFilesPerRun <= 30`;
- `COPY_ONLY`;
- SHA-256 e protocollo READY;
- no overwrite;
- no source/transport automatic cleanup;
- OneDrive come transport/staging, non repository autorevole;
- task SMB legacy disabilitata salvo rollback esplicito.

## 3. Authority boundary

AP-013 mantiene autorità su:

- scientific asset identity;
- integrity/checksum semantics;
- storage locator semantics;
- scientific asset lifecycle;
- processing provenance model;
- ingestion integrity rules.

AP-014 mantiene una proiezione catalog/search read-only e non può alterare retroattivamente asset, checksum o provenance AP-013.

AP-013 non possiede autorità di comando verso dispositivi fisici dell'osservatorio; interlock e safety authority restano indipendenti.

## 4. Stakeholder approval

Il Project Owner registra la seguente approvazione comunicata:

> Leonardo Di Egidio ha letto ed approvato.

L'approvazione stakeholder integra, ma non sostituisce, la decisione indipendente ARB-013 e le relative condizioni.

## 5. Closure statement

Con:

- ARB-013 = `Approved with conditions`;
- AP-013-OAT-001 = `Passed`;
- AP-013 Operational Acceptance = `Accepted`;
- AP-013B QG-20 = `Passed — Limited Production`;

il package **AP-013 può essere classificato `completed` secondo l'evidence contract repository**, mantenendo aperte e visibili le condizioni ARB-013 come vincoli di evoluzione e non come blocker della chiusura architetturale.

## 6. Stato finale

**Stato: Accepted**

**AP-013 — Formal Closure Authorized.**