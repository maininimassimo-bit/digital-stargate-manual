# BKL-046 · Acquisizione con scadenza su DSG-Shared

Il candidato esegue PrintWindow in un processo ausiliario. Il processo principale conserva l'handle originale e la facoltà di inviare WM_CLOSE. L'ausiliario verifica identità di processo e finestra e controlla che la finestra risponda prima e dopo la cattura. Il chiamante verifica formato BMP e identità prima di autorizzare una sola chiusura.

Due esecuzioni indipendenti hanno riprodotto tre esiti:

| Caso | Riscontro |
| --- | --- |
| Finestra testimone reattiva | BMP di riferimento riprodotto. Chiusura prima dell'acquisizione respinta e chiusura ordinaria osservata dopo l'acquisizione. |
| Finestra con coda messaggi sospesa | Acquisizione respinta in circa 0,48 s. Processo e HWND originali ancora presenti. |
| Ausiliario sostituito nel test con un processo in attesa | Termine scaduto in circa 3 s. Processo e HWND originali ancora presenti. |

Nei due casi di errore il supervisore ha respinto chiusura e tentativi ulteriori. La sostituzione dell'ausiliario è confinata al test. Resta da integrare e revisionare il candidato nel launcher e da qualificare la resa della finestra Qt sotto ammissione. Le prove native e le chiusure scientifiche restano a zero.
SHA-256 archivio H: b1923ad56e70348b5fc4c8d7d6499ffe14850d734ef7dabc20880f7aa4c5e6b2.
