# BKL-046 — Ricorrenza del flag DQ 4096 all'interno delle scie ACS 11677

Sul chip 2 ho riusato il fit affine congelato e verificato le 29.109 proiezioni al pixel saturo più vicino nella seconda posa. Ho ripetuto il conteggio eliminando 22 proiezioni verso lo stesso pixel, scegliendo quella più vicina al centro del pixel di destinazione senza usare il flag. Restano 29.087 pixel di destinazione distinti, distribuiti in 121 componenti.

Il bit 4096 coincide in 3.046 posizioni, contro 1.064,6 attese usando soltanto la frequenza del flag in ciascuna scia. In 256 rotazioni cicliche della sequenza dei flag all'interno di ogni scia, l'intervallo descrittivo centrale al 95% va da 649 a 1.469 coincidenze. Nessuna rotazione raggiunge il conteggio osservato.

Il modello di rotazione preserva le frequenze per scia ma non ogni struttura spaziale o strumentale. Il risultato mostra una ricorrenza maggiore di quella spiegata dalle sole frequenze. Non distingue i raggi cosmici reali dalle risposte ripetute del rigetto su scie luminose e non autorizza a ignorare i flag. Il confronto riguarda una sola coppia e il chip con geometria già verificata. Replay identico. Nessuna nuova fotometria.