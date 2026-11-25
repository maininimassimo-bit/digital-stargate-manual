# GD153 · Verifica ePSF su pixel osservati tenuti fuori dal fit

Il controllo usa le librerie ACS/WFC STDPBF SM4 ufficiali per F435W, F606W e F814W e i 18 FLT GD153 sull'amplificatore B. Ogni libreria è vincolata per SHA-256. Il lettore usa il solo array primario big-endian con le dimensioni dichiarate nel FITS. Le versioni scaricate contengono byte di riempimento finali non conformi che fanno fallire il lettore HDU generico. Il modello usa la griglia WFC1 e campiona la ePSF con interpolazione bilineare a sovracampionamento 4×. [Librerie ACS ePSF di STScI](https://www.stsci.edu/hst/instrumentation/acs/data-analysis/psf)

Per ogni posa si ruota o riflette la geometria dei due pixel mancanti nell'apertura a 5 pixel e si conservano solo le configurazioni distinte in cui entrambi i pixel sono osservati e DQ zero. Le misure nascoste restano fuori dal fit. Si stima la scala lasciando variare il piano di fuoco e gli spostamenti subpixel entro ±0,3 pixel dall'ancora misurata, con fondo fisso dall'anello 25–40 pixel. Il confronto usa la mediana dei pixel osservati alla stessa distanza radiale entro 0,45 pixel. L'errore è il valore assoluto della somma residua sui due pixel, pesata con PAM, divisa per il flusso osservato sui pixel validi dell'apertura a 5 pixel.

| Banda | Configurazioni | Mediana ePSF | Massimo ePSF | Mediana radiale | Massimo radiale |
| --- | ---: | ---: | ---: | ---: | ---: |
| F435W | 26 | 0,017% | 0,160% | 0,059% | 0,154% |
| F606W | 22 | 0,027% | 0,232% | 0,118% | 0,288% |
| F814W | 26 | 0,038% | 0,134% | 0,089% | 0,898% |
| Totale | 74 | 0,027% | 0,232% | 0,072% | 0,898% |

Le configurazioni sono correlate perché riutilizzano 18 pose e tre visite. Il risultato prova la predizione su difetti artificiali della stessa geometria, in posizioni dove esiste una misura osservata. La libreria e il modello non sono verificati sulle lacune reali, sul raggio di 10 pixel, su altri amplificatori o dopo una correzione CTE. Il massimo osservato non è un limite di confidenza. Il riscontro conserva il valore dei pixel tenuti fuori, le due predizioni e il piano di fuoco scelto per ogni caso. Zero pixel reali ricostruiti, zero avvii nativi e zero chiusure scientifiche.

Replay con gli archivi riletti su H:, con JSON identico byte per byte. SHA-256 riscontro `55931f9f77edab694a439831480d009e798e71ad995183a3502fd770eb54cedc`. SHA-256 archivio `1a001bdfda583a86001d59fe404d6de36e3a9e8153139d2019e4e361ffdc5810`.

[Copertura delle coppie ACS/WFC](BKL-046-GD153-ACS-SUPPORTO-APERTURA.md).
