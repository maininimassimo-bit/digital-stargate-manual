# BKL-046 · Copertura di un riferimento Gaia nel campo GO16380

Ho interrogato Gaia DR3 in un cono da 0,08 gradi centrato a RA 201,73 e Dec −47,60. La risposta contiene 22.124 righe e 5.447 stelle superano i filtri congelati di qualità astrometrica, magnitudine, parallasse e incertezza propagata. Le coordinate sono state propagate da J2016.0 all'epoca Hubble con il moto proprio lineare. La parallasse non è stata applicata e il suo valore assoluto è limitato a 1,5 mas. [Modello astrometrico Gaia](https://gea.esac.esa.int/archive/documentation/GEDR3/Gaia_archive/chap_datamodel/sec_dm_main_tables/ssec_dm_gaia_source.html)

La proiezione di partenza usa il WCS alternativo A ICRS `IDC_4bb1536mj` di A40. Il disegno usa i tasselli pari con margine di 56 pixel per stimare lo scarto iniziale e cercare associazioni univoche. Il limite di 24 riferimenti e 8 tasselli si applica a ogni sensore. La ricerca ha individuato lo stesso scarto iniziale di [1, 3] pixel su entrambi i sensori.

| Sensore | Gaia proiettate nel sensore con margine | Abbinamenti preliminari di calibrazione | Tasselli di calibrazione | Sorgenti Hubble di verifica prima dell'associazione |
| --- | ---: | ---: | ---: | ---: |
| 1 | 487 | 20 | 12 | 431 |
| 2 | 462 | 20 | 10 | 539 |

La soglia di supporto in stelle non è raggiunta su nessuno dei due sensori. Il protocollo conserva l'esito di arresto prima del fit affine e l'assenza di valutazione sui tasselli dispari. La copertura effettiva delle 40 stelle appaiate per sensore rimane da misurare. Questo risultato riguarda l'incrocio con il campione di centroidi già selezionato da Hubble. Il prossimo confronto di copertura può partire dalle sorgenti Gaia e rimisurare le due pose brevi conservando le soglie. L'asse `SATURATION_BLEND/4` resta aperto. Nessuna prova nativa o chiusura scientifica.

| Evidenza conservata | SHA-256 |
| --- | --- |
| Risposta dell'archivio Gaia | `fd85451ae62da626da12680954629fb0aa0a25acf33fd07d5a3993d13695c18b` |
| Protocollo | `f9fa70946198f0c957b435b4300a5f7c14e0c75156199ac43db05f74f79e8578` |
| Ricevuta | `d479d7618176583df95d4e06fa5f4a29c469798224959f13067fd5ae925cdb07` |
