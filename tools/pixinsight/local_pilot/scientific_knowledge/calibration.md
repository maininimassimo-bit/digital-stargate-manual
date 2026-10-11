# SHO/HOO: calibrazione e presentazione

## Dati necessari e checkpoint fotometrico

Verificare marca/modello e banda passante dei filtri; i soli nomi SII/Hα/OIII nei master non ne provano la larghezza. Riutilizzare le informazioni già confermate dall'Owner per quella acquisizione, senza estenderle ad altri dataset. Dichiarare lunghezze d'onda nominali, banda, modello QE e disponibilità delle curve reali. Un modello nominale non equivale a una caratterizzazione misurata.

Controllare registrazione e soluzione astrometrica prima di SPCC. Una soluzione valida presente nei master può essere riutilizzata; non risolvere nuovamente per abitudine. Nel ramo con BlurX, valutare Correct Only prima della calibrazione e la deconvoluzione successiva sui dati lineari, secondo il manuale della versione installata.

Per SPCC narrowband consultare la sezione pertinente del manuale installato. Nel workflow SHO provato è stato usato Photon Flux con mappatura SII→R, Hα→G, OIII→B. Registrare catalogo, stelle effettivamente usate, fattori e dispersioni dei fit: un fit molto disperso limita l'affidabilità anche quando il processo termina con successo. Conservare un checkpoint lineare subito dopo SPCC.

## Rendere leggibile la nebulosa

SHO è una rappresentazione a colori assegnati. SPCC non la trasforma in colore naturale. Il manuale SPCC descrive, per una presentazione SHO, ColorCalibration con riferimento sulla nebulosa e rilevamento delle strutture stellari disabilitato. Se adottato, documentare ROI, maschere e guadagni; bande deboli amplificate aumentano anche rumore e incertezza.

ColorCalibration estetica, SCNR, saturazione e curve modificano i rapporti del checkpoint SPCC. Identificare quindi il finale come presentazione e conservare separatamente il risultato calibrato. Non usare i colori del finale per inferire rapporti fisici delle emissioni.

Dopo il bilanciamento, rimisurare fondo e dinamica: un punto nero o uno stretch ricavati prima dei guadagni possono produrre un cielo troppo chiaro e rumoroso. Valutare il fondo sui singoli canali e fuori dalle emissioni, proteggendo polveri e nebulosità debole. Una transizione morbida evita il taglio numerico ma non prova da sola la conservazione del segnale.

Confrontare deconvoluzione, contrasto locale e finitura del rumore su identici ritagli e checkpoint. Controllare di nuovo il campo intero dopo l'applicazione: maschere e intensità adatte alla nebulosa possono alterare il cielo. Una maschera delle strutture scure può derivare da residui multiscala e differenze con la luminanza, ma non va presentata come esecuzione dello script DarkStructureEnhance se tale script non è stato usato.

La scelta più aggressiva non è automaticamente migliore. Conservare i rami scartati e dichiarare quando il riferimento Owner rimane più inciso. Non aumentare indefinitamente sharpening o denoise per ottenere un'impressione di equivalenza.

## Esperienza verificata, non preset universale

Nel nuovo ramo Sh2-301 del 7 ottobre 2026, l'Owner ha confermato ZWO 3 nm su tutte e tre le bande. Sono state confrontate intensità BlurX 0,55/0,75/0,90 e finiture NoiseX 0,15/0,35/0,55 su un checkpoint già denoisato. Le selezioni 0,75 e 0,35, con maschere e altre impostazioni registrate, appartengono a quel dataset: non sono valori iniziali obbligatori per altre immagini. Il confronto NoiseX era una finitura, non un confronto tra motori su master non trattati.

Per percorsi, accettazione e parametri completi leggere il contesto [Digital StarGate](digital-stargate.md). Non copiare nel workflow di un nuovo oggetto i guadagni o le ROI di Sh2-301.

## Fonti da consultare per l'applicazione

- SPCC: https://pixinsight.com/doc/docs/SPCC/SPCC.html — se il sito non è accessibile, usare la copia ufficiale installata e dichiararlo.
- BlurX: https://www.rc-astro.com/blurxterminator-technical-manual/
- NoiseX: https://www.rc-astro.com/noisexterminator-2-ai3-user-manual-pixinsight/
- NASA, significato dei colori assegnati: https://science.nasa.gov/asset/hubble/colors-of-the-southern-crab-nebula/
- ESA/Hubble, principi di elaborazione: https://esahubble.org/projects/hiddentreasures/imageprocessing/

Le fonti NASA/ESA spiegano principi di visualizzazione, non certificano una ricetta PixInsight ideale per questi master. Studiare le funzioni pertinenti e registrare quelle realmente eseguite, senza dichiarare una ricognizione esaustiva di tutti i processi/plugin.
