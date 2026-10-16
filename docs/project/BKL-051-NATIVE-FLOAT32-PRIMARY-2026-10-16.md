# BKL-051: lettura diretta del piano primario Float32

Stato: candidato tecnico W2 per il wrapper di sviluppo. Nessun avvio nativo,
nessuna immagine osservativa elaborata da queste prove, nessuna qualificazione.

`native_float32_primary.jsh` controlla il sottoinsieme previsto dalla specifica:
FITS non compresso, piano primario monocromatico a due dimensioni, `BITPIX=-32`,
senza riscalatura. Il formato non viene riconosciuto per tentativi: altri formati
richiedono adattatori separati e restano tra gli obblighi del progetto completo.

`DSGNativeFloat32Primary.inspect(bytes, expected, monitor)` controlla il layout;
`decode` ripete i controlli e restituisce un vettore Float64 privato con tutti i
campioni primari. Il chiamante locale fidato fornisce byte nativi e un oggetto
con esattamente `byteLength`, `dataOffset`, `width`, `height`. Il helper copia
questi quattro valori prima di chiamare il monitor, evitando modifiche tardive
della geometria. Non accetta un layout restituito in precedenza come autorità.

| Limite | Massimo |
|---|---:|
| File sorgente | 64 MiB |
| Header primario | 1048320 byte |
| Campioni decodificati | 4194304 |
| Vettore Float64 risultante | 32 MiB |

Header e lunghezza del file devono rispettare i blocchi FITS da 2880 byte.
I primi cinque record devono essere `SIMPLE`, `BITPIX`, `NAXIS`, `NAXIS1`,
`NAXIS2`, nell’ordine; dimensioni e offset devono coincidere con quelli attesi.
I record obbligatori e quelli di scala non possono essere duplicati. Il lettore
rifiuta header non ASCII stampabile, END o padding errati, assi aggiuntivi,
gruppi, BLANK, formato compresso e dati primari troncati. Gli altri record sono
lasciati nel file originale senza interpretarne WCS, tempi o calibrazione.

Se presenti, `BSCALE` e `BZERO` devono esprimere **esattamente** uno e zero.
Il controllo usa le cifre decimali e l’esponente, evitando di accettare
`1.000000000000000001` come uno o `1E-999` come zero per arrotondamento
Float64. Una rappresentazione negativa di zero è rifiutata da questo adattatore.
In loro assenza valgono i default del formato. Non viene applicata alcuna
calibrazione, sottrazione del cielo, inversione o normalizzazione.

La decodifica usa IEEE754 Float32 big-endian tramite DataView e conserva i valori
finiti in Float64, inclusi negativi, valori sopra uno, subnormali Float32 e `-0`.
NaN e infinito in qualsiasi campione bloccano il risultato; non vengono riempiti
o esclusi silenziosamente. L’ordine è asse1 veloce, senza inversioni, con indice
`y*width+x`. Questo stabilisce la corrispondenza dei campioni, non quella celeste.

Il formato di memorizzazione e le parole chiave sono descritti nello
[standard FITS pubblicato da NASA/GSFC](https://fits.gsfc.nasa.gov/standard40/fits_standard40aa.pdf).
Il lettore implementa soltanto il sottoinsieme dichiarato; gli HDU successivi
non vengono decodificati né approvati da questo componente.

Il monitor, fornito esclusivamente dal codice locale revisionato, controlla
tempo e annullamento ogni 4096 byte di header o campioni, oltre alle fasi iniziale
e finale. Deve lasciare immutati i byte; non è codice deserializzato dal file.
Il wrapper deve creare il buffer con lettura limitata, tenere il sorgente
protetto in lettura, verificare hash di file e header e rispettare il termine
monotono del supervisore anche dopo le chiamate sincrone.

Le prove Node costruiscono soltanto file sintetici in memoria. Confrontano
pattern IEEE con risultati matematici noti, segno dello zero, ordine 3×2,
offset del buffer, header su più blocchi, scala esatta, rifiuti strutturali,
limiti prima dell’allocazione e interruzione cooperativa.

Queste prove non attestano le API PJSR, `ImageWindow.setSamples`, la conservazione
di un checkpoint riaperto o la fedeltà di un’importazione reale. Il wrapper deve
ancora confrontare tutti i valori nativi con i byte sorgente, conservare History,
checkpoint e provenienza e superare il proprio collaudo autorizzato. L’output
del helper mantiene `fileIntegrityVerified:false` e
`physicalApplicabilityVerified:false`: il parsing non verifica l’hash, l’unità
fisica, il rumore, le maschere o la validità scientifica del modello.
