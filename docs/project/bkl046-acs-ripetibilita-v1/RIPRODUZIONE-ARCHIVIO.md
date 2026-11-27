# BKL-046 – Riproduzione del supplemento ACS sulle aperture

Il supplemento comprende undici file di analisi e un manifest. In DSG-Shared ho ripristinato 43 file di coorte dallo ZIP originale, tra cui i FITS, e undici file dal supplemento. Ho rigenerato cinque riscontri e le relative impronte SHA-256 coincidono con quelle dell'archivio.

Il ricalcolo copre pesatura frazionaria, spostamenti simulati del centro, finestre di centratura misurate, ripetibilità entro visita e scelta delle esposizioni. Sulle 12 pose GRW+70D5824, passando da una finestra di 5×5 pixel a 3×3 o 7×7, il centro cambia al massimo di 0,0754 pixel per asse. Lo scarto F658N/F660N resta tra +0,513% e +0,562% a 3 pixel. Su una griglia di spostamenti indipendenti di ±0,25 pixel per asse lo stesso rapporto attraversa lo zero a 3 pixel. La griglia misura la sensibilità, mentre l'errore assoluto di centratura resta da determinare.

Lo ZIP del supplemento contiene script e risultati derivati. Per ripetere i calcoli dai FITS occorrono anche lo ZIP di base, SHA-256 7833f865b9bba285eb857e090db9c985e05f57190f7aca798e27cbdecf92d850, archiviato su H:, e l'ambiente di analisi della VM. Questa riproduzione lascia aperta la qualifica del trasferimento fotometrico tra visite. Restano zero controlli qualificati e zero chiusure scientifiche.

[Supplemento](BKL046-ACS-evidenze-apertura-v2.zip) · [Ricevuta di riproduzione](replay-archivio-v2.json)
