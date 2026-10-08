# BKL-051 S4 — Rapporto locale privato

| Campo | Valore |
|---|---|
| Versione | 1.0 |
| Data | 2026-10-08 |
| Stato | Candidate; exact-head CI/review/release gates pending |
| Baseline | PR #514 merge `fc57631112f3ec098d8dbc7f443e6cb50b757f62`, gate e ricevute nella PR |

## Perimetro

`tools/scientific_transients/local_report.py` esporta JSON e HTML privati da un attempt journal già COMPLETED.
Non avvia PixInsight, non acquisisce job/credenziali e non effettua richieste o segnalazioni. Il digest tecnico atteso
è fornito separatamente, ad esempio dalla ricevuta Owner. Identità, sigillo tecnico, catena journal e tutti i byte
snapshot/operazioni/checkpoint sono verificati prima dell'esportazione e ricontrollati dopo la scrittura.
L'HTML mostra il digest tecnico conservato nel portale; `export.json` distingue questo digest da quello dei nuovi
byte `report.json`. Nessuna route, schema di coda, authority, policy o activation modificata.

Le misure sono estratte soltanto dai bundle History del produttore di aperture già supportato: schema chiuso,
input e parametri correlati allo snapshot, checkpoint e quattro History conservate, ordine/sourceRef/unità/runtime
legati alla ricevuta del kernel. Il validatore delle righe è condiviso con il collector nativo, senza modifiche
alla semantica. Le misure restano NORMALIZED_SAMPLE_SUM, coordinate PI_NATIVE_GEOMETRIC, varianza completa e
significatività null. Conteggi confrontati con le righe: measured=0, clipped esclusi, altri incompleti.
Queste qualificazioni non attestano validità della fotometria, origine scientifica, compatibilità di banda,
indipendenza, ricerca cieca, assenza di sorgenti, falsi positivi, candidato o scoperta.

## Uso sul PC

Il chiamante fidato fornisce una directory attempt esistente, il digest tecnico ottenuto indipendentemente e
una root privata esistente e separata. `python -m tools.scientific_transients.local_report --help` elenca gli
argomenti. La CLI non deduce il digest atteso dai file locali e non carica token. Un attempt sigillato può essere
letto dopo restart; un attempt attivo/failed/cancel/recovery non viene esportato come successo o rilanciato.

Directory destinazione esclusiva per attemptId: nessuna sovrascrittura o retry implicito. File parziali e ricevuta
failed restano conservati; senza `export.json` il pacchetto non è completo. HTML passivo, testo escaped e CSP senza
script/network; nessun collegamento eseguibile dalle evidenze. Dati individuali, path e coordinate restano sul PC.
Quiescenza/ACL Owner necessarie: la verifica puntuale dei byte non è sandbox o attestazione indipendente.

Il rapporto JSON conserva tutte le righe, parametri, runtime, riferimenti ai file e relativi hash. Checkpoint,
runtime transitive e archivio genitore restano esterni nella directory indicata; completeDependencyArchive=false.
Esecuzione CALLER_REPORTED_NOT_ATTESTED, History a monte NOT_ATTESTED, science NOT_VALIDATED. Esportazione,
ACK remoto, valutazione Owner e acceptance finale sono eventi separati.

## Validazione

Otto test locali aggiuntivi: sigillo/digest e byte alterati, riapertura del solo attempt terminale, esclusività,
root sovrapposta, attempt attivo, HTML escaping, unità/varianza/authority/binding e failure durante il ricontrollo.
Fixture sintetiche del supervisore, nessun avvio PixInsight o cloud OAT. Suite e CI Windows/Linux nella PR.
Suite locale: 96 prove Python, 95 PASS e un symlink skip per privilegi Windows; 104 prove Node PASS,
MkDocs strict e coerenza roadmap/projection PASS. Non sostituiscono i gate CI sull'head esatto.
Una prova di esportazione sui byte del precedente controllo numerico nativo ha conservato due righe e i limiti,
senza ripetere kernel, solve, detection o elaborazioni. Non è una nuova epoca astronomica né validazione scientifica.

## Residui e rollback

Rapporto di misura del kernel disponibile; workflow scientifico confrontabile completo ancora aperto: calibrazione,
variance/covariance, matching, riferimenti, validation e policy quantitativa. Driver/recovery, accessi/PC/cloud OAT
e reporting CBAT/TNS/VSX/MPC restano successivi. BKL-051 OPEN, S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata.
P6 Accepted, F4/F5/BKL-050, root C→F, gallery, dispositivi/S10/Safety invariati. Runtime e invii restano disabilitati.
Rollback via revert library/test/docs e rigenerazione projection, senza cancellare rapporti/journal/History/input.

[Ricevuta minimizzata](evidence/BKL-051-S4-LOCAL-REPORT-2026-10-08.json).
