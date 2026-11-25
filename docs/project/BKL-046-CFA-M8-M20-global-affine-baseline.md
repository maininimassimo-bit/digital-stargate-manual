# BKL-046 · Baseline CFA con matrici globali per M8–M20

Le matrici affini congelate mappano il riferimento comune in ciascuna delle 14 pose. Il calcolo offline usa l'inversa per proiettare i quattro vertici di ogni deposito quadrato. Interseca il poligono con i pixel del reticolo a passo nativo e normalizza il peso per l'area trasformata del deposito. I controlli verificano identità, traslazione frazionaria rispetto al depositore precedente e conservazione del peso per una trasformazione con shear. Restano fissi i 53 soggetti stellari, le calibrazioni A e B, la maschera, il raggio delle aperture e gli insiemi di pose. L'intersezione del supporto comprende tutti i pixel delle regioni misurate, anche per l'anello del fondo nelle due metà.

| Canale | P90 della variazione assoluta del flusso, deposito 1,00 px, calibrazione A / B | Deposito 0,70 px, calibrazione A / B |
| --- | ---: | ---: |
| R | 0,210% / 0,193% | 0,352% / 0,336% |
| G1 | 0,117% / 0,117% | 0,177% / 0,133% |
| G2 | 0,114% / 0,129% | 0,158% / 0,126% |
| B | 0,117% / 0,101% | 0,182% / 0,200% |
| G combinato | 0,086% / 0,077% | 0,134% / 0,101% |

Il verde combinato somma i numeratori e i pesi dei due reticoli prima di calcolare il rapporto. La sensibilità resta sotto la soglia diagnostica dell'1% su tutte le combinazioni. Il confronto precedente con riquadri ricentrati per stella cambiava anche il riferimento locale e conservava depositi assiali. I due risultati riguardano convenzioni geometriche diverse e il divario non isola il contributo del ricentraggio da quello della forma del deposito. Restano da verificare nella prova nativa la serializzazione delle matrici e la semantica dei pesi RGB, oltre all'accuratezza fotometrica con riferimento indipendente.

Due esecuzioni coincidono con SHA-256 `99509d242e5d7fc22e0626946d5a302aeed5a4acec31196b0dc45ba460569c8c`. Zero esecuzioni native e zero chiusure scientifiche.
