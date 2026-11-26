# BKL-046 · Sequenze CFA RAW a esposizione crescente

Ho acquisito le prime due sequenze statiche del gruppo complex, parte 1, nel dataset di Karaduzovic-Hadziabdic, Hasic Telalovic e Mantiuk. Il download usa intervalli dello ZIP, verifica ETag e Content-Range e controlla CRC e SHA-256 di ogni CR2. Tutte e dieci le pose sono Canon EOS 1000D, ISO 100 e RGGB, con durate 0,125, 0,25, 0,5, 1 e 2 s per sequenza. Sono scene di laboratorio, con alcuni oggetti colorati, disponibili con licenza CC BY 4.0. [Dataset Cambridge](https://doi.org/10.17863/CAM.6881)

Nella scena 1 i massimi delle quattro fasi sono sempre 3.651 DN. I campioni esattamente a quel codice crescono da 72 nella posa più breve a 137.472 nella più lunga. I limiti per fase restituiti dal decoder variano tra 3.735 e 4.022 DN, quindi un controllo basato soltanto su quei limiti restituisce zero per tutte e cinque le pose.

Nella scena 2 il limite per fase del decoder è 3.500 DN. Ci sono sette celle con alcune fasi al limite nella posa più breve e 711.161 nella posa da 1 s. Nella posa da 2 s, 675.833 celle hanno tutte le fasi al limite. La posa più breve di questa scena richiede quindi una maschera locale per essere usata come riferimento. [Interfaccia rawpy](https://letmaik.github.io/rawpy/api/rawpy.RawPy.html)

La prova verifica disponibilità, decodifica e soglie osservate. L'accumulo dei codici e la sua crescita con l'esposizione richiedono un confronto delle stesse posizioni per stimare la risposta. La registrazione e la ricostruzione del flusso per canale non sono ancora qualificate. Lo studio non trasferisce le soglie di questa fotocamera alle pose astronomiche.

Per ripetere, eseguire `verifica.py` con la directory estratta, il wheel rawpy 0.25.1 archiviato nel precedente dossier CFA, la cartella dei pacchetti estratti dal wheel, le DLL VCLibs e un nuovo percorso di uscita. Il codice verifica il wheel, gli originali e la funzione EXIF per SHA-256. [Dossier CFA precedente](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/1aa418144f7df776547e9dfe0e6101b266078736/docs/project/bkl046-cfa-native-code-limits-v1)
