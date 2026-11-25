# BKL-046 — Controllo dark e struttura per riga in TV4

Ho recuperato tutti i 24 fotogrammi DRKCOLD in modalità 1 del 2 marzo 2003 e verificato i checksum PDS dei FITS e delle etichette. Il registro documenta l'otturatore chiuso e la finestra della camera coperta. La durata registrata è 3,5 ms come nel gruppo illuminato CL a comando zero. Il sensore Hall dei dark e la testata FITS indicano RED, mentre il gruppo CL usa CLEAR1. L'ultimo dark precede CL di 177,5 minuti. Il CCD dei dark è a 175,490–175,624 K e quello di CL a 178,172–178,274 K. Queste differenze limitano il dark a un controllo diagnostico del rumore. [Registro MRI](https://pds-smallbodies.astro.umd.edu/holdings/dif-cal-hrii_hriv_mri-2-ground-tv4-v1.0/document/imagelog/tv4_mri.asc) · [Checksum PDS](https://pds-smallbodies.astro.umd.edu/holdings/dif-cal-hrii_hriv_mri-2-ground-tv4-v1.0/index/checksum.tab)

Nella regione centrale, dopo sottrazione dell'overscan parallelo, il dark ha offset medio di −2,58 DN e varianza appaiata di 1,21–1,24 DN² per pixel. Il gruppo CL riproduce l'offset di −10,10 DN e la varianza di 1,09–1,19 DN². Sottrarre direttamente il livello dei dark da CL lascerebbe una differenza centrale di circa −7,53 DN, prima di considerare le differenze di acquisizione. [Confronto a sette livelli](BKL-046-TV4-CLEAR1-SETTE-LIVELLI.md)

Per il controllo spaziale ho diviso la regione centrale per quadrante e stimato ciascun offset di riga da metà dei pixel, valutando l'altra metà. L'operazione è stata ripetuta scambiando le metà. Nelle coppie adiacenti la varianza mediana delle somme 16 × 16, divisa per il numero di pixel, scende da 12,11 a 1,20 DN² nei dark e da 6,42 a 1,06 DN² in CL. La riduzione si osserva in tutte le 96 verifiche di metà regione nei dark e nelle 32 in CL. Le verifiche dentro la stessa sequenza riusano gruppi e fotogrammi. Il controllo per colonna dà variazioni molto minori delle mediane. Questo riscontro localizza una componente condivisa lungo le righe nelle differenze appaiate.

Il controllo stabilisce la presenza della struttura in un gruppo a otturatore chiuso. Resta da verificare una calibrazione trasferibile con dark contemporanei e condizioni corrispondenti, e da misurare la conservazione del segnale diffuso prima di applicare la sottrazione a immagini scientifiche.

| Evidenza | SHA-256 |
| --- | --- |
| Riscontro dark e replay | 99782051697845bc463e72be6a866f7c5a2df1184d69e1f6185ca963f6c9f4ac |
| Controllo per riga e colonna con replay | fd2da79889b2227844bfe28349e1ea1a81db0fec1ab2ecf06074aec8978528fa |
| Archivio riletto su H: | a021f9b2e27029be940e6e5d9b0c244b8b5ede182a7f971877292e22651b96a9 |

Zero chiusure scientifiche e zero esecuzioni native in questo incremento.
