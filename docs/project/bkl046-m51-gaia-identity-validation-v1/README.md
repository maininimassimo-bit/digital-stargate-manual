# Riferimento Gaia indipendente per le pose RAW di M51

Il catalogo Gaia DR3 Lite di GAVO ha restituito 579 identificativi univoci nel cono di 1,8° centrato sulle coordinate ICRS di M51. La risposta del TAP ESA era HTML, quindi il programma usa il VOTable GAVO con stato QUERY_STATUS OK. Il protocollo applica i moti propri all’epoca approssimata 2022,19 e proietta il catalogo sul piano tangente. [Coordinate SIMBAD](https://simbad.cds.unistra.fr/simbad/sim-id?Ident=M51) · [Gaia DR3 Lite](https://dc.g-vo.org/tableinfo/gaia.dr3lite)

La geometria di ciascuna posa viene stimata solo con le zone di catalogo riservate all’aggiustamento. Le zone complementari sono abbinate con prossimità reciproca e distanza minima dalla seconda alternativa. L’aggancio trova rispettivamente 68, 69 e 79 stelle di verifica per le tre pose. Il P90 dei residui rispetto al piano Gaia è 0,82, 0,72 e 0,81 pixel nativi.

| Confronto con la prima posa | Identificativi Gaia comuni di verifica | P90 traslazione | P90 similarità |
| --- | ---: | ---: | ---: |
| Centrale | 59 | 8,14 px | 0,58 px |
| Ultima | 59 | 17,69 px | 1,01 px |

Le associazioni di ciascuna posa sono condizionate dall’aggancio al catalogo e dai criteri di prossimità. I risultati confermano il limite del modello di pura traslazione anche sui confronti con identità Gaia comuni. I residui della similarità superano ancora 0,30 pixel. Restano aperti la qualificazione subpixel, la verifica nativa e l’origine delle variazioni di puntamento.

Per replicare eseguire `misura.py <directory-studio> <acquisizione-RAW> <sorgente-matcher> <rawpy-estratto> <pacchetti-Python> <directory-DLL-VC> <nuovo-riscontro.json>`. Il protocollo verifica impronte del catalogo, del matcher e dei RAW. Il VOTable originale, la query ADQL, il codice e il rapporto fanno parte dell’archivio locale.
