# BKL‑046 · Fase subpixel e fotometria ACS/WFC

Questa scheda integra il ramo di studio dell’asse `PSF_PIXEL/2` per ACS/WFC F606W nei campi NGC 6341 e NGC 5986. Il suo stato è **aperto**. Le misure riguardano la ripetibilità in conteggi per unità di tempo e la sensibilità alla fase subpixel. Il dominio completo include anche ellitticità e orientazione, altri regimi di campionamento e la verifica nativa prevista dal requisito. [Registro tecnico e ricostruzione delle prove](BKL-046-SPATIAL-STATS-NATIVE-CONTROL-2026-11-13.md)

## Procedura per il confronto

1. Fissare le esposizioni di riferimento, di controllo e di fotometria prima di leggere i risultati. Verificare programma, data, filtro, chip fisico, WCS strumentale e impronte degli input.
2. Usare tessere di calibrazione separate da quelle di verifica. Fissare il centro di ciascuna stella a partire dalle pose di riferimento prima di calcolarne il flusso. Tenere distinti i campioni con abbinamento assente o ambiguo e i rifiuti per qualità dei pixel.
3. Verificare il P90 radiale della previsione per ogni coppia posa–chip. Conservare la soglia del protocollo e l’incertezza del ricampionamento spaziale. Se la prova supera la soglia, mantenere la disposizione e investigare il segnale o la registrazione prima di un nuovo protocollo.
4. Confrontare le ampiezze a centro fisso con fondo e tempo di esposizione espliciti. Mantenere le classi di fase, riportare i cambi di classe tra pose e conservare le repliche che perdono una classe. Valutare l’effetto delle mappe dell’area dei pixel sullo stesso campione.

## Esiti verificati

| Campo e regime | Evidenza | Disposizione |
| --- | --- | --- |
| NGC 6341, pose da 5 e 90 s del 2002 | Il centraggio ePSF cambia l’occupazione al bordo da 7 a 278 stelle nella posa da 5 s e da 3 a 259 nella posa da 90 s, sui rispettivi campioni confrontabili. | La copertura al bordo dipende dallo stimatore. La fase derivata dagli stessi pixel della fotometria ha portata diagnostica. |
| NGC 6341, pose da 7 e 140 s del 2006 | Il P90 sul chip 2 della posa da 7 s è 0,1032 pixel. Rimane sopra 0,10 escludendo a turno ciascuna delle 118 tessere. Entrambi i chip della posa lunga restano sotto soglia nel ricampionamento. | La coppia corta–lunga resta da qualificare. |
| NGC 5986, pose da 350 s | Il trasferimento di fase ha P90 tra 0,044 e 0,063 pixel sui quattro gruppi posa–chip. La fotometria a previsione congelata conserva 115 delle 117 associazioni comuni. | Trasferimento verificato entro il campione. Gli intervalli descrittivi bordo–centro includono zero su entrambi i chip, anche con le mappe medie dell’area dei pixel. |

L’inclusione dello zero negli intervalli descrive l’incertezza del confronto. Una conclusione di equivalenza richiederebbe una tolleranza scientifica fissata prima della prova e dati abbastanza precisi per verificarla. La calibrazione assoluta, la coppia corta–lunga e la qualifica nativa restano aperte.

## Tracciabilità

L’indice locale riconcilia sette ricevute di H: con il criterio letterale di `PSF_PIXEL/2` nel registro VM v57. SHA‑256 dell’indice `ed080875f66437a0ca385be1e3d1f9b14bd39695d8a2176fec52be55520cf25a`. Le acquisizioni e le analisi sono descritte nel registro tecnico. [Registro tecnico](BKL-046-SPATIAL-STATS-NATIVE-CONTROL-2026-11-13.md) · [Indice della consegna della conoscenza](BKL-046-KNOWLEDGE-DELIVERY-v1.171.json)

