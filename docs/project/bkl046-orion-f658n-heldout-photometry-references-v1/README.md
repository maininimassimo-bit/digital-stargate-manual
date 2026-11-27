# BKL-046 — Controllo dei riferimenti fotometrici su Orione F658N

Tre coppie di componenti DQ, fissate dal censimento precedente, avevano un disco pulito a raggio 3 pixel nelle pose da 150, 150 e 340 s. Questo controllo individua e centra un picco in ciascun riferimento e misura aperture complete con raggi di 3, 5 e 8 pixel. Usa due anelli per il fondo locale, SCI, ERR e DQ, correzione PAM e PHOTFLAM. La posa da 340 s resta esclusa dalla media delle pose brevi.

| Candidato | Esito |
|---|---|
| 5/5 | Centroidi entro 0,011 arcsec. Con raggio 3 px la differenza fra le pose brevi è 0,45–0,52% e il flusso della posa da 340 s è più alto del 36,82–36,84% nei due anelli. Le aperture da 5 e 8 px hanno supporto incompleto. |
| 6/7 | Separazione massima 0,242 arcsec, oltre la soglia di 0,15. Il raggio da 3 px non supera il controllo sul segnale e le aperture maggiori hanno supporto incompleto. |
| 18/22 | Almeno un riferimento non contiene un picco idoneo entro la finestra di ricerca. |

Nessun candidato supera il controllo primario congelato di 5 pixel, fondo 12–18 pixel, SNR formale minimo di 20, ripetibilità delle pose brevi entro il 3% e accordo della posa esclusa entro il 5%. L'errore formale combina ERR e l'incertezza del fondo locale. Restano fuori dalla stima le sistematiche inter-epoca, la forma della PSF e le componenti confuse. Lo scarto misurato a 3 pixel non stabilisce se la causa sia variabilità astrofisica, calibrazione o contaminazione. Questi riferimenti non consentono una misura indipendente della fedeltà del recupero sulle pose sature. Zero esecuzioni native e chiusure scientifiche.

Lo script accetta directory del dossier, directory delle dipendenze, dossier degli header di esposizione, percorso di output, modo replay e directory del censimento precedente. L'archivio H conserva entrambe le PAM, i blocchi FITS letti e le impronte.

[Censimento precedente](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/5c625350478c2b99d11ad52720087f6a9d951cbb/docs/project/bkl046-orion-f658n-repeat-saturation-v1) · [Calibrazione fotometrica ACS](https://hst-docs.stsci.edu/acsdhb/chapter-5-acs-data-analysis/5-1-photometry)
