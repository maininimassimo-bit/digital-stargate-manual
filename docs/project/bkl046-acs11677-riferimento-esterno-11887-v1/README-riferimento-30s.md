# BKL-046 — Esposizione indipendente ACS/WFC F606W da 30 secondi

Il FITS `jbbf01i1q_flc.fits` del programma 11887 proviene da un'esposizione acquisita 176,92 giorni prima di quella di riferimento. Il controllo ha verificato la versione dell'oggetto, l'ETag a parte singola, lo SHA-256 locale, il FITS e l'identità del programma e del filtro. Il provider non espone un CRC64 per questa versione. Le testate sorgente e destinazione dichiarano ICRS.

La proiezione con le distorsioni ACS copre 316 dei 340 centri. Fra i centri coperti, 284 falliscono il filtro per supporto del picco o ricentraggio, 6 mostrano il flag di pieno pozzo e 26 altri flag DQ. Il protocollo di registrazione ha trovato 448 previsioni di stelle di controllo interne nelle quattro coppie di chip, senza alcun ancoraggio valido. Nessuna coppia raggiunge quindi il minimo congelato e nessun centro viene ammesso alla fotometria.

Il risultato riguarda la registrazione con la WCS nominale e i criteri dichiarati. L'assenza di corrispondenze valide lascia da verificare un eventuale disallineamento iniziale con un controllo separato che conservi la soglia geometrica sulla parte di verifica. Rimangono aperte la misura indipendente del flusso stellare e la chiusura scientifica.
