# BKL-046 · Controllo della registrazione di IC 1805 con Gaia DR3

Le due misure separate sui verdi originali del mosaico producono un centro medio per ogni stella. Le posizioni Gaia DR3, propagate all'epoca della sequenza e proiettate nel WCS congelato, forniscono un riferimento di catalogo. Il protocollo riusa gli identificativi della verifica precedente e conserva lo stesso confine spaziale tra stima e controllo. Sono ammesse solo le associazioni con un'alternativa nel catalogo proiettato a più di otto pixel nativi. Per posa, tutte le geometrie usano le stesse 40–46 stelle di stima e vengono valutate sulle stesse 24–38 stelle escluse, distribuite in 12–16 regioni.

| Residuo | P90 complessivo (px nativi) | Pose con P90 fino a 0,30 px |
| --- | ---: | ---: |
| Posizione per posa contro Gaia | 0,321838 | 17/38 |
| Variazione del residuo Gaia rispetto alla posa di riferimento | 0,379726 | 6/38 |
| Registrazione diretta sulla posa di riferimento | 0,380383 | 8/38 |

Le 1.123 associazioni di verifica appartengono a 42 stelle. Il confronto diretto per posa valuta una coincidenza di posizione con il catalogo. Il test differenziale sottrae il residuo Gaia della posa di riferimento dopo il trasporto affine e valuta lo spostamento relativo. Il suo valore è vicino alla registrazione diretta sullo stesso rivelatore. Il P90 della differenza assoluta fra i due residui radiali è 0,012245 pixel. I due test relativi condividono centroidi, pose e stelle di stima. Non costituiscono due repliche indipendenti.

Su questo sottoinsieme associato al catalogo, la registrazione relativa resta sopra la soglia complessiva di 0,30 pixel. La copertura limitata alle sorgenti dell'associazione precedente non consente un'estensione a tutto il campo. La validazione CFA alla stessa scala resta aperta.

I due rapporti prodotti rileggendo le pose coincidono con SHA-256 `1670e598211ff0a4a87c217422a8f84905c62eab180f2c38cb7a7f40fcaf65aa`. Il protocollo fissa le impronte delle sorgenti e del catalogo. Zero esecuzioni native. [Catalogo Gaia DR3 ESA](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html)
