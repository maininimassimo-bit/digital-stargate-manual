# Handover TVCC interna pubblica — 14 ottobre 2026

L'Owner autorizza la ripresa interna sul portale pubblico. La vista Interno e
la selezione automatica OPEN usano un ponte JPEG/MJPEG sul Raspberry AllSky;
le credenziali RTSP rimangono nella configurazione privata fuori dal webroot.
Esterno e Dall'alto conservano il modello illustrativo. Nessuna autorità di
comando o Safety è aggiunta; i badge continuano a dipendere dalla telemetria.

Contratto, installazione, limiti, freshness, sospensione, test e rollback:
[DSG-DOME-CAMERA-001](../developer/dome-camera-public-relay.md).
La verifica reale della pubblicazione deve essere registrata nella ricevuta
di rilascio della PR: i test simulati non certificano da soli il video live.

Il collaudo pubblico PR591 ha rilevato un reset della selezione manuale al
riavvio del renderer dopo Vista essenziale. Il fix successivo preserva la vista
manuale in mountScene e aggiunge una regressione specifica: la ripresa dopo la
pausa deve tornare su Interno anche con badge UNKNOWN, senza alterare il badge.

La precedente documentazione delle catene informative è integrata e pubblicata
con PR #590, merge `414835120031186ed6cfb74f8053aa40746033d2`, 17 gate post-merge
positivi e Pages run 38553859316. La TVCC è un'integrazione distinta da quel rilascio.
