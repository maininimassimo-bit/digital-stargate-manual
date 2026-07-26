# Documentation Modernization Charter

| Campo | Valore |
|---|---|
| Identificativo | DSG-GOV-001 |
| Versione | 1.0 |
| Stato | Active |
| Data | 26/07/2026 |
| Ambito | Intero repository Digital StarGate |

## 1. Scopo

Il presente Charter istituisce il programma di modernizzazione documentale di Digital StarGate.

L'obiettivo è trasformare la documentazione da insieme di pagine tecniche a sistema organico, versionato, navigabile e storicizzato, capace di descrivere il progetto senza richiedere la consultazione diretta della cronologia Git.

## 2. Obiettivi

Il programma deve:

- definire un'architettura documentale stabile;
- ricostruire la storia delle release e delle milestone concluse;
- collegare decisioni, assessment, release note e risultati;
- introdurre standard permanenti per package e baseline;
- rendere la documentazione verificabile con quality gate ripetibili;
- preservare la separazione tra engineering e operations.

## 3. Ambito

Sono inclusi:

- manuale tecnico;
- documentazione architetturale;
- ADR e assessment;
- documentazione developer e UI;
- release note e milestone package;
- baseline documentali;
- project history;
- procedure operative e di validazione.

Non sono inclusi nella prima fase:

- riscrittura indiscriminata dei capitoli tecnici già validi;
- modifica retroattiva dei commit storici;
- alterazione dei dati operativi prodotti dall'EAGLE.

## 4. Principi

1. **Repository come fonte ufficiale** — ogni documento approvato risiede nel repository.
2. **File completi** — gli aggiornamenti vengono consegnati come documenti completi, non come frammenti.
3. **Tracciabilità** — ogni milestone deve essere collegata alle proprie evidenze.
4. **Coerenza temporale** — la ricostruzione storica distingue fatti documentati, inferenze e lacune.
5. **Validazione obbligatoria** — ogni wave deve superare `mkdocs build --strict`.
6. **Separazione dei ruoli** — PC Principale per engineering, EAGLE per operations.
7. **Evoluzione controllata** — ogni modifica strutturale segue branch, review e merge.

## 5. Organizzazione in wave

### Wave 1 — Documentation Foundation

Definizione degli standard, degli indici, della governance e dell'architettura documentale.

### Wave 2 — Historical Reconstruction

Ricostruzione delle release e delle milestone concluse usando commit, documenti, release note e ADR.

### Wave 3 — Documentation Intelligence

Introduzione di timeline, project evolution, relazioni incrociate e indicatori di copertura documentale.

## 6. Deliverable minimi

- ADR-004 — Operational Architecture;
- Documentation Modernization Charter;
- Milestone Package Standard;
- Documentation Baseline Standard;
- Project History Framework;
- Milestone Index;
- aggiornamento della navigazione MkDocs;
- checklist di validazione.

## 7. Criteri di completamento di una wave

Una wave è completata quando:

- tutti i file previsti sono presenti;
- la navigazione è aggiornata;
- i riferimenti interni sono validi;
- non sono presenti placeholder non dichiarati;
- `mkdocs build --strict` termina senza errori;
- il riepilogo della wave è disponibile;
- le modifiche sono pronte per review e merge.

## 8. Governance

Il PC Principale mantiene la responsabilità di integrazione, validazione e rilascio.

L'EAGLE riceve esclusivamente contenuti approvati da `main` e continua a svolgere il ruolo di nodo operativo.

## 9. Risultato atteso

Al termine del programma, Digital StarGate disporrà di un Engineering Handbook capace di descrivere:

- architettura;
- operatività;
- governance;
- storia del progetto;
- motivazioni delle decisioni;
- stato delle release;
- criteri di manutenzione ed evoluzione.
