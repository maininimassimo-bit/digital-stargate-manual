# BKL-051 — Ricerca di sorgenti variabili e candidati transienti

## Stato corrente — 8 ottobre 2026

P6 resta Accepted nei limiti del dossier. BKL-051 resta aperta. PR #505 integrata e verificata sul merge `d15529722cdd9e2ac8b9a629e2fc2aff4cd83e01`: coda privata candidata, disabilitata per default; nessun deployment, IAM o credenziale modificati. Owner approva anche dossier e segnalazioni CBAT/TNS/AAVSO-VSX/MPC, incluse ricerca di oggetti mobili e capacità di invio autonomo condizionata; funzionalità da realizzare, nessun invio attivato. S1/S2 scientifiche aperte, S3 parziale, S4 incompleta, S5 non accettata. Soglie, policy autonoma e accettazione finale restano gated. F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva; S10/Safety invariati. [Handover corrente](HANDOVER_2026-10-08-BKL051-REPORTING-PLAN.md).

| Campo | Valore |
|---|---|
| Identificativo | BKL-051 |
| Versione | 1.2 |
| Data | 2026-10-08 |
| Stato | In Progress — coda candidata consegnata; analisi, segnalazioni e accettazione ancora aperte |
| Priorità | P2; prossimo sviluppo dopo chiusura operativa P6 |
| Dipendenza di avvio | Chiusura BKL-049-EXT-PIAI/P6, con riconciliazione dei collaudi e accettazione operativa Owner |
| Milestone | M-BKL051-SCIENTIFIC-TRANSIENT-CANDIDATES |
| Termine | Nessuna data promessa |

## Decisione e sequenza

Il 7 ottobre 2026 Massimo Mainini ha approvato la nuova estensione scientifica e richiesto di inserirla nella roadmap: conclusa P6, si passa allo sviluppo del modulo. La presente consegna è di pianificazione, non implementa il servizio e non chiude P6.

Sequenza del lavoro scientifico: **P6 chiusa e accettata operativamente → BKL-051 → BKL-050 conclusiva**, subordinata anche alle altre attività approvate. BKL-043 F4 mantiene l'attesa del lifecycle reale; F5 resta successiva alla piena accettazione F4. F4/F5 non diventano una nuova dipendenza di avvio BKL-051, ma restano dipendenze della milestone finale BKL-050.

## Obiettivo e confine scientifico

Offrire all'Owner un modulo privato nel portale per confrontare le proprie riprese con archivi pubblici NASA/ESA e riferimenti osservativi, individuando sorgenti senza corrispondenza e variazioni di luminosità meritevoli di verifica, incluse possibili nove. L'output è un candidato motivato, non una scoperta confermata o una classificazione automatica di nova. Una sorgente non catalogata può dipendere da profondità, copertura, banda, confusione o epoca del riferimento.

L'analisi parte da master lineari e, quando disponibili, singoli scatti calibrati con data/ora, filtri, esposizione e provenienza. Le immagini estetiche con deconvoluzione, denoise, rimozione stelle o stretch possono visualizzare le segnalazioni ma non sostituiscono la base di misura. La calibrazione SPCC di una SHO non la rende direttamente comparabile con fotometria broadband. Dati storici senza sessioni sono ammessi con dichiarazione esplicita, senza associazioni inventate; epoca mancante o integrazione su più notti limita il risultato e non viene colmata con la data di elaborazione.

## Estensione Owner — 8 ottobre 2026

Il [piano di segnalazione](BKL-051-SCIENTIFIC-REPORTING-PLAN-2026-10-08.md) aggiunge dossier e invii CBAT/TNS/VSX/MPC, ricerca di possibili asteroidi, percorso assistito e capacità di invio autonomo condizionata. S1-R/S3-M/S4-R/S5-R entrano nei requisiti di chiusura BKL-051. [Evento Owner](evidence/BKL-051-OWNER-REPORTING-SCOPE-2026-10-08.json). Nessuna attivazione, soglia, account o pubblicazione autorizzata da questa registrazione. Le precedenti esclusioni di invio implicito restano valide per il runtime corrente; il nuovo sviluppo esplicito è disciplinato dal piano.

