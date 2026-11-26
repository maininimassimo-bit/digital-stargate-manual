# BKL-046 · Due riferimenti brevi indipendenti nel programma ACS 17656

I FITS jfdp02vwq e jfdp02w3q confermano ACS/WFC F606W, gain 2 e 40 s. Nei log HST la modalità prevista ed effettiva è FINE LOCK/GYRO per entrambe le pose, senza mancata acquisizione e con 14/14 campioni TakeData attivi. Il collegamento temporale fra i log e i FITS concorda entro 0,36 s. [Uso dei log HST](https://hst-docs.stsci.edu/hstdhb/5-observation-logs/5-2-using-observation-logs)

| Posa | P90 verifica chip 1 | P90 verifica chip 2 | Sorgenti Gaia comuni con jfln02qzq, sui chip corrispondenti |
| --- | ---: | ---: | ---: |
| jfdp02vwq | 0,159 px | 0,156 px | 116 / 126 |
| jfdp02w3q | 0,150 px | 0,170 px | 124 / 123 |

I 25–28 identificativi Gaia comuni per chip nei tasselli di verifica non entrano nella stima. Le due pose 17656 sono quindi disponibili come riferimenti candidati con guida e corrispondenza astrometrica verificate. La verifica del flusso richiede ancora l'esame delle aperture, della saturazione locale, di CTE e della differenza d'epoca. Le pose lunghe non fanno parte di questa prova. [Catalogo Gaia DR3](https://gea.esac.esa.int/archive/documentation/GDR3/) · [Riscontro precedente sul programma 17979](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/fa81eab025d9df14b1e3c965a5004bc8a29a7b5c/docs/project/bkl046-acs-17979-gaia-astrometry-v1)

Per ripetere la guida, eseguire `verifica-guida.py` con runtime Astropy, directory dei log, directory dei FITS, protocollo della guida e nuovo file di uscita. Per Gaia, eseguire `registra.py` con runtime Astropy e SciPy, directory del catalogo e degli operatori vincolati, directory dei FITS, protocollo Gaia e nuovo file di uscita. Il FITS jfln02qzq è conservato nell'archivio H: della preselezione 17979. Le impronte SHA-256 sono nei protocolli.
