# BKL-046 — Sensibilità ai flag DQ nelle due pose GO-11887

Il confronto rilegge le diagnosi delle due esposizioni da 30 secondi. Le 316 proiezioni comuni sono identificate dalla coorte congelata di componenti sature. L'abbinamento per identificativo di coorte serve a confrontare i filtri. Le registrazioni di entrambe le pose restano fuori soglia.

| Bit DQ ignorati per il controllo diagnostico | Posa Gaia | Posa con traslazione iniziale | Comuni |
| --- | ---: | ---: | ---: |
| Nessuno | 1 | 0 | 0 |
| 16 | 11 | 0 | 0 |
| 16 e 64 | 118 | 55 | 45 |

Il risultato riguarda la sensibilità del filtro diagnostico. I bit 16 e 64 segnalano pixel caldi e tiepidi nella tabella ACS. Le estensioni delle maschere erano già previste per la sola diagnosi. Il controllo operativo conserva DQ zero, la soglia geometrica e l'esclusione del pieno pozzo. Nessuna sorgente è ammessa a una misura fotometrica.

[Definizioni DQ ACS](https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps)
