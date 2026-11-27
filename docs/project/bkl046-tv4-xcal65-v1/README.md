# BKL-046 — TV4 CLEAR1 del 6 marzo 2003

Il controllo di trasferibilità di `DIFFUSE_BACKGROUND/2` usa la sessione MRI `AB / XCAL65` del 6 marzo 2003, con la sfera integratrice da 65 pollici. La selezione registrata prima del download dei FITS include i primi sei dei sette frame in ordine cronologico con filtro CLEAR1, modalità 1, 1024 × 1024, esposizione comandata di 0 ms e integrazione effettiva di 3,5 ms. La configurazione ottica è diversa dalla sessione di riferimento del 2 marzo. La selezione non usa i valori dei pixel.

Sono stati verificati 12 oggetti PDS, sei FITS e sei etichette, contro il manifesto MD5 della fonte. La rilettura locale controlla anche SHA-256, dimensione, associazione etichetta–FITS e geometria. La regione centrale resta `[384:640, 384:640]`; il protocollo esclude un frame in presenza di pixel negativi o pari o superiori a 15.000 DN.

Tutti e sei i frame raggiungono 16.383 DN nella regione centrale, con 20.277–34.063 pixel esclusi per frame su 65.536. Esito `ABSTAIN_SUPPORT` per tutte le sei coppie previste, tre adiacenti e tre separate. Non sono disponibili stime di varianza o un confronto delle aperture per questa sessione. Le due esecuzioni producono lo stesso SHA-256 del risultato, `ffef48f8b6f281d772a5a721386274d60d77eea8e74bc7841b45dcf0296d1024`.

Il risultato delimita la trasferibilità del protocollo: per questo controllo serve una sessione indipendente con regione centrale utilizzabile secondo gli stessi criteri. Il settimo frame non è stato analizzato. Nessuna chiusura scientifica o prova nativa.

[Dataset NASA PDS](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-HRII%2FHRIV%2FMRI-2-GROUND-TV4-V1.0)