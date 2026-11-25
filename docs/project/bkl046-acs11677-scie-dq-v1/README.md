# BKL-046 — Diagnosi dei flag DQ che escludono le scie ACS 11677

Ho riletto le 340 componenti della posa da 1.457 s e le aperture corrispondenti nella posa da 1 s. Il replay ha conservato tutte le decisioni della preselezione. Ho separato i bit DQ invece di trattare le parole composite come un'unica categoria.

Il bit 4096 è il flag aggiuntivo più frequente. Compare in 14.372 degli 82.560 pixel delle componenti lunghe con bit di full well, e in 3.834 occorrenze di pixel nelle aperture brevi scartate per DQ. Le aperture possono sovrapporsi. Secondo la tabella CALACS, il bit 4096 indica un rifiuto di raggi cosmici da AstroDrizzle. La misura identifica il flag registrato, senza determinare se il rifiuto sia corretto per ciascun pixel.

Ho ricalcolato i conteggi lasciando invariati i controlli geometrici e di segnale. Anche ammettendo a titolo diagnostico i soli bit 16 e 64 oltre ai valori previsti, nessuna coppia supera la preselezione. La verifica suggerisce di esaminare la provenienza del flag 4096 e la sensibilità al rigetto di AstroDrizzle prima di qualsiasi uso fotometrico di questi pixel. Nessuna nuova accettazione o ricomposizione.

[Tabella 3.4 del manuale ACS](https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps)