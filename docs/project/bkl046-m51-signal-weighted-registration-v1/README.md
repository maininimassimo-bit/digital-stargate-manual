# Registrazione di M51 con pesi basati sul segnale stellare

Sulle tre pose RAW Canon EOS 6D, per ciascuna stella è stato misurato il rapporto fra il picco sopra il fondo e la stima robusta del rumore nell’anello circostante. Si usa il valore minimo fra le due pose della coppia e fra G1 e G2. La misura include il rumore di fondo e non stima il rumore fotonico della stella.

La similarità pesata e quella a pesi unitari usano le stesse stelle Gaia. I pesi sono il quadrato del rapporto rispetto alla mediana delle sole stelle di stima e sono limitati fra 0,25 e 4. Il P90 si valuta su tutte le stelle riservate alla verifica. Il rapporto riporta anche i risultati sopra e sotto la mediana di stima, con le rispettive numerosità.

| Posa rispetto alla prima | Centroidi | Stelle di verifica | P90 unitario | P90 pesato |
| --- | --- | ---: | ---: | ---: |
| Centrale | Preview | 57 | 0,614 | 0,451 |
| Centrale | G1/G2 | 57 | 0,593 | 0,581 |
| Ultima | Preview | 51 | 0,790 | 0,578 |
| Ultima | G1/G2 | 51 | 0,847 | 0,733 |

Il P90 con la preview pesata diminuisce del 27% circa in entrambe le coppie. Il fit G1/G2 pesato peggiora il P90 del sottogruppo a segnale più debole nella posa centrale da 0,633 a 0,715 pixel. Tutte le combinazioni restano sopra il criterio diagnostico di 0,30 pixel nativi. La misura riguarda queste esposizioni e non stabilisce un rapporto causale fra rumore e residuo.

Per replicare eseguire `misura.py <protocollo.json> <studio-centroidi> <studio-Gaia> <acquisizione-RAW> <sorgente-matcher> <rawpy-estratto> <pacchetti-Python> <directory-DLL-VC> <nuovo-riscontro.json>`. Il programma controlla la similarità pesata su coordinate sintetiche e verifica byte per byte la riesecuzione del rapporto dei centroidi.
