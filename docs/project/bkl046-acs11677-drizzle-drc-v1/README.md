# ACS 11677. DRC ufficiale e riscontro delle maschere

Il DRC pubblico `jb6v01010_drc.fits` ha 245.940.480 byte. L'acquisizione da MAST coincide con il prefisso già registrato, il CRC64/NVME dell'oggetto cloud STScI e il suo ETag. L'archivio su H: e la copia su O: nel VHDX ospitato su K: sono stati verificati, incluse le sette voci dello ZIP.

Per le dodici maschere di AstroDrizzle 3.11.0 il riscontro registra due riletture identiche dal filesystem del guest, con l'uscita del mosaico ancora in elaborazione. Su 100.663.296 posizioni, il confronto con il bit 4096 delle DQ archivistiche ha 2.910.514 posizioni marcate su entrambi i lati, 97.752.782 su nessuno e zero disaccordi. Le impronte di questo riscontro saranno riconciliate con le maschere trasferite nell'archivio finale.

I confronti SCI e WHT applicano il vincolo della stessa griglia e delle unità SCI. Il confronto CTX richiede in più lo stesso ordine delle dodici associazioni tra bit e ingresso, ricostruito dalle card `DnnnDATA`. Il risultato sulle maschere misura la riproducibilità del flag in questo insieme di dati. Rimangono aperti il confronto dei mosaici e la verifica del braccio con Driz_CR disattivato.

[FITS pubblico MAST](https://mast.stsci.edu/api/v0.1/Download/file?uri=mast%3AHST%2Fproduct%2Fjb6v01010_drc.fits) · [Archivio cloud HST](https://archive.stsci.edu/missions-and-data/hst) · [Verifica del checksum completo](https://docs.aws.amazon.com/AmazonS3/latest/API/API_Checksum.html)
