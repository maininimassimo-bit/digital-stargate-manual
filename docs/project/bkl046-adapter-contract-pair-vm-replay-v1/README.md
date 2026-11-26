# BKL-046 · Confronto offline dei due adattatori di decisione

Il programma rilegge i 12 file delle due revisioni archiviate e ripete le 1.680 decisioni già fissate in una directory isolata. Il rapporto e le fixture rigenerati coincidono byte per byte con gli originali. Il test esegue le funzioni di schema e del contratto locale. Le decisioni sono fornite dalle fixture.

Lo schema più recente esclude 841 decisioni che il runtime avrebbe respinto. Conserva tutte le decisioni valide del campione e i sette arresti validi. Restano 43 decisioni ammesse dallo schema ma respinte dal runtime.

| Motivo del rifiuto a runtime | Casi |
| --- | ---: |
| Campi terminali incompatibili | 16 |
| Campi di selezione incompatibili | 10 |
| Genitore diverso da quello richiesto | 9 |
| Selezione priva della verifica necessaria | 4 |
| Ripetizione identica di una prova | 2 |
| Campi del passo incompatibili | 2 |

Il set comprende 16 STOP, 14 SELECT e 13 TEST malformati o incompatibili con lo stato. I disaccordi sono fixture storiche da conservare per ogni modifica dell'adattatore. I rapporti non attestano la conformità di un provider, prestazioni del modello, frequenza statistica dei rifiuti o ammissione PixInsight.

Il programma riceve protocollo, directory delle fonti archiviate e directory di uscita. L'archivio H/K conserva le due revisioni, il programma storico e le fixture esatte. Zero chiamate e zero nuove chiusure scientifiche.