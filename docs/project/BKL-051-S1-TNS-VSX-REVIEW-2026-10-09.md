# BKL-051 — schede private di revisione TNS e VSX

| Campo | Valore |
|---|---|
| Identificativo | DSG-BKL051-CHANNEL-REVIEW-001 |
| Versione / data | 1.0 / 2026-10-09 |
| Stato | Implementazione locale candidata; release gates pending |
| Perimetro | S1-R/S4-R, schede private, nessun payload provider o invio |
| Predecessore | PR #536, merge `3f9c93d5e142a0f01c5676a7477dc7ad46519712`, post-merge verificato |

## Risultato e limiti

`tools/scientific_transients/channel_review.py` prepara schede locali JSON/UTF-8 per le sole categorie dichiarate EXTRAGALACTIC_TRANSIENT_CANDIDATE/TNS e VARIABLE_STAR_CANDIDATE/VSX. L'Owner può controllare dati, sistemi/unità e riferimenti alle evidenze prima di costruire un payload definitivo. Non classifica la sorgente, non misura immagini, non sceglie il destinatario dal contenuto, non valida requisiti o identificatori provider e non modifica queue/authority. Le schede non sono compatibili per invio diretto con API o moduli provider.

Ogni richiesta ha SHA256 fissato dal chiamante locale fidato, identificatori opachi, schema chiuso, origine dichiarata e binding al registro privato. Il manifest e tutti i byte registrati sono verificati prima e dopo l'esportazione. La verifica attesta solo integrità point-in-time su file Owner quiescenti, non autenticità, correttezza o indipendenza scientifica. I percorsi restano nel JSON privato; la scheda testuale li omette. Sono conservati ruoli, dimensioni e hash.

Sempre PRIVATE_REVIEW_WORKSHEET, NOT_VALIDATED, declarationsAttested false, providerPayload false, providerSchemaValidated false, providerReadiness NOT_EVALUATED, submissionAuthorized false, externalSubmission NONE e providerAcknowledgement NONE. Nessun campo di consenso, API key, endpoint arbitrario o allegato è accettato. Nessuna chiamata di rete, account, credenziale, bozza mailbox, upload o pubblicazione. API e CLI locali esplicite; nessun intake di file nel browser o attivazione cloud.

## Contratto locale

- Campi comuni: autore dichiarato; coordinate in gradi; frame ICRS/FK5/non attestato, equinozio separato, epoca coordinata in anno giuliano e scala TCB/TDB/TT/non attestata; evidenza astrometrica. ICRS non viene chiamato equinozio J2000. Le associazioni restano non attestate.
- Fotometria dichiarata da 1–128 immagini registrate distinte: metà esposizione UTC, durata, magnitudine, errore casuale 1σ in mag, sistema AB/Vega/strumentale/non attestato, banda e riduzione. Nessuna trasformazione di flussi/bande o correzione temporale. Stessi byte su percorsi distinti non provano indipendenza. Errore casuale non è budget completo.
- Controlli di variabili/oggetti mobili/report precedenti: dichiarazioni distinte NOT_CHECKED/NO_MATCH/POSSIBLE_MATCH/INCONCLUSIVE. I controlli dichiarati eseguiti richiedono data UTC ed evidenza registrata, senza attestare completezza, aggiornamento o verità. Cataloghi e identificazioni restano non validati.
- Sezione TNS: nome interno, gruppo e fonte dichiarati senza ID provider inventati; immagine di scoperta dichiarata selezionata tra le osservazioni; immagini precedenti e stato di presenza distinto dal limite; sigma del limite dichiarata senza criterio operativo; contesto archivistico con evidenza; ospite/redshift dichiarati senza associazione dedotta. Un limite non produce NON_DETECTION. Il contesto non sostituisce automaticamente i requisiti del provider.
- Sezione VSX: nome e cross-ID testuali con evidenza; tipo di variabilità dichiarato senza validazione del vocabolario provider; range con magnitudine più brillante numericamente minore o uguale a quella più debole; banda/evidenza; periodo in giorni, epoca HJD e scala temporale/evento separati, evidenza; riferimenti a curve/diagrammi di fase/carte dichiarati. Nessuna inferenza di periodo, classificazione, origine o qualità dei grafici; nessuna lettura/upload delle figure. HJD non viene ricavato da UTC, JD o nomi FITS.

Null resta UNKNOWN; NOT_ATTESTED/NOT_ASSESSED/NOT_CHECKED restano espliciti. Numeri stringa decimale fino a nove cifre frazionarie e 24 caratteri, senza arrotondamento/esponenti/nonfinite/bool. Date UTC ordinarie Z fino a sei frazioni, date false/leap second respinti senza normalizzazione. Limiti di lunghezza, liste e valore numerico sono capacità del parser, non soglie scientifiche o vincoli provider. Testo UTF-8 single-line; controlli, bidi invisibile e surrogati respinti, nessuna traslitterazione. Schema chiuso e JSON duplicate-key fail-closed.

