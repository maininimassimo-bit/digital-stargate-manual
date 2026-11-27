# GD153 · Controllo astrometrico con Gaia DR3

La query ESA ADQL ha acquisito il singolo record Gaia DR3 `3944400490365194368` identificato come GD153. Il calcolo propaga la posizione ICRS con il moto proprio all'istante centrale di ciascuna esposizione e la proietta attraverso il WCS SCI, mantenendo il WCS già presente nel FITS. Il modello è baricentrico, con velocità radiale assunta nulla e senza parallasse dell'osservatore. [Identificazione pubblicata](https://academic.oup.com/mnras/article/534/3/2758/7804368) · [Modello astrometrico Gaia](https://gea.esac.esa.int/archive/documentation/GEDR3/Data_processing/chap_cu3ast/sec_cu3ast_cali/ssec_cu3ast_cali_source.html)

| Confronto sui 48 FLC | Esito |
| --- | --- |
| Separazione tra RA_TARG/DEC_TARG e Gaia propagato | 1,830–1,846 arcsec |
| Distanza tra le due proiezioni nel piano SCI | 48,63–49,08 pixel |
| Massimo locale entro quattro pixel | 22 con il seed dell'header, 23 con il seed Gaia |
| Esposizioni in cui cambia l'esito del controllo di distanza | 19 |
| Massimo dell'intero SCI entro quattro pixel dal seed Gaia | 0 |

Le 48 immagini sono subarray UVIS1-C512A-SUB. WCS principale: 44 soluzioni a priori HSC30 e quattro soluzioni senza allineamento secondo l'header. Il massimo locale è il pixel più luminoso nel riquadro 9×9 e può essere rumore o un artefatto. Anche il massimo globale è un indicatore diagnostico. Il confronto richiede una registrazione indipendente per attribuire una sorgente, con incertezza coerente con il WCS e l'epoca. [STScI, astrometria assoluta HST](https://hst-docs.stsci.edu/drizzpac/chapter-4-astrometric-information-in-the-header/4-5-absolute-astrometry)

Nella sola esposizione passata dal filtro fotometrico precedente, `iaah11ddq_flc.fits`, le due finestre contengono picchi distinti di 7,18 e 7,39 elettroni. Il massimo globale è a 10,90 arcsec da Gaia e ha DQ 4096. La misura di 39,4221 elettroni/s resta priva di attribuzione verificata a GD153. La diagnosi lascia aperto `FILTER_COLOR/2` con zero chiusure e zero avvii nativi.

La ripetizione, combinando i due archivi riletti da H:, ha riprodotto il riscontro JSON byte per byte.

| Evidenza | SHA-256 |
| --- | --- |
| Risposta Gaia CSV | `13dd14b1c5d90a4acc2ee6196a5d99a1d04c33a3a2346f175376c410d28b73fc` |
| Riscontro JSON | `a72e762d9ced11cdbdd9980eac932b8a3175ff87533fdeb9326455288b53e117` |
| Archivio astrometrico | `4297ccb1d630f97d8c7e5fc65567cd1c63263b9132b232ad5aa6f08f04119ba4` |

Dataset originario e criteri: [visite puntate GD153](BKL-046-WFC3-GD153-VISITE-PUNTATE.md).
