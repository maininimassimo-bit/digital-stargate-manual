# Controllo di fase Bayer su M51 con Canon EOS 6D

Il catalogo dell’autore indica Canon EOS 6D e telescopio Skywatcher N200/1000. La directory centrale ZIP64 della revisione HTTP fissata elenca 159 pose light CR2. Sono state selezionate la prima, la centrale e l’ultima nell’ordinamento lessicografico, con richieste HTTPS per intervallo. Per ciascuna sono verificati lunghezza e CRC della directory ZIP, SHA‑256 locale e modello nell’EXIF. Una ripresa dopo timeout ha riletto il CRC delle due pose già ricevute e ha scaricato la terza a intervalli più piccoli. [Catalogo di Santiago Rodriguez](https://amor.cms.hu-berlin.de/~rodrigus/datasets.html)

Tutte e tre le pose riportano 45,3 secondi a ISO 800. Il decoder legge RGGB nella mappa RAW intera e in quella visibile, con origine del ritaglio alla riga 38 e colonna 72. Le due coordinate pari conservano la fase. Il rapporto registra l’orientamento dichiarato dal decoder e analizza il mosaico senza applicare quel valore come rotazione.

M51 aggiunge un’acquisizione distinta e una terza camera ai controlli sulla fase memorizzata. L’archivio completo non è stato scaricato. Il riscontro copre tre pose e lascia aperta la verifica fisica dell’orientamento e la lettura nativa. Il dataset MILAN M3 del catalogo Zenodo è rimasto indisponibile dalla sessione. [Record MILAN](https://zenodo.org/records/6865830)

Il metodo di acquisizione legge una coda ZIP64 già fissata e verifica ETag e Content-Range. Per riprodurre offline usare `verifica.py <originali> <directory-IC1805> <rawpy-estratto> <pacchetti-Python> <directory-DLL-VC> <nuovo-riscontro.json>`. I tre file originali restano nella custodia locale. La PR contiene il codice e i riscontri di verifica.
