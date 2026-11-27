# BKL-046 — Scia ACS estesa nel caso pubblicato da STScI

Ho riletto i due FITS F606W indicati nel notebook STScI e la mappa PAM del chip 2. Ho mantenuto il centro del notebook (1711, 225), un'apertura circolare di 10 pixel e una finestra di raggio 100 pixel. La misura estesa include i pixel con bit di full well connessi all'apertura. Ho ripetuto il conteggio della posa lunga sul centro trasferito mediante WCS primario come controllo di sensibilità. La separazione dei due centri è 1,070 pixel.

Nella posa da 400 s la scia connessa aggiunge 143 pixel con il centro fisso. Di questi, 139 riportano soltanto il bit di full well e quattro hanno flag combinati. Con il centro trasferito si aggiungono 142 pixel. La posa da 40 s ha già pixel con bit di full well nel nucleo. Il tasso diagnostico lungo passa da 26.266 a 55.987 elettroni/s estendendo l'apertura. Quello della posa breve è 60.733 elettroni/s.

I flag misti e gli altri flag impediscono l'accettazione fotometrica con il protocollo BKL-046. Inoltre la posa breve non fornisce un nucleo interamente non saturo. Il confronto dimostra che l'apertura circolare perde una parte rilevante del segnale per questo caso, e misura quanto cambia includendo la scia. Il recupero accurato del flusso, con una posa indipendente non satura e geometria qualificata, resta aperto. Il rapporto e il replay coincidono byte per byte.

[Notebook STScI](https://spacetelescope.github.io/hst_notebooks/notebooks/ACS/acs_saturation_trails/acs_saturation_trails.html)