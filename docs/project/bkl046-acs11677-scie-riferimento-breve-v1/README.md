# BKL-046 — Riferimento di un secondo per le scie ACS del programma 11677

Dal censimento congelato ho selezionato i due estremi di durata F606W della stessa associazione, `jb6v01010`. I prodotti FLC sono `jb6v01dfq` da 1 s e `jb6v01e0q` da 1.457 s. Le impronte coincidono con i manifest di acquisizione precedenti. Ho applicato i criteri di preselezione già usati su GO14949: componenti con bit di full well di almeno 21 pixel in verticale, proiezione WCS nella posa breve, controllo del picco e apertura di 10 pixel priva di flag.

Sono state misurate 340 componenti lunghe, 213 sul chip 1 e 127 sul chip 2. Tutte contengono almeno un pixel con un altro flag oltre al bit di full well. Nessuna apertura breve supera l'intera preselezione. Le esclusioni sono 77 ai bordi, 83 per supporto o posizione del picco e 180 per altri flag nella posa breve. Il rapporto conserva le singole misure e l'ordine dei controlli. Il replay è identico.

La posa da 1 s amplia il rapporto di esposizione rispetto a GO14949. In questa coppia i flag di qualità e la registrazione diagnostica lasciano ancora aperta la verifica del recupero. Il rifiuto vale per le soglie utilizzate e per questa associazione. Nessuna stima di flusso recuperato.

[ACS, struttura dei prodotti dati](https://hst-docs.stsci.edu/acsdhb/chapter-2-acs-data-structure/2-1-types-of-acs-files)