## Perimetro funzionale previsto

1. Selezione privata dell'immagine e controllo di formato, integrità, linearità, metadati temporali, filtri e qualità disponibile.
2. Soluzione astrometrica, identificazione delle sorgenti e confronto con cataloghi, considerando epoca e moto proprio.
3. Recupero di riferimenti storici con provenienza, data, banda, qualità e copertura dichiarate; confronto anche con riprese Owner dello stesso campo in altre date.
4. Confronto fotometrico con incertezze e compatibilità delle bande; sottrazione d'immagine solo se giustificata, dopo registrazione, normalizzazione del fondo/flusso e adeguamento della PSF. Caso non confrontabile esplicito, senza differenze artificiali presentate come transienti.
5. Verifica dei candidati nei singoli scatti o sottointegrazioni indipendenti, esclusione motivata di artefatti e controllo di variabili e oggetti in movimento noti.
6. Scheda privata con immagine, riferimento, differenza quando valida, coordinate, epoche, misure/incertezze, limiti e motivazione. Stati di candidato, scartato o da approfondire distinti dalla conferma esterna.
7. Rapporto esportabile e decisione umana tracciata. La conferma può richiedere osservazioni indipendenti e spettroscopia.
8. Ricerca e associazione temporale di possibili asteroidi sui dati adatti; dossier e segnalazioni per destinatario, anteprima/conferma Owner, ricevute e capacità autonoma condizionata secondo il piano dell’8 ottobre.

## Fonti e architettura da definire nella prima fase

| Fonte candidata | Scopo | Verifica richiesta prima dell'integrazione |
|---|---|---|
| ESA Gaia Archive | Astrometria, stelle note, moto proprio, fotometria disponibile | Release, epoca, copertura, sistema fotometrico e accesso programmatico |
| NASA/IPAC IRSA, prodotti ZTF | Immagini multi-epoca e curve di luce | Campo coperto, epoche effettivamente pubbliche, filtri, flag e limiti API |
| MAST, Pan-STARRS | Cataloghi e immagini storiche | Copertura, profondità, risoluzione, banda ed epoca |
| AAVSO/VSX e Minor Planet Center | Controlli complementari su variabili e oggetti mobili | Interfacce ammesse, condizioni d'uso e corrispondenza temporale |

La proposta di partenza è elaborazione sul PC Owner con consultazione privata dal portale, usando i confini esistenti dove compatibili. Non è ancora una scelta definitiva di infrastruttura o dipendenze. La fase S1 deve verificare compatibilità con Scientific Data Engine, AP-013/AP-014 e ADR-019, prevenire accessi diretti ai cataloghi dal frontend fuori dai boundary governati e determinare se occorre un Architecture Package/ADR dedicato.

L'approvazione autorizza pianificazione e sviluppo successivo a P6 entro lo scope concordato. Non attiva oggi collector, analisi periodiche, servizi cloud, nuove credenziali/IAM o API a pagamento. Eventuali decisioni strutturali e costi seguono i gate esistenti. Nessun comando agli apparati, scheduler osservativo, remediation o Safety Authority.

## Fasi e criteri di accettazione

| Fase | Risultato verificabile |
|---|---|
| S1 — fattibilità e contratto scientifico | Fonti accessibili e limiti documentati; input e stati di comparabilità definiti; privacy, architettura, algoritmo, soglie e protocollo di validazione esplicitati prima del loro uso operativo. Nessuna soglia quantitativa inventata da questa roadmap. |
| S2 — confronto di base | Soluzione astrometrica e cross-match ripetibili su campi noti, con moto proprio/epoca e incertezze; riferimenti tracciati; dati mancanti, timeout e assenza di copertura producono stati espliciti. |
| S3 — candidati e falsi positivi | Confronti multi-epoca e differenze compatibili; campioni reali con eventi noti e campi di controllo; artefatti, stelle sature/confuse, oggetti mobili e filtri incompatibili verificati. Test sintetici etichettati e separati dai dati reali. |
| S4 — modulo privato e report | Percorso Owner completo selezione → analisi → evidenze → revisione/esportazione; accessi negati verificati; ripresa/annullamento/idempotenza definiti; originali e provenienza preservati. |
| S5 — collaudo e accettazione | Misure di recupero e falsi positivi con limiti/dataset dichiarati, soglie approvate nel contratto, UI accessibile e regressioni; gate CI/review/rilascio e accettazione operativa Owner. Nessuna equivalenza tra test sintetico, candidato e scoperta. |

