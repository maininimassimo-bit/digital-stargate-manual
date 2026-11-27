# BKL‑046 · Prova empirica di orientazione con quattro fasi subpixel

Il protocollo confronta quattro ripetizioni alla stessa fase con quattro esposizioni a scarti di mezzo pixel sui due assi, a parità di SNR nominale complessivo pari a 100. Il terzo fit riusa gli stessi pixel delle quattro fasi con errori di registrazione fino a 0,025 pixel. La forma e il centro relativo sono comuni, con ampiezza e fondo distinti per esposizione. I 108 confronti accoppiati comprendono due realizzazioni di rumore per ognuna delle 54 geometrie Moffat. [Limiti teorici di pianificazione](BKL-046-PSF-INFORMAZIONE-ANGOLARE.md)

| Profilo | Prove per modalità | Entro 5° alla stessa fase | Entro 5° con quattro fasi esatte | Entro 5° con quattro fasi e registrazione perturbata |
| --- | ---: | ---: | ---: | ---: |
| Rapporto assiale 0,60 | 48 | 15 | 41 | 35 |
| Rapporto assiale 0,85 | 48 | 6 | 17 | 15 |

Per rapporto assiale 0,60, le quattro fasi esatte recuperano 27 angoli e perdono un successo rispetto alle ripetizioni. L’errore di registrazione fa perdere sei dei 41 successi. Per rapporto 0,85, le quattro fasi esatte ne recuperano 12 e ne perdono uno. Perturbando la registrazione si perdono quattro dei 17 successi e se ne guadagnano due.

Nei 12 controlli circolari per modalità, nessun fit qualificato assegna un angolo. Un controllo circolare per ciascuna modalità a fasi diverse resta non qualificato. Il numero di controlli è insufficiente per stimare con precisione il tasso di angoli spuri. Non qualificati anche cinque fit ellittici a fase ripetuta e uno con registrazione perturbata. La ricevuta conserva esiti e arresti per ciascuna coppia.

Il vantaggio osservato vale per questa simulazione con profili della stessa famiglia, scala e rumore noti. Nessuna modalità raggiunge il 90% di orientazioni utili richiesto nei gruppi ellittici. Una deviazione standard teorica entro 5° non implica che il 90% degli errori cada entro 5°. L’asse `PSF_PIXEL/2` resta aperto.

SHA‑256 della ricevuta `a3ff67a41645534f82a29851c11d495aaad636ac0447f5962040769b2ba409e5`.
