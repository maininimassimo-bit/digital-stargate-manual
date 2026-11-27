# BKL-046 · Custodia degli ingressi del controllo XDRZ

Il custode apre in lettura esclusiva rispetto a scrittura e cancellazione i 12 XDRZ e i sei FITS del manifest del controllo sull'origine. Ricalcola gli SHA-256 dagli stessi handle che lascia aperti. Emette HELD solo dopo la verifica di tutti gli ingressi e mantiene gli handle fino alla chiusura della pipe. Riusa le primitive Windows del custode v4, fissate per impronta.

Nel collaudo su copie esatte in NTFS su DSG-Shared, tutti i 18 ingressi erano leggibili e tutti i 18 tentativi di aprirli in scrittura sono stati respinti mentre gli handle erano attivi. Dopo la chiusura, tutti tornavano apribili e le impronte coincidevano. Negli altri tre casi il custode non ha segnalato disponibilità: XDRZ alterato, FITS mancante e conflitto con un handle di scrittura già aperto. Nel fallimento gli handle già aperti sono stati rilasciati.

Questo componente prepara la protezione degli ingressi tra controllo e uso. Restano da associare i percorsi effettivi all'installazione protetta, adoperare l'handshake nel parent revisionato e mantenere il custode vivo fino alla fine dell'elaborazione. I test usano copie locali e non eseguono PixInsight o R4. [Manifest del batch candidato](../bkl046-cfa-origin-batch-candidate-v1/batch-manifest.json)

Il comando riceve il file batch-manifest.json, il modulo Windows originario archive_hold.py, la directory dei 12 XDRZ e la directory dei sei FITS. La verifica offline con Python 3.12 si ripete con collaudo.py, directory del kit e percorso di uscita. Il kit include gli ingressi usati.