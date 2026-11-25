# ACS 11677. Posa indipendente da 100 secondi

Nel censimento F606W del programma 11677, le sole pose da meno di 1.000 secondi sono `jb6v01dfq` da 1 s e `jb6v25aaq` da 100 s. La seconda appartiene a una visita e a un'associazione diverse da `jb6v01010`, usata per la replica AstroDrizzle.

Il headerlet di `jb6v25aaq` contiene il modello SIP, le correzioni di detector e le tabelle di distorsione. Ho proiettato i 340 centri delle scie L1457 e richiesto un margine di 20 pixel ai bordi. 289 centri cadono su un solo chip di destinazione e 51 restano fuori dal supporto. Le corrispondenze per coppia di chip sono 69 per 1→1, 96 per 1→2, 58 per 2→1 e 66 per 2→2.

Per ogni coppia di chip, la prova sul FLC deve soddisfare la soglia geometrica P90 di 0,1 pixel su stelle tenute fuori dal fit. Restano anche i minimi congelati di 24 stelle e 8 tasselli per gruppo. Solo dopo questa verifica il controllo del picco e dei flag DQ può qualificare una posa come riferimento non saturo. Qui il risultato riguarda la copertura geometrica prevista. Non sono state misurate aperture fotometriche.
