# BKL-046 — Effetto della correzione overscan sulla chioma di Tempel 1

L'indice MRI grezzo contiene 433 pose a pieno formato sul bersaglio Tempel 1. Il piano seleziona tutte le cinque pose non compresse in CLEAR1 o CLEAR6 e le abbina ai corrispondenti RADREV v3.0. L'abbinamento verifica osservazione, numero immagine, strumento, filtro, integrazione e coerenza del tempo di bordo. I checksum PDS corrispondono per dieci FITS e dieci etichette. [Archivio MRI grezzo](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-C-MRI-2-9P-ENCOUNTER-V1.0) · [Archivio ridotto v3](https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=DIF-C-MRI-3%2F4-9P-ENCOUNTER-V3.0)

L'esperimento applica ai grezzi la [correzione per riga adattata solo sui dark TV4](BKL-046-TV4-OVERSCAN-PER-RIGA.md). Usa RADREV per localizzare la chioma e le maschere PDS per selezionare i pixel. Mantiene fissi centro, anelli e supporto per entrambe le misure. Il flusso confrontato è il segnale grezzo in DN al netto del fondo locale. La qualità minima richiesta è l'85% dei pixel nell'anello e nella corona di fondo.

Nelle due pose CLEAR1 tutte le aperture passano e la variazione assoluta del flusso arriva allo 0,16%. Nella posa CLEAR6 pre-impatto 9000515, più debole, la correzione aumenta invece il flusso dell'1,15%, 3,94% e 27,88% negli anelli 12–24, 24–48 e 48–96 px. Nella posa CLEAR6 9000942 due anelli interni sono esclusi per supporto insufficiente. I casi diversi per filtro, segnale ed epoca restano riportati separatamente.

Il FITS RADREV 9000515 contiene una correzione ufficiale DESTRIPE non nulla. I quattro confronti di profilo centrato per quadrante danno correlazioni fra 0,37 e 0,60 e differenze RMS da 0,27 a 0,36 DN. Negli altri quattro prodotti DESTRIPE è nullo. Il metodo sperimentale produce una correzione anche in quei casi. Il confronto documenta perché una correzione fissa, pur utile su dark TV4, richiede un criterio di applicazione prima di misurare una chioma debole.

La variazione di flusso misura la sensibilità alla scelta del metodo. Restano aperti il riferimento fotometrico indipendente per la chioma, la contaminazione ottica del bordo e il confronto nativo.

| Evidenza | SHA-256 |
| --- | --- |
| Cattura delle cinque pose appaiate | 784c7436085223e63621f8f2b3ed8d2ad942efd3e072d7a75edf100502a328d5 |
| Misure nelle aperture e replay identico | e6e827c0d2419a8bf0770171d7b1d1af9b0aaa546d79e3d8b418244cc3304e0d |
| Confronto dei vettori e replay identico | 2f901629653f2d5857a30614ae7a6c70fa7b918d8e4f5585d5d288c610fe1cd5 |
| Archivio riletto su H: | cfd39a7b2979319a9bea0017bb8e8446ff02da182c09c62da616d17643611540 |

Zero chiusure scientifiche e zero esecuzioni native in questo incremento.
