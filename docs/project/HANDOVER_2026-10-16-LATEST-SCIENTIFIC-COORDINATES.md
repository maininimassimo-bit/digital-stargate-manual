# Ultima osservazione e pacchetti senza acquisizione — 16 ottobre 2026

> Rettifica18 ottobre2026: conteggi, ultima sessione e misure citati qui descrivono lo stato storico precedente alla [riconciliazione per finestra manifest](HANDOVER_2026-10-18-CATALOG-NIGHT-RECONCILIATION.md). Il RAW è preservato; usare i derivati riconciliati per lo stato corrente.

## Richiesta e diagnosi

Owner richiede coordinate dinamiche dall’ultima sessione importata e chiarisce che, senza nuova sessione scientifica, il sistema non deve fare nulla. La notte 15–16 ottobre è stata importata come pacchetto COMPLETE con log/telemetria ma `light_started=0`, `light_completed=0` e coordinate assenti. Il reporter l’ha scelta per data e ha sostituito il riferimento al 14–15 ottobre. Il consumer convertiva `null` con `Number(null)` in 0, presentando una survey centrata a 0°,0° come attiva; inoltre poteva usare un target fisso LDN1320.

## Comportamento corretto

Il workflow dopo la validazione del pacchetto legge i log N.I.N.A. mediante lo stesso parser canonico. Se non esistono LIGHT avviate o salvate, salta ogni successivo aggiornamento scientifico: niente report, history, catalogo o nuova latest observation. Il pacchetto tecnico e il manifest restano come ricevuta di trasferimento; non si cancellano dati. Le evidenze e le righe storiche già archiviate non vengono riscritte retroattivamente da questa correzione.

Una posa LIGHT avviata ma fallita resta una vera acquisizione da analizzare: non viene nascosta solo perché nessun frame è completato. Calibrazioni, sola telemetria o connessione strumenti non costituiscono nuove acquisizioni LIGHT. Il guard non aggiunge authority, esecuzioni dispositivi o modifiche alla Safety.

Difesa nel reporter: `update_latest_observation.py` non tocca byte o mtime del file esistente per pacchetti senza acquisizioni o importazioni storiche più vecchie. Il refresh di build seleziona la più recente sessione normalizzata con LIGHT avviate/completate, conserva generated_at quando il payload è invariato e non crea un falso snapshot se non ce ne sono. Il riferimento ripristinato è NGC281, sessione 14–15 ottobre: RA13.10416667°, Dec56.565°, J2000, fonte nina-log. Non è un fallback silenzioso a una sessione qualsiasi: è l’ultima acquisizione scientifica, esplicitamente identificata nella scheda.

Consumer: coordinate ammesse solo come coppia di numeri finiti in RA[0,360), Dec[-90,90], epoch J2000. Mancanti, stringhe, booleani, intervalli invalidi o epoch ignota non vengono trasformati in zero né risolti per nome. Coordinate zero realmente numeriche restano valide. Senza coordinate la mappa è nascosta con avviso; l’immagine dell’osservatorio resta un fallback dichiarato. Non si apre una survey su target inventati. Errori HTTP rimuovono la presentazione dei dati precedenti come correnti.

Refresh ogni60s mentre la pagina è visibile, al ritorno della visibilità e con pulsante Aggiorna. Si rileggono i byte no-store, si aggiornano sessione, target, coordinate e metriche insieme; una nuova identità ricentra con `gotoRaDec` dell’API Aladin. Se la sorgente è invariata si conserva il puntamento esplorato dall’utente. Request/inizializzazione bounded e controllo del nodo connesso impediscono aggiornamenti di DOM dismesso. La source JSON resta schema1.2 e nessun RAW viene modificato.

## Verifiche e rilascio

Test Python: scelta più recente con acquisizione, pacchetto tecnico ignorato, acquisizione fallita conservata, vero no-op byte/mtime, repository senza acquisizioni, contatori non validi, importazione storica, confronto dei log reali 14–15 e15–16 ottobre. Test workflow: job/probe storico invariato eccetto guard restrittivo; tutti i passi di pubblicazione subordinati al guard. Test browser sintetico: coppia esatta passata ad Aladin, missing/invalid/zero, recupero, errore HTTP, refresh manuale/automatico e assenza di ricentramento inutile. Suite portal desktop/mobile, build strict, ARB poi RQ e gate exact-head/postmerge/Pages restano obbligatori, attestati nella PR.

API Aladin di riferimento: https://cds-astro.github.io/aladin-lite/Aladin.html#gotoRaDec . La survey è visualizzazione esterna illustrativa; non rappresenta un’immagine acquisita nella notte.

Rollback: revert coordinato di guard/reporter/consumer e proiezione latest; RAW, ricevute tecniche e report storici preservati. Nessuna modifica allo schedulatore EAGLE o al trasferimento sul dispositivo.