Output root esistente separata da artifact/registry/source; directory reviewRef creata esclusivamente, senza overwrite o retry implicito. worksheet.json e worksheet.txt precedono il secondo controllo; solo dopo si scrive export.json con digest. Un errore conserva partial e failed.json, senza ricevuta di successo. Conservare genitori: completeDependencyArchive false.

## Fonti e verifica dei requisiti esterni

Il 9 ottobre la [guida VSX](https://vsx.aavso.org/index.php?view=about.notice) è consultabile: chiede coordinate e identificazioni, controllo duplicati, fotometria/banda e grafici di supporto; per periodicità prevede periodo/epoca e diagrammi di fase. Il percorso resta assistito nel modulo ufficiale e soggetto a moderazione. Questa scheda organizza dichiarazioni ed evidenze; non attesta qualità, completezza o accettazione.

L'apertura diretta della [guida TNS](https://www.wis-tns.org/content/tns-getting-started), [FAQ](https://www.wis-tns.org/content/faq) e [manuale Bulk 2.0](https://www.wis-tns.org/sites/default/files/api/tns2_manuals/TNS2.0_bulk_reports_manual.pdf) restituisce HTTP403 nella sessione. Estratti indicizzati delle stesse fonti ufficiali descrivono report AT, fotometria/non-detection o informazioni archivistiche e sviluppo delle API soltanto nel sandbox. Non abbiamo scaricato né fissato i byte del manuale corrente: nessuno schema ufficiale viene dichiarato validato; mappatura degli ID, payload e requisiti attuali restano aperti. Le ricevute private conservano esiti/limiti, senza aggirare il controllo di accesso. Nessun sandbox o endpoint di invio è contattato.

## Verifica e criteri residui

Venti test sintetici PASS sul renderer aggiornato, inclusa CLI locale/stale digest; suite aggiunta alla CI Windows/Linux. Coprono precisione/origine/unknown, UTF-8 e injection, unità/epoche, limiti/non-detection, HJD non trasformato, range e cross-ID, manifest e byte cambiati, request stale/duplicate keys, output overlap/create-only e partial dopo seconda verifica fallita. La regressione locale precedente comprende 72 casi: 71 PASS, uno SKIP Windows per privilegi symlink; MkDocs strict e layout desktop chiaro/scuro, tablet e focus PASS. L'aggiornamento testuale del renderer è poi verificato dai 20 test mirati; CI sul commit corrente deve coprire la regressione completa. Review ARB poi RQ sul commit esatto, merge protetto e post-merge/Pages restano gate di rilascio propri. Nessuna prova su dati reali o provider viene dedotta dai test.

Restano necessari: misure e classificazioni indipendenti con budget completo, astrometria/timing/covarianze, recuperi e falsi positivi ciechi, moving objects/tracklet; intero percorso scientifico e servizio; payload correnti TNS/VSX e estensioni MPC/CBAT, ledger, conferma esatta, authority, revoca, invio/risposta persa/riconciliazione, test provider quando ammessi, policy quantitativa Owner, accessibilità e S5. Le condizioni di invio/pubblicazione restano separate dallo sviluppo già approvato. BKL-051 OPEN / NOT_VALIDATED.

## Continuità e rollback

PR #536 conclusa: ARB poi RQ AI-assistite sul `7ca5655899565f02917899e6ee6c3a0c2a364557`, 17 check/15 workflow; merge reale sopra, 15 workflow post-merge e sette risorse pubblicate verificate. Non è accettazione scientifica o umana. Prove native Atami/AT2018cow, master/pixel/History e archivi sono conservati senza rilancio. Refunc ZTF completo verificato diagnosticamente; input storico, rumore interno/covarianze e calibrazione ancora non attestati. IRSASD-21929/21930: nell'ultima ricerca conservata sole prese in carico, nessuna risposta tecnica attestata o reinvio. Gaia TOP100 incompleto, associazioni non accettate, timing condizionale.

Rollback: revert coerente di modulo/test/CI/docs e rigenerazione delle projection tramite generator ufficiali; conservare tutte le evidenze ed esportazioni private. Nessuna migration, dipendenza runtime, nuovo cloud/account/credenziale, soglia o fotografia. P6 Accepted nei limiti; F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva, S10/Safety e collegamento C→F invariati. [Handover](HANDOVER_2026-10-09-BKL051-TNS-VSX-REVIEW.md), [piano reporting](BKL-051-SCIENTIFIC-REPORTING-PLAN-2026-10-08.md), [ADR-020](../architecture/ADR-020-Private-Scientific-Transient-Analysis.md).

Versione 1.0: preparazione locale delle schede per TNS/VSX, nessun canale operativo o milestone chiusa.
