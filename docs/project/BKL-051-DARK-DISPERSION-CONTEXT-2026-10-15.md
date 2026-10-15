# BKL-051 — dispersione dei dark e contesto locale

## Perimetro

Incremento del requisito R04: consultare nel portale le evidenze parziali dei
dark del 2024, distinguendo dispersione osservata e varianza condizionata della
media. Nessuna mappa viene assegnata automaticamente a una LIGHT. Il contesto
di calibrazione V1, i budget storici e gli esiti precedenti restano invariati.

**BKL-051 OPEN / NOT_VALIDATED, stima37%, zero controlli qualificati.** La
varianza dell'effettivo master con rigetto, la stabilità 2024–2026 e il budget
completo restano sconosciuti. Nessuna accettazione scientifica o authority.

## Evidenza scientifica locale

Un'unica esecuzione locale isolata di PixInsight 1.9.5 build1706 ha letto 50
dark da 600s, 2752×2160×1. Originali invariati, History e terminale conservati;
tre mappe Float64 salvate e riaperte con errore zero. Il processo posseduto è
stato chiuso dopo il terminale valido e la conservazione dei prodotti: exit1,
senza dichiarare un'uscita spontanea riuscita con exit0.

Una ricomputazione indipendente dei 297.216.000 campioni ha trovato errori
massimi rispettivamente di 1,39e-17, 1,09e-19 e 1,70e-21. ARB poi RQ delle
evidenze locali approvate; non sostituiscono i gate del presente rilascio.

| Prodotto | Significato e limite |
|---|---|
| Media senza rigetto | Campioni normalizzati nativi; non riproduce il master con rejection |
| Varianza campionaria | Dispersione descrittiva dei 50 dark, denominatore49 |
| Varianza della media, s²/50 | Condizionata a indipendenza e identica distribuzione, non attestate |

Il master storico impiega Average e WinsorizedSigmaClip. La varianza della
media senza rigetto non ne diventa automaticamente l'incertezza. Questi dark
non quantificano da soli deriva temporale, covarianze condivise o errore della
calibrazione delle LIGHT. Il massimo della dispersione resta visibile: non
viene eliminato o classificato automaticamente.

## Produttore e vista

`tools/scientific_transients/dark_dispersion_context.py` rilegge i record
scientifici referenziati: sigillo, configurazione, 50 sorgenti, History,
terminale, chiusura del processo, tre mappe e prova indipendente. Le note di
continuità modificabili nella cartella non sono dipendenze scientifiche: non
viene dichiarato un archivio completo di ogni file storico.

La ricevuta minimizzata `BKL051_DARK_DISPERSION_CONTEXT_V1` omette percorsi,
PID, coordinate, credenziali e contenuto degli originali. Contiene impronte,
statistiche, unità e limiti. Il produttore verifica i byte locali referenziati;
il browser confronta soltanto dichiarazioni importate e non autentica autore,
data, byte originali o accettazione. Il valore importato non autorizza avvii.

La sezione «Dispersione dei dark e limiti del master» legge un JSON in memoria
(massimo1MiB), con campi e unità stretti. File mancante, invalido, sostituito o
lettura superata da una scelta successiva cancellano la vista precedente.
Navigazione e uscita dalla pagina invalidano i dati caricati. Nessun upload,
storage del browser, rete, comando o modifica al servizio è introdotto.

## Verifica e rilascio

Le prove mirate coprono esportazione Python→JavaScript, sorgenti/mappe/History
alterate, conteggi e identità incoerenti, promozioni scientifiche, divisione
condizionale, unità, dimensioni, limiti UTF8 e risposte asincrone tardive.
Prima del rilascio servono CI exact-head, ARB poi RQ, prova visiva del candidato,
gate premerge e postmerge/Pages sulla versione esatta. I risultati dei dark
non attestano da soli questi gate.

Rollback: revert del package del contesto, preservando evidenze e originali.
Il rilascio della pagina non attiva il servizio, non ripete la prova cloud,
non avvia PixInsight e non invia dati astronomici. R04 e R14 restano parziali;
gli altri requisiti, IRSA e accettazione Owner restano aperti.
