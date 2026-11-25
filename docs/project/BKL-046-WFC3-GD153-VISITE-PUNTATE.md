# GD153 · Visite puntate WFC3/UVIS del programma HST 11450

Prova offline dell'asse `FILTER_COLOR/2`. La query pubblica MAST per GD153, GD 153 e GD-153, nelle bande F438W, F606W e F814W, ha restituito 853 record di catalogo tra MJD 55000 e 60309.99999. Per il programma 11450 sono stati fissati tutti i quattro membri FLC di ognuna delle 12 associazioni selezionate, quattro visite per tre bande. Il protocollo conserva gli hash dei 48 FLC e delle due Pixel Area Map.

Sono stati applicati i controlli di identità FITS e associazione, di qualità dell'esposizione e dei pixel, di associazione tra WCS e picco entro quattro pixel, e di supporto per apertura e fondo. Per formare il confronto, il protocollo richiede due misure valide per banda sullo stesso chip nella stessa visita e tre bande entro 0,05 giorni per ciascuna terna. Le esposizioni escluse restano nella ricevuta.

| Visita | F438W validi / acquisiti | F606W validi / acquisiti | F814W validi / acquisiti |
| --- | ---: | ---: | ---: |
| iaah11 | 0/4 | 0/4 | 1/4 |
| iaah12 | 0/4 | 0/4 | 0/4 |
| iaah13 | 0/4 | 0/4 | 0/4 |
| iaah14 | 0/4 | 0/4 | 0/4 |

Dei 48 FLC, 26 sono stati esclusi al controllo WCS-picco, 16 al controllo di supporto di apertura o fondo e cinque per flag DQ nel nucleo. L'unico valore ammesso dai filtri, da `iaah11ddq_flc.fits`, è 39,4221 elettroni/s in F814W. La frazione di incertezza derivata dal solo piano ERR è 0,6730. Il valore resta una misura strumentale isolata e richiede una conferma indipendente dell'identità della sorgente. Per una calibrazione assoluta servono anche le correzioni fotometriche pertinenti. [WFC3 Data Handbook, Photometry](https://hst-docs.stsci.edu/wfc3dhb/chapter-9-wfc3-data-analysis/9-1-photometry)

Nessuna visita ha prodotto colori ripetuti. Prossima verifica discriminante per questo insieme: ricostruire la posizione attesa da un riferimento astrometrico indipendente e le modalità di puntamento dalle associazioni prima di esaminare nuovamente i picchi. La misura resta offline, con zero avvii nativi e zero chiusure scientifiche.

| Evidenza | SHA-256 |
| --- | --- |
| Acquisizione | `ee3a363e54dea51fd29a71ce9961b86fe6b83a58c1c75d7149b807754ac75e45` |
| Protocollo | `7636924bce5cb8ab6f2832052565d335bdcc083f90e2597bb40e28316e9ecfaa` |
| Riscontro | `8915a2bd0a1e81b4026690096f4cfecb54ea65401cac0a501811e1b835d4fa78` |
| Archivio BKL046-WFC3-GD153-visite-puntate-v1.zip | `53651924f27b876d590395077ea7242f828ab38a72c337d9e680254059d4c19c` |

L'archivio contiene le risposte MAST, gli input, il misuratore e il protocollo precedente usati per la ripetizione. Il replay dalla copia H: ha riprodotto byte per byte protocollo e riscontro.
