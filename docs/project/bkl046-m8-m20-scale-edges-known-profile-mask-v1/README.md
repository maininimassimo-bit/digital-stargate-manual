# BKL-046 · Supporto del fit con profilo diffuso noto su M8/M20

Il controllo riprende le 148 combinazioni di pose e scala che superavano i test sui residui e le 27 coppie a scala unitaria. Esclude dal fit ogni cella che raggiunge una frazione fissata del picco iniettato. Usa la stessa maschera prima e dopo l'iniezione, verifica almeno 12 celle pulite per partizione spaziale e controlla il rango e il condizionamento del piano. Misura flusso e forma sul supporto originale.

| Profilo | Celle pulite con soglia al 2% | Prove entro il 5% su flusso e forma con offset | Prove entro il 5% con piano | Astensioni su 148 |
| --- | ---: | ---: | ---: | ---: |
| Filamento corto | 160 | 148 | 148 | 0 |
| Filamento lungo | 160 | 148 | 148 | 0 |
| Diffuso largo | 0 | 0 | 0 | 148 |

Per il profilo largo, la soglia all'1% lascia zero celle e quella al 5% ne lascia otto, quattro per partizione. Il controllo si astiene anche in questi due casi. A scala unitaria i due filamenti passano in 27 coppie su 27 e il profilo largo porta a 27 astensioni. La maschera sfrutta la forma nota del segnale iniettato. Mostra che per questi filamenti esiste supporto sufficiente se la posizione del segnale è nota con precisione. Per il profilo largo serve supporto esterno o un vincolo di fondo indipendente. Restano da verificare una regola di mascheratura applicabile ai dati, la sua incertezza e il comportamento nativo.

Il programma riceve il protocollo, la directory del precedente studio d'iniezione, il protocollo storico di mascheratura, la directory del riferimento M8/M20, il rapporto congiunto completo, le dipendenze e una directory di uscita nuova. L'archivio contiene i 1.575 esiti per soglia, inclusi tutti i casi di astensione. [Iniezioni senza maschera](../bkl046-m8-m20-scale-edges-diffuse-injection-v1/README.md)