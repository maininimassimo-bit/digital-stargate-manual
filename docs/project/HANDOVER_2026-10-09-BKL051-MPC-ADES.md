# Handover — BKL-051 anteprima ADES e provenienza ZTF

| Campo | Valore |
|---|---|
| Versione | 1.0 |
| Data | 2026-10-09 |
| Stato | Package proposto; gate di rilascio da verificare |

## Stato verificato e incremento

BKL-051 OPEN / NOT_VALIDATED. P6 Accepted nei limiti. PR #530 conclusa sul merge `39d6e39977caaae2a68b56f493ec172417e6da4b`; ricevuta finale supersede il postMergePending storico. Main avanzata con PR #531/#532 e forecast governato; nuova branch dall'head `e586c993` senza sovrascrivere il lavoro scientifico privato.

[Dossier corrente](BKL-051-S1-MPC-ADES-PREVIEW-2026-10-09.md): exporter locale ADES 2022 per oggetti numerati, CCD/CMO, Gaia3. Tredici test sintetici e motore XSD indipendente, due positivi/tre negativi. Registro/digest verificati prima e dopo; tentativi parziali conservati, no overwrite. Dichiarazioni non attestate; NOT_VALIDATED, unknown espliciti, nessun invio o policy. CI exact-head, ARB→RQ, merge/post-merge e Pages devono essere verificati sulla consegna effettiva prima di dichiararne il rilascio.

## Evidenze private da preservare

Proseguire dal [passaggio TPV](HANDOVER_2026-10-09-BKL051-LOCAL-TPV.md), senza ripetere 72 fit Atami/36 AT2018cow o i 108 controlli TPV. Originali, History, checkpoint e rami falliti restano genitori esterni; History a monte incompleta. SN2023ixf404 non ritentato. Gaia TOP100 incompleto, tempi HJD/OBSJD e calibrazione ancora condizionali.

Riconciliazione privata del 9 ottobre: riferimento ZTF completo, MD5 calcolato uguale al checksum storico; input effettivo della sottrazione non attestato. Prodotti pubblici corretti e interni differiscono; sigma del fondo non è rumore elettronico; covarianze complete ignote. Sei richieste, negative/timeout/cap preservati, nessun retry automatico. Corretto confronto iniziale tra ora locale Pacific e UTC; nessuna contraddizione temporale dimostrata.

Una sola nuova comunicazione IRSA rumore/provenienza autorizzata e inviata tramite connettore; ricevuta privata e testo esatto conservati nella consegna locale. Non è un resend di IRSASD-21929. Nessuna risposta tecnica attestata dalla ricerca mirata di ripresa. Non adottare UNC come varianze/σ, colori null come zero o un secondo fattore di correzione del rumore.

## Prossima sequenza e confini

Proseguire autonomamente i gate dell'export e gli altri residui di reporting senza invii reali. Per la scienza: acquisire chiarimenti/prodotti sufficienti, verificare input/rumore/registrazione, misure PSF native su copie e confronto indipendente, recuperi/falsi positivi reali e ciechi. Nessuna nuova soglia quantitativa accettata. Moving objects, tracklet, rapporti/integrità del servizio, CBAT/TNS/VSX/MPC, payload Owner/duplicati/revoca/ricevute, accessibilità/S5 restano obbligatori.

Non riattivare servizi o estrarre credenziali: autorizzazioni delle due build, cinque OAT e due probe GCS concluse. Adapter Astropy/NumPy già autorizzato solo locale TPV. Nessun account, segnalazione astronomica, fotografia, dispositivo o modifica della radice C→F. F4 attende lifecycle, F5 segue F4, BKL-050 conclusiva. Non chiudere BKL-051 dalle sole prove diagnostiche o sintattiche.
