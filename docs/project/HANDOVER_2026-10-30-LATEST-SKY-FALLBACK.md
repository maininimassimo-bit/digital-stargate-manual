# Ultima osservazione: campo DSS2 senza Aladin — 30 ottobre 2026

## Problema e contratto

Aladin JS/init va in timeout mentre latest-observation.json contiene la sessione16–17ottobre,NGC281 e coordinate J2000 valide. La precedente foto dell’osservatorio come ripiego non rappresenta il campo dell’oggetto. Il pacchetto26–27ottobre non ha nuove LIGHT: il no-op resta corretto, non è motivo per cambiare latest.

Il consumer carica un ritaglio statico DSS2 tramite HiPS2FITS, indipendente dal JavaScript/WebAssembly/WebGL di Aladin. Parametri: coordinate numeriche J2000 dalla projection,frameICRS,proiezioneSIN,FOV pubblicato validato,800x800pixel,JPG,surveyesatta CDS/P/DSS2/color. Non usa risoluzione del nome o target fisso. La richiesta parte mentre si tenta Aladin; la mappa interattiva, se pronta, ha precedenza. Badge,alt e nota dichiarano immagine di archivio: non è la fotografia della sessione e non certifica acquisizione o astrometria strumentale.

EndpointHTTPS consentiti: alasky.cds.unistra.fr/hips-image-services/hips2fits,poi alaskybis.cds.unistra.fr/hips-image-services/hips2fits. Ogni tentativo è limitato a12secondi; due tentativi massimi per identità della vista. Nessun proxy,credenziale o accessoapparati. Referrer escluso. I due endpoint appartengono a CDS: non garantiscono disponibilità quando tutta l’infrastruttura CDS è fuori servizio. Se entrambi falliscono il campo resta indisponibile con coordinate e messaggio espliciti; nessuna fotografia estranea presentata come survey.

Identità=sessione+coordinate+FOV: cambia insieme ai dati,nessun vecchio ritaglio resta sotto una nuova sessione. Guard generazionali respingono callback tardive dopo cambio dati/rimozioneDOM. Coordinate mancanti/invalide o errore projection eliminano l’immagine astronomica; zero numerico resta valido. Refresh manuale/60svisibile/ritorno visibilità conservati; Aladin recuperabile. Dataset, RAW,ultimaacquisizione e authority immutati.

## Verifiche e rollback

Test browser con fornitori simulati: coordinateesatte,zero,assenza Aladin,ritaglio primario,failoversecondario,entrambiindisponibili,cambiosessione,erroredati e contratti precedenti. FixtureJPEG è soltanto un’immagine di test: non evidenza scientifica. Buildstrict,CI,ARBpoiRQ e postmerge/Pages richiesti;esiti nella PR. Verifica reale del servizio e della pagina senza inventare disponibilità quando esternoirraggiungibile.

Rollback unitario consumer/test/documentazione,nessun rollbackdati. Nessuna installazione o modifica all’osservatorio. DocumentazioneAPI: https://alasky.cds.unistra.fr/hips-image-services/hips2fits .
