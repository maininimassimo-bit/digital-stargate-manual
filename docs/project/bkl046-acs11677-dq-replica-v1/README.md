# BKL-046 — Ripetizione delle scie ACS 11677 su due pose lunghe

Ho selezionato prima della lettura dei pixel le due esposizioni F606W più lunghe della stessa associazione: 1.457 s e 1.456 s. Il secondo FLC è stato acquisito da MAST e verificato per dimensione, SHA-256 e metadati concordanti con il censimento già conservato. I due FITS hanno tempi di inizio distinti.

Ho proiettato con il WCS primario i pixel delle 340 componenti lunghe, mantenendo il chip fisico. Dei 82.560 pixel di riferimento, 80.502 ricadono nella regione verificabile della seconda posa. Su 67.035 proiezioni il pixel più vicino conserva il bit di full well. Cercando anche negli otto pixel adiacenti, il numero sale a 76.004. Lo spostamento mediano del campione sul rivelatore è circa 102–104 pixel secondo il chip.

Tra le 67.035 proiezioni con full well nel pixel più vicino di entrambe le pose, il bit 4096 compare su 6.268 in entrambe, su 2.043 solo nella prima e su 2.898 solo nella seconda. Le proiezioni possono riusare pixel della seconda posa. Questa è una misura di ricorrenza sul supporto proiettato, non un conteggio di eventi cosmici indipendenti. Il WCS primario non qualifica da solo l'allineamento subpixel. Il replay coincide byte per byte. La fotometria del flusso recuperato resta aperta.

[Archivio HST MAST](https://archive.stsci.edu/missions-and-data/hst) · [Definizioni DQ ACS](https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps)