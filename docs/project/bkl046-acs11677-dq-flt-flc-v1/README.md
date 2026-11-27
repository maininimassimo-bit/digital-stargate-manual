# BKL-046 — Confronto dei flag DQ fra FLT e FLC su ACS 11677

Ho verificato i quattro prodotti FLT e FLC delle esposizioni da 1 e 1.457 s, con la stessa identità e griglia del rivelatore per ogni coppia. Il bit 4096 differisce fra FLT e FLC su entrambi i chip. La somma dei pixel presenti in una sola maschera è 12.287 e 14.012 sulla posa breve e 32.666 e 33.257 sulla posa lunga, rispettivamente sui chip 2 e 1. Il manuale attribuisce il bit a un rifiuto AstroDrizzle. Il confronto non identifica quale maschera rappresenti meglio i raggi cosmici reali.

Mantenendo fisse le coordinate e le 340 componenti definite nel FLC, ho sostituito soltanto la griglia DQ a scopo diagnostico. Nei pixel delle componenti lunghe il bit 4096 conta 14.360 occorrenze in FLT e 14.372 in FLC. Nessuna componente lunga diventa pura e nessuna apertura breve diventa priva di flag sui riferimenti che avevano già superato i controlli di geometria e segnale. Il cambio di prodotto DQ, a parità di supporto, non rende disponibile una coppia utile.

I due rapporti e i rispettivi replay coincidono byte per byte. La validazione del rigetto per raggi cosmici e del recupero fotometrico resta aperta.

[Definizioni DQ del manuale ACS](https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps)