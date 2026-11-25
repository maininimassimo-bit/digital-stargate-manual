# BKL-046 — Fotometria diagnostica dei nuclei GO14949 con flag di full well

Ho mantenuto i tre candidati storici 2, 10 e 11 sul chip 2 e le due pose F606W da 400 s. Entrambe le pose avevano riportato bit DQ di full well nei nuclei, con la prequalifica geometrica ancora fuori soglia. Ho confrontato i tassi corretti con PAM e fondo locale rispetto alle pose da 40 e 150 s. Il protocollo tratta separatamente il solo bit 256 e le combinazioni con altri flag. La componente connessa al nucleo è inclusa solo quando resta interamente contenuta nella finestra di misura.

A raggio 3 pixel tutte e sei le misure lunghe sono disponibili. Le differenze rispetto a B da 40 s vanno da +0,67% a +1,70%. La componente connessa con bit di full well resta all'interno dell'apertura in tutti i sei casi, quindi la misura non aggiunge pixel di scia esterna. A raggio 5 e 10 pixel tutte le aperture lunghe sono respinte per flag estranei o valori non utilizzabili. Non c'è supporto per un confronto a raggi maggiori o per il recupero di scie estese.

Il rapporto e il replay coincidono. La prova riusa tre sorgenti selezionate a partire da dati precedenti e la stessa visita. I nuclei rimangono fuori dalla preselezione geometrica e nessun pixel del FITS viene sostituito. Le pose e la mappa PAM sono vincolate da SHA-256.

[Procedura STScI per la fotometria ACS con scie di saturazione](https://spacetelescope.github.io/hst_notebooks/notebooks/ACS/acs_saturation_trails/acs_saturation_trails.html)