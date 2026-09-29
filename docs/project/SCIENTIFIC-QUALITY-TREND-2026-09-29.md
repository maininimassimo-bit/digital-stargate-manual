# Scientific Data Quality — andamento score per setup

Il riquadro Q è sostituito da un grafico SVG accessibile, senza librerie grafiche o rendering continuo aggiuntivi. L'introduzione occupa l'intera larghezza; grafico e atlas3D condividono la riga seguente con bordi superiore/inferiore allineati. Sotto700px si dispongono in verticale.

## Fonte e aggiornamento

Il consumer continua a validare SHA-256 del catalogo, projection e reportF5 prima di renderizzare. scientific-quality-trend.mjs unisce assessments e catalogo per sessionId e raggruppa per configurationId; usa observationDate per l'asse temporale e assessment.score.value senza ricalcolo, ranking o media tra setup. Ogni punto apre il dettaglio della sessione. Legenda attivabile con tastiera; tabella espandibile con tutti i valori e gli stati.

La pipeline analyze-session-automatic.yml e refresh-scientific-session-catalog.sh già rigenerano projection e validation dopo importazione. Il grafico usa gli stessi file: nessun dataset parallelo da mantenere. Alla pubblicazione dei nuovi JSON, una nuova visita li recupera senza cache; una pagina aperta e visibile li ricontrolla ogni5 minuti. Una scheda nascosta non effettua polling. La pipeline GitHub/Pages determina quando l'importazione diventa visibile, non il solo orario di upload.

Score null, non finiti, fuori0–100, INVALID/UNAVAILABLE e date non valide non diventano0. Le sessioni mancanti interrompono le linee del loro setup; uno score isolato rimane un punto. Setup UNKNOWN è conteggiato esplicitamente e non attribuito a uno dei due setup. I gruppi sono ricavati dinamicamente, non limitati a due ID fissi. Il profilo resta sperimentale e non autorizzato per decisioni produttive. Un errore di fetch o integrità rimuove il grafico precedente e mostra l'indisponibilità.

## Verifica

Test mapping: ordine diverso, join per identità, nuova sessione/setup, zero valido, valori/date mancanti. Browser: conteggi contro dati correnti, toggle serie, focus su punto, allineamento, nessun overflow a1440/1157/768/390px, temi chiaro/scuro e fail-closed al refresh automatico. Controlli esistenti di freshness invariati. Build MkDocs strict.