S1/S3/S4/S5 includono ora gli incrementi R/M del [piano di segnalazione](BKL-051-SCIENTIFIC-REPORTING-PLAN-2026-10-08.md); i loro criteri sono necessari alla chiusura, senza attribuire acceptance a funzionalità ancora pianificate.

## Privacy, pubblicazione e rollback

Immagini, candidati, coordinate delle osservazioni e rapporti restano privati salvo decisione esplicita. Nessun upload scientifico a servizi esterni, pubblicazione gallery o invio di segnalazioni astronomiche è implicito. Le interrogazioni necessarie alle fonti e i dati trasmessi vanno documentati nel contratto S1. TNS non è un canale universale: la sua documentazione esclude le nove galattiche; il canale appropriato va verificato al momento di un'eventuale segnalazione autorizzata.

Il rollback della pianificazione è un revert governato dei documenti e rigenerazione delle projection. Il futuro rollback del modulo dovrà sospendere nuove analisi conservando risultati, decisioni e input, senza cancellare evidenze. Questa roadmap non introduce nuovo debito implementativo; le scelte irrisolte sono gate S1, non risultati acquisiti.

## Fonti e tracciabilità

- [Gaia: accesso programmatico](https://www.cosmos.esa.int/web/gaia-users/archive/programmatic-access)
- [IRSA/ZTF API](https://irsa.ipac.caltech.edu/docs/program_interface/ztf_api.html)
- [MAST/Pan-STARRS](https://archive.stsci.edu/panstarrs/)
- [AAVSO: verifica delle variabili](https://archive.aavso.org/index.php/how-report-new-variable-star-discoveries)
- [MPC: servizi](https://docs.minorplanetcenter.net/services/)
- [TNS: ambito delle segnalazioni](https://www.wis-tns.org/)
- [Backlog](BACKLOG.md), [roadmap funzionale](FUNCTIONAL_ROADMAP_EXPANSION_2026-08-30.md), [dossier P6](PIAI-P6-CANDIDATE-2026-10-06.md), [milestone finale](BKL-050-FINAL-PORTAL-QUALITY-MILESTONE-2026-09-23.md).

Versione 1.0: registrazione dell'approvazione Owner e della sequenza, 07/10/2026. Nessuna implementazione o analisi scientifica avviata da questo aggiornamento.

## Dipendenza P6 accettata il 7 ottobre

L’Owner ha accettato operativamente P6 con i limiti del [dossier finale](PIAI-P6-OPERATIONAL-ACCEPTANCE-2026-10-07.md), dopo HOO richiesto e completato. [Chiusura](BKL-049-EXT-PIAI-P6-CLOSURE-2026-10-07.md). Il package BKL-051 passa alla preparazione S1; iniziare lo sviluppo solo dopo verifica della consegna P6 nella PR #499. Nessuna scelta strutturale, soglia scientifica, nuova risorsa, credenziale o analisi su foto è introdotta da questo passaggio. La roadmap v1.0 sopra resta snapshot di pianificazione precedente.


## BKL-051 S1 — preparazione autonoma del 7 ottobre

P6 delivery verificata sulla PR #499 e sul merge `0bd6e20df0b449cd163543ed30bd69d9264862b0`: 16/16 workflow post-merge SUCCESS incluse Pages e proiezioni pubbliche conformi. [Handover corrente](HANDOVER_2026-10-07-BKL051-S1.md), [fattibilità e contratto proposto](BKL-051-S1-FEASIBILITY-AND-CONTRACT-2026-10-07.md). Accessi pubblici limitati verificati, tentativi negativi conservati, nove test di intake offline. S1 non accettata: decisioni su architettura/trasporto, query minime su campi Owner e dataset pilota ancora pendenti. Nessuna soglia, analisi Owner, runtime o foto pubblicata. Le sezioni precedenti restano snapshot storici.
