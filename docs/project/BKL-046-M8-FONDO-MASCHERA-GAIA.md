# BKL-046 · Maschere Gaia per stimare il fondo su M8/M20

La ricerca Gaia DR3 estesa a G < 19,5 ha restituito 9.225 sorgenti uniche entro i coni attorno alle 39 stelle di riferimento. Il conteggio per blocco coincide con quello restituito da TAP. Le posizioni sono riportate sul mosaico tramite la soluzione astrometrica congelata e i moti propri disponibili. Il censimento proietta una sorgente vicina entro 8 pixel per 38/39 stelle, di cui 10 hanno una vicina entro 3 magnitudini in G. Per 38/39 compare almeno un centro sorgente nell'anello del fondo. La posizione a catalogo identifica una contaminazione possibile, il suo contributo in ciascuna banda resta da misurare. [Gaia DR3](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html)

La misura rimuove dall'anello 9–13 px i pixel entro 3 px dalle sorgenti candidate. I due controlli ruotano le posizioni della maschera di 90° e 180° attorno alla stella. Il flusso dell'apertura usa gli stessi pixel in tutti i casi. La prova richiede almeno il 70% dei pixel iniziali del fondo, almeno 40 pixel e almeno 10 stelle in ciascuna ripartizione comune. Il criterio cromatico richiede che il P90 migliori di almeno 0,010 mag rispetto allo stesso fondo senza maschera e di almeno 0,005 mag rispetto a entrambi i controlli ruotati, nelle due calibrazioni. [Fotometria d'apertura e fondo](https://docs.astropy.org/projects/photutils/en/stable/user_guide/aperture.html)

| Configurazione | Stima | Verifica | Esito |
| --- | ---: | ---: | --- |
| Sorgenti entro 5 mag in G | 14 | 9 | Sotto la copertura minima. Nessuna valutazione cromatica valida |
| Sorgenti entro 3 mag in G | 20 | 19 | Controllo esplorativo. Fondo mediano a 6 px sotto il criterio in tutti i 6 confronti |

Nel controllo esplorativo con fondo planare a 6 px, la maschera reale supera sia il piano senza maschera sia i controlli ruotati in 5 dei 6 confronti (tre ricostruzioni e due riferimenti spettrali). In 3/6 la riduzione del P90 supera anche 0,010 mag per entrambe le calibrazioni rispetto alla mediana senza maschera a 6 px. La maschera reale rimuove il 2,95% mediano dei pixel del fondo, vicino ai due controlli ruotati. Il risultato riguarda le sorgenti che influenzano la stima del fondo. Il flusso delle sorgenti sovrapposte all'apertura richiede modellazione separata. La seconda soglia è stata introdotta dopo il primo esito e necessita di verifica indipendente.

## Riproducibilità

- Archivio H: `Produzione/2026-10-13/Digital-StarGate-PixInsight/archives/BKL046-M8-maschera-Gaia-79b9f5799f23-verificato.zip`.
- Rapporto maschera a 5 mag: `6c7a0bf10054191ca2a2dc316571ea2612f3b531cb41c78daba5f3751d99ed75`.
- Rapporto maschera a 3 mag: `79b9f5799f237451019aba33ca4bd2f59af31c6fd9235447e13b4114f83b0faf`.
- Lo ZIP conserva le query e le risposte TAP, le proiezioni, il codice e le misure. Gli ingressi preesistenti sono fissati per impronta.
- FILTER_COLOR/3 resta aperto. Zero chiusure scientifiche e zero avvii nativi.
