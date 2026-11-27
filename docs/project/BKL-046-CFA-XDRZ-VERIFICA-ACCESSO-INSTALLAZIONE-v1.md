# BKL-046 — Permessi effettivi per l’installazione del launcher CFA v4

Su DSG‑Shared, dal token ordinario, due riletture hanno ottenuto lo stesso esito. Il chiamante può aprire in scrittura sia il launcher sia il modulo di configurazione nella cartella di collaudo su O:. Può anche eliminare o cambiare la DACL di entrambi. La verifica apre e chiude handle con diritti specifici e non effettua modifiche.

Sulla radice Program Files, lo stesso token può leggere il descrittore ma riceve Win32 5 per creazione di file o sottocartelle, eliminazione di figli e modifiche a DACL e proprietario. La radice è quindi una candidata per una futura installazione protetta. L’esito va ripetuto sulla directory effettiva e sui due file dopo la posa, sotto il token ordinario. La directory di prova e i risultati di elaborazione possono restare su O: e H: secondo il soggetto CFA v4.

Il modulo operativo resta da configurare con le identità dei revisori e la provenienza dell’approvazione. Non sono stati modificati permessi o file installati. Nessuna ammissione richiesta, nessuna esecuzione nativa.
SHA-256 archivio H: 662bf85d776a5e30938cbd0126706ac3bf329cc2941bd7e45601fa753d4992e4.
