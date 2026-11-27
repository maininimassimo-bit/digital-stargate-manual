# BKL-046 · Campioni alternativi al clipping nelle pose M8/M20

Per 36.601 delle 59.386 occorrenze di clipping analizzate (61,63%) esiste almeno un campione della stessa parità CFA sotto 62.000 entro un pixel dal punto proiettato in un'altra posa. Il campione deve essere lo stesso secondo entrambe le geometrie affini. Per 24.016 occorrenze (40,44%) la condizione si verifica in almeno tre altre pose. In 22.785 casi manca un'alternativa a quella distanza e soglia.

| Confronto a codice inferiore a 62.000 | Almeno una posa alternativa | Almeno tre pose alternative |
| --- | ---: | ---: |
| Accordo delle due affini, entro 1 pixel | 36.601 (61,63%) | 24.016 (40,44%) |
| Accordo delle due affini, entro 1,5 pixel | 42.229 (71,11%) | 32.185 (54,20%) |
| Stessa coordinata del sensore | 56.734 (95,53%) | 49.330 (83,07%) |

La riga alle coordinate fisse indica quanto si sovrastimerebbe la disponibilità di alternative per una stessa posizione del cielo usando solo le coordinate del sensore. Per ciascuna delle 15 pose si considerano le altre 14. Il confronto usa il fotosito CFA più vicino della stessa parità, senza interpolazione. L'interno comune esclude 299 occorrenze presso i bordi e le 15 del fotosito rosso già al limite nei dark. Il fotosito rosso è escluso anche dalle ricerche nella posa di destinazione.

Il limite 62.000 è una soglia di analisi. Questi campioni provengono da posizioni subpixel e pose diverse, con possibili differenze di PSF e contesto del segnale. Il rapporto misura disponibilità e ripetizione del supporto. Per verificare il recupero fotometrico servono un riferimento indipendente, un modello del flusso e tolleranze congelate. Zero avvii PixInsight e zero chiusure scientifiche.

Per ripetere passare a `misura.py` il protocollo, la directory estratta dal kit della verifica geometrica precedente, lo ZIP delle pose, la ricevuta delle pose, lo ZIP dei dark, la directory con NumPy 2.3.5 e Astropy 7.2.0 e un nuovo file di uscita. Le impronte dei sorgenti e dei dati sono fissate dai due protocolli. [Confronto delle coordinate](../bkl046-m8-m20-clip-detector-sky-coordinate-v1/README.md)
