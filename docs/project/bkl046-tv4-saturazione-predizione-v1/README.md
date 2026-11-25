# BKL-046 — Previsione della saturazione su pose TV4 trattenute

Ho fissato due calibrazioni sullo stesso rivelatore, prima e dopo il riallineamento della sfera. Ogni calibrazione usa sei pose da 7,5035 secondi e sei da 15,0035 secondi. I modelli per pixel extrapolano le mediane dei due livelli, con o senza sottrazione dell'overscan parallelo. Dodici pose da 22,5035 e 30,0035 secondi sono rimaste fuori dal fit. Le cinque regioni sono quelle del protocollo precedente.

Nella regione centrale, sulle pose da 22,5035 secondi i quattro modelli prevedono correttamente l'assenza di pixel al limite digitale. L'errore assoluto medio per posa sui pixel non tagliati è in media fra 27,9 e 37,9 DN. Sulle pose da 30,0035 secondi, i modelli individuano tutti i 179.248 pixel tagliati, ma segnalano erroneamente tra 81.147 e 94.888 dei 213.968 pixel che restano sotto soglia, pari al 37,9–44,4%. L'errore medio sui pixel ancora osservabili sale a 235–296 DN.

I quattro modelli riusano le stesse pose di verifica e la stessa sessione. La prova quantifica il rischio di sovrastimare l'estensione della saturazione usando pose più brevi. Le intensità oltre il limite digitale non sono osservabili nel gruppo saturo. Nessuna stima del flusso recuperato, del full well o dell'incertezza per altri sensori. Il confronto resta aperto per la chiusura scientifica.

[Dataset NASA PDS](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-CAL-HRII%2FHRIV%2FMRI-2-GROUND-TV4-V1.0)