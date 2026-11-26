# BKL-046 · Registrazione ACS 17979 ancorata a Gaia DR3

Sono state usate 3.184 sorgenti ammissibili nel cono Gaia DR3 già archiviato per 47 Tuc, dopo i filtri di magnitudine, qualità astrometrica e vicinato. Il nuovo tentativo TAP per ottenere un cono più ampio ha restituito HTML. I risultati usano il cono precedente da 0,06° e valgono per la porzione di campo coperta. Il moto proprio è propagato linearmente all'epoca TCB di ciascuna posa. Non sono modellati parallasse annuale e accelerazione prospettica. I tasselli celesti di verifica sono identici fra le pose. [Gaia DR3](https://gea.esac.esa.int/archive/documentation/GDR3/)

| Posa | Guide chip 1 | Guide chip 2 | Esito |
| --- | ---: | ---: | --- |
| jfln02qtq, 40 s | 0 | 1 | Riferimenti sotto il minimo di segnale in 1.061 finestre |
| jfln02qzq, 40 s | 266 | 266 | Correzioni affini entro soglia sui due chip |
| jfln05ykq, 400 s | 1 | 2 | Picchi sopra il limite per le guide in 1.118 finestre |
| jfln05ymq, 400 s | 1 | 5 | Picchi sopra il limite per le guide in 1.116 finestre |

Per jfln02qzq il P90 dei residui di verifica passa da 0,314 a 0,185 px sul chip 1 e da 0,300 a 0,161 px sul chip 2. Restano al massimo un identificativo Gaia comune per combinazione di posa lunga e breve e nessuno comune nei tasselli di verifica. La correzione Gaia è quindi documentata soltanto per jfln02qzq. Il limite di picco di 50.000 elettroni è una scelta del protocollo per le guide e non coincide con la soglia di saturazione del CCD. La selezione non qualifica l'allineamento fra visite né il recupero fotometrico a gain 2.

Per ripetere, eseguire `verifica.py` con i runtime Astropy e SciPy, la directory estratta di questo archivio, la directory dei quattro FITS, il protocollo e un nuovo percorso di uscita. Il catalogo, il metodo preesistente e i FITS sono verificati per SHA-256. [Prova astrometrica precedente](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/9a44673e30553275e8585681af6946f0e76d6bc1/docs/project/bkl046-acs-17979-cross-visit-astrometry-v1)